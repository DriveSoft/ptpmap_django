# Generated by Django 2.2.2 on 2019-07-11 10:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mapedit', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ptp',
            old_name='date',
            new_name='datetime',
        ),
    ]