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

# Configuracion del envio de OTP (SoundMe Mail Relay)

Railway (plan Hobby) bloquea las conexiones SMTP salientes, por lo que el envio
del OTP se delega al microservicio `SoundMe-MailRelay` (repo aparte), que corre
en una maquina con salida SMTP normal. Copia `.env.example` como `.env` y
define `MAIL_RELAY_URL` (URL HTTPS del relay) y `MAIL_RELAY_API_KEY` (debe
coincidir con `RELAY_API_KEY` configurado en ese servicio). No subas el archivo
`.env` ni las API keys al repositorio.

python manage.py migrate

python manage.py runserver

# Posibles Errrores 

Si instalar un paquete da error o se instala pero no lo encuentra, intentar instalarlo con python delante

pip install djangorestframework -> python -m pip install djangorestframework
