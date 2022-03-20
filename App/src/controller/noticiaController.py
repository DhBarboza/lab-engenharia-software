import json

from flask import Blueprint, render_template, request, current_app, Response
from flask_sqlalchemy import SQLAlchemy

from src.model.models import Noticia as NoticiaModel
from src.model.models import Assunto as AssuntoModel

from src.controller.assuntoController import get_assuntos

noticia_controller = Blueprint('noticia', __name__, url_prefix='/noticias')


@noticia_controller.route('/', methods=['GET'])
def index():
    try:
        noticias = get_noticias().json['noticias']

    except Exception as error:
        print(error)
        noticias = []

    return render_template('noticia/noticia.html', title='Noticias', noticias=noticias)


def get_noticias():
    try:
        noticias = NoticiaModel.query.all()
        if not noticias:
            raise Exception('Nenhuma noticia')

        noticias = list(map(lambda x: {'id': x.id, 'name': x.name, 'assuntos': list(
            map(lambda ing: {'id': ing.id, 'name': ing.name}, x.assuntos)), 'steps': x.steps,
                                      'created_at': str(x.created_at)},
                           noticias))

        res = json.dumps({'noticias': noticias})
        return Response(res, mimetype='application/json', status=200)

    except Exception as error:
        res = json.dumps([])
        print(error)
        return Response(res, mimetype='application/json', status=500)


@noticia_controller.route('/create', methods=['GET', 'POST'])
def create_noticia():
    if request.json:
        try:
            db = SQLAlchemy(current_app)
            obj = request.json

            name = obj['name']
            steps = obj['steps']
            assunto_ids = obj['assuntos']

            assuntos = list(map(lambda x: AssuntoModel.query.filter_by(id=x).first(), assunto_ids))

            noticia = NoticiaModel(
                name=name,
                steps=steps,
                assuntos=assuntos
            )

            with current_app.app_context():
                db.session.merge(noticia)
                db.session.commit()

            res = json.dumps({'message': 'Notícia cadastrada!', 'error': False})
            return Response(res, mimetype='application/json', status=200)

        except Exception as error:
            res = json.dumps({'message': str(error), 'error': True})
            return Response(res, mimetype='application/json', status=200)
    else:
        try:
            stored_assuntos = get_assuntos().json['assuntos']
        except Exception as error:
            print(error)
            stored_assuntos = []
        return render_template('noticia/create-noticia/create-noticia.html',
                               data={'stored_assuntos': stored_assuntos})


@noticia_controller.route('/edit/<_id>')
def get_noticia_by_id(_id):
    noticia = NoticiaModel.query.filter_by(id=_id).first()
    return render_template('noticia/edit-noticia/edit-noticia.html', noticia=noticia)

