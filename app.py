from flask import Flask, render_template, request, url_for, flash, redirect,render_template_string,session
from markupsafe import escape

from RegistroForm import RegistroForm
from LoginForm import LoginForm

from sqlalchemy.exc import SQLAlchemyError

from models import db,Usuario


'''
Crea una instancia de la aplicación Flask
 __name__ es una variable especial en Python que contiene el nombre del módulo en el que se está ejecutando el script.
Si el script se ejecuta directamente, __name__ tendrá el valor "__main__".
Si el script se importa como un módulo en otro archivo, __name__ tomará el nombre del archivo (sin la extensión .py).
'''
app = Flask(__name__)
app.config['SECRET_KEY']= '12QAS4'
# Configuración de la base de datos (ajusta los valores a tu configuración)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://alexisduran01:root@localhost/proyecto'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desactivar el seguimiento de modificaciones
'''
Realiza un seguimiento de los cambios en los objetos SQLAlchemy (modelos) para poder 
emitir señales cuando se modifican. Esto es útil en ciertos casos, como cuando se 
integra con extensiones o librerías que necesitan saber cuándo los objetos han cambiado (por ejemplo, para actualizar cachés o disparar eventos)
'''

app.secret_key = '3234D34'

# Inicializar SQLAlchemy con la aplicación
db.init_app(app)

# Crea las tablas en la base de datos
with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        print(f"Error al conectar o crear tablas: {e}")


# Ruta principal y con nombre opcional
@app.route('/')
@app.route('/<nombre>')
@app.route('/index/')
@app.route('/index/<path:nombre>')

def index(nombre=None):
    """
    Función para renderizar la página de inicio.
    - Cuando se le pone None al parámetro nombre lo hace opcional,
    ya que usara el valor por defecto osea None

    - Esto permite manejar rutas sin el parámetro nombre como por ejemplo
    /index/ sin causar errores
    """
    """
    Esta función maneja una ruta dinámica con el convertidor `path`.

    - **¿Qué es `<path>`?**
      - `<path>` es un convertidor de ruta en Flask que permite capturar texto que incluye barras (`/`).
      - A diferencia de otros convertidores como `string`, que no permiten barras, `<path>` es ideal para manejar rutas jerárquicas o estructuras complejas.

    - **¿Qué hace `<path:nombre>`?**
      - Captura cualquier texto después de `/index/`, incluyendo barras, y lo asigna al parámetro `nombre`.
      - Ejemplo:
        - URL: `/index/carpeta/subcarpeta/archivo.txt`
        - Valor capturado: `nombre = "carpeta/subcarpeta/archivo.txt"`

    - **Casos de uso comunes:**
      - Simulación de sistemas de archivos virtuales.
      - Manejo de recursos jerárquicos en APIs RESTful.
      - Rutas dinámicas con múltiples niveles de profundidad.

    - **Consideraciones importantes:**
      - Validar y escapar siempre el contenido capturado para evitar vulnerabilidades como XSS (Cross-Site Scripting).
      - Si el parámetro es opcional, definir múltiples rutas para manejar casos donde no se proporcione un valor.
    """
    nombre = session.get('nombre')
    apellido_paterno=session.get('apellido_paterno')

    if nombre or apellido_paterno:
     return redirect(url_for('dashboard'))

    return render_template('index.html', name=nombre)

# Ruta para mostrar código
@app.route('/code/')
@app.route('/code/<path:code>')
def code(code=None):
    if code is None:
        return "<code>No code provided</code>"
    else:
        # Escapa el contenido para evitar XSS y lo envuelve en etiquetas <code>
        return f"<code>{escape(code)}</code>"

@app.route('/ingresar', methods=['GET', 'POST'])
def ingresar():
    form = LoginForm()  # Crear una instancia del formulario de login

    if request.method == 'POST':

        if form.validate_on_submit():  # Si el formulario se envía y es válido
            try:
                email = form.email.data  # Obtener el valor del campo email
                password = form.contrasenia.data  # Obtener el valor del campo contraseña

                # Buscar el usuario en la base de datos por su correo
                usuario = Usuario.query.filter_by(correo=email).first()

                if usuario:
                    if usuario.contraseña == password:  # Verificar la contraseña
                        # Almacenar información del usuario en la sesión
                        session['nombre'] = usuario.nombre
                        session['apellido_paterno'] = usuario.apellido_paterno

                        # Redirigir al dashboard después del login exitoso
                        flash('Inicio de sesión exitoso ¡Bienvenido!', 'success')

                        session['nuevo_usuario'] = False
                        return redirect(url_for('dashboard'))  # Redirigir sin parámetros en la URL

                    else:
                        # Contraseña incorrecta
                        flash('Contraseña incorrecta', 'danger')
                else:
                    # Usuario no encontrado
                    flash('Usuario no encontrado', 'danger')

            except SQLAlchemyError as e:
                # En caso de error, mostrar un mensaje y redirigir a la página de inicio de sesión
                flash('Error interno. Por favor, inténtalo de nuevo, mas tarde', 'danger')
                print(f'Error: {e}')
        else:
            # Si el formulario no es válido, mostrar un mensaje de error
            flash('Por favor, revisa los errores en el formulario y vuelve a intentarlo', 'danger')

    nombre = session.get('nombre')
    apellido_paterno=session.get('apellido_paterno')

    if nombre or apellido_paterno:
        return redirect(url_for('dashboard'))

    # Renderizar la plantilla de login para solicitudes GET o si el formulario no es válido
    return render_template('login.html', form=form)



@app.route('/registro', methods=['GET', 'POST'])
def registro():
    form = RegistroForm()  # Crear una instancia del formulario de registro

    # Comprobamos si el método de la solicitud es POST (cuando se envía el formulario)
    if request.method == 'POST':
        if form.validate_on_submit():  # Si el formulario se envía y es válido
            try:
                # Obtener los valores de los campos del formulario
                nombre_recuperado = form.nombre.data
                segundo_nombre_recuperado = form.segundo_nombre.data
                apellido_paterno_recuperado = form.apellido_paterno.data
                apellido_materno_recuperado = form.apellido_materno.data
                telefono_recuperado = form.telefono.data
                email_recuperado = form.email.data
                contrasenia_recuperado = form.contrasenia.data

                # Verificar si el correo ya está registrado
                usuario_existente = Usuario.query.filter_by(correo=email_recuperado).first()
                if usuario_existente:
                    flash('El correo electrónico ya está en uso Por favor, utiliza otro.', 'danger')
                    form.email.data=""
                    return render_template('registro.html', form=form)  # Mantener los datos del formulario

                # Crear un nuevo usuario
                nuevo_usuario = Usuario(
                    nombre=nombre_recuperado,
                    segundo_nombre=segundo_nombre_recuperado,
                    apellido_paterno=apellido_paterno_recuperado,
                    apellido_materno=apellido_materno_recuperado,
                    telefono=telefono_recuperado,
                    correo=email_recuperado,
                    contraseña=contrasenia_recuperado
                )

                # Agregar el nuevo usuario a la sesión de la base de datos
                db.session.add(nuevo_usuario)
                # Confirmar la transacción
                db.session.commit()
                # Almacenar información del usuario en la sesión
                session['nombre'] = nuevo_usuario.nombre
                session['apellido_paterno'] = nuevo_usuario.apellido_paterno

                # Redirigir al dashboard después del registro exitoso
                flash('Registro exitoso. ¡Bienvenido!', 'success')

                session['nuevo_usuario'] = True
                return redirect(url_for('dashboard'))

            except SQLAlchemyError as e:
                # En caso de error, deshacer la transacción
                db.session.rollback()
                flash('Error interno. Por favor, inténtalo de nuevo más tarde', 'danger')
                print(f'Error: {e}')

        else:
            # Si el formulario no es válido, mostrar un mensaje de error
            flash('Por favor, revisa los errores en el formulario y vuelve a intentarlo', 'danger')

    nombre = session.get('nombre')
    apellido_paterno = session.get('apellido_paterno')

    if nombre or apellido_paterno:
        return redirect(url_for('dashboard'))

    # Renderizar la plantilla de registro para solicitudes GET o si el formulario no es válido
    return render_template('registro.html', form=form)


@app.route('/logout')
def logout():

    # Verificar si el usuario ha iniciado sesión
    if 'nombre' not in session and 'apellido_paterno' not in session:
        return redirect(url_for('ingresar'))  # Redirigir a la página de inicio de sesión

    # Limpiar la sesión
    session.clear()
    flash('Has cerrado sesión correctamente.', 'success')
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    nombre = session.get('nombre')
    apellido_paterno = session.get('apellido_paterno')
    nuevo_usuario = session.pop('nuevo_usuario', False)  # Obtener y eliminar de la sesión

    if not nombre or not apellido_paterno:
        return redirect(url_for('ingresar'))

    # Renderizar la plantilla del dashboard
    return render_template('dashboard.html', nombre=nombre, apellido_paterno=apellido_paterno, nuevo_usuario=nuevo_usuario)

@app.route('/vulnerable/<path:codigoJs>')
def vulnerable(codigoJs):
    """
    Esta ruta es vulnerable a XSS porque no escapa el contenido recibido.
    - El parámetro 'codigoJs' se incluye directamente en la respuesta HTML sin escaparlo.
    - Esto permite la ejecución de scripts maliciosos.
    """
    '''
    La función render_template_string se utiliza para renderizar una plantilla 
    HTML directamente desde una cadena en Python.
    
    Por ello se usa render_template_string para renderizar el contenido directamente
    asi ejecutar el codigo de JavaScript, ya que cuando se usar por ejemplo
    render_template, Jinja2 escape automáticamente los caracteres especiales
     (como `<`, `>`, etc.) cuando insertas variables en la URL usando {} en la cadena
    '''
    return render_template_string(f'''
        <h1>Prueba de XSS Vulnerable</h1>
        <p>El valor ingresado es: {codigoJs}</p>
    ''')



'''
El if __name__ == '__main__': se usa en Python para asegurarse de que un bloque de 
código solo se ejecute cuando el script se ejecuta directamente y no cuando se importa 
como un módulo en otro archivo.

Ya que cuando se importe como otro modulo y no tiene este IF Flask iniciara el servidor
 automaticamente
'''
if __name__ == '__main__':
    app.run(debug=True)

