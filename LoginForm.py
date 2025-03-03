from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TelField,IntegerField
from wtforms.validators import DataRequired, Email, Length,Regexp,Optional

class LoginForm (FlaskForm): # LoginForm hereda de FlaskForm


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
    submit = SubmitField('Acceder')  # Etiqueta del botón que se mostrará como "Registrarse"

