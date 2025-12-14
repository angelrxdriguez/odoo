from odoo import models, fields, api
from odoo.exceptions import ValidationError
class BibliotecaEjemplar(models.Model):
    _name = "biblioteca.ejemplar"
    _description = "Ejemplar de cómic"

    codigo = fields.Char(string="Código", required=True)

    comic_id = fields.Many2one(
        "biblioteca.comic",
        string="Cómic",
        required=True,
        ondelete="cascade"
    )
    estado = fields.Selection(
    [("disponible", "Disponible"), ("prestado", "Prestado")],
    string="Estado",
    default="disponible"
    )

    socio_id = fields.Many2one(
        "biblioteca.socio",
        string="Prestado a"
    )

    fecha_inicio = fields.Date(string="Fecha inicio")
    fecha_fin = fields.Date(string="Fecha fin")
    @api.constrains("fecha_inicio", "fecha_fin")
    def _check_fechas_prestamo(self):
        hoy = fields.Date.context_today(self)

        for rec in self:
            if rec.fecha_inicio and rec.fecha_inicio > hoy:
                raise ValidationError("La fecha de préstamo no puede ser posterior al día actual.")

            if rec.fecha_fin and rec.fecha_fin < hoy:
                raise ValidationError("La fecha prevista de devolución no puede ser anterior al día actual.")