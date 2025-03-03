from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TelField,IntegerField
from wtforms.validators import DataRequired, Email, Length,Regexp,Optional

class RegistroForm (FlaskForm):

    # Definimos un campo de tipo StringField llamado "nombre".
    # Este campo es obligatorio y acepta un texto de longitud mínima de 2 caracteres y máxima de 30 caracteres.
    # El validador DataRequired() asegura que el campo no quede vacío.
    # El validador Length(min=2, max=30) asegura que el texto tenga entre 2 y 30 caracteres.
    nombre = StringField(
        'Nombre',  # Etiqueta que se mostrará en el formulario como "Nombre"
        validators=[
            DataRequired(message="Campo requerido"),  # Validador que obliga a que el campo no esté vacío
            Length(min=2, max=30, message="El campo debe tener entre 2 y 30 caracteres")  # Validador que restringe la longitud mínima y máxima del texto
        ]
    )

    # Definimos un campo de tipo StringField llamado "segundo_nombre".
    # Este campo es opcional, por lo que no requiere validación de obligatoriedad.
    # El validador Length asegura que el segundo nombre (si se proporciona) tenga entre 2 y 30 caracteres.
    segundo_nombre = StringField(
        'Segundo Nombre',  # Etiqueta que se mostrará en el formulario como "Segundo Nombre"
        validators=[
            Optional(),  # Campo no obligatorio
            Length(min=2, max=30,message="El campo debe tener entre 2 y 30 caracteres")  # Validador que restringe la longitud mínima y máxima del texto
        ]
    )

    # Definimos un campo de tipo StringField llamado "apellido_paterno".
    # Este campo es obligatorio y acepta un texto de longitud mínima de 2 caracteres y máxima de 50 caracteres.
    # El validador DataRequired() asegura que el campo no quede vacío.
    # El validador Length(min=2, max=30) asegura que el texto tenga entre 2 y 50 caracteres.
    apellido_paterno = StringField(
        'Apellido Paterno',  # Etiqueta que se mostrará en el formulario como "Apellido Paterno"
        validators=[
            DataRequired(message="Campo requerido"),  # Validador que obliga a que el campo no esté vacío
            Length(min=2, max=30,message="El campo debe tener entre 2 y 30 caracteres")  # Validador que restringe la longitud mínima y máxima del texto
        ]
    )

    # Definimos un campo de tipo StringField llamado "apellido_materno".
    # Este campo es opcional, por lo que no requiere validación de obligatoriedad.
    # El validador Length asegura que el apellido materno (si se proporciona) tenga entre 2 y 50 caracteres.
    apellido_materno = StringField(
        'Apellido Materno',  # Etiqueta que se mostrará en el formulario como "Apellido Materno"
        validators=[
            Optional(),  # Campo no obligatorio
            Length(min=2, max=30,message="El campo debe tener entre 2 y 30 caracteres")  # Validador que restringe la longitud mínima y máxima del texto
        ]
    )

    # Definimos un campo de tipo IntegegerField
    # Este campo es opcional, por lo que no requiere validación de obligatoriedad.
    # El validador Length asegura que el teléfono (si se proporciona) sea de 10.
    telefono = StringField(
        'Teléfono',  # Etiqueta que se mostrará en el formulario como "Teléfono"
        validators=[
            Optional(),  # Campo no obligatorio
            Length(min=10, max=10, message="El teléfono debe tener exactamente 10 dígitos"),  # Validador de longitud
            Regexp(r'^\d{10}$', message="El teléfono solo puede contener numeros")  # Validador de expresión regular para solo números
        ]
    )

    # Definimos un campo de tipo StringField llamado "email".
    # Este campo es obligatorio y debe ser una dirección de correo electrónico válida.
    # El validador DataRequired() asegura que el campo no quede vacío.
    # El validador Email() asegura que el texto ingresado sea un correo electrónico válido.
    email = StringField(
        'Email',  # Etiqueta que se mostrará en el formulario como "Email"
        validators=[
            DataRequired(message="El email es requerido"),  # Validador que obliga a que el campo no esté vacío
            Email(message="Formato invalido")  # Validador que asegura que el campo contenga un correo electrónico válido
        ]
    )

    # Definimos un campo de tipo PasswordField llamado "contrasenia".
    # Este campo es obligatorio y debe tener entre 6 y 50 caracteres.
    # El validador DataRequired() asegura que el campo no quede vacío.
    # El validador Length(min=6, max=50) asegura que la contraseña tenga entre 8 y 16 caracteres.
    contrasenia = PasswordField(
        'Contraseña',  # Etiqueta que se mostrará en el formulario como "Contraseña"
        validators=[
            DataRequired(message="Contraseña requerida"),  # Validador que obliga a que el campo no esté vacío
            Length(min=8, max=16, message="La contraseña debe tener entre 8 y 16 caracteres")  # Validador que restringe la longitud mínima y máxima de la contraseña
        ]
    )

    # Definimos un campo de tipo SubmitField llamado "submit".
    # Este campo representará el botón de envío del formulario.
    submit = SubmitField('Registrarse')  # Etiqueta del botón que se mostrará como "Registrarse"

