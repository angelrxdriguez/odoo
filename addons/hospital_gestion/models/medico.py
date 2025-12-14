from odoo import models, fields

class HospitalMedico(models.Model):
    _name = "hospital.medico"
    _description = "Médico"

    nombre = fields.Char(string="Nombre", required=True)
    apellidos = fields.Char(string="Apellidos", required=True)
    num_colegiado = fields.Char(string="Número de colegiado", required=True)
