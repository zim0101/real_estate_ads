from odoo import fields, models, api
from datetime import timedelta
from odoo.exceptions import ValidationError


class AbstractOffer(models.AbstractModel):
    _name = "abstract.model.offer"
    _description = "Abstract Property Offer"

    partner_email = fields.Char(string="Email")
    partner_phone = fields.Char(string="Phone")


class PropertyOffer(models.Model):
    _name = "property_offer"
    _inherit = ["abstract.model.offer"]
    _description = 'Property Offer'

    @api.depends('property_id', 'partner_id')
    def _compute_name(self):
        for record in self:
            if record.property_id and record.partner_id:
                record.name = f"{record.property_id.name} - {record.partner_id.name}"
            else:
                record.name = False

    name = fields.Char(string="description", compute=_compute_name)
    price = fields.Float(string="Price")
    status = fields.Selection([
        ("accepted", "Accepted"),
        ("refused", "Refused")
    ], string="Status")
    validity = fields.Integer(string="Validity", default=7)
    deadline = fields.Date(string="Deadline", compute='_compute_deadline', inverse='_inverse_deadline')
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

    # cron job
    @api.autovacuum
    def _delete_refused_offers(self):
        self.search([('status', '=', 'refused')]).unlink()

    @api.model
    def _set_creation_date(self):
        return fields.Date.today()

    creation_date = fields.Date(string="Create Date", default=_set_creation_date)

    # validations

    @api.constrains('validity')
    def _check_validity(self):
        for record in self:
            if record.deadline <= record.creation_date:
                raise ValidationError("Deadline can not be before creation date!")

    def _validate_accepted_offer(self):
        offer_ids = self.env['property_offer'].search([
            ('property_id', '=', self.property_id.id),
            ('status', '=', 'accepted')
        ])

        if offer_ids:
            raise ValidationError("You have an accepted offer already!")

    # _sql_constraints = [
    #     ('check_validity', 'check(validity > 0)', 'Deadline can not be before creation date!')
    # ]

    # ----------------------- crud -----------------------
    # @api.model_create_multi
    # def create(self, vals_list):
    #     for record in vals_list:
    #         if not record.get('creation_date'):
    #             record['creation_date'] = fields.Date.today()
    #
    #     return super(PropertyOffer, self).create(vals_list)

    def action_accept_offer(self):
        if self.property_id:
            self._validate_accepted_offer()
            self.property_id.write({
                'selling_price': self.price,
                'state': 'accepted',
            })
        self.status = 'accepted'

    def action_decline_offer(self):
        self.status = 'refused'
        if all(self.property_id.offer_ids.mapped('status')):
            self.property_id.write({
                'selling_price': 0,
                'state': 'received'
            })
