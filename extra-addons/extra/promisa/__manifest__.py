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
        'account',
    ],
    "data": [
        # Main Configuration
        # Data
        # Security
        'security/security.xml',
        # Views
        'views/purchase_order.xml',
        'views/hr_employee.xml',
        'views/sale_order.xml',
        'views/stock_picking.xml',
        'views/account_move.xml',
        # 'views/treatment_certificate.xml',
        'views/account_payment.xml',
        'views/product_template.xml',
        # Reports
        'reports/invoice.xml',
        'reports/remision.xml',
        'reports/invoice_no_price.xml',
        # 'reports/certificado_tratamiento.xml',
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
