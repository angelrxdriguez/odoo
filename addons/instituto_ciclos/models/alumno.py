from odoo import models, fields

class InstitutoAlumno(models.Model):
    _name = "instituto.alumno"
    _description = "Alumno"

    name = fields.Char(string="Nombre y apellidos", required=True)

    modulo_ids = fields.Many2many(
        "instituto.modulo",
        "instituto_modulo_alumno_rel",
        "alumno_id",
        "modulo_id",
        string="Módulos"
    )
