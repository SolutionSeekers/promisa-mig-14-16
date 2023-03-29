# -*- coding: utf-8 -*-

from odoo import models,fields,api,exceptions,SUPERUSER_ID,_
from odoo.exceptions import UserError
import datetime
from datetime import timedelta
import pytz
import time
from . import const
from .base import ZK
from werkzeug.urls import url_encode

from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

import logging
_logger = logging.getLogger(__name__)

class zkMachineLocation(models.Model):
    _name= 'zk.machine.location'
    name = fields.Char("Location",required=True)


class zkMachine(models.Model):
    _name= 'zk.machine'
    
    machine_name = fields.Char("Name")
    name =  fields.Char("IP")
    state =  fields.Selection([('draft','Draft'),('done','Done')], 'State', default='draft')
    location_id =  fields.Many2one('zk.machine.location', string="Location")
    port =  fields.Integer("Port Number")
    employee_ids = fields.Many2many("hr.employee", 'zk_machine_employee_rel', 'employee_id', 'machine_id',string='Employees', readonly=True, copy=False, required=False)
    
    def msg_box(self, title='', message=''):
        view = self.env.ref('sh_message.sh_message_wizard')
        # view_id = view and view.id or False
        context = dict(self._context or {})
        context['message'] = message
        return {
            'name':title,
            'type':'ir.actions.act_window',
            'view_type':'form',
            'view_mode':'form',
            'res_model':'sh.message.wizard',
            'views':[(view.id,'form')],
            'view_id':view.id,
            'target':'new',
            'context':context,
        }

    # Función para probar conexión y lista los usuarios guardados en el dispositivo ZK en caso de que la conexión sea exitosa
    def list_usrs_btn(self):
        for r in self:
            machine_ip = r.name
            str_to_show = ''
            port = r.port
            zk = ZK(machine_ip, port=port, timeout=50, password=0, force_udp=False, ommit_ping=True)
            conn = ''
            cont = 0
            try:
                conn = zk.connect()
                users = conn.get_users()
                if len(users) > 0:
                    for user in users:
                        str_to_show += "uid: "+str(user.uid) + \
                                    "\nname: "+user.name+\
                                    "\nprivilege: "+str(user.privilege)+\
                                    "\npassword: "+str(user.password)+\
                                    "\ngroup_id: "+str(user.group_id)+\
                                    "\nuser_id: "+str(user.user_id)+\
                                    "\ncard: "+str(user.card)+\
                                    "\n-------------------------------------------\n"
                else:
                    str_to_show += "No users found in ZK device"
                    
            except Exception as e:
                raise UserError('The connection has not been achieved\n\n' + str(e))
            finally:
                if conn:
                    conn.disconnect()
                    return self.msg_box("ZK device user's list", str_to_show)

    # Función de prueba
    def set_new_user(self):
        for r in self:
            machine_ip = r.name
            port = r.port
            zk = ZK(machine_ip, port=port, timeout=50, password=0, force_udp=False, ommit_ping=True)
            conn = ''
            res = False
            try:
                conn = zk.connect()
                conn.disable_device()
            except Exception as e:
                raise UserError('Error when saving information\n\n' + str(e))
            finally:
                if conn != '':
                    conn.enable_device()
                    conn.disconnect()
                if res:
                    return self.msg_box('Information', str(res))
                    
    
    def try_connection(self):
        for r in self:
            machine_ip = r.name
            port = r.port
            zk = ZK(machine_ip, port=port, timeout=50, password=0, force_udp=False, ommit_ping=True)
            conn = ''
            try:
                conn = zk.connect()
                users = conn.get_users()
            except Exception as e:
                raise UserError('The connection has not been achieved\n\n' + str(e))
            finally:
                if conn:
                    conn.disconnect()
                    return self.msg_box('Successful connection', 'The connection has been achieved succesfully')
                    
    
    def restart(self):
        for r in self:
            machine_ip = r.name
            port = r.port
            zk = ZK(machine_ip, port=port, timeout=5, password=0, force_udp=False, ommit_ping=True)
            conn = ''
            try:
                conn = zk.connect()
                conn.restart()
            except Exception as e:
                raise UserError('The connection has not been achieved\n\n' + str(e))
            finally:
                if conn:
                    conn.disconnect()
                    
    
    def synchronize(self):
        for r in self:
            employee  = self.env['hr.employee']
            employee_location_line=self.env['zk.employee.location.line']
            employee_list = []
            machine_ip = r.name
            port = r.port
            zk = ZK(machine_ip, port=port, timeout=5, password=0, force_udp=False, ommit_ping=True)
            conn = ''
            try:
                conn = zk.connect()
                conn.disable_device()
                users = conn.get_users()
                for user in users:
                    employee_id=employee.search([('id','=',user.user_id)])
                    if employee_id:
                        employee_list.append(employee_id)
                        if employee_id not in r.employee_ids:
                            r.employee_ids += employee_id
                            employee_location_line.create({'employee_id':employee_id.id,
                                                           'zk_num':employee_id.id,
                                                           'machine_id':r.id,
                                                           'uid':user.uid,
                                                           'location_id':r.location_id.id})
                for emp in employee_list:
                    employee+=emp
                employees_unlink = r.employee_ids - employee
                for emp1 in employees_unlink:
                    employee_location_line_id = employee_location_line.search([('id','=',emp1.id),('machine_id','=',r.id)])
                    employee_location_line_id.unlink()
                r.employee_ids = employee
            except Exception as e:
                raise UserError('The connection has not been achieved:\n\n'+str(e))
            finally:
                if conn:
                    conn.disconnect()
                    
    
    def clear_attendance(self):
        for r in self:
            machine_ip = r.name
            port = r.port
            zk = ZK(machine_ip, port=port, timeout=5, password=0, force_udp=False, ommit_ping=True)
            conn = ''
            try:
                conn = zk.connect()
                conn.disable_device()
                conn.clear_attendance()
            except Exception as e:
                raise UserError('The connection has not been achieved\n\n' + str(e))
            finally:
                if conn:
                    conn.enable_device()
                    conn.disconnect()
    
    def download_attendance2(self):
        users  = self.env['res.users']
        attendance_obj =  self.env["hr.attendance"]
        employee_location_line_obj = self.env["zk.employee.location.line"]
        user = self.env.user
        if not user.partner_id.tz:
            raise exceptions.ValidationError("Timezone is not defined on this %s user." % user.name)
        tz = pytz.timezone(user.partner_id.tz) or False
        for machine in self:
            machine_ip = machine.name
            port = machine.port
            zk = ZK(machine_ip, port=port, timeout=50, password=0, force_udp=False, ommit_ping=True)
            conn = ''
            try:
                conn = zk.connect()
                attendances = conn.get_attendance()
            except Exception as e:
                print (e)
                raise UserError('The connection has not been achieved\n\n' + str(e))
            finally:
                if conn:
                    conn.disconnect()
                    raise UserError(_('Successful connection:  "%s".') %
                            (attendances))
    
    
    def download_attendance(self):
        users  = self.env['res.users']
        attendance_obj =  self.env["hr.attendance"]
        employee_location_line_obj = self.env["zk.employee.location.line"]
        user = self.env.user
        if not user.partner_id.tz:
            raise exceptions.ValidationError("Timezone is not defined on this %s user." % user.name)
        tz = pytz.timezone(user.partner_id.tz) or False
        for machine in self:
            machine_ip = machine.name
            port = machine.port
            zk = ZK(machine_ip, port=port, timeout=10, password=0, force_udp=False, ommit_ping=True)
            conn = ''
            try:
                conn = zk.connect()
                conn.disable_device()
                attendances = conn.get_attendance()
                for attendance in attendances:
                    employee_location_line = employee_location_line_obj.search([("zk_num", "=", int(attendance.user_id)),('location_id','=',machine.location_id.id),('machine_id','=',machine.id)])
                    if employee_location_line:
                        employee_id = employee_location_line.employee_id
                        date = attendance.timestamp
                        date1 =datetime.datetime.strptime(str(date), DEFAULT_SERVER_DATETIME_FORMAT)
                        date = tz.normalize(tz.localize(date1)).astimezone(pytz.utc).strftime ("%Y-%m-%d %H:%M:%S")
                        if attendance.punch == 0:
                            attendance_id = attendance_obj.search([('employee_id','=',employee_id.id),('check_in','=',str(date))])
                            if not attendance_id:
                                attendance_obj.create({'check_in':date,'employee_id':employee_id.id,'check_in_source':machine.machine_name})
                        if attendance.punch == 1:
                            attendance_id = attendance_obj.search([('employee_id','=',employee_id.id),('check_out','=',str(date))])
                            if not attendance_id:
                                attendance_ids = attendance_obj.search([('employee_id','=',employee_id.id),('check_in','<',str(date))],order='check_in')
                                if attendance_ids:
                                    found = False
                                    for att in reversed(attendance_ids):
                                        if datetime.datetime.strptime(str(att.check_in), '%Y-%m-%d %H:%M:%S').date() == datetime.datetime.strptime(str(date), '%Y-%m-%d %H:%M:%S').date():
                                            att.write({'check_out':date,'check_out_source':machine.machine_name})
                                            found = True
                                            break
                                        attendance_id = attendance_obj.search([('employee_id','=',employee_id.id),('check_in','=',str(date))])
                                        if not attendance_id:
                                            attendance_obj.create({'check_in':date,'check_out':date,'employee_id':employee_id.id,'check_in_source':machine.machine_name,'check_out_source':machine.machine_name})
                                else:
                                    attendance_obj.create({'check_out':date,'employee_id':employee_id.id,'check_out_source':machine.machine_name})
            except Exception as e:
                #raise UserError(e)
                uio = False
            finally:
                if conn:
                    conn.enable_device()
                    conn.disconnect()
            
                    
                
class HrAttendance(models.Model):
    _inherit = "hr.attendance"
    
    check_in = fields.Datetime(string="Check In", default='', required=False)
    check_in_source = fields.Char(string="Check In Source", required=False, store=True, readonly=True)
    check_out_source = fields.Char(string="Check Out Source", required=False, store=True, readonly=True)
    

    def name_get(self):
        result = []
        for attendance in self:
            if not attendance.check_out:
                result.append((attendance.id, _("%(empl_name)s from %(check_in)s") % {
                    'empl_name': attendance.employee_id.name,
                    'check_in': fields.Datetime.to_string(fields.Datetime.context_timestamp(attendance, fields.Datetime.from_string(attendance.check_in))),
                }))
            else:
                if attendance.check_in:
                    result.append((attendance.id, _("%(empl_name)s from %(check_in)s to %(check_out)s") % {
                        'empl_name': attendance.employee_id.name,
                        'check_in': fields.Datetime.to_string(fields.Datetime.context_timestamp(attendance, fields.Datetime.from_string(attendance.check_in))),
                        'check_out': fields.Datetime.to_string(fields.Datetime.context_timestamp(attendance, fields.Datetime.from_string(attendance.check_out))),
                    }))
                else:
                    result.append((attendance.id, _("%(empl_name)s from %(check_in)s to %(check_out)s") % {
                        'empl_name': attendance.employee_id.name,
                        'check_in': 'Undefined',
                        'check_out': fields.Datetime.to_string(fields.Datetime.context_timestamp(attendance, fields.Datetime.from_string(attendance.check_out))),
                    }))
        return result
    
    
    @api.depends('check_in', 'check_out')
    def _compute_worked_hours(self):
        for attendance in self:
            if attendance.check_in and attendance.check_out:
                delta = attendance.check_out - attendance.check_in
                attendance.worked_hours = delta.total_seconds() / 3600.0
    
    @api.constrains('check_in', 'check_out', 'employee_id')
    def _check_validity(self):
        """ Verifies the validity of the attendance record compared to the others from the same employee.
            For the same employee we must have :
                * maximum 1 "open" attendance record (without check_out)
                * no overlapping time slices with previous employee records
        """
        for attendance in self:
            # we take the latest attendance before our check_in time and check it doesn't overlap with ours
            last_attendance_before_check_in = self.env['hr.attendance'].search([
                ('employee_id', '=', attendance.employee_id.id),
                ('check_in', '<=', attendance.check_in),
                ('id', '!=', attendance.id),
            ], order='check_in desc', limit=1)
            if last_attendance_before_check_in and last_attendance_before_check_in.check_out and last_attendance_before_check_in.check_out > attendance.check_in:
                raise exceptions.ValidationError(_("Cannot create new attendance record for %(empl_name)s, the employee was already checked in on %(datetime)s") % {
                    'empl_name': attendance.employee_id.name,
                    'datetime': fields.Datetime.to_string(fields.Datetime.context_timestamp(self, fields.Datetime.from_string(attendance.check_in))),
                })

            if not attendance.check_out:
                # if our attendance is "open" (no check_out), we verify there is no other "open" attendance
                no_check_out_attendances = self.env['hr.attendance'].search([
                    ('employee_id', '=', attendance.employee_id.id),
                    ('check_out', '=', False),
                    ('id', '!=', attendance.id),
                ])
                # ~ if no_check_out_attendances:
                    # ~ raise exceptions.ValidationError(_("Cannot create new attendance record for %(empl_name)s, the employee hasn't checked out since %(datetime)s") % {
                        # ~ 'empl_name': attendance.employee_id.name_related,
                        # ~ 'datetime': fields.Datetime.to_string(fields.Datetime.context_timestamp(self, fields.Datetime.from_string(no_check_out_attendances.check_in))),
                    # ~ })
            else:
                # we verify that the latest attendance with check_in time before our check_out time
                # is the same as the one before our check_in time computed before, otherwise it overlaps
                last_attendance_before_check_out = self.env['hr.attendance'].search([
                    ('employee_id', '=', attendance.employee_id.id),
                    ('check_in', '<', attendance.check_out),
                    ('id', '!=', attendance.id),
                ], order='check_in desc', limit=1)
                if last_attendance_before_check_out and last_attendance_before_check_in != last_attendance_before_check_out:
                    raise exceptions.ValidationError(_("Cannot create new attendance record for %(empl_name)s, the employee was already checked in on %(datetime)s") % {
                        'empl_name': attendance.employee_id.name,
                        'datetime': fields.Datetime.to_string(fields.Datetime.context_timestamp(self, fields.Datetime.from_string(last_attendance_before_check_out.check_in))),
                    })                     



class hrEmployee(models.Model):
    _inherit = 'hr.employee'
    
    zk_location_line_ids = fields.One2many('zk.employee.location.line','employee_id',string='Locations')

    def msg_box(self, title='', message=''):
        view = self.env.ref('sh_message.sh_message_wizard')
        # view_id = view and view.id or False
        context = dict(self._context or {})
        context['message'] = message
        return {
            'name':title,
            'type':'ir.actions.act_window',
            'view_type':'form',
            'view_mode':'form',
            'res_model':'sh.message.wizard',
            'views':[(view.id,'form')],
            'view_id':view.id,
            'target':'new',
            'context':context,
        }
    
    def delete_employee_zk(self):
        machine_id = self.env['zk.machine'].search([('id','=',int(self.env.context.get('machine_id')))])
        machine_ip = machine_id.name
        port = machine_id.port
        zk = ZK(machine_ip, port=port, timeout=10, password=0, force_udp=False, ommit_ping=True)
        conn = ''
        try:
            conn = zk.connect()
            conn.disable_device()
            employee_location_line = self.env['zk.employee.location.line'].search([('employee_id','=',self.id),('machine_id','=',machine_id.id)])
            conn.delete_user(uid=employee_location_line.uid)
            machine_id.employee_ids = machine_id.employee_ids - self
            employee_location_line.unlink()
        except Exception as e:
            raise UserError('Unable to complete user registration:\n'+str(e))
        finally:
            if conn != '':
                conn.enable_device()
                conn.disconnect()
        return True
    
    def disassociate_employee_zk(self):
        machine_id = self.env['zk.machine'].search([('id','=',int(self.env.context.get('machine_id')))])
        employee_location_line = self.env['zk.employee.location.line'].search([('employee_id','=',self.id),('machine_id','=',machine_id.id)])
        machine_id.employee_ids = machine_id.employee_ids - self
        employee_location_line.unlink()
        return True

    @api.model
    def create(self, vals):
        if vals.get('user_id'):
            user = self.env['res.users'].browse(vals['user_id'])
            vals.update(self._sync_user(user))
            vals['name'] = vals.get('name', user.name)
        employee = super(hrEmployee, self).create(vals)
        # raise UserError('CREATE\n\n'+str(vals))
        url = '/web#%s' % url_encode({
            'action': 'hr.plan_wizard_action',
            'active_id': employee.id,
            'active_model': 'hr.employee',
            'menu_id': self.env.ref('hr.menu_hr_root').id,
        })
        employee._message_log(body=_('<b>Congratulations!</b> May I recommend you to setup an <a href="%s">onboarding plan?</a>') % (url))
        if employee.department_id:
            self.env['mail.channel'].sudo().search([
                ('subscription_department_ids', 'in', employee.department_id.id)
            ])._subscribe_users()
        employee.identification_id = str(employee.id)
        return employee

    def write(self, vals):
        if 'address_home_id' in vals:
            account_id = vals.get('bank_account_id') or self.bank_account_id.id
            if account_id:
                self.env['res.partner.bank'].browse(account_id).partner_id = vals['address_home_id']
        if vals.get('user_id'):
            vals.update(self._sync_user(self.env['res.users'].browse(vals['user_id'])))
        res = super(hrEmployee, self).write(vals)
        # raise UserError('WRITE\n\n'+str(vals))
        if vals.get('department_id') or vals.get('user_id'):
            department_id = vals['department_id'] if vals.get('department_id') else self[:1].department_id.id
            # When added to a department or changing user, subscribe to the channels auto-subscribed by department
            self.env['mail.channel'].sudo().search([
                ('subscription_department_ids', 'in', department_id)
            ])._subscribe_users()
        return res


class hrZkEmployeeLocationLine(models.Model):
    _name = 'zk.employee.location.line'

    employee_id = fields.Many2one('hr.employee',string="Employee")
    zk_num = fields.Integer(string="ZKSoftware Number", help="ZK Attendance User Code",required=True)
    machine_id = fields.Many2one('zk.machine',string="Machine",required=True)
    machine_name = fields.Char(related='machine_id.machine_name')
    location_id =  fields.Many2one('zk.machine.location',related='machine_id.location_id', string="Location")
    uid =  fields.Integer('Uid')
    
    _sql_constraints = [('unique_location_emp', 'unique(employee_id,location_id)', 'There is a record of this employee for this location.')]
    
