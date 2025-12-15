{
    "name": "Ciclos Instituto",
    "summary": "Ciclos, módulos, alumnos y profesores",
    "version": "1.0",
    "category": "Tools",
    "depends": ["base"],
"data": [
    "security/groups.xml",
    "security/ir.model.access.csv",

    "views/ciclo_views.xml",
    "views/modulo_views.xml",
    "views/alumno_views.xml",
    "views/profesor_views.xml",
    "views/menus.xml",
],


    "application": True,
    "installable": True,
}
