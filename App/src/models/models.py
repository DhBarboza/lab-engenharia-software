from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

tb_assunto = db.Table('tb_assunto',
                             db.Column('noticia_id', db.Integer, db.ForeignKey('noticia.id'), primary_key=True),
                             db.Column('assunto_id', db.Integer, db.ForeignKey('assunto.id'), primary_key=True),
                             db.Column('classificacao', db.Integer)
                             )


class Noticia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    steps = db.Column(db.String(1000), nullable=False)
    assuntos = db.relationship(
        'Assunto', secondary=tb_assunto, lazy='subquery',
        backref=db.backref('noticia', cascade='all,delete', lazy=True)
    )
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self):
        return '{}'.format(self.name)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'steps': self.steps,
            'created_at': str(self.created_at)
        }


class Assunto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self):
        return '{}'.format(self.name)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
        }
