from odoo import fields, models


class PropertyTag(models.Model):
    _name = 'property_tag'
    _description = 'Property Tag'

    name = fields.Char(string="Property Tag")
    color = fields.Integer(string="Color")
