# Generated by Django 3.1.1 on 2020-11-29 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='applicant',
            name='firstName',
        ),
        migrations.RemoveField(
            model_name='applicant',
            name='lastName',
        ),
        migrations.AddField(
            model_name='applicant',
            name='firstname',
            field=models.CharField(blank='True', max_length=50, null='True'),
            preserve_default='True',
        ),
        migrations.AddField(
            model_name='applicant',
            name='lastname',
            field=models.CharField(blank='True', max_length=50, null='True'),
            preserve_default='True',
        ),
        migrations.AddField(
            model_name='applicant',
            name='phone',
            field=models.CharField(default=0, max_length=11),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='applicant',
            name='emailAddress',
            field=models.CharField(blank='True', max_length=50, null='True'),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='gender',
            field=models.CharField(blank='True', max_length=10, null='True'),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='password',
            field=models.CharField(blank='True', max_length=50, null='True'),
        ),
    ]
