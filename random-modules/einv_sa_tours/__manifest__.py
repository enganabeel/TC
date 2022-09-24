# -*- coding: utf-8 -*-

{
    "name": "Tourism e-Invoice KSA",
    "version": "1.3",
    "depends": [
        'base', 'web', 'account', 'einv_sa','hr_payroll_community',
    ],
    "author": "Genius Valley",
    "category": "Accounting",
    "website": "https://genius-valley.com/",
    "support": "odoo@gvitt.com",
    "images": ["static/description/assets/main_screenshot.gif", "static/description/assets/main_screenshot.png",
               "static/description/assets/ghits_desktop_inv.jpg",
               "static/description/assets/ghits_labtop1.jpg"],
    "price": "0",
    "license": "OPL-1",
    "currency": "USD",
    "summary": "e-Invoice in Kingdom of Saudi Arabia KSA | tax invoice | vat  | electronic | e invoice | accounting | tax | free | ksa | sa |Zakat, Tax and Customs Authority | الفاتورة الضريبية | الفوترة  الالكترونية |   هيئة الزكاة والضريبة والجمارك",
    "description": """
    e-Invoice in Kingdom of Saudi Arabia
    and prepare tax invoice to be ready for the second phase.
    Zakat, Tax and Customs Authority
    الفوترة الإلكترونية - الفاتورة الضريبية - المملكة العربية السعودية
    المرحلة الاولي -  مرحلة الاصدار 
    هيئة الزكاة والضريبة والجمارك

    Versions History --------------------
                * version 1.3: 27-Nov-2021
                 - update qrcode format with base64 ref:
                 https://zatca.gov.sa/ar/E-Invoicing/SystemsDevelopers/Documents/QRCodeCreation.pdf 
                 
                * version 1.2: 27-sept-2021
                  - fix field vat when qrcode scanning 
                
                * version 1.1: 26-sept-2021
                    - Add fields (company_id.name,company_id.vat,
                        invoice_date,amount_total,amount_tax_signed) to qrcode scanning 
                    - Update Tax Invoice from html to pdf
               
                * version 1.0: 20-sept-2021
                    - Initial version contains missing fields to generate tax invoice report with qrcode
    
    """
    ,
    "data": [
         "security/ir.model.access.csv",
        "data/report_paperformat.xml",
        "report/account_move.xml",
        "view/account_move_views.xml",
    ],
    "installable": True,
    "auto_install": False,
    "application": True,
}