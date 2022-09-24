#  See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _


class SaleOrderTemplete(models.Model):
    _inherit = "sale.order.template"

    ticket_package_line_ids = fields.One2many('ticket.package.line',
                                              'sale_order_templete_id',
                                              string='Ticket Package Lines')
    visa_package_line_ids = fields.One2many('visa.package.line',
                                            'sale_order_templete_id',
                                            string='Visa Package Lines')

    def get_cost_price(self):
        res = super(SaleOrderTemplete, self).get_cost_price()
        for order in self:
            visa_price = sum(
                [line.cost_price for line in order.visa_package_line_ids])
            ticket_price = sum(
                [line.cost_price * line.qty for line in order.ticket_package_line_ids if line.qty != 0])
        return res + visa_price + ticket_price

    def get_sell_price(self):
        res = super(SaleOrderTemplete, self).get_sell_price()
        for order in self:
            visa_sell_price = sum(
                [line.unit_price for line in order.visa_package_line_ids])
            ticket_sell_price = sum(
                [line.unit_price * line.qty for line in order.ticket_package_line_ids if line.qty != 0])
        return res + visa_sell_price + ticket_sell_price

    @api.depends('ticket_package_line_ids.cost_price', 'visa_package_line_ids.cost_price')
    def _compute_cost_per_person(self):
        for order in self:
            total_cost = self.get_cost_price()
            order.update({'cost_per_person': total_cost})

    @api.depends('ticket_package_line_ids.unit_price', 'visa_package_line_ids.unit_price')
    def _compute_sell_per_person(self):
        for order in self:
            total_sale_price = self.get_sell_price()
            order.update({'sell_per_person': total_sale_price})


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    ticket_id = fields.Many2one('tour.registration.line', 'Ticket')
    visa_id = fields.Many2one('tour.registration.line', 'Visa')


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    ticket_line_ids = fields.One2many('tour.registration.line', 'sale_id', 'Tickets')

    def get_package_lines(self):
        ticket_lines = []
        extra_lines = []
        template = self.sale_order_template_id.with_context(
            lang=self.partner_id.lang)
        for line in template.ticket_package_line_ids:
            data = {'name': line.display_name,
                    'display_type': line.display_type}
            pax_qty = 1
            total_pax = (self.adults + self.children)
            if total_pax > 1:
                pax_qty = total_pax
            qty = 1
            while qty <= pax_qty:
                if not line.display_type:
                    data = {
                        'name': line.product_id.display_name,
                        'product_id': line.product_id.id,
                        'source_id': line.source_id.id,
                        'destination_id': line.destination_id.id,
                        'fare_type_id': line.fare_type_id.id,
                        'display_type': line.display_type,
                        'price_unit': line.unit_price,
                        'product_id': line.product_id.id,
                        'product_uom': line.product_id.uom_id.id,
                        'customer_lead': self._get_customer_lead(line.product_id.product_tmpl_id),
                    }
                    qty += 1
                ticket_lines.append((0, 0, data))
        for line in template.visa_package_line_ids:
            data = {'name': line.name,
                    'display_type': line.display_type}
            pax_qty = 1
            total_pax = (self.adults + self.children)
            if total_pax > 1:
                pax_qty = total_pax
            qty = 1
            while qty <= pax_qty:
                data = {
                    'name': line.product_id.display_name or line.name,
                    'product_id': line.product_id.id or False,
                    'price_unit': line.unit_price or False,
                    'product_uom': line.product_id.uom_id.id or False,
                    'customer_lead': self._get_customer_lead(line.product_id.product_tmpl_id),
                }
                qty += 1
            extra_lines.append((0, 0, data))
        return ticket_lines, extra_lines

    @api.onchange('sale_order_template_id')
    def onchange_sale_order_template_id(self):
        ticket_lines, extra_lines = self.get_package_lines()
        self.ticket_line_ids = [(5,)]
        self.extra_service_ids = [(5,)]
        self.update({'ticket_line_ids': ticket_lines,
                     'extra_service_ids': extra_lines})
        for rec in self.extra_service_ids:
            if rec.product_id and rec.product_id.type_travel_product == 'visa':
                rec.onchange_visa_qty()
            rec._compute_tax_id()
        for rec in self.ticket_line_ids:
            if rec.display_type == False:
                rec.onchange_ticket_qty()
                rec._compute_tax_id()
        return super(SaleOrder, self).onchange_sale_order_template_id()


class TourRegistrationLine(models.Model):
    _inherit = 'tour.registration.line'

    sale_id = fields.Many2one('sale.order', 'Ticket Order', ondelete='cascade')
    source_id = fields.Many2one('city.city', 'Source')
    destination_id = fields.Many2one('city.city', 'Destination')
    passenger_id = fields.Many2one('travellers.list', 'Passenger', ondelete='restrict')
    issue_date = fields.Date('Issue Date')
    expire_date = fields.Date('Expire Date')
    fare_type_id = fields.Many2one("fare.type", "Fare Type", ondelete='restrict')
    ticket_no = fields.Char("Ticket No")
    visa_no = fields.Char("Visa No")

    @api.model
    def create(self, vals):
        if 'sale_id' in vals:
            sale = self.env["sale.order"].browse(vals['sale_id'])
            vals.update({'order_id': sale.id})
        res = super(TourRegistrationLine, self).create(vals)
        if res.product_id and res.product_id.type_travel_product == 'tickets':
            res.order_line_id.ticket_id = res.id
        if res.product_id and res.product_id.type_travel_product == 'visa':
            res.order_line_id.visa_id = res.id
        return res

    def set_ticket_description(self):
        name_list = []
        if self.passenger_id.name:
            name_list.append("Passenger:  %s" % (self.passenger_id.name))
        if self.product_id and self.fare_type_id:
            name_list.append("%s, %s" % (self.fare_type_id.name, self.product_id.name))
        if self.source_id and self.destination_id:
            name_list.append("%s -> %s" % (self.source_id.name, self.destination_id.name))
        if self.ticket_no:
            name_list.append("PNR No: %s" % (self.ticket_no))
        name = '\n'.join(name_list)
        return name

    def set_visa_description(self):
        name_list = []
        if self.product_id and self.product_id.type_travel_product == 'visa':
            if self.passenger_id.name:
                name_list.append("Traveller:  %s" % self.passenger_id.name)
            if self.product_id:
                name_list.append("%s" % self.product_id.name)
            if self.visa_no:
                name_list.append("Visa No: %s" % self.visa_no)
            name = '\n'.join(name_list)
            return name
        return

    @api.onchange('fare_type_id', 'passenger_id', 'source_id', 'destination_id', 'ticket_no')
    def onchange_ticket_qty(self):
        for rec in self:
            rec.name = rec.set_ticket_description() or rec.name

    @api.onchange('passenger_id', 'destination_id', 'visa_no')
    def onchange_visa_qty(self):
        for rec in self:
            rec.name = rec.set_visa_description() or rec.name

    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            self.update({'product_id': self.product_id.id,
                         'order_id': self.sale_id.id})
            self.product_id_change()


class InvoiceLine(models.Model):
    _inherit = 'account.move.line'

    ticket_id = fields.Many2one('tour.registration.line', 'Ticket', related='sale_line_ids.ticket_id')
    visa_id = fields.Many2one('tour.registration.line', 'Visa', related='sale_line_ids.visa_id')
