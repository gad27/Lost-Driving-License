# Generated by Django 3.1.4 on 2021-06-20 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gbdl', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='license',
            name='dln',
            field=models.CharField(default='1', max_length=16, null=True),
        ),
    ]
