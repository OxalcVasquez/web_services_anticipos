from conexionBD import Conexion as bd
import json
from util import CustomJsonEncoder
from datetime import datetime


class Anticipo():
    def __init__(self, descripcion=None, fecha_inicio=None, fecha_fin=None, motivo_anticipo_id=None, sede_id=None, usuario_id=None):
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.motivo_anticipo_id = motivo_anticipo_id
        self.sede_id = sede_id
        self.usuario_id = usuario_id

    def registrar(self):
        # Open connection
        con = bd().open
        # Configure transaction
        con.autocommit = False
        # Create cursor
        cursor = con.cursor()

        try:

            # Difference days
            dias = datetime.strptime(
                self.fecha_fin, "%Y-%m-%d") - datetime.strptime(self.fecha_inicio, "%Y-%m-%d")

            # Generate total amount
            sql = "SELECT SUM(monto_maximo)* %s AS monto_rubros_por_dia FROM tarifa t INNER JOIN rubro r ON t.rubro_id = r.id WHERE sede_id = %s AND r.se_calcula_por_dia = %s"
            cursor.execute(sql, [dias, self.sede_id, '1'])
            datos = cursor.fetchone()
            monto_rubros_por_dia = datos['monto_rubros_por_dia']

            sql = "SELECT monto_maximo AS monto_rubro_fijo FROM tarifa t INNER JOIN rubro r ON t.rubro_id = r.id WHERE sede_id = %s AND r.se_calcula_por_dia = %s"
            cursor.execute(sql, [self.sede_id, '0'])
            datos = cursor.fetchone()
            monto_rubro_fijo = datos['monto_rubro_fijo']
            monto_total = float(monto_rubros_por_dia) + float(monto_rubro_fijo)

            # Prepare statement for register a new anticipo
            sql = "INSERT INTO anticipo(descripcion,fecha_inicio,fecha_fin,monto_total,estado_anticipo_id,motivo_anticipo_id,sede_id,usuario_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, [self.descripcion, self.fecha_inicio, self.fecha_fin,
                           monto_total, 1, self.motivo_anticipo_id, self.sede_id, self.usuario_id])

            # Get registered anticipo sale id
            anticipo_id = con.insert_id()

            sql = "INSERT INTO historial_anticipo(estado_id,tipo,anticipo_id) VALUES (%s,%s,%s)"
            cursor.execute(sql, [1, 'A', anticipo_id])

            # confirm the transaction
            con.commit()

            # Return response
            return json.dumps({'status': True, 'data': {'id': anticipo_id}, 'message': 'Anticipo registered'})

        except con.Error as error:
            # Revoque all operations
            con.rollback()
            return json.dumps({'status': False, 'data': '', 'message': format(error)}, cls=CustomJsonEncoder)
        finally:
            cursor.close()
            con.close()

    def listar_anticipos(self, usuario_id):
        # Abrir la conexion
        con = bd().open

        # Crear un cursor
        cursor = con.cursor()

        sql0 = "SELECT rol_id FROM usuario WHERE id = %s"
        cursor.execute(sql0, [usuario_id])
        datos0 = cursor.fetchone()
        tipoUsuario = datos0['rol_id']

        if(tipoUsuario == 1):
            sql = "SELECT an.id,an.descripcion, an.fecha_inicio, an.fecha_fin, an.monto_total,an.sede_id, CONCAT('/static/imgs-sede/', an.sede_id, '.jpg') AS img, es.descripcion AS estado FROM anticipo AS an INNER JOIN estado_anticipo AS es on (es.id = an.estado_anticipo_id) WHERE an.usuario_id=%s"

            # Ejecutar la consulta
            cursor.execute(sql, [usuario_id])

            # Almacenar los datos que devuelva de la conulsta
            datos = cursor.fetchall()

            # Cerrar el cursor y la conexion
            cursor.close()
            con.close()

             # Retornar datos
            if (datos):
                return json.dumps({'status': True, 'data': datos, 'message': 'Listado anticipos docente'}, cls=CustomJsonEncoder)

            else:
                return json.dumps({'status': False, 'data': '', 'message': 'No hay datos para mostrar'})

        else:
            if(tipoUsuario == 2):
                sql = "SELECT an.id,an.descripcion, an.fecha_inicio, an.fecha_fin, an.monto_total, CONCAT('/static/imgs-sede/', an.sede_id, '.jpg') AS img, es.descripcion AS estado FROM anticipo AS an INNER JOIN estado_anticipo AS es on (es.id = an.estado_anticipo_id) WHERE an.estado_anticipo_id=1"
                cursor.execute(sql)
                # Almacenar los datos que devuelva de la conulsta
                datos = cursor.fetchall()
                # Cerrar el cursor y la conexion
                cursor.close()
                con.close()
                # Retornar datos
                if (datos):
                    return json.dumps({'status': True, 'data': datos, 'message': 'Listado anticipos jefe'}, cls=CustomJsonEncoder)

                else:
                    return json.dumps({'status': False, 'data': '', 'message': 'No hay datos para mostrar'})
            else:

                sql = "SELECT an.id,an.descripcion, an.fecha_inicio, an.fecha_fin, an.monto_total, CONCAT('/static/imgs-sede/', an.sede_id, '.jpg') AS img, es.descripcion AS estado FROM anticipo AS an INNER JOIN estado_anticipo AS es on (es.id = an.estado_anticipo_id) WHERE an.estado_anticipo_id=3"
                cursor.execute(sql)
                # Almacenar los datos que devuelva de la conulsta
                datos = cursor.fetchall()
                # Cerrar el cursor y la conexion
                cursor.close()
                con.close()
                # Retornar datos
                if (datos):
                    return json.dumps({'status': True, 'data': datos, 'message': 'Listado anticipos administrativo'}, cls=CustomJsonEncoder)

                else:
                    return json.dumps({'status': False, 'data': '', 'message': 'No hay datos para mostrar'})



    def listar_anticipos_docente_estado(self, docente_id, estado):
        # Abrir la conexion
        con = bd().open

        # Crear un cursor
        cursor = con.cursor()

        # Preparar la consulta SQL
        sql = "SELECT an.id,an.descripcion, an.fecha_inicio, an.fecha_fin, an.monto_total, es.descripcion AS estado , an.sede_id FROM anticipo AS an INNER JOIN estado_anticipo AS es on (es.id = an.estado_anticipo_id) WHERE an.usuario_id=%s and an.estado_anticipo_id = %s"

        # Ejecutar la consulta
        cursor.execute(sql, [docente_id, estado])

        # Almacenar los datos que devuelva de la conulsta
        datos = cursor.fetchall()

        # Cerrar el cursor y la conexion
        cursor.close()
        con.close()

        # Retornar datos
        if (datos):
            return json.dumps({'status': True, 'data': datos, 'message': 'Listado anticipos docente'}, cls=CustomJsonEncoder)

        else:
            return json.dumps({'status': False, 'data': '', 'message': 'No hay datos para mostrar'})

    def listar_anticipos_jefe(self, estado_id=0):
        # Abrir la conexion
        con = bd().open

        # Crear un cursor
        cursor = con.cursor()
        if estado_id == 0:
            sql = "SELECT an.id,an.descripcion, an.fecha_inicio, an.fecha_fin, an.monto_total, es.descripcion AS estado, CONCAT (doc.nombres, ', ', doc.apellidos) AS docente FROM anticipo AS an INNER JOIN estado_anticipo AS es on (es.id = an.estado_anticipo_id) INNER JOIN usuario AS doc on (doc.id = an.usuario_id)"
            cursor.execute(sql)

        else:
            sql = "SELECT an.id,an.descripcion, an.fecha_inicio, an.fecha_fin, an.monto_total, es.descripcion AS estado, CONCAT (doc.nombres, ', ', doc.apellidos) AS docente FROM anticipo AS an INNER JOIN estado_anticipo AS es on (es.id = an.estado_anticipo_id) INNER JOIN usuario AS doc on (doc.id = an.usuario_id) WHERE an.estado_anticipo_id=%s"
            cursor.execute(sql, [estado_id])

        # Almacenar los datos que devuelva de la conulsta
        datos = cursor.fetchall()

        # Cerrar el cursor y la conexion
        cursor.close()
        con.close()

        # Retornar datos
        if (datos):
            return json.dumps({'status': True, 'data': datos, 'message': 'Listado anticipos admin'}, cls=CustomJsonEncoder)

        else:
            return json.dumps({'status': False, 'data': '', 'message': 'No hay datos para mostrar'})

    def listar_anticipos_admin(self):
        # Abrir la conexion
        con = bd().open

        # Crear un cursor
        cursor = con.cursor()
        sql = "SELECT an.id,an.descripcion, an.fecha_inicio, an.fecha_fin, an.monto_total, es.descripcion AS estado, CONCAT (doc.nombres, ', ', doc.apellidos) AS docente FROM anticipo AS an INNER JOIN estado_anticipo AS es on (es.id = an.estado_anticipo_id) INNER JOIN usuario AS doc on (doc.id = an.usuario_id) WHERE an.estado_anticipo_id = 3"
        cursor.execute(sql)
        # Almacenar los datos que devuelva de la conulsta
        datos = cursor.fetchall()

        # Cerrar el cursor y la conexion
        cursor.close()
        con.close()

        # Retornar datos
        if (datos):
            return json.dumps({'status': True, 'data': datos, 'message': 'Listado anticipos admin'}, cls=CustomJsonEncoder)

        else:
            return json.dumps({'status': False, 'data': '', 'message': 'No hay datos para mostrar'})

    def actualizarEstado(self, estado_anticipo_id, id, usuario_id):
            #Open connection
            con = bd().open
            #Configure transaction
            con.autocommit = False
            #Create cursor
            cursor = con.cursor()

            try:
                sql0 = "SELECT rol_id  FROM usuario WHERE id = %s"
                cursor.execute(sql0,[usuario_id])
                datos = cursor.fetchone()
                evaluador = datos['rol_id']

                sql="select estado_anticipo_id from anticipo where id= %s"
                cursor.execute(sql,[id])
                datos = cursor.fetchone()
                est=datos['estado_anticipo_id']


                if(est != 10 and est != 4):

                    if(evaluador==1):
                        return json.dumps({'status': False, 'data': datos, 'message': 'Este usuario no puede evaluar anticipos'}, cls=CustomJsonEncoder)
                    else:
                        if(evaluador==3 and estado_anticipo_id=='4'):
                            return json.dumps({'status': False, 'data': datos, 'message': 'Este usuario no puede rechazar el anticipo'}, cls=CustomJsonEncoder)
                        else:

                            #Generate total amount
                            sql = "UPDATE anticipo set estado_anticipo_id= %s  WHERE id = %s"
                            cursor.execute(sql, [estado_anticipo_id, id])



                            sql2 = "INSERT INTO historial_anticipo(estado_id, descripcion, tipo, usuario_evaluador_id,anticipo_id) VALUES (%s,%s,%s,%s,%s)"
                            cursor.execute(sql2, [estado_anticipo_id,self.descripcion,'A',usuario_id, id])

                            #confirm the transaction
                            con.commit()
                                    #Return response
                            return json.dumps({'status':True,'data':{'anticipo_id':id},'message':'Actualizacion correcta'})
                else:
                    return json.dumps({'status': False, 'data': datos, 'message': 'Este anticipo no puede ser modificado.'}, cls=CustomJsonEncoder)


            except con.Error as error:
                #Revoque all operations
                con.rollback()
                return json.dumps({'status':False,'data':'','message':format(error)},cls=CustomJsonEncoder)
            finally:
                cursor.close()
                con.close()

    def validar_anticipos_pendientes(self,usuario_id):
        # Open connection
        con = bd().open
        # Create cursor
        # Crear un cursor
        cursor = con.cursor()
        sql = "SELECT COUNT(*)>=3 validacion FROM anticipo WHERE estado_anticipo_id = 7 AND usuario_id = %s"
        cursor.execute(sql,[usuario_id])
        # Almacenar los datos que devuelva de la conulsta
        datos = cursor.fetchone()
        # Cerrar el cursor y la conexion
        cursor.close()
        con.close()

        # Retornar datos
        if (datos):
            return json.dumps({'status': True, 'data': datos, 'message': 'Validacion estado'}, cls=CustomJsonEncoder)

        else:
            return json.dumps({'status': False, 'data': '', 'message': 'No hay datos para mostrar'})