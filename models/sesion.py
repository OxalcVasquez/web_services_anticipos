from conexionBD import Conexion as bd
import json
from util import CustomJsonEncoder

class Sesion():
    def __init__(self,email=None,password=None):
      self.email = email
      self.password = password

    def iniciar_sesion(self):
      #Open database
      con = bd().open
      #Creation cursor
      cursor = con.cursor()
      #Query sql
      sql = 'SELECT u.*, r.nombre AS rol FROM usuario u  INNER JOIN rol r ON r.id = u.rol_id WHERE email = %s and password = %s'
      #Execute SQL query
      cursor.execute(sql,[self.email,self.password])
      #Get data from cursor
      datos = cursor.fetchone()
      #Close the cursor
      cursor.close()
      #Clse connection
      con.close()

      if datos:
        if datos['estado_usuario'] == '1':
          return json.dumps({'status': True,'data': datos,'message':'Credenciales correcta'})
        else :
          return json.dumps({'status':False,'data':'','message':'El usuario se encuentra inactivo'})
      else :
        return json.dumps({'status' : False, 'data':'','message':'Credenciales incorrectas o el usuario no existe'})

    def actualizar_token(self,token,user_id):
      #Open connection
      con = bd().open
      #Create cursor
      cursor = con.cursor()
      #Prepare query - Update data
      sql = "UPDATE usuario SET token = %s, estado_token = '1' WHERE id = %s"

      try:
        cursor.execute(sql,[token,user_id])
        con.commit() #Save
        return json.dumps({'status':True,'message':'Token actualizado'})
      except con.Error as error:
        print(error)
        con.rollback()
        return json.dumps({'status':False,'message':format(error)} , cls = CustomJsonEncoder)
      finally:
        cursor.close()
        con.close()

    def validar_estado_token(self,user_id):
      #Open connection
      con = bd().open
      #Create cursor
      cursor = con.cursor()
      #Prepare query - Update data
      sql = "SELECT estado_token FROM usuario WHERE id = %s"

      #Execute query
      cursor.execute(sql,[user_id])

      datos = cursor.fetchone()

      cursor.close()
      con.close()

      if datos:
        return json.dumps({'status':True,'data':datos,'message':'Estado del token'})
      else :
        return json.dumps({'status': True, 'data': '', 'message': 'Estado del token'})








