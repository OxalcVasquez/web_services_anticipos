# Web services Tarifa
from flask import Blueprint, request, jsonify
from models.informe_gasto import Informe_gasto
import json
import validar_token as vt
import FCMManager as fcm

ws_informe_gasto = Blueprint('ws_informe_gasto', __name__)


@ws_informe_gasto.route('/informe_gasto/registrar', methods=['POST'])
@vt.validar_token
def registrar():
    if request.method == 'POST':
        anticipo_id = request.form['anticipo_id']
        detalle_comprobantes = request.form['detalle_comprobantes']
        #instantiate informe class
        obj_informe = Informe_gasto(anticipo_id,detalle_comprobantes)
        rpta_JSON = obj_informe.registrar()
        datos_informe_gasto = json.loads(rpta_JSON)

        if datos_informe_gasto['status']:
            fcm.sendPush("Registro infrome gasto", "Se registró un nuevo informe", "admin")
            return jsonify(datos_informe_gasto), 201  # CREATED
        else:
            return jsonify(datos_informe_gasto), 500  # INTERNAL SERVER ERROR



@ws_informe_gasto.route('/informe_gasto/docente/listar', methods=['POST'])
@vt.validar_token
def listar_informe_gasto_docente():
    if request.method == 'POST':
        if not 'docente_id' in request.form:
          return jsonify({'status': False, 'data': '', 'message': 'Falta docente'}), 403
        else:
            docente_id = request.form['docente_id']
            obj = Informe_gasto()
            rpta_informe_gasto_docente = obj.listar_informes_gasto_docente(docente_id)
            datos = json.loads(rpta_informe_gasto_docente)
            return jsonify(datos), 200
    else:
        return jsonify(datos), 401


@ws_informe_gasto.route('/informe_gasto/administracion/listar', methods=['POST'])
@vt.validar_token
def listar_informe_gasto_jefe_admin():
    if request.method == 'POST':
        obj = Informe_gasto()
        rpta_informe_gasto_admin = obj.listar_informes_gasto_jefe_admin()
        datos = json.loads(rpta_informe_gasto_admin)
        return jsonify(datos), 200
    else:
        return jsonify(datos), 401

@ws_informe_gasto.route('/informe/evaluar', methods=['POST'])
@vt.validar_token #f
def actualizar_informe():
    if request.method == 'POST':
        estado_id = request.form['estado_id']
        id = request.form['id']
        usuario_evaluador_id= request.form['usuario_evaluador_id']

        obj_informe = Informe_gasto()
        
        rpta_JSON = obj_informe.aceptarRechazarRendicion(int(estado_id), int(usuario_evaluador_id), id)
        datos_informe_gasto = json.loads(rpta_JSON)

        if datos_informe_gasto['status']:
            return jsonify(datos_informe_gasto), 200  # CREATED
        else:
            return jsonify(datos_informe_gasto), 500  # INTERNAL SERVER ERROR