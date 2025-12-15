from odoo import models, fields

class InstitutoProfesor(models.Model):
    _name = "instituto.profesor"
    _description = "Profesor"

    name = fields.Char(string="Nombre y apellidos", required=True)

    modulo_ids = fields.One2many(
        "instituto.modulo",
        "profesor_id",
        string="Módulos que imparte"
    )
