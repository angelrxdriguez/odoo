from odoo import models, fields

class HospitalConsulta(models.Model):
    _name = "hospital.consulta"
    _description = "Consulta"

    paciente_id = fields.Many2one(
        "hospital.paciente",
        string="Paciente",
        required=True,
        ondelete="cascade"
    )

    medico_id = fields.Many2one(
        "hospital.medico",
        string="Médico",
        required=True,
        ondelete="cascade"
    )

    diagnostico = fields.Text(string="Diagnóstico")
