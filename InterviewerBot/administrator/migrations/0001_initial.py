# Generated by Django 3.1.1 on 2020-12-03 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Administrator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(blank=True, max_length=50, null=True)),
                ('lastname', models.CharField(blank=True, max_length=50, null=True)),
                ('phone', models.CharField(max_length=11)),
                ('password', models.CharField(blank=True, max_length=50, null=True)),
                ('gender', models.CharField(blank=True, max_length=10, null=True)),
                ('emailAddress', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'Administrator',
            },
        ),
        migrations.CreateModel(
            name='Login',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('emailAddress', models.CharField(blank=True, max_length=50, null=True)),
                ('password', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'currentAdmin',
            },
        ),
        migrations.CreateModel(
            name='CreateJob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id-title', models.CharField(blank=True, max_length=50, null=True)),
                ('id-description', models.CharField(blank=True, max_length=50, null=True)),
                ('id-question', models.CharField(blank=True, max_length=50, null=True)),
                ('id-answer', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'CreateJob',
            },
        ),
    ]
