from django.contrib.auth.models import BaseUserManager

class UserManager (BaseUserManager):

    def create_user(self, identification, email, password=None, **extra_fields):
        if not identification:
            raise ValueError("Identification is required")
        if not email:
            raise ValueError("Email is required")
        
        # Esta es una función interna que permite normalizar los dominios de los correos, es decir, del @ en adelante
        # Usuario.Prueba@Gmail.COM sin normalizar
        # Usuario.Prueba@gmail.com normalizado
        
        email = self.normalize_email(email)

        user = self.model(
            identification = identification,
            email = email,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    # Antes de crear como super usuario, primero crea el usuario normal y luego toma los datos previos, por lo que el email en 
    # create_superuser ya llega normalizado

    def create_superuser(self, identification, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("The superuser would be have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
                    raise ValueError("The superuser would be have is_superuser=True")

        return self.create_user(identification, email, password, **extra_fields)