# Generated by Django 3.1.1 on 2020-12-09 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='createjob',
            name='question_1',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
