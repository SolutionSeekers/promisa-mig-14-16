# -*- coding: utf-8 -*-

{
    'name': 'Nomina Indboo',
    'summary': 'Agrega modificaciones a los cálculos del IMSS y al reporte de raya.',
    'description': '''
    Nomina Deli
    ''',
    'author': 'IT Admin',
    'version': '14.01',
    'category': 'Employees',
    'depends': [
        'nomina_cfdi_ee', 'om_hr_payroll', 'nomina_cfdi_extras_ee',
    ],
    'data': [
        'views/hr_payslip_view.xml',
        'wizard/reporte_imss.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}
