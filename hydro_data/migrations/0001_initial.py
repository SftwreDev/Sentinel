# Generated by Django 3.0.8 on 2020-07-24 11:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Acid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(allow_unicode=True, default='hydro_farm_acid', editable=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(allow_unicode=True, default='hydro_farm_activity', editable=False, unique=True)),
            ],
            options={
                'verbose_name': 'activity',
                'verbose_name_plural': 'activities',
            },
        ),
        migrations.CreateModel(
            name='Box',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(allow_unicode=True, editable=False, unique=True)),
                ('description', models.TextField(blank=True, default='')),
                ('description_html', models.TextField(blank=True, default='', editable=False)),
            ],
            options={
                'verbose_name': 'box',
                'verbose_name_plural': 'boxes',
            },
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(allow_unicode=True, default='hydro_farm_acid', editable=False, unique=True)),
                ('type', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='GrowMedium',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(allow_unicode=True, default='hydro_farm_acid', editable=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='HarvestData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, default=django.utils.timezone.now)),
                ('time', models.TimeField(blank=True, default=django.utils.timezone.now)),
                ('harvest_weight_kg', models.FloatField(blank=True, null=True)),
                ('no_of_heads', models.PositiveSmallIntegerField(blank=True, default=0)),
                ('box', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hydro_data.Box')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(allow_unicode=True, default='hydro_farm_sqm_id', editable=False, unique=True)),
                ('x_cor', models.FloatField(blank=True, null=True)),
                ('y_cor', models.FloatField(blank=True, null=True)),
                ('is_open', models.CharField(choices=[('0', 'Occupied'), ('1', 'Open')], default='0', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Nutrient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(allow_unicode=True, default='hydro_farm_nutrient', editable=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='PlantingData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, default=django.utils.timezone.now)),
                ('time', models.TimeField(blank=True, default=django.utils.timezone.now)),
                ('box', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hydro_data.Box')),
                ('growmedium', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hydro_data.GrowMedium')),
            ],
        ),
        migrations.CreateModel(
            name='ProduceType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(allow_unicode=True, default='hydro_farm_produce', editable=False, unique=True)),
                ('variety', models.CharField(max_length=100, unique=True)),
                ('seed_brand', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(allow_unicode=True, default='hydro_farm_rack', editable=False)),
                ('x_cor', models.FloatField(blank=True, null=True)),
                ('y_cor', models.FloatField(blank=True, null=True)),
                ('box', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hydro_data.Box')),
            ],
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(allow_unicode=True, editable=False, unique=True)),
                ('description', models.TextField(blank=True, default='')),
                ('description_html', models.TextField(blank=True, default='', editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Tank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(allow_unicode=True, default='hydro_farm_tank', editable=False)),
                ('box', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hydro_data.Box')),
            ],
        ),
        migrations.CreateModel(
            name='Tray',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(allow_unicode=True, default='hydro_farm_acid', editable=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='WaterReading',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, default=django.utils.timezone.now)),
                ('time', models.TimeField(blank=True, default=django.utils.timezone.now)),
                ('prev_ph', models.FloatField(blank=True, null=True)),
                ('current_ph', models.FloatField(blank=True, null=True)),
                ('prev_ec', models.FloatField(blank=True, null=True)),
                ('current_ec', models.FloatField(blank=True, null=True)),
                ('acid_used_ml', models.FloatField(blank=True, null=True)),
                ('nutrient_used_ml', models.FloatField(blank=True, null=True)),
                ('water_level_liters', models.FloatField(blank=True, null=True)),
                ('acid_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hydro_data.Acid')),
                ('activity', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hydro_data.Activity')),
                ('box', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hydro_data.Box')),
                ('nutrient_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hydro_data.Nutrient')),
                ('site', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hydro_data.Site')),
                ('staff', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('tank', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hydro_data.Tank')),
            ],
        ),
        migrations.CreateModel(
            name='WaterConsumption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, default=django.utils.timezone.now)),
                ('time', models.TimeField(blank=True, default=django.utils.timezone.now)),
                ('water_reading', models.FloatField(blank=True, null=True)),
                ('site', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hydro_data.Site')),
                ('staff', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WastageData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, default=django.utils.timezone.now)),
                ('time', models.TimeField(blank=True, default=django.utils.timezone.now)),
                ('wastage_kg', models.FloatField(blank=True, null=True)),
                ('wastage_reason', models.CharField(max_length=100)),
                ('box', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hydro_data.Box')),
                ('rack', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hydro_data.Rack')),
                ('seedlingdata', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hydro_data.PlantingData')),
                ('square_meter_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hydro_data.Location')),
                ('staff', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TransplantData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, default=django.utils.timezone.now)),
                ('time', models.TimeField(blank=True, default=django.utils.timezone.now)),
                ('box', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hydro_data.Box')),
                ('rack', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hydro_data.Rack')),
                ('seedlingdata', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hydro_data.PlantingData')),
                ('square_meter_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hydro_data.Location')),
                ('staff', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SpoilageData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, default=django.utils.timezone.now)),
                ('time', models.TimeField(blank=True, default=django.utils.timezone.now)),
                ('wastage_kg', models.FloatField(blank=True, null=True)),
                ('wastage_reason', models.CharField(max_length=100, unique=True)),
                ('harvestdata', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hydro_data.HarvestData')),
                ('staff', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SeedlingWastageData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, default=django.utils.timezone.now)),
                ('time', models.TimeField(blank=True, default=django.utils.timezone.now)),
                ('wastage_reason', models.CharField(max_length=100)),
                ('seedlingdata', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hydro_data.PlantingData')),
                ('staff', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RackLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hydro_data.Location')),
                ('rack', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hydro_data.Rack')),
            ],
        ),
        migrations.AddField(
            model_name='plantingdata',
            name='produce_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hydro_data.ProduceType'),
        ),
        migrations.AddField(
            model_name='plantingdata',
            name='rack',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hydro_data.Rack'),
        ),
        migrations.AddField(
            model_name='plantingdata',
            name='square_meter_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hydro_data.Location'),
        ),
        migrations.AddField(
            model_name='plantingdata',
            name='staff',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='plantingdata',
            name='tray',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hydro_data.Tray'),
        ),
        migrations.AddField(
            model_name='location',
            name='rack',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hydro_data.Rack'),
        ),
        migrations.CreateModel(
            name='LightReading',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, default=django.utils.timezone.now)),
                ('time', models.TimeField(blank=True, default=django.utils.timezone.now)),
                ('par_reading', models.FloatField(blank=True, null=True)),
                ('box', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hydro_data.Box')),
                ('rack', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hydro_data.Rack')),
                ('site', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hydro_data.Site')),
                ('square_meter_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hydro_data.Location')),
                ('staff', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='harvestdata',
            name='rack',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hydro_data.Rack'),
        ),
        migrations.AddField(
            model_name='harvestdata',
            name='seedlingdata',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hydro_data.TransplantData'),
        ),
        migrations.AddField(
            model_name='harvestdata',
            name='square_meter_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hydro_data.Location'),
        ),
        migrations.AddField(
            model_name='harvestdata',
            name='staff',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='EnergyConsumption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, default=django.utils.timezone.now)),
                ('time', models.TimeField(blank=True, default=django.utils.timezone.now)),
                ('electrical_reading', models.FloatField(blank=True, null=True)),
                ('box', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hydro_data.Box')),
                ('staff', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DeviceCalibration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, default=django.utils.timezone.now)),
                ('time', models.TimeField(blank=True, default=django.utils.timezone.now)),
                ('device', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hydro_data.Device')),
                ('staff', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='device',
            name='tank',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hydro_data.Tank'),
        ),
        migrations.CreateModel(
            name='BoxRack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('box', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hydro_data.Box')),
                ('rack', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hydro_data.Rack')),
            ],
        ),
        migrations.AddField(
            model_name='box',
            name='site',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hydro_data.Site'),
        ),
        migrations.CreateModel(
            name='AirReading',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, default=django.utils.timezone.now)),
                ('time', models.TimeField(blank=True, default=django.utils.timezone.now)),
                ('current_relative_humidity', models.FloatField(blank=True, null=True)),
                ('current_temp', models.FloatField(blank=True, null=True)),
                ('current_co2_level', models.FloatField(blank=True, null=True)),
                ('box', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hydro_data.Box')),
                ('site', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hydro_data.Site')),
                ('staff', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]