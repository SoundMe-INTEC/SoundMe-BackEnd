git clone <https://github.com/SoundMe-INTEC/backend-django-app>
cd SoundMe-BackEnd

python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# Instalar librerias 
pip install -r requirements.txt

# Crear el archivo `.env` a partir de `.env.example`

# Configuracion SMTP

El registro envia el OTP usando SMTP. Copia `.env.example` como `.env` y completa
`EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` y `DEFAULT_FROM_EMAIL`. Con Gmail debes
usar una contrasena de aplicacion y tener activada la verificacion en dos pasos.

Para otro proveedor SMTP cambia `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USE_TLS` y
`EMAIL_USE_SSL` segun los datos de tu proveedor. No subas el archivo `.env` al
repositorio.

python manage.py migrate

python manage.py runserver

# Posibles Errrores 

Si instalar un paquete da error o se instala pero no lo encuentra, intentar instalarlo con python delante

pip install djangorestframework -> python -m pip install djangorestframework
