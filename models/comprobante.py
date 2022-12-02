from conexionBD import Conexion as bd
import json
from util import CustomJsonEncoder


class Comprobante():
    def __init__(self, id=None, serie=None, correlativo=None, fecha_emision=None,monto_total=None,ruc=None,descripcion=None,tipo_comprobante_id=None,rubro_id=None,foto=None,num_operacion=None,informe_gasto_id=None):
        self.id = id
        self.serie = serie
        self.correlativo = correlativo
        self.fecha_emision = fecha_emision
        self.monto_total = monto_total
        self.ruc = ruc
        self.descripcion = descripcion
        self.tipo_comprobante_id = tipo_comprobante_id
        self.rubro_id = rubro_id
        self.num_operacion = num_operacion
        self.informe_gasto_id = informe_gasto_id

    def listar_comprobante_informe(self, informe_id):
        #Abrir la conexion
        con = bd().open

        #Crear un cursor
        cursor = con.cursor()

        #Preparar la consulta SQL
        sql = "SELECT CONCAT(serie, '-', correlativo) AS comprobante, fecha_emision, monto_total, ruc, descripcion, r.nombre AS rubro, tc.nombre AS tipo, informe_gasto_id, foto, num_operacion FROM comprobante c INNER JOIN rubro r  ON c.rubro_id = r.id INNER JOIN tipo_comprobante tc ON  c.tipo_comprobante_id = tc.id WHERE c.informe_gasto_id = %s"

        #Ejecutar la consulta
        cursor.execute(sql, [informe_id])

        #Almacenar los datos que devuelva de la conulsta
        datos = cursor.fetchall()

        #Cerrar el cursor y la conexion
        cursor.close()
        con.close()

        #Retornar datos
        if (datos):
            return json.dumps({'status': True, 'data': datos, 'message': 'Listado comprobantes por informe'}, cls=CustomJsonEncoder)

        else:
            return json.dumps({'status': False, 'data': '', 'message': 'No hay datos para mostrar'})