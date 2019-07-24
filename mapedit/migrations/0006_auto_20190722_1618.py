# Generated by Django 2.2.2 on 2019-07-22 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mapedit', '0005_city_sysname'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='latitude',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='city',
            name='longitude',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='city',
            name='zoom',
            field=models.SmallIntegerField(default=0),
            preserve_default=False,
        ),
    ]