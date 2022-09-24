from odoo import api, fields, models

from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError , AccessDenied
class HrEmployeePrivate(models.Model):
    """
    NB: Any field only available on the model hr.employee (i.e. not on the
    hr.employee.public model) should have `groups="hr.group_hr_user"` on its
    definition to avoid being prefetched when the user hasn't access to the
    hr.employee model. Indeed, the prefetch loads the data for all the fields
    that are available according to the group defined on them.
    """
    _inherit = "hr.employee"
    choose_branch = fields.Selection([
                ('a', 'Egypt'),
                        ('b', 'Madina')
                            ], string='Choose branch', required=True, default='a')
    choose_shift = fields.Selection([
        ('MorningShift', 'Morning shift'),
        ('NightShift', 'Night shift')
    ], string='Choose shift', required=True, default='MorningShift')
    group_name = fields.Selection([
        ('a', 'A 9am - 5pm'),
        ('b', 'B 10am - 6pm'),
        ('c', 'C'),
        ('d', 'D'),
        ('e', 'E'),
    ], string='group name', default='a',tracking=True,required=True)
    biometric_id = fields.Integer(string='Boimetric id' ,tracking=True,required=True)

class AttendanceReport(models.Model):
    _name = "report.attendance"
    _description="report attendance"
    dat = fields.Date(required=True,string="from")
    date_end = fields.Date(string="to")
    employee_id = fields.Many2one('hr.employee',string="Employee Egypt")
    employee_id_Madina = fields.Many2one('hr.employee',string="Employee")
    choose_group = fields.Selection([
        ('a', 'Group A'),
        ('b', 'Group B'),
        ('c', 'Group C'),
    ], string='choose option', required=True, default='a')
    choose_shift = fields.Selection([
        ('Morning', 'Morning shift'),
        ('Night', 'Night shift')
    ], string='choose option', required=True, default='Morning')
    choose_branch = fields.Selection([
        ('a', 'Egypt'),
        ('b', 'Madina')
    ], string='choose branch', required=True, default='a')
    choose_option =fields.Selection([
        ('a', 'All employees'),
        ('b', 'specific employee'),
        ('c','specific group'),
    ],string='choose option',required=True,default='a')
    @api.model
    def create(self,vals):
        res_ids = super(AttendanceReport, self).create(vals)
        if vals['date_end']:
            if vals['date_end'] < vals['dat']:
                raise UserError(("date end can't be greater than starting date"))
        return res_ids



