# Generated by Django 3.0.8 on 2020-07-25 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hydro_data', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='plantingdata',
            name='seedling_batch_no',
            field=models.PositiveSmallIntegerField(blank=True, default=0),
        ),
    ]