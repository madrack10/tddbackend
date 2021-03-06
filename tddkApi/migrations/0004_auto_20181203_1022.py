# Generated by Django 2.1.2 on 2018-12-03 10:22

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tddkApi', '0003_auto_20181121_1231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offre',
            name='domaine',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='Domaine', to='tddkApi.Domaine'),
        ),
        migrations.AlterField(
            model_name='offre',
            name='publishOn',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
