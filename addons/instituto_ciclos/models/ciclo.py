from odoo import models, fields

class InstitutoCiclo(models.Model):
    _name = "instituto.ciclo"
    _description = "Ciclo Formativo"

    name = fields.Char(string="Nombre del ciclo", required=True)

    modulo_ids = fields.One2many(
        "instituto.modulo",
        "ciclo_id",
        string="Módulos"
    )
