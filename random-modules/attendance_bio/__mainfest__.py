# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'ATTENDANCE_REPORT',
    'version': '1.1',
    'category': 'Education',
    'sequence': 15,
    'summary': '',
    'description': "",
    'website': '',
    'license':'LGPL-3',
    'depends': [
        'mail',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/attend_bio.xml'
    ],
    'demo': [

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
