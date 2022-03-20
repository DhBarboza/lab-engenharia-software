import json

from flask import Blueprint, render_template, request, current_app, Response
from flask_sqlalchemy import SQLAlchemy

from src.model.models import Assunto as AssuntoModel

assunto_controller = Blueprint('assunto', __name__, url_prefix='/assuntos')


@assunto_controller.route('/')
def index():
    try:
        assuntos = get_assuntos().json['assuntos']
    except Exception as error:
        print(error)
        assuntos = []
    return render_template('assunto/assunto.html', title='Assuntos', data={'assuntos': assuntos})


@assunto_controller.route('/create', methods=['GET', 'POST'])
def create_assuntos():
    if request.json:
        try:
            db = SQLAlchemy(current_app)
            obj = request.json

            assunto = AssuntoModel(**obj)

            with current_app.app_context():
                db.session.add(assunto)
                db.session.commit()

            res = json.dumps({'message': 'Assunto cadastrado!', 'error': False})
            return Response(res, mimetype='application/json', status=200)

        except Exception as error:
            res = json.dumps({'message': str(error), 'error': True})
            return Response(res, mimetype='application/json', status=500)
    else:
        return render_template('assunto/create-assunto/create-assunto.html', title='Adicionar assuntos')


@assunto_controller.route('/edit/<_id>', methods=['GET', 'PUT'])
def update_assunto(_id):
    if request.json:
        try:
            db = SQLAlchemy(current_app)
            obj = request.json

            assunto = AssuntoModel.query.filter_by(id=_id).first()
            assunto.name = obj['name']

            with current_app.app_context():
                db.session.merge(assunto)
                db.session.commit()

            res = json.dumps({'message': 'Assunto atualizado com sucesso', 'error': False})
            return Response(res, mimetype='application/json', status=200)
        except Exception as error:
            res = json.dumps({'message': str(error), 'error': True})
            return Response(res, mimetype='application/json', status=500)
    else:
        assunto = AssuntoModel.query.filter_by(id=_id).first()
        return render_template('assunto/edit-assunto/edit-assunto.html', title='Editar assuntos',
                               assunto=assunto)


@assunto_controller.route('/delete/<_id>', methods=['DELETE'])
def delete_assunto(_id):
    try:
        db = SQLAlchemy(current_app)

        with current_app.app_context():
            db.session.query(AssuntoModel).filter_by(id=_id).delete()
            db.session.commit()

        res = json.dumps({'message': 'Assunto excluído', 'error': False})
        return Response(res, mimetype='application/json', status=200)

    except Exception as error:
        res = json.dumps({'message': str(error), 'error': True})
        return Response(res, mimetype='application/json', status=500)


@assunto_controller.route('/getAssuntos')
def get_assuntos():
    try:
        assuntos = AssuntoModel.query.all()
        if not assuntos:
            raise Exception('Nenhum assunto')

        assuntos = list(map(lambda x: {'id': x.id, 'name': x.name, 'created_at': str(x.created_at)}, assuntos))
        res = json.dumps({'assuntos': assuntos})
        return Response(res, mimetype='application/json', status=200)

    except Exception as error:
        res = []
        return Response(res, mimetype='application/json', status=500)
