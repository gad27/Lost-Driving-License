# Generated by Django 3.1.4 on 2021-04-25 10:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dln', models.CharField(max_length=16, null=True)),
                ('name', models.CharField(max_length=200, null=True)),
                ('dob', models.DateField(null=True)),
                ('class1', models.CharField(max_length=14, null=True)),
                ('sex', models.CharField(choices=[('Gabo', 'Gabo'), ('Gore', 'Gore')], max_length=4, null=True)),
                ('expd', models.DateField(null=True)),
                ('place', models.CharField(max_length=6, null=True)),
                ('phone', models.CharField(max_length=15, null=True)),
                ('group1', models.CharField(choices=[('LOST', 'LOST'), ('FOUND', 'FOUND')], max_length=6, null=True)),
                ('status', models.CharField(choices=[('NOT DECLARED', 'NOT DECLARED'), ('DECLARED', 'DECLARED')], max_length=50, null=True)),
                ('action', models.CharField(choices=[('IN STOCK', 'IN STOCK'), ('RETURNED', 'RETURNED')], max_length=8, null=True)),
                ('date_added_on', models.DateField(auto_now_add=True)),
                ('found_on', models.DateField(editable=False, null=True)),
                ('declared_on', models.DateField(null=True)),
                ('returned_on', models.DateField(editable=False, null=True)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='license', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
