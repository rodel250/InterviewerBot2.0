# Generated by Django 3.1.1 on 2020-12-13 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0006_currentjob'),
    ]

    operations = [
        migrations.CreateModel(
            name='currentApplicant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('applicantID', models.IntegerField()),
            ],
            options={
                'db_table': 'currentApplicant',
            },
        ),
    ]
