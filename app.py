from flask import Flask

from src.view.web.vista_nomina import vista


def crear_aplicacion():
    aplicacion = Flask(__name__)
    aplicacion.register_blueprint(vista)
    return aplicacion


app = crear_aplicacion()


if __name__ == "__main__":
    app.run()