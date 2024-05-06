from odoo import models, fields


class PropertyType(models.Model):
    _name = "property_type"
    _description = "Property description"

    name = fields.Char(string="Property Type", required=True)