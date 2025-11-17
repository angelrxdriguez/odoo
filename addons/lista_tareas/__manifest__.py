# -*- coding: utf-8 -*-
{
    'name': "Lista de tareas",
    'summary': "Sencilla Lista de tareas",
    'description': """
Sencilla lista de tareas utilizada para crear un nuevo módulo con un nuevo
modelo de datos.
""",
    'author': "Sergi García",
    'website': "https://apuntesfpinformatica.es",
    'application': True,
    'category': 'Productivity',
    'version': '0.1',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
}
