# Generated by Django 3.1.1 on 2020-11-30 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='login',
            name='user_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
