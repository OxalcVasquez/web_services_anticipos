from conexionBD import Conexion as bd
import json
from util import CustomJsonEncoder

class Tarifa():
    def __init__(self, id=None,monto_maximo=None,rubro_id = None,sede_id=None):
        self.id = id
        self.monto_maximo = monto_maximo
        self.rubro_id = rubro_id
        self.sede_id = sede_id

    def mostrar_tarifa_viaticos(self,sede_id):
        #Abrir la conexion
        con = bd().open

        #Crear un cursor
        cursor = con.cursor()

        #Preparar la consulta SQL
        sql = "SELECT  ta.id, monto_maximo, rubro_id, ru.nombre AS rubro,ru.se_calcula_por_dia, sede_id, se.nombre AS sede FROM  tarifa ta INNER	JOIN  rubro ru ON  ta.rubro_id = ru.id INNER JOIN  sede se ON  ta.sede_id = se.id WHERE se.id = %s"

        #Ejecutar la consulta
        cursor.execute(sql,[sede_id])

        #Almacenar los datos que devuelva de la conulsta
        datos = cursor.fetchall()

        #Cerrar el cursor y la conexion
        cursor.close()
        con.close()

        #Retornar datos
        if (datos):
            return json.dumps({'status': True, 'data' : datos , 'message' : 'Tabla de tarifa de viaticos'} , cls= CustomJsonEncoder)

        else :
            return json.dumps({'status': False,'data':'', 'message' : 'No hay datos para mostrar'})






