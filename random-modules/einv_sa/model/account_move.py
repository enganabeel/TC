#!/usr/bin/python
# -*- coding: utf-8 -*-
import base64
# from base64 import b64encode

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning


def generate_tlv_hex(*args):
    """to combine all tags with conversion to hex decimal"""
    b_array = bytearray()
    for index, val in enumerate(args):
        b_array.append(index + 1)
        b_array.append(len(val))
        b_array.extend(val.encode('utf-8'))
    return b_array


def generate_tlv_base64(*args):
    tlv_hex = generate_tlv_hex(args)  # true
    return str(base64.b64encode(tlv_hex), "utf-8")


class AccountMove(models.Model):
    _name = "account.move"
    _inherit = "account.move"

    discount_type = fields.Selection([('percent', 'Percentage'), ('amount', 'Amount')], string='Discount Type',
                                                 readonly=True, states={'draft': [('readonly', False)]}, default='percent')
    discount_rate = fields.Float('Discount Amount', digits=(16, 2), readonly=True,
                                             states={'draft': [('readonly', False)]})
    amount_discount = fields.Monetary(string='Discount', store=True, readonly=True, compute='_compute_amount',
                                                  track_visibility='always')

    einv_amount_sale_total = fields.Monetary(string="Amount sale total", compute="_compute_total", store='True',
                                             help="")
    einv_amount_discount_total = fields.Monetary(string="Amount discount total", compute="_compute_total", store='True',
                                                 help="")
    einv_amount_tax_total = fields.Monetary(string="Amount tax total", compute="_compute_total", store='True', help="")

    # einv_qr = fields.Char(string="Amount tax total", compute="_compute_total", store='True', help="", readonly=True)

    # region odoo standard -------------------------
    einv_sa_delivery_date = fields.Date(string='Delivery Date', default=fields.Date.context_today, copy=False)
    einv_sa_show_delivery_date = fields.Boolean(compute='_compute_show_delivery_date')
    einv_sa_qr_code_str = fields.Char(string='Zatka QR Code', compute='_compute_qr_code_str')
    einv_sa_confirmation_datetime = fields.Datetime(string='Confirmation Date', readonly=True, copy=False)

    @api.depends('country_code', 'move_type')
    def _compute_show_delivery_date(self):
        for move in self:
            move.einv_sa_show_delivery_date = move.country_code == 'SA' and move.move_type in (
                'out_invoice', 'out_refund')

    @api.depends('amount_total', 'amount_untaxed', 'einv_sa_confirmation_datetime', 'company_id', 'company_id.vat')
    def _compute_qr_code_str(self):
        """ Generate the qr code for Saudi e-invoicing. Specs are available at the following link at page 23
        https://zatca.gov.sa/ar/E-Invoicing/SystemsDevelopers/Documents/20210528_ZATCA_Electronic_Invoice_Security_Features_Implementation_Standards_vShared.pdf
        https://zatca.gov.sa/ar/E-Invoicing/SystemsDevelopers/Documents/QRCodeCreation.pdf
        """

        def get_qr_encoding(tag, field):
            company_name_byte_array = field.encode('UTF-8')
            company_name_tag_encoding = tag.to_bytes(length=1, byteorder='big')
            company_name_length_encoding = len(company_name_byte_array).to_bytes(length=1, byteorder='big')
            return company_name_tag_encoding + company_name_length_encoding + company_name_byte_array

        for record in self:
            qr_code_str = ''
            if record.einv_sa_confirmation_datetime and record.company_id.vat:
                seller_name_enc = get_qr_encoding(1, record.company_id.display_name)
                company_vat_enc = get_qr_encoding(2, record.company_id.vat)
                time_sa = fields.Datetime.context_timestamp(self.with_context(tz='Asia/Riyadh'),
                                                            record.einv_sa_confirmation_datetime)
                timestamp_enc = get_qr_encoding(3, time_sa.isoformat())
                invoice_total_enc = get_qr_encoding(4, str(record.amount_total))
                total_vat_enc = get_qr_encoding(5, str(record.currency_id.round(
                    record.amount_total - record.amount_untaxed)))

                str_to_encode = seller_name_enc + company_vat_enc + timestamp_enc + invoice_total_enc + total_vat_enc
                qr_code_str = base64.b64encode(str_to_encode).decode('UTF-8')
            record.einv_sa_qr_code_str = qr_code_str

    def _post(self, soft=True):
        res = super()._post(soft)
        for record in self:
            if record.country_code == 'SA' and record.move_type in ('out_invoice', 'out_refund'):
                if not record.einv_sa_show_delivery_date:
                    raise UserError(_('Delivery Date cannot be empty'))
                if record.einv_sa_delivery_date < record.invoice_date:
                    raise UserError(_('Delivery Date cannot be before Invoice Date'))
                self.write({
                    'einv_sa_confirmation_datetime': fields.Datetime.now()
                })
        return res

    # endregion

    @api.depends('invoice_line_ids', 'amount_total')
    def _compute_total(self):
        for r in self:
            r.einv_amount_sale_total = r.amount_untaxed + sum(line.einv_amount_discount for line in r.invoice_line_ids)
            r.einv_amount_discount_total = sum(line.einv_amount_discount for line in r.invoice_line_ids)
            r.einv_amount_tax_total = sum(line.einv_amount_tax for line in r.invoice_line_ids)

            # tags = seller_name, vat_no, inv_date, total, vat
            # r.einv_qr = generate_tlv_base64(r.company_id.name, r.company_id.vat, r.invoice_date, r.amount_total, )


class AccountMoveLine(models.Model):
    _name = "account.move.line"
    _inherit = "account.move.line"

    einv_amount_discount = fields.Monetary(string="Amount discount", compute="_compute_amount_discount", store='True',
                                           help="")
    einv_amount_tax = fields.Monetary(string="Amount tax", compute="_compute_amount_tax", store='True', help="")

    @api.depends('discount', 'quantity', 'price_unit')
    def _compute_amount_discount(self):
        for r in self:
            r.einv_amount_discount = r.quantity * r.price_unit * (r.discount / 100)

    @api.depends('tax_ids', 'discount', 'quantity', 'price_unit')
    def _compute_amount_tax(self):
        for r in self:
            r.einv_amount_tax = sum(r.price_subtotal * (tax.amount / 100) for tax in r.tax_ids)
class Company(models.Model):
    _inherit = 'res.company'
    so_double_validation = fields.Selection([
        ('one_step', 'Confirm sale orders in one step'),
        ('two_step', 'Get 2 levels of approvals to confirm a sale order')], string="Levels of Approvals", default='one_step',
        help="Provide a double validation mechanism for sales discount")
    so_double_validation_limit = fields.Float(string="Percentage of Discount that requires double validation'",
                                                          help="Minimum discount percentage for which a double validation is required")
class ResDiscountSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    so_order_approval = fields.Boolean("Sale Discount Approval", default=lambda self: self.env.user.company_id.so_double_validation == 'two_step')
    so_double_validation = fields.Selection(related='company_id.so_double_validation',string="Levels of Approvals *", readonly=False)
    so_double_validation_limit = fields.Float(string="Discount limit requires approval in %",related='company_id.so_double_validation_limit', readonly=False)
    def set_values(self):
        super(ResDiscountSettings, self).set_values()
        self.so_double_validation = 'two_step' if self.so_order_approval else 'one_step'

