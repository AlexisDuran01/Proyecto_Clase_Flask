from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30), nullable=False)
    segundo_nombre = db.Column(db.String(30), nullable=True)
    apellido_paterno = db.Column(db.String(30), nullable=False)
    apellido_materno= db.Column(db.String(30), nullable=True)
    telefono = db.Column(db.String(10), nullable=True)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    contraseña = db.Column(db.String(16), nullable=False)