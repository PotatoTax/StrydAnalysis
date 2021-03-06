# Generated by Django 3.1 on 2020-08-08 22:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20200805_2225'),
    ]

    operations = [
        migrations.CreateModel(
            name='PowerCurveEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('power', models.IntegerField()),
                ('duration', models.IntegerField()),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.activity')),
            ],
        ),
    ]
