# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2021-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Cybrosys Techno Solutions(<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

{
    'name': 'Dynamic Financial Reports',
    'version': '14.02',
    'category': 'Accounting',
    'summary': """Reportes contables""",
    'description': "Dynamic Financial Reports, DynamicFinancialReports, FinancialReport, Accountingreports, odoo reports, odoo"
                   "This module creates dynamic Accounting General Ledger, Trial Balance, Balance Sheet "
                   "Proft and Loss, Cash Flow Statements, Partner Ledger,"
                   "Partner Ageing, Day book"
                   "Bank book and Cash book reports in Odoo 14 community edition.",
    'author': 'Cybrosys Techno Solutions',
    'website': "https://www.cybrosys.com",
    'depends': ['base', 'base_accounting_kit','account', 'report_xlsx', 'date_range'],
    'data': [
        'security/ir.model.access.csv',
        'data/data_financial_report.xml',
        'views/templates.xml',
        'views/views.xml',
        'views/kit_menus.xml',
        'views/financial_report_view.xml',
        'views/account_view.xml',
        'report/general_ledger.xml',
       # 'report/financial_report_template.xml',
        'report/partner_ledger.xml',
        'report/ageing.xml',
        'wizard/financial_report_view.xml',
        'wizard/trial_balance_wizard_view.xml',
        'menuitems.xml',
        'reports.xml',
        'report/templates/layouts.xml',
        'report/templates/trial_balance.xml',
        'views/report_trial_balance.xml',
    ],
    'qweb': [
        'static/src/xml/general_ledger_view.xml',
        'static/src/xml/financial_reports_view.xml',
        'static/src/xml/partner_ledger_view.xml',
        'static/src/xml/ageing.xml',
        'static/src/xml/view.xml',
        'static/src/xml/report.xml',
    ],
    'license': 'LGPL-3',
    'images': ['static/description/banner.png'],
    'installable': True,
    'auto_install': False,
    'application': True,
}
