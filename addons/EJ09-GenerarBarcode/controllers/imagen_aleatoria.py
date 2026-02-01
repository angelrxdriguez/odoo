from odoo import http
from odoo.http import request

import base64
from io import BytesIO
import os

from PIL import Image  # Pillow
# /imagenaleatoria?ancho=200&alto=100
# /imagenaleatoria?ancho=200&alto=100&modo=base64

class ImagenAleatoria(http.Controller):

    @http.route('/imagenaleatoria', auth='public', cors='*', type='http')
    def imagen_aleatoria(self, **kw):

        try:
            ancho = int(kw.get("ancho", 200))
            alto = int(kw.get("alto", 200))
        except ValueError:
            return http.Response("Parámetros ancho/alto inválidos", status=400)

        if ancho < 1 or alto < 1 or ancho > 2000 or alto > 2000:
            return http.Response("tamaño hasta 200", status=400)

        data = os.urandom(ancho * alto * 3)
        img = Image.frombytes("RGB", (ancho, alto), data)

        fp = BytesIO()
        img.save(fp, format="PNG")
        png_bytes = fp.getvalue()

        modo = (kw.get("modo", "png") or "").lower()

        if modo == "base64":
            img_str = base64.b64encode(png_bytes).decode("utf-8")
            html = f'<div><img src="data:image/png;base64,{img_str}"/></div>'
            return html

        return request.make_response(
            png_bytes,
            headers=[("Content-Type", "image/png")]
        )
