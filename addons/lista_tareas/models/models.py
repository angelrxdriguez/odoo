from odoo import models, fields, api

class ListaTareas(models.Model):
    _name = 'lista_tareas.lista_tareas'
    _description = 'Lista de tareas'

    tarea = fields.Char(string="Tarea")
    prioridad = fields.Integer(string="Prioridad", default=0)
    urgente = fields.Boolean(string="Urgente", compute="_value_urgente", store=True)
    realizada = fields.Boolean(string="Realizada", default=False)
    responsable = fields.Char(string="Responsable")

    estado = fields.Selection(
        [
            ('todo', 'Por hacer'),
            ('doing', 'Haciendo'),
            ('done', 'Hecha'),
        ],
        string="Estado",
        default='todo',
    )
    fecha = fields.Date(string="Fecha") 
    @api.depends('prioridad')
    def _value_urgente(self):
        for record in self:
            record.urgente = record.prioridad > 10
 