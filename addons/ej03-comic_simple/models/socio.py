from odoo import models, fields
class BibliotecaSocio(models.Model):
    _name = 'biblioteca.socio'
    _description = 'Socio'

    identificador = fields.Char(string="Identificador", required=True)
    nombre = fields.Char(string="Nombre", required=True)
    apellido = fields.Char(string="Apellido", required=True)
