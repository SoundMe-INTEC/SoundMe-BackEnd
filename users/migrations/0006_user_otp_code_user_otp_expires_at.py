from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0005_alter_user_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="otp_code",
            field=models.CharField(
                blank=True, editable=False, max_length=6, null=True
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="otp_expires_at",
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
    ]