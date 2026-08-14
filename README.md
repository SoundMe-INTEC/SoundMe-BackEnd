git clone <https://github.com/SoundMe-INTEC/backend-django-app>
cd SoundMe-BackEnd

python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# Instalar librerias 
pip install -r requirements.txt

# Crear el archivo .env

python manage.py migrate

python manage.py runserver

# Posibles Errrores 

Si instalar un paquete da error o se instala pero no lo encuentra, intentar instalarlo con python delante

pip install djangorestframework -> python -m pip install djangorestframework
