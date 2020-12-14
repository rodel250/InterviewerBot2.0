# Generated by Django 3.1.1 on 2020-12-14 08:40

from django.db import migrations, models
import django.db.models.deletion


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
            name='currentApplicant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('applicantID', models.IntegerField()),
            ],
            options={
                'db_table': 'currentApplicant',
            },
        ),
        migrations.CreateModel(
            name='currentJob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jobID', models.IntegerField()),
            ],
            options={
                'db_table': 'currentJob',
            },
        ),
        migrations.CreateModel(
            name='CreateJob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=50, null=True)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('question_1', models.CharField(blank=True, max_length=250, null=True)),
                ('question_2', models.CharField(blank=True, max_length=250, null=True)),
                ('question_3', models.CharField(blank=True, max_length=250, null=True)),
                ('question_4', models.CharField(blank=True, max_length=250, null=True)),
                ('question_5', models.CharField(blank=True, max_length=250, null=True)),
                ('question_6', models.CharField(blank=True, max_length=250, null=True)),
                ('question_7', models.CharField(blank=True, max_length=250, null=True)),
                ('question_8', models.CharField(blank=True, max_length=250, null=True)),
                ('question_9', models.CharField(blank=True, max_length=250, null=True)),
                ('question_10', models.CharField(blank=True, max_length=250, null=True)),
                ('question_11', models.CharField(blank=True, max_length=250, null=True)),
                ('question_12', models.CharField(blank=True, max_length=250, null=True)),
                ('question_13', models.CharField(blank=True, max_length=250, null=True)),
                ('question_14', models.CharField(blank=True, max_length=250, null=True)),
                ('question_15', models.CharField(blank=True, max_length=250, null=True)),
                ('question_16', models.CharField(blank=True, max_length=250, null=True)),
                ('question_17', models.CharField(blank=True, max_length=250, null=True)),
                ('question_18', models.CharField(blank=True, max_length=250, null=True)),
                ('question_19', models.CharField(blank=True, max_length=250, null=True)),
                ('question_20', models.CharField(blank=True, max_length=250, null=True)),
                ('requirement1', models.CharField(blank=True, max_length=250, null=True)),
                ('requirement2', models.CharField(blank=True, max_length=250, null=True)),
                ('requirement3', models.CharField(blank=True, max_length=250, null=True)),
                ('requirement4', models.CharField(blank=True, max_length=250, null=True)),
                ('requirement5', models.CharField(blank=True, max_length=250, null=True)),
                ('requirement6', models.CharField(blank=True, max_length=250, null=True)),
                ('requirement7', models.CharField(blank=True, max_length=250, null=True)),
                ('requirement8', models.CharField(blank=True, max_length=250, null=True)),
                ('requirement9', models.CharField(blank=True, max_length=250, null=True)),
                ('requirement10', models.CharField(blank=True, max_length=250, null=True)),
                ('requirement11', models.CharField(blank=True, max_length=250, null=True)),
                ('requirement12', models.CharField(blank=True, max_length=250, null=True)),
                ('requirement13', models.CharField(blank=True, max_length=250, null=True)),
                ('requirement14', models.CharField(blank=True, max_length=250, null=True)),
                ('requirement15', models.CharField(blank=True, max_length=250, null=True)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Administrator', to='administrator.administrator')),
            ],
            options={
                'db_table': 'CreateJob',
            },
        ),
    ]
