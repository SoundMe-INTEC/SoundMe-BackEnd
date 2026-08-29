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

# Configuracion de correo con Resend

El registro envia el OTP por SMTP usando Resend. Copia `.env.example` como `.env`,
crea una API key de envio en Resend y define `RESEND_API_KEY` y
`DEFAULT_FROM_EMAIL`. Con solo `RESEND_API_KEY`, la configuracion usa
automáticamente `smtp.resend.com`, puerto `465`, usuario `resend` y SSL.

Para pruebas usa `SoundMe <onboarding@resend.dev>`; Resend solo permitirá enviar
al correo propietario de la cuenta. Para enviar a usuarios finales, verifica un
dominio en Resend y usa un remitente de ese dominio. No subas el archivo `.env`
ni las API keys al repositorio.

python manage.py migrate

python manage.py runserver

# Posibles Errrores 

Si instalar un paquete da error o se instala pero no lo encuentra, intentar instalarlo con python delante

pip install djangorestframework -> python -m pip install djangorestframework
