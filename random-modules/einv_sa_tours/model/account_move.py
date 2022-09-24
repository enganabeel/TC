#!/usr/bin/python
# -*- coding: utf-8 -*-
import base64
# from base64 import b64encode

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning
import calendar
from datetime import date, datetime, time
from datetime import timedelta
from collections import defaultdict

class AccountMove(models.Model):
    _name = "account.move"
    _inherit = "account.move"

    einv_is_tour = fields.Boolean(string='Is Tour Invoice?')
    einv_diff_tax = fields.Float(string='Tax 15 %',readonly=True)
    tax_five_percent = fields.Float(string='ضريبة الاستقطاع',readonly=True)
    einv_is_hotel = fields.Boolean(string='Activate hotels ?')
    einv_is_ticket = fields.Boolean(string='Activate Ticket?')
    einv_is_visa = fields.Boolean(string='Activate Visas')
    total_amount_hotels = fields.Float(string='amount',readonly=True,store=True)
    WithHold_hotels = fields.Float(string='الضريبه الاستقطاعيه',readonly=True,store=True)
    total_tax_hotels = fields.Float(string='15%',readonly=True,store=True)
    hotel_create_line = fields.One2many('hotel.create.lines', 'child_id', string='V') 
    total_tax_visas = fields.Float(string='15%',readonly=True)
    total_amount_visas = fields.Float(string='amount',readonly=True)
   # total_tax_visas = fields.Float(string='15%',readonly=True)
   # total_amount_visas = fields.Float(string='amount',readonly=True)
   # total_tax_visas = fields.Float(string='15%',readonly=True)
   # total_amount_visas = fields.Float(string='amount',readonly=True)
    visas_create_line = fields.One2many('visas.create.lines', 'child_id_visas', string='V')
class HotelPage(models.Model):

    _name = 'hotel.create.lines'
    _description = 'Here to create new hotel'
    child_id = fields.Many2one('account.move',string='Hotel Id')
    country = fields.Many2one('res.country',string='البلد')
    hotel_name = fields.Many2one('product.template',string='اسم الفندق')
    number_of_night = fields.Integer(string='عدد الليالي',readonly=False)
    Date_of_entry = fields.Date('تاريخ الدخول')
    Date_of_exit = fields.Date('تاريخ الخروج')
    type_of_hotel = fields.Selection([('in_hotel','الفنادق الدخليه'),
        ('inter_hotel','فنادق دوليه-مورد داخلي'),
        ('inter_hotel_ex_res','فنادق دوليه-مورد خارجي')
        ,],
        string='نوع الفندق')

    night_price = fields.Float(string='سعر الليله',readonly=False)
    org_price = fields.Float(string='التكلفه',readonly=False)
    total = fields.Float('الاجمالي')

class VisaPage(models.Model):

    _name = 'visas.create.lines'
    _description = 'Here to create new visas'
   # name_child = fields.Char('Name')
   # age_child = fields.Integer('Age')
    
    child_id_visas = fields.Many2one('account.move',string='Hotel Id')
    country_account = fields.Many2one('account.country',string='Visa')
    visa_type = fields.Char(string='نوع الفيزا',related='country_account.country_name')
    service = fields.Char(string='الخدمه',related='country_account.service')

    # = fields.Integer(string='ﻉﺩﺩ ﺎﻠﻠﻳﺎﻠﻳ',readonly=False)
    visa_duration = fields.Char(string='مدة الفيزا ',related='country_account.duration')
    client_name = fields.Char('اسم العميل')
    price_unit = fields.Float('سعر الوحده',related='country_account.price',readonly=False)
    number_of_units = fields.Float(string='العدد',readonly=False)
    discount = fields.Float(string='الخصم',readonly=False)
    total = fields.Float('الاجمالي')
    original_price_visa = fields.Float(string='التكلفه',related='country_account.original_price',readonly=False)
class AccountMoveLine(models.Model):
    _name = "account.move.line"
    _inherit = "account.move.line"

    einv_ticket_no = fields.Char(string='Ticket No.')
    einv_passenger_name = fields.Char(string='Passenger Name')
    einv_route = fields.Char(string='Route')
    einv_original_price = fields.Float(string='Original Price')
    temp_price_total = fields.Monetary(string='Total taxed per line')
#        temp_price_total = fields.Monetary(string='Total taxed per line')

    type_of_tourism_line = fields.Selection([('in_ticket','التذكره الداخليه'),
        ('inter_ticket','التذكره الدوليه'),
        ('inter_ticket_ex_res','مورد خارجي-التذكره الدوليه')
        ,],
        string='Type of tourism')

class AccountCountry(models.Model):
    _name = 'account.country'
    _inherit = ['mail.thread']
    country_name = fields.Char(required=True)
    service = fields.Char(required=True)
    price = fields.Float(tracking=True)
    duration = fields.Char(required=True)
    original_price = fields.Float()
    tax = fields.Selection([
        ('tax','tax'),
        ('notax','No tax')
    ],required=False)

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, '%s - %s - %s'  % (rec.country_name, rec.service,rec.duration)))
        return result

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        if args is None:
            args = []
        domain = args + ['|', ('country_name', operator, name), ('service', operator, name)]
        return self._search(domain, limit=limit, access_rights_uid=name_get_uid)
class HrPayslip(models.Model):
    _inherit = 'hr.payslip'
    first_month = fields.Boolean()
    is_madina = fields.Boolean()
    deduct_emp = fields.Integer()
    adjustments = fields.Float()
    currency_difference = fields.Float()
    def compute_sheet(self):

        for payslip in self:
            number = payslip.number or self.env['ir.sequence'].next_by_code('salary.slip')
            # delete old payslip lines
            payslip.line_ids.unlink()
            # set the list of contract for which the rules have to be applied
            # if we don't give the contract, then the rules to apply should be for all current contracts of the employee
            contract_ids = payslip.contract_id.ids or \
                           self.get_contract(payslip.employee_id, payslip.date_from, payslip.date_to)
            lines = [(0, 0, line) for line in self._get_payslip_lines(contract_ids, payslip.id)]
            payslip.write({'line_ids': lines, 'number': number})
        return True
    @api.model
    def _get_payslip_lines(self, contract_ids, payslip_id):

        def _sum_salary_rule_category(localdict, category, amount):
            if category.parent_id:
                localdict = _sum_salary_rule_category(localdict, category.parent_id, amount)
            localdict['categories'].dict[category.code] = category.code in localdict['categories'].dict and \
                                                          localdict['categories'].dict[category.code] + amount or amount
            return localdict

        class BrowsableObject(object):
            def __init__(self, employee_id, dict, env):
                self.employee_id = employee_id
                self.dict = dict
                self.env = env

            def _getattr_(self, attr):
                return attr in self.dict and self.dict._getitem_(attr) or 0.0

        class InputLine(BrowsableObject):
            """a class that will be used into the python code, mainly for usability purposes"""

            def sum(self, code, from_date, to_date=None):
                if to_date is None:
                    to_date = fields.Date.today()
                self.env.cr.execute("""
                    SELECT sum(amount) as sum
                    FROM hr_payslip as hp, hr_payslip_input as pi
                    WHERE hp.employee_id = %s AND hp.state = 'done'
                    AND hp.date_from >= %s AND hp.date_to <= %s AND hp.id = pi.payslip_id AND pi.code = %s""",
                                    (self.employee_id, from_date, to_date, code))
                return self.env.cr.fetchone()[0] or 0.0

        class WorkedDays(BrowsableObject):
            """a class that will be used into the python code, mainly for usability purposes"""

            def _sum(self, code, from_date, to_date=None):
                if to_date is None:
                    to_date = fields.Date.today()
                self.env.cr.execute("""
                    SELECT sum(number_of_days) as number_of_days, sum(number_of_hours) as number_of_hours
                    FROM hr_payslip as hp, hr_payslip_worked_days as pi
                    WHERE hp.employee_id = %s AND hp.state = 'done'
                    AND hp.date_from >= %s AND hp.date_to <= %s AND hp.id = pi.payslip_id AND pi.code = %s""",
                                    (self.employee_id, from_date, to_date, code))
                return self.env.cr.fetchone()

            def sum(self, code, from_date, to_date=None):
                res = self._sum(code, from_date, to_date)
                return res and res[0] or 0.0

            def sum_hours(self, code, from_date, to_date=None):
                res = self._sum(code, from_date, to_date)
                return res and res[1] or 0.0

        class Payslips(BrowsableObject):
            """a class that will be used into the python code, mainly for usability purposes"""

            def sum(self, code, from_date, to_date=None):
                if to_date is None:
                    to_date = fields.Date.today()
                self.env.cr.execute("""SELECT sum(case when hp.credit_note = False then (pl.total) else (-pl.total) end)
                            FROM hr_payslip as hp, hr_payslip_line as pl
                            WHERE hp.employee_id = %s AND hp.state = 'done'
                            AND hp.date_from >= %s AND hp.date_to <= %s AND hp.id = pl.slip_id AND pl.code = %s""",
                                    (self.employee_id, from_date, to_date, code))
                res = self.env.cr.fetchone()
                return res and res[0] or 0.0

        # we keep a dict with the result because a value can be overwritten by another rule with the same code
        result_dict = {}
        rules_dict = {}
        worked_days_dict = {}
        inputs_dict = {}
        blacklist = []
        list_minus = []

        not_salary = 0.0
        diff_sal = 0.0
        HouseRA = 0.0
        test = 0.0
        cur_difference = 0.0
        adjust = 0.0

        payslip = self.env['hr.payslip'].browse(payslip_id)
        for worked_days_line in payslip.worked_days_line_ids:
            worked_days_dict[worked_days_line.code] = worked_days_line
        for input_line in payslip.input_line_ids:
            inputs_dict[input_line.code] = input_line

        categories = BrowsableObject(payslip.employee_id.id,{} , self.env)
        inputs = InputLine(payslip.employee_id.id, inputs_dict, self.env)
        worked_days = WorkedDays(payslip.employee_id.id, worked_days_dict, self.env)
        payslips = Payslips(payslip.employee_id.id, payslip, self.env)
        rules = BrowsableObject(payslip.employee_id.id, rules_dict, self.env)

        baselocaldict = {'categories': categories, 'rules': rules, 'payslip': payslips, 'worked_days': worked_days,
                         'inputs': inputs}
        # get the ids of the structures on the contracts and their parent id as well
        contracts = self.env['hr.contract'].browse(contract_ids)
        if len(contracts) == 1 and payslip.struct_id:
            structure_ids = list(set(payslip.struct_id._get_parent_structure().ids))
        else:
            structure_ids = contracts.get_all_structures()
        # get the rules of the structure and thier children
        rule_ids = self.env['hr.payroll.structure'].browse(structure_ids).get_all_rules()
        # run the rules by sequence
        sorted_rule_ids = [id for id, sequence in sorted(rule_ids, key=lambda x: x[1])]
        sorted_rules = self.env['hr.salary.rule'].browse(sorted_rule_ids)

        for contract in contracts:
            employee = contract.employee_id
            localdict = dict(baselocaldict, employee=employee, contract=contract)
            for rule in sorted_rules:
                key = rule.code + '-' + str(contract.id)
                localdict['result'] = None
                localdict['result_qty'] = 1.0
                localdict['result_rate'] = 100
                # check if the rule can be applied
                if rule._satisfy_condition(localdict) and rule.id not in blacklist:
                    # compute the amount of the rule
                    amount, qty, rate = rule._compute_rule(localdict)
                    # check if there is already a rule computed with that code
                    previous_amount = rule.code in localdict and localdict[rule.code] or 0.0
                    #############################################################
                    for emp in self:
                        emp._cr.execute('''
                                               select date_start from hr_contract where employee_id = %s
                                                ''', [emp.employee_id.id])
                        res_supervisor_approve = emp._cr.fetchall()
                        boolean_first = emp.first_month
                        boolean_madina = emp.is_madina
                        ded_emp = emp.deduct_emp
                        cur_difference = emp.currency_difference
                        adjust = emp.adjustments

                    contract_date = res_supervisor_approve[0][0]
                    today = date.today()
                    mon = str(contract_date).split('-')[1]
                    year = str(contract_date).split('-')[0]
                    # today =
                    mon = mon[1]
                    sting_days = calendar.monthrange(int(str(contract_date).split('-')[0]), int(mon))
                    string_conc = year + '-' + mon + '-' + str(sting_days[1])
                    dt_obj = datetime.strptime(string_conc, '%Y-%m-%d').date()
                    count = 0

                    gross_salaire = 0
                    for d_ord in range(contract_date.toordinal(), dt_obj.toordinal()):
                        d = date.fromordinal(d_ord)
                        if (d.weekday() == 4):
                            count += 1
                    print(amount, 'amount')
                    if amount < 0 and rule.category_id.name !='House Rent Allowance':
                        try:
                            amount = ded_emp
                        except:
                            pass
                        if amount == -1:
                            amount =0

                        list_minus.append(amount)

                    delta = dt_obj - contract_date
                    total_days = (delta.days - count) + 1
                    print('rule.total_days', rule.category_id.id,rule.category_id.name,rule.id)
                    # if rule.category_id.id != 'Basic'  and rule.category_id.name != 'Net' and rule.category_id.name != 'Gross' and amount >0:
                    if rule.category_id.name =='Adjustments':
                        amount = adjust
                    if rule.category_id.name =='currency_difference':
                        amount = cur_difference
                    
                    if rule.category_id.name !='currency_difference' and rule.category_id.name !='Adjustments' and rule.category_id.name !='Net' and rule.category_id.name !='Gross' and rule.category_id.name !='Basic' and amount >0:
                        not_salary +=amount
                    if rule.category_id.name =='House Rent Allowance':
                        HouseRA = amount
                    # if rule.category_id.name == 'Basic':
                    if rule.category_id.name =='Basic':
                        basic_salaire = amount
                    # if rule.category_id.id == 'Gross':
                    elif rule.category_id.name =='Gross':
                        gross_salaire = amount
                        diff_sal = gross_salaire - basic_salaire

                        diff_sal = not_salary
                        amount = amount +diff_sal
                        # if rule.category_id.id == 'Net':
                    elif rule.category_id.name =='Net':
                        # total_amount_salary = amount / total_hours_worked
                        total_amount_salary = (basic_salaire / 30)
                        print(total_amount_salary, 'total_amount_salary')
                            # amount = ((total_amount_salary * total_days) + diff_sal ) + sum(list_minus)
                        if  boolean_first:
                            amount = ((total_amount_salary * (delta.days-1)) + diff_sal) + sum(list_minus) - test
                        else:
                            if not boolean_madina:
                                amount = cur_difference + adjust + amount + diff_sal + sum(list_minus) - test
                            else:
                                amount = amount + diff_sal + sum(list_minus) - test
                    if rule.category_id.name =='Insurance_madina' and boolean_madina:
                        test = (HouseRA + basic_salaire)*0.10
                        amount = -test
                    ############################################################
                    # set/overwrite the amount computed for this rule in the localdict
                    tot_rule = amount * qty * rate / 100.0
                    localdict[rule.code] = tot_rule
                    rules_dict[rule.code] = rule
                    # sum the amount for its salary category
                    localdict = _sum_salary_rule_category(localdict, rule.category_id, tot_rule - previous_amount)
                    # create/overwrite the rule in the temporary results
                    result_dict[key] = {
                        'salary_rule_id': rule.id,
                        'contract_id': contract.id,
                        'name': rule.name,
                        'code': rule.code,
                        'category_id': rule.category_id.id,
                        'sequence': rule.sequence,
                        'appears_on_payslip': rule.appears_on_payslip,
                        'condition_select': rule.condition_select,
                        'condition_python': rule.condition_python,
                        'condition_range': rule.condition_range,
                        'condition_range_min': rule.condition_range_min,
                        'condition_range_max': rule.condition_range_max,
                        'amount_select': rule.amount_select,
                        'amount_fix': rule.amount_fix,
                        'amount_python_compute': rule.amount_python_compute,
                        'amount_percentage': rule.amount_percentage,
                        'amount_percentage_base': rule.amount_percentage_base,
                        'register_id': rule.register_id.id,
                        'amount': amount,
                        'employee_id': contract.employee_id.id,
                        'quantity': qty,
                        'rate': rate,
                    }
                else:
                    # blacklist this rule and its children
                    blacklist += [id for id, seq in rule._recursive_search_of_rules()]

        return list(result_dict.values()) 
class HrPayslipLine(models.Model):
    _inherit = 'hr.payslip.line'
    

    @api.depends('quantity', 'amount', 'rate')
    def _compute_total(self):
        for line in self:
            global current_deduct
            if line.amount<=0:
                current_deduct = line.amount
               # print('current_deduct',current_deduct)
            # current_deduct = line.amount
            # print('line.amount',current_deduct)
            line.total = float(line.quantity) * line.amount * line.rate / 100
class HelpdeskTicketTeam(models.Model):
    _inherit = "helpdesk.ticket.team"
    todo_ticket_ids = fields.Many2one()
