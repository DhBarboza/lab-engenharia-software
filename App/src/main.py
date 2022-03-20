import os
from flask import Flask, render_template
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv, find_dotenv
from werkzeug.middleware.proxy_fix import ProxyFix

from src.model.models import db as models

from src.controller.assuntoController import assunto_controller, get_assuntos
from src.controller.noticiaController import noticia_controller, get_noticias

load_dotenv(find_dotenv())

try:
    template_dir = os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
    template_dir = os.path.join(template_dir, 'src')
    template_dir = os.path.join(template_dir, 'view')

    app = Flask(__name__, template_folder=template_dir, static_folder=template_dir)
    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'

    _USERNAME = os.getenv('MYSQL_USERNAME')
    _PASS = os.getenv('MYSQL_PASSWORD')
    _DB = os.getenv('MYSQL_DATABASE')
    _HOST = os.getenv('MYSQL_HOST')
    _PORT = os.getenv('MYSQL_PORT')

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{_USERNAME}:{_PASS}@{_HOST}:{_PORT}/{_DB}'

    models.init_app(app)

    app.wsgi_app = ProxyFix(app.wsgi_app)

    app.register_blueprint(assunto_controller)
    app.register_blueprint(noticia_controller)


except Exception as err:
    print(f'Error: {err}')


def initialize_db():
    db = SQLAlchemy(app)
    engine = db.create_engine(f'mysql+pymysql://{_USERNAME}:{_PASS}@{_HOST}:{_PORT}', {})
    try:
        engine.execute(f'CREATE DATABASE {_DB}')
    except Exception as error:
        print(f'database error: {error}')
    with app.app_context():
        models.create_all()


@app.route('/')
@cross_origin()
def index():
    try:
        assuntos = get_assuntos().json['assuntos']
        noticias = get_noticias().json['noticias']
    except Exception as error:
        print('error', error)
        assuntos = []
        noticias = []
    data = {'assuntos': assuntos, 'noticias': noticias}
    return render_template('dashboard/dashboard.html', title='Dashboard', data=data)
