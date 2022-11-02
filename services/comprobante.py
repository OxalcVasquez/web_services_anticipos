# Web services Comprobante
from flask import Blueprint, request, jsonify
from models.comprobante import Comprobante
import json
import validar_token as vt

ws_comprobante = Blueprint('ws_comprobante', __name__)


@ws_comprobante.route('/comprobante/listado', methods=['POST'])
@vt.validar_token
def listar_comprobante_informe():
    if request.method == 'POST':
        if not 'informe_id' in request.form:
           return jsonify({'status': False, 'data': '', 'message': 'Falta informe id'}), 403
        informe_id = request.form['informe_id']
        obj = Comprobante()
        rpta_comprobante_informe = obj.listar_comprobante_informe(informe_id)
        datos = json.loads(rpta_comprobante_informe)
        return jsonify(datos), 200
    else:
        return jsonify(datos), 401
