# Web services Tarifa
from flask import Blueprint,request,jsonify
from models.tarifa import Tarifa
import json
import validar_token as vt

ws_tarifa = Blueprint('ws_tarifa',__name__)

@ws_tarifa.route('/tarifa/viaticos', methods = ['POST'])
@vt.validar_token

def listar_tarifas_viaticos():
    if request.method == 'POST':
        if not 'sede_id' in request.form:
           return jsonify({'status': False, 'data': '', 'message': 'Falta sede'}), 403
        sede_id = request.form['sede_id']
        dias = int(request.form['dias'])
        obj = Tarifa()
        rpta_tarifa_viaticos = obj.mostrar_tarifa_viaticos(sede_id,dias)
        datos = json.loads(rpta_tarifa_viaticos)
        return jsonify(datos), 200
    else:
        return jsonify(datos), 401

