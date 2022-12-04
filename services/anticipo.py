# Web services Tarifa
from flask import Blueprint, request, jsonify
from models.anticipo import Anticipo
import json
import validar_token as vt

ws_anticipo = Blueprint('ws_anticipo', __name__)

@ws_anticipo.route('/anticipo/registrar', methods=['POST'])
@vt.validar_token #f
def registrar_anticipo():
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        fecha_inicio = request.form['fecha_inicio']
        fecha_fin = request.form['fecha_fin']
        motivo_anticipo_id = request.form['motivo_anticipo_id']
        sede_id = request.form['sede_id']
        usuario_id = request.form['docente_id']

        obj_anticipo = Anticipo(descripcion,fecha_inicio,fecha_fin,motivo_anticipo_id,sede_id,usuario_id)
        rpta_JSON = obj_anticipo.registrar()
        datos_anticipo = json.loads(rpta_JSON)

        if datos_anticipo['status']:
            return jsonify(datos_anticipo), 201 #CREATED
        else:
            return jsonify(datos_anticipo), 500 #INTERNAL SERVER ERROR


@ws_anticipo.route('/anticipos/listar', methods=['POST'])
@vt.validar_token
def listar_anticipos():
    if request.method == 'POST':
        if not 'usuario_id' in request.form:
          return jsonify({'status': False, 'data': '', 'message': 'Falta docente'}), 403
        else :
            usuario_id = request.form['usuario_id']
            obj = Anticipo()
            rpta_anticipos_docente = obj.listar_anticipos(usuario_id)
            datos = json.loads(rpta_anticipos_docente)
            return jsonify(datos), 200
    else:
        return jsonify(datos), 401


@ws_anticipo.route('/anticipos/docente/listar/estado', methods=['POST'])
@vt.validar_token
def listar_anticipos_docente_estado():
    if request.method == 'POST':
        if not 'docente_id' in request.form:
          return jsonify({'status': False, 'data': '', 'message': 'Falta docente'}), 403
        else:
            docente_id = request.form['docente_id']
            estado = request.form['estado']
            obj = Anticipo()
            rpta_anticipos_docente = obj.listar_anticipos_docente_estado(docente_id,estado)
            datos = json.loads(rpta_anticipos_docente)
            return jsonify(datos), 200
    else:
        return jsonify(datos), 401


@ws_anticipo.route('/anticipos/jefe/listar', methods=['POST'])
@vt.validar_token
def listar_anticipos_jefe():
    if request.method == 'POST':
          if not 'estado_anticipo_id' in request.form:
              obj = Anticipo()
              rpta_anticipos_jefe = obj.listar_anticipos_jefe()
              datos = json.loads(rpta_anticipos_jefe)
              return jsonify(datos), 200
          else :
            estado_anticipo_id = request.form['estado_anticipo_id']
            obj = Anticipo()
            rpta_anticipos_jefe = obj.listar_anticipos_jefe(estado_anticipo_id)
            datos = json.loads(rpta_anticipos_jefe)
            return jsonify(datos), 200
    else:
        return jsonify(datos), 401


@ws_anticipo.route('/anticipos/admin/listar', methods=['POST'])
@vt.validar_token
def listar_anticipos_admin():
    if request.method == 'POST':
        obj = Anticipo()
        rpta_anticipos_admin = obj.listar_anticipos_admin()
        datos = json.loads(rpta_anticipos_admin)
        return jsonify(datos), 200
    else:
        return jsonify(datos), 401

@ws_anticipo.route('/anticipo/evaluar', methods=['POST'])
@vt.validar_token #f
def actualizar_anticipo():
    if request.method == 'POST':
        estado_anticipo_id = request.form['estado_anticipo_id']
        id = request.form['id']
        usuario_id = request.form['usuario_evaluador_id']

        obj_anticipo = Anticipo()
        rpta_JSON = obj_anticipo.actualizarEstado(estado_anticipo_id, id, usuario_id)
        datos_anticipo = json.loads(rpta_JSON)

        if datos_anticipo['status']:
            return jsonify(datos_anticipo), 201 #CREATED
        else:
            return jsonify(datos_anticipo), 500 #INTERNAL SERVER ERROR

@ws_anticipo.route('/anticipo/validar/pendientes', methods=['POST'])
@vt.validar_token
def validar_pendientes():
    if request.method == 'POST':
        usuario_id = request.form['usuario_id']
        obj_anticipo = Anticipo()
        rpta_JSON = obj_anticipo.validar_anticipos_pendientes(usuario_id)
        datos_anticipo = json.loads(rpta_JSON)

        if datos_anticipo['status']:
            return jsonify(datos_anticipo), 200  # OK
        else:
            return jsonify(datos_anticipo), 500  # INTERNAL SERVER ERROR


@ws_anticipo.route('/anticipo/subsanar', methods=['POST'])
@vt.validar_token  # f
def subsanar_anticipo():
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        fecha_inicio = request.form['fecha_inicio']
        fecha_fin = request.form['fecha_fin']
        motivo_anticipo_id = request.form['motivo_anticipo_id']
        sede_id = request.form['sede_id']

        id = request.form['id']

        obj_anticipo = Anticipo(descripcion, fecha_inicio,
                                fecha_fin, motivo_anticipo_id,sede_id)
        rpta_JSON = obj_anticipo.subsanarAnticipo(id)
        datos_anticipo = json.loads(rpta_JSON)

        if datos_anticipo['status']:
            return jsonify(datos_anticipo), 200  # OK
        else:
            return jsonify(datos_anticipo), 500  # INTERNAL SERVER ERROR
