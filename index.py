from flask import Flask
from services.sesion import ws_sesion
from services.rol import ws_rol
from services.sede import ws_sede
from services.tipo_comprobante import ws_tipo_comprobante
from services.rubro import ws_rubro
from services.motivo_anticipo import ws_motivo_anticipo
from services.tarifa import ws_tarifa
from services.estado_anticipo import ws_estado_anticipo
from services.anticipo import ws_anticipo
from services.historial_anticipo import ws_historial_anticipo
from services.informe_gasto import ws_informe_gasto
from services.comprobante import ws_comprobante

#Create app variable with Flask
app = Flask(__name__)

#Register modules contains web services
app.register_blueprint(ws_sesion)
app.register_blueprint(ws_rol)
app.register_blueprint(ws_sede)
app.register_blueprint(ws_tipo_comprobante)
app.register_blueprint(ws_rubro)
app.register_blueprint(ws_motivo_anticipo)
app.register_blueprint(ws_tarifa)
app.register_blueprint(ws_estado_anticipo)
app.register_blueprint(ws_anticipo)
app.register_blueprint(ws_historial_anticipo)
app.register_blueprint(ws_informe_gasto)
app.register_blueprint(ws_comprobante)


@app.route('/')
def home():
    return 'Web Services Running'


#Start web services
if __name__ == '__main__':
    app.run(port=3001, debug=True, host='0.0.0.0')
