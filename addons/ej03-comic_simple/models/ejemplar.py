from odoo import models, fields

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
