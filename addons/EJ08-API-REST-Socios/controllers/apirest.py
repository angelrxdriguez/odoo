# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json

# ------------------------------------------------------------------------------
# CONTROLADOR API REST
# Permite realizar operaciones CRUD sobre el modelo 'socio' mediante llamadas HTTP.
# Ejemplos de uso:
# - POST: crear socio
# - PUT/PATCH: modificar socio
# - GET: consultar socio
# - DELETE: eliminar socio
# ------------------------------------------------------------------------------

class ApiRest(http.Controller):

    # --------------------------------------------------------------------------
    # RUTA PARA: POST (crear), PUT / PATCH (modificar)
    # --------------------------------------------------------------------------
    @http.route('/gestion/apirest/<model>', auth="none", cors='*', csrf=False,
                methods=["POST", "PUT", "PATCH"], type='http')
    def apiPost(self, model, **args):
        model = (model or "").strip()  # <-- CLAVE (quita \n, espacios, etc.)

        # Validación de modelo para evitar 500
        try:
            Model = request.env[model].sudo()
        except KeyError:
            return http.Response(json.dumps({'estado': 'MODELNOTFOUND', 'model': model}),
                                 status=404, mimetype='application/json')

        if 'data' in args:
            dicDatos = json.loads(args['data'])
        else:
            raw_data = request.httprequest.data.decode('utf-8')
            dicDatos = json.loads(raw_data or '{}')

        if not dicDatos.get("num_socio"):
            return http.Response(json.dumps({'estado': 'SOCIONOINDICADO'}), status=400, mimetype='application/json')

        search = [('num_socio', '=', int(dicDatos["num_socio"]))]

        if request.httprequest.method == 'POST':
            record = Model.create(dicDatos)
            return http.Response(json.dumps(record.read(), default=str), status=200, mimetype='application/json')

        elif request.httprequest.method in ['PUT', 'PATCH']:
            record = Model.search(search)
            if record:
                record[0].write(dicDatos)
                return http.Response(json.dumps(record.read(), default=str), status=200, mimetype='application/json')
            else:
                return http.Response(json.dumps({'estado': 'NOTFOUND'}), status=404, mimetype='application/json')

        return request.env['ir.http'].session_info()
    # --------------------------------------------------------------------------
    # RUTA PARA: GET (consultar), DELETE (eliminar)
    # --------------------------------------------------------------------------
    @http.route('/gestion/apirest/<model>', auth="none", cors='*', csrf=False,
                methods=["GET", "DELETE"], type='http')
    def apiGet(self, model, **args):
        """
        Consultar o eliminar un socio vía API REST.
        """
        # Convertimos el contenido de 'data' a diccionario
        dicDatos = json.loads(args.get('data', '{}'))

        # Si no se indica num_socio, devolvemos error
        if not dicDatos.get("num_socio"):
            return http.Response(json.dumps({'estado': 'SOCIONOINDICADO'}), status=400, mimetype='application/json')

        search = [('num_socio', '=', int(dicDatos["num_socio"]))]

        # ----------------------------------------------------------------------
        # CASO GET → Consultar datos del socio
        # ----------------------------------------------------------------------
        if request.httprequest.method == 'GET':
            record = request.env[model].sudo().search(search)
            if record:
                return http.Response(
                    json.dumps(record[0].read(), default=str),
                    status=200,
                    mimetype='application/json'
                )
            return http.Response(json.dumps({'estado': 'NOTFOUND'}), status=404, mimetype='application/json')

        # ----------------------------------------------------------------------
        # CASO DELETE → Eliminar registro del socio
        # ----------------------------------------------------------------------
        elif request.httprequest.method == 'DELETE':
            record = request.env[model].sudo().search(search)
            if record:
                # Guardamos los datos antes de borrar
                data_deleted = record[0].read()
                record[0].unlink()
                return http.Response(
                    json.dumps(data_deleted, default=str),
                    status=200,
                    mimetype='application/json'
                )
            return http.Response(json.dumps({'estado': 'NOTFOUND'}), status=404, mimetype='application/json')

        return request.env['ir.http'].session_info()
