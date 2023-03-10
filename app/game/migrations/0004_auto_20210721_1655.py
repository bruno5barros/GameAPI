# Generated by Django 3.1.7 on 2021-07-21 16:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('game', '0003_auto_20210721_1107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playsession',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='last_played_session', to=settings.AUTH_USER_MODEL),
        ),
    ]
