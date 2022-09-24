'''
Created on Nov 26, 2018

@author: Zuhair Hammadi
'''
from odoo import models, fields, api


class HREmployee(models.Model):
    _inherit = 'hr.employee'

    employee_no = fields.Char('Employee Company ID', copy=False)

    _sql_constraints = [
        ('employee_no_unqiue', 'unique(company_id, employee_no)', 'Employee Company ID must be unique!')
    ]

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('name', operator, name), ('employee_no', operator, name)]
        return self._search(domain + args, limit=limit, access_rights_uid=name_get_uid)

    def name_get(self):
        result = []
        for record in self:
            if record.name and record.employee_no:
                display_name = record.name + ' [' + record.employee_no + ']'
                result.append((record.id, display_name))
            if not record.employee_no:
                display_name = record.name + ' []'
                result.append((record.id, display_name))
        return result
