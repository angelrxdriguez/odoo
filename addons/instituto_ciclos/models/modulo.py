from odoo import models, fields

class InstitutoModulo(models.Model):
    _name = "instituto.modulo"
    _description = "Módulo"

    name = fields.Char(string="Nombre del módulo", required=True)

    ciclo_id = fields.Many2one(
        "instituto.ciclo",
        string="Ciclo formativo",
        required=True
                )

    profesor_id = fields.Many2one(
        "instituto.profesor",
        string="Profesor"
    )

    alumno_ids = fields.Many2many(
        "instituto.alumno",
        "instituto_modulo_alumno_rel",
        "modulo_id",
        "alumno_id",
        string="Alumnos"
    )
