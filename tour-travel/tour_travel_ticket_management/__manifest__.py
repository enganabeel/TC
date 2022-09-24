#  See LICENSE file for full copyright and licensing details.
{
    'name': 'Tours & Travels Ticket Management',
    'version': '14.0.1.0.0',
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'sequence': 1,
    'license': 'AGPL-3',
    'category': 'Tours & Travels',
    'website': 'http://www.serpentcs.com',
    'description': """
        Tours & Travels Ticket Management
    """,
    'summary': """
        Tours & Travels Ticket Management
    """,
    'depends': ['tour_travel_management', 'einv_sa'],
    'data': [
        'data/report_paperformat.xml',
        'security/ir.model.access.csv',
        'views/sale_view.xml',
        'views/ticket_view.xml',
        'views/tour_registration_view.xml',
        'report/report_quotation_ticket_package.xml',
        'report/account_move.xml',
    ],
    'demo': ['demo/ticketing_data.xml'],
    'installable': True,
    'application': True,
}
