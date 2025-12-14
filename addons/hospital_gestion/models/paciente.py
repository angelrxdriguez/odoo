from odoo import models, fields

class HospitalPaciente(models.Model):
    _name = "hospital.paciente"
    _description = "Paciente"

    nombre = fields.Char(string="Nombre", required=True)
    apellidos = fields.Char(string="Apellidos", required=True)
    sintomas = fields.Text(string="Síntomas")
