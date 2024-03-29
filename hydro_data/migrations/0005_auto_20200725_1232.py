# Generated by Django 3.0.8 on 2020-07-25 04:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hydro_data', '0004_batch_num'),
    ]

    operations = [
        migrations.AddField(
            model_name='harvestdata',
            name='site',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hydro_data.Site'),
        ),
        migrations.AddField(
            model_name='plantingdata',
            name='site',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hydro_data.Site'),
        ),
        migrations.AddField(
            model_name='seedlingwastagedata',
            name='site',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hydro_data.Site'),
        ),
        migrations.AddField(
            model_name='spoilagedata',
            name='site',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hydro_data.Site'),
        ),
        migrations.AddField(
            model_name='transplantdata',
            name='site',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hydro_data.Site'),
        ),
        migrations.AddField(
            model_name='wastagedata',
            name='site',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hydro_data.Site'),
        ),
        migrations.AlterField(
            model_name='batch',
            name='num',
            field=models.PositiveSmallIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='location',
            name='is_open',
            field=models.CharField(choices=[('0', 'Occupied'), ('1', 'Open')], default='1', max_length=1),
        ),
        migrations.AlterField(
            model_name='producetype',
            name='seed_brand',
            field=models.CharField(blank=True, max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='producetype',
            name='variety',
            field=models.CharField(blank=True, max_length=100, unique=True),
        ),
    ]
