# Web services Comprobante
from flask import Blueprint, request, jsonify
from models.comprobante import Comprobante
import json
import validar_token as vt
from werkzeug.utils import secure_filename
from os.path import join, dirname, realpath

ws_comprobante = Blueprint('ws_comprobante', __name__)

UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static\\imgs-comprobante')

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

@ws_comprobante.route('/comprobante/foto', methods=['POST'])
def guardarFoto():
    if request.method == 'POST':
        file = request.files['image']
        filename = secure_filename(file.filename)
        file.save(filename)
        return jsonify({'status': True, 'data': 'Subido', 'message': 'Si se subió'}), 200
    else:
        return jsonify({'status': False, 'data': 'No subido', 'message': 'No se subió'}), 401    