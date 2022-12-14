from conexionBD import Conexion as bd
import json
from util import CustomJsonEncoder
from datetime import date


class Informe_gasto():
    def __init__(self,anticipo_id=None,detalle_comprobantes=None):
        self.anticipo_id = anticipo_id
        self.detalle_comprobantes = detalle_comprobantes

    def registrar(self):
        #Open connection
        con = bd().open
        #Configure transaction
        con.autocommit = False
        #Create cursor
        cursor = con.cursor()

        try:

            #Generate informe
            anio = date.today().year
            sql = "SELECT usuario_id, monto_total FROM anticipo WHERE id = %s"
            cursor.execute(sql,[self.anticipo_id])
            datos = cursor.fetchone()
            docente_id = datos['usuario_id']
            monto_rendir = datos['monto_total']
            monto_rendido = 0
            num_informe = str(anio)+"-"+str(docente_id)+"-"+str(self.anticipo_id)

            sql = "INSERT INTO informe_gasto(num_informe,estado_id,total_rendir,total_rendido,anticipo_id) VALUES(%s,%s,%s,%s,%s)"
            cursor.execute(sql,[num_informe,1,monto_rendir,monto_rendido,self.anticipo_id])

            #Get registered informe gasto id
            informe_gasto_id = con.insert_id()

            sql = "INSERT INTO historial_anticipo(estado_id,tipo,anticipo_id) VALUES (%s,%s,%s)"
            cursor.execute(sql, [1, 'I', self.anticipo_id])

            sql = "INSERT INTO historial_anticipo(estado_id,tipo,anticipo_id) VALUES (%s,%s,%s)"
            cursor.execute(sql, [5, 'A', self.anticipo_id])

            sql = "UPDATE anticipo set estado_anticipo_id = %s WHERE id = %s"
            cursor.execute(sql, [5, self.anticipo_id])

            #Comprobantes
            json_detalle_comprobantes_array = json.loads(self.detalle_comprobantes)

            sql = "INSERT INTO comprobante(serie,correlativo,fecha_emision,monto_total,ruc,descripcion,tipo_comprobante_id,rubro_id,foto,num_operacion,informe_gasto_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

            monto_rendido = 0

            for comprobante in json_detalle_comprobantes_array:
                serie = comprobante['serie']
                correlativo = comprobante['correlativo']
                fecha_emision = comprobante['fecha_emision']
                monto_total = comprobante['monto_total']
                ruc = comprobante['ruc']
                descripcion = comprobante['descripcion']
                tipo_comprobante_id = comprobante['tipo_comprobante_id']
                rubro_id = comprobante['rubro_id']
                foto = comprobante['foto']
                num_operacion = comprobante['num_operacion']
                monto_rendido += float(monto_total)
                cursor.execute(
                    sql, [serie, correlativo, fecha_emision, monto_total, ruc, descripcion, tipo_comprobante_id, rubro_id, foto, num_operacion,informe_gasto_id])


            sql = "UPDATE informe_gasto SET total_rendido = %s WHERE id = %s"
            cursor.execute(sql, [monto_rendido, informe_gasto_id])

            sql = f"SELECT CONCAT(u.nombres, ' ', u.apellidos) AS docente, DATE_FORMAT(ha.fecha_hora,'%d/%m/%Y') AS fecha FROM historial_anticipo AS ha INNER JOIN anticipo AS a ON (ha.anticipo_id = a.id) INNER JOIN usuario AS u ON (a.usuario_id = u.id) WHERE ha.anticipo_id = {self.anticipo_id} AND ha.estado_id = 1 AND ha.tipo = 'A'"
            cursor.execute(sql)
            datos = cursor.fetchone()
            #confirm the transaction
            con.commit()
            #Return response
            return json.dumps({'status': True, 'data': {'num_informe':num_informe, 'docente': datos["docente"], "anticipo_id": self.anticipo_id, 'fecha': datos["fecha"]}, 'message': 'Informe gasto created'})

        except con.Error as error:
            #Revoque all operations
            con.rollback()
            return json.dumps({'status': False, 'data': '', 'message': format(error)}, cls=CustomJsonEncoder)
        finally:
            cursor.close()
            con.close()



    def listar_informes_gasto_docente(self, docente_id):
        # Abrir la conexion
        con = bd().open

        # Crear un cursor
        cursor = con.cursor()

        # Preparar la consulta SQL
        sql = "SELECT a.id as anticipo_id,num_informe, fecha_hora, e.id AS estado_id, e.descripcion AS estado, total_rendido, a.descripcion AS anticipo, a.fecha_inicio, a.fecha_fin FROM informe_gasto inf INNER JOIN estado_anticipo e ON inf.estado_id = e.id INNER JOIN anticipo a ON inf.anticipo_id = a.id INNER JOIN usuario doc ON a.usuario_id = doc.id WHERE doc.id = %s; "

        # Ejecutar la consulta
        cursor.execute(sql, [docente_id])

        # Almacenar los datos que devuelva de la conulsta
        datos = cursor.fetchall()

        # Cerrar el cursor y la conexion
        cursor.close()
        con.close()

        # Retornar datos
        if (datos):
            return json.dumps({'status': True, 'data': datos, 'message': 'Listado informe gastos docente'}, cls=CustomJsonEncoder)

        else:
            return json.dumps({'status': False, 'data': '', 'message': 'No hay datos para mostrar'})

    def listar_informes_gasto_jefe_admin(self):
        # Abrir la conexion
        con = bd().open

        # Crear un cursor
        cursor = con.cursor()
        sql = "SELECT inf.id AS id_informe, num_informe, fecha_hora, e.id AS estado_id, e.descripcion AS estado, total_rendido, a.descripcion AS anticipo, a.fecha_inicio, a.fecha_fin, CONCAT(doc.nombres, ', ', doc.apellidos) AS docente FROM informe_gasto inf INNER JOIN estado_anticipo e ON inf.estado_id = e.id INNER JOIN anticipo a ON inf.anticipo_id = a.id INNER JOIN usuario doc ON a.usuario_id = doc.id"
        cursor.execute(sql)
        # Almacenar los datos que devuelva de la conulsta
        datos = cursor.fetchall()

        # Cerrar el cursor y la conexion
        cursor.close()
        con.close()

        # Retornar datos
        if (datos):
            return json.dumps({'status': True, 'data': datos, 'message': 'Listado informes gasto'}, cls=CustomJsonEncoder)

        else:
            return json.dumps({'status': False, 'data': '', 'message': 'No hay datos para mostrar'})


    def aceptarRechazarRendicion(self, estado_id,usuario_evaluador_id, id):
            #Open connection
            con = bd().open
            #Configure transaction
            con.autocommit = False
            #Create cursor
            cursor = con.cursor()

            try:
                sql = "SELECT rol_id  FROM usuario WHERE id = %s"
                cursor.execute(sql,[usuario_evaluador_id])
                datos = cursor.fetchone()
                evaluador = datos['rol_id']

                print(evaluador)
                #
                sql2="select estado_id from informe_gasto where id= %s"
                cursor.execute(sql2,[id])
                datos = cursor.fetchone()
                est=datos['estado_id']
                print(est)
                #
                sql="select anticipo_id from informe_gasto where id= %s"
                cursor.execute(sql,[id])
                datos = cursor.fetchone()
                anticipo_id=datos['anticipo_id']
                print(anticipo_id)

                #Generate total amount


                if(est != 10 and est != 4 and est != 8 and est != 6 and est != 9):

                    print(estado_id)
                    if(evaluador==1):
                        return json.dumps({'status': False, 'data': datos, 'message': 'Este usuario no puede evaluar informes de rendici??n'}, cls=CustomJsonEncoder)
                    else:
                        if(estado_id==2): #rendicion a
                            print('hola')
                            sql = "UPDATE informe_gasto set estado_id= 7  WHERE id = %s"
                            cursor.execute(sql, [id])
                                                         
                            sql = "INSERT INTO historial_anticipo(estado_id, tipo, usuario_evaluador_id,anticipo_id) VALUES (%s,%s,%s,%s)"
                            cursor.execute(sql, [2,'I',usuario_evaluador_id, anticipo_id])


                        
                        if(estado_id==4): #rendicion r
                            sql = "UPDATE anticipo set estado_anticipo_id= 8  WHERE id = %s"
                            cursor.execute(sql, [anticipo_id])
                                
                            sql = "INSERT INTO historial_anticipo(estado_id, descripcion, tipo,anticipo_id) VALUES (%s,%s,%s,%s)"
                            cursor.execute(sql, [8,'Rechazado','A', anticipo_id])

                            sql = "INSERT INTO historial_anticipo(estado_id, descripcion, tipo,anticipo_id) VALUES (%s,%s,%s,%s)"
                            cursor.execute(sql, [4,'Rechazado','I', anticipo_id])

                            sql = "UPDATE informe_gasto set estado_id= 4  WHERE id = %s"
                            cursor.execute(sql, [id])

                        if (evaluador==2):
                            sql = "SELECT COUNT(*) AS aprobado from historial_anticipo ha INNER JOIN usuario u ON u.id = ha.usuario_evaluador_id WHERE estado_id = 2 AND anticipo_id = %s AND tipo = 'I' AND u.rol_id=3"
                        else: 
                            sql = "SELECT COUNT(*) AS aprobado from historial_anticipo ha INNER JOIN usuario u ON u.id = ha.usuario_evaluador_id WHERE estado_id = 2 AND anticipo_id = %s AND tipo = 'I' AND u.rol_id=2"    
                            
                        cursor.execute(sql,[anticipo_id])
                        datos = cursor.fetchone()
                        ap1=datos['aprobado']
                        print(ap1)
                        
                        
                                    

                        if(ap1>=1):
                            sql = "UPDATE anticipo set estado_anticipo_id= 10  WHERE id = %s"
                            cursor.execute(sql, [anticipo_id])

                            sql = "UPDATE informe_gasto set estado_id= 2  WHERE id = %s"
                            cursor.execute(sql, [id])

                            sql = "INSERT INTO historial_anticipo(estado_id, descripcion, tipo,anticipo_id) VALUES (%s,%s,%s,%s)"
                            cursor.execute(sql, [10,'Finalizado','A', anticipo_id])
 
                #confirm the transaction
                        con.commit()

                 #Return response
                        return json.dumps({'status':True,'data':{'informe_id':id},'message':'Actualizacion correcta'})
                else:
                    return json.dumps({'status': False, 'data': datos, 'message': 'Este informe no puede ser modificado.'}, cls=CustomJsonEncoder)

            except con.Error as error:
                #Revoque all operations
                con.rollback()
                return json.dumps({'status':False,'data':'','message':format(error)},cls=CustomJsonEncoder)
            finally:
                cursor.close()
                con.close()