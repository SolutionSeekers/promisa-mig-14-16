# coding: utf-8
{
    "name": "Promisa's ERP Instance",
    "author": "Indboo",
    "summary": """
    All the necessary modules to auto install our service instance
    """,
    "website": "https://odoo.indboo.net",
    "license": "LGPL-3",
    "category": "Promisa ",
    "version": "14.0",
    "depends": [
        # Account section

        # Project Section.

        # Human resources

        # Localizations

        # Website modules

        # Sales
        # Tools
        'product',
        'stock',
        'purchase',
        'sale',
        'nomina_cfdi_ee',
    ],
    "data": [
        # Main Configuration
        # Data
        # Security
        'security/security.xml',
        # Views
        'views/purchase_order.xml',
        'views/hr_employee.xml',
        # Reports
        'reports/invoice.xml',
        'reports/remision.xml',
        # Wizards (One Per Wizard)
        # Stages Data
    ],
    "demo": [
    ],
    "test": [
    ],
    "qweb": [''],
    "auto_install": False,
    "application": True,
    "installable": True,
}
