from conexionBD import Conexion as bd
import json
from util import CustomJsonEncoder


class Historial_anticipo():
    def __init__(self, id=None, estado_id=None, descripcion=None, tipo=None,usuario_evaluador_id=None,anticipo_id=None):
        self.id = id
        self.estado_id = estado_id
        self.descripcion = descripcion
        self.tipo = tipo
        self.usuario_evaluador_id = usuario_evaluador_id
        self.anticipo_id = anticipo_id


    def mostrar_historial_anticipo(self, anticipo_id,tipo,ultima_instancia=0):
        #Abrir la conexion
        con = bd().open

        #Crear un cursor
        cursor = con.cursor()

        #Preparar la consulta SQL
        if (ultima_instancia==0) :
            sql = "SELECT e.descripcion AS estado, ha.descripcion, fecha_hora, tipo, CONCAT(u.nombres, ', ', u.apellidos) AS evaluador, r.nombre AS instancia FROM  historial_anticipo ha INNER JOIN estado_anticipo e ON(ha.estado_id=e.id) INNER JOIN anticipo a ON(ha.anticipo_id=a.id) LEFT JOIN usuario u ON(ha.usuario_evaluador_id=u.id) LEFT JOIN rol r ON(r.id=u.id)  WHERE a.id = %s AND tipo = %s"
        else :
            sql = "SELECT e.descripcion AS estado, ha.descripcion, fecha_hora, tipo, CONCAT(u.nombres, ', ', u.apellidos) AS evaluador, r.nombre AS instancia FROM  historial_anticipo ha INNER JOIN estado_anticipo e ON(ha.estado_id=e.id) INNER JOIN anticipo a ON(ha.anticipo_id=a.id) LEFT JOIN usuario u ON(ha.usuario_evaluador_id=u.id) LEFT JOIN rol r ON(r.id=u.id)  WHERE a.id = %s AND tipo = %s ORDER BY fecha_hora DESC LIMIT 1"


        cursor.execute(sql, [anticipo_id, tipo])
        datos = cursor.fetchone()
        #Cerrar el cursor y la conexion
        cursor.close()
        con.close()

        #Retornar datos
        if (datos):
            return json.dumps({'status': True, 'data': datos, 'message': 'Historial Anticipo'}, cls=CustomJsonEncoder)

        else:
            return json.dumps({'status': False, 'data': '', 'message': 'No hay datos para mostrar'})
