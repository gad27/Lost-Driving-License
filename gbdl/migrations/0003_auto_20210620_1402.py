# Generated by Django 3.1.4 on 2021-06-20 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gbdl', '0002_auto_20210620_1356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='license',
            name='phone',
            field=models.CharField(default='+250', max_length=15, null=True),
        ),
    ]
