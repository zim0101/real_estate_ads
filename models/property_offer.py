from odoo import fields, models, api
from datetime import timedelta


class PropertyOffer(models.Model):
    _name = 'property_offer'
    _description = 'Property Offer'

    price = fields.Float(string="Price")
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")],
        string="Status"
    )
    creation_date = fields.Date(string="Create Date")
    validity = fields.Integer(string="Validity")
    partner_id = fields.Many2one("res.partner", string="Customer")
    property_id = fields.Many2one("property", string="Property")

    @api.depends('validity', 'creation_date')
    def _compute_deadline(self):
        for record in self:
            if record.creation_date and record.validity:
                record.deadline = record.creation_date + timedelta(days=record.validity)
            else:
                record.deadline = False

    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.deadline - record.creation_date).days

    deadline = fields.Date(string="Deadline", compute=_compute_deadline, inverse=_inverse_deadline)
