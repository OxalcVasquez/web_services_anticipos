# Web services Historial_anticipo
from flask import Blueprint, request, jsonify
from models.historial_anticipo import Historial_anticipo
import json
import validar_token as vt

ws_historial_anticipo = Blueprint('ws_historial_anticipo', __name__)


@ws_historial_anticipo.route('/historial/anticipo', methods=['POST'])
@vt.validar_token
def mostrar_historial_anticipo():
    if request.method == 'POST':
        if not 'anticipo_id' or not 'tipo' or not 'ultima_instancia' in request.form:
           return jsonify({'status': False, 'data': '', 'message': 'Faltan parametros '}), 403
        anticipo_id = request.form['anticipo_id']
        tipo = request.form['tipo']
        ultima_instancia = request.form['ultima_instancia']

        obj = Historial_anticipo()
        rpta_historial_anticipo = obj.mostrar_historial_anticipo(
                anticipo_id, tipo,ultima_instancia=ultima_instancia)

        datos = json.loads(rpta_historial_anticipo)
        return jsonify(datos), 200
    else:
        return jsonify(datos), 401
