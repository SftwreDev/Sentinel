from django.db import models
from django.utils.text import slugify
from django.utils.timezone import localtime, now
import misaka

from django.contrib.auth import get_user_model
User = get_user_model()

class Site(models.Model):
    name = models.CharField(max_length=100,unique=True)
    slug = models.SlugField(allow_unicode=True,unique=True, editable=False)
    description = models.TextField(blank=True,default='')
    description_html = models.TextField(editable=False,default='',blank=True)

    def __str__(self):
        return self.name if self.name else ''

    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        self.description_html = misaka.html(self.description)
        super().save(*args,**kwargs)

class Box(models.Model):
    site = models.ForeignKey(Site,on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100,unique=True)
    slug = models.SlugField(allow_unicode=True,unique=True, editable=False)
    description = models.TextField(blank=True,default='')
    description_html = models.TextField(editable=False,default='',blank=True)

    def __str__(self):
        try:
            return self.site.name + ' | ' + self.name
        except:
            return 'Missing Values'

    def save(self,*args,**kwargs):
        self.slug = slugify(self.site.name + ' ' + self.name)
        self.description_html = misaka.html(self.description)
        super().save(*args,**kwargs)

    class Meta:
        verbose_name = 'box'
        verbose_name_plural = 'boxes'

class WaterConsumption(models.Model):
    date = models.DateField(default=now,blank=True)
    time = models.TimeField(default=now,blank=True)
    site = models.ForeignKey(Site,on_delete=models.SET_NULL,null=True)
    water_reading = models.FloatField(blank=True,null=True)
    staff = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        try:
            return str(self.date) + ' | ' + str(self.time) + ' | ' + self.site.name
        except:
            return 'Missing Values'

    def save(self,*args,**kwargs):
        try:
            self.time = localtime(self.time)
        except:
            pass
        super().save(*args,**kwargs)

class EnergyConsumption(models.Model):
    date = models.DateField(default=now,blank=True)
    time = models.TimeField(default=now,blank=True)
    box = models.ForeignKey(Box,on_delete=models.SET_NULL,null=True)
    electrical_reading = models.FloatField(blank=True,null=True)
    staff = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        try:
            return str(self.date) + ' | ' + str(self.time) + ' | ' + self.box.name
        except:
            return 'Missing Values'

    def save(self,*args,**kwargs):
        try:
            self.time = localtime(self.time)
        except:
            pass
        super().save(*args,**kwargs)

class Rack(models.Model):
    box = models.ForeignKey(Box, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(allow_unicode=True, editable=False, default='hydro_farm_rack')
    x_cor = models.FloatField(blank=True,null=True)
    y_cor = models.FloatField(blank=True,null=True)

    def __str__(self):
        try:
            return self.box.name + ' | ' + self.name
        except:
            return 'Missing Values'

    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        super().save(*args,**kwargs)

class BoxRack(models.Model):
    box = models.ForeignKey(Box, on_delete=models.SET_NULL, null=True)
    rack = models.ForeignKey(Rack, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        try:
            return self.box.name + ' | ' + self.rack.name
        except:
            return 'Missing Values'

class ProduceType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(allow_unicode=True,unique=True, editable=False, default='hydro_farm_produce')
    variety = models.CharField(max_length=100, unique=True, blank=True, null=True)
    seed_brand = models.CharField(max_length=100, unique=True, blank=True, null=True)

    def __str__(self):
        try:
            if self.variety:
                return self.variety + ' ' + self.name
            else:
                return self.name
        except:
            return 'Missing Values'

    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        super().save(*args,**kwargs)

class Location(models.Model):
    bool_choices = [
        ('0','Occupied'),
        ('1','Open')
    ]
    rack = models.ForeignKey(Rack, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(allow_unicode=True,unique=True, editable=False, default='hydro_farm_sqm_id')
    x_cor = models.FloatField(blank=True,null=True)
    y_cor = models.FloatField(blank=True,null=True)
    is_open = models.CharField(
        max_length = 1,
        choices=bool_choices,
        default='1'
    )

    def plant(self):
        self.is_open = '0'
        self.save()

    def put_transplant(self):
        self.is_open = '0'
        self.save()

    def transplant(self):
        self.is_open = '1'
        self.save()

    def wasted(self):
        self.is_open = '1'
        self.save()

    def clear(self):
        self.is_open = '1'
        self.save()

    def harvest(self):
        self.is_open = '1'
        self.save()

    def __str__(self):
        try:
            return self.rack.box.name + ' | ' + self.rack.name + ' | ' + self.name
        except:
            return 'Missing Values'

    def save(self,*args,**kwargs):
        self.slug = slugify(self.rack.name + ' ' + self.name)
        super().save(*args,**kwargs)

class RackLocation(models.Model):
    rack = models.ForeignKey(Rack, on_delete=models.SET_NULL, null=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        try:
            return self.rack.name + ' | ' + self.location.name
        except:
            return 'Missing Values'

class Acid(models.Model):
    name = models.CharField(max_length=100,unique=True)
    slug = models.SlugField(allow_unicode=True,unique=True, editable=False, default='hydro_farm_acid')

    def __str__(self):
        try:
            return self.name
        except:
            return 'Missing Values'

    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        super().save(*args,**kwargs)

class Nutrient(models.Model):
    name = models.CharField(max_length=100,unique=True)
    slug = models.SlugField(allow_unicode=True,unique=True, editable=False, default='hydro_farm_nutrient')

    def __str__(self):
        try:
            return self.name
        except:
            return 'Missing Values'

    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        super().save(*args,**kwargs)

class Activity(models.Model):
    name = models.CharField(max_length=100,unique=True)
    slug = models.SlugField(allow_unicode=True,unique=True, editable=False, default='hydro_farm_activity')

    def __str__(self):
        try:
            return self.name
        except:
            return 'Missing Values'

    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        super().save(*args,**kwargs)

    class Meta:
        verbose_name = 'activity'
        verbose_name_plural = 'activities'

class GrowMedium(models.Model):
    name = models.CharField(max_length=100,unique=True)
    slug = models.SlugField(allow_unicode=True,unique=True, editable=False, default='hydro_farm_acid')

    def __str__(self):
        try:
            return self.name
        except:
            return 'Missing Values'

    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        super().save(*args,**kwargs)

class Tray(models.Model):
    name = models.CharField(max_length=100,unique=True)
    slug = models.SlugField(allow_unicode=True,unique=True, editable=False, default='hydro_farm_acid')

    def __str__(self):
        try:
            return self.name
        except:
            return 'Missing Values'

    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        super().save(*args,**kwargs)

class Tank(models.Model):
    box = models.ForeignKey(Box, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(allow_unicode=True, editable=False, default='hydro_farm_tank')

    def __str__(self):
        try:
            return self.box.name + ' | ' + self.name
        except:
            return 'Missing Values'

    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        super().save(*args,**kwargs)

class Device(models.Model):
    tank = models.ForeignKey(Tank,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=100,unique=True)
    slug = models.SlugField(allow_unicode=True,unique=True, editable=False, default='hydro_farm_acid')
    type = models.CharField(max_length=100,unique=True)

    def __str__(self):
        try:
            return self.name
        except:
            return 'Missing Values'

    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        super().save(*args,**kwargs)

class DeviceCalibration(models.Model):
    date = models.DateField(default=now,blank=True)
    time = models.TimeField(default=now,blank=True)
    device = models.ForeignKey(Device,on_delete=models.SET_NULL,null=True)
    staff = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        try:
            return str(self.date) + ' | ' + str(self.time) + ' | ' + self.device.name
        except:
            return 'Missing Values'

    def save(self,*args,**kwargs):
        try:
            self.time = localtime(self.time)
        except:
            pass
        super().save(*args,**kwargs)

class Batch(models.Model):
    date = models.DateField(default=now,blank=True)
    time = models.TimeField(default=now,blank=True)
    num = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f'Batch {str(self.num)}'

class PlantingData(models.Model):
    date = models.DateField(default=now,blank=True)
    time = models.TimeField(default=now,blank=True)
    site = models.ForeignKey(Site,on_delete=models.SET_NULL,null=True)
    box = models.ForeignKey(Box,on_delete=models.SET_NULL,null=True)
    rack = models.ForeignKey(Rack,on_delete=models.SET_NULL,null=True)
    seedling_batch_no = models.ForeignKey(Batch,on_delete=models.SET_NULL,null=True)
    growmedium = models.ForeignKey(GrowMedium,on_delete=models.SET_NULL,null=True)
    tray = models.ForeignKey(Tray,on_delete=models.SET_NULL,null=True)
    produce_type = models.ForeignKey(ProduceType,on_delete=models.SET_NULL,null=True)
    square_meter_id = models.ForeignKey(Location,on_delete=models.SET_NULL,null=True)
    staff = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        try:
            return str(self.date) + ' | ' + str(self.time) + ' | ' + self.box.name + ' | ' + self.rack.name
        except:
            return 'Missing Values'

    def get_model_type(self):
        return "PLANT"

    def save(self,*args,**kwargs):
        try:
            self.time = localtime(self.time)
        except:
            pass
        super().save(*args,**kwargs)

class TransplantData(models.Model):
    date = models.DateField(default=now,blank=True)
    time = models.TimeField(default=now,blank=True)
    site = models.ForeignKey(Site,on_delete=models.SET_NULL,null=True)
    box = models.ForeignKey(Box,on_delete=models.SET_NULL,null=True)
    rack = models.ForeignKey(Rack,on_delete=models.SET_NULL,null=True)
    square_meter_id = models.ForeignKey(Location,on_delete=models.SET_NULL,null=True)
    seedling_batch_no = models.ForeignKey(Batch,on_delete=models.SET_NULL,null=True)
    staff = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        try:
            return str(self.date) + ' | ' + str(self.time) + ' | ' + self.box.name + ' | ' + self.rack.name
        except:
            return 'Missing Values'

    def get_model_type(self):
        return "TRANSPLANT"

    def save(self,*args,**kwargs):
        try:
            self.time = localtime(self.time)
        except:
            pass
        super().save(*args,**kwargs)

class SeedlingWastageData(models.Model):
    date = models.DateField(default=now,blank=True)
    time = models.TimeField(default=now,blank=True)
    site = models.ForeignKey(Site,on_delete=models.SET_NULL,null=True)
    box = models.ForeignKey(Box,on_delete=models.SET_NULL,null=True)
    rack = models.ForeignKey(Rack,on_delete=models.SET_NULL,null=True)
    square_meter_id = models.ForeignKey(Location,on_delete=models.SET_NULL,null=True)
    seedling_batch_no = models.ForeignKey(Batch,on_delete=models.SET_NULL,null=True)
    wastage_reason = models.CharField(max_length=100)
    staff = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        try:
            return str(self.date) + ' | ' + str(self.time) + ' | ' + self.box.name + ' | ' + self.rack.name
        except:
            return 'Missing Values'

    def get_model_type(self):
        return "SEEDLING WASTAGE"

    def save(self,*args,**kwargs):
        try:
            self.time = localtime(self.time)
        except:
            pass
        super().save(*args,**kwargs)

class HarvestData(models.Model):
    date = models.DateField(default=now,blank=True)
    time = models.TimeField(default=now,blank=True)
    site = models.ForeignKey(Site,on_delete=models.SET_NULL,null=True)
    box = models.ForeignKey(Box,on_delete=models.SET_NULL,null=True)
    rack = models.ForeignKey(Rack,on_delete=models.SET_NULL,null=True)
    square_meter_id = models.ForeignKey(Location,on_delete=models.SET_NULL,null=True)
    harvest_weight_kg = models.FloatField(blank=True,null=True)
    seedling_batch_no = models.ForeignKey(Batch,on_delete=models.SET_NULL,null=True)
    no_of_heads = models.PositiveSmallIntegerField(blank=True,null=True)
    staff = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        try:
            return str(self.date) + ' | ' + str(self.time) + ' | ' + self.box.name + ' | ' + self.rack.name
        except:
            return 'Missing Values'

    def get_model_type(self):
        return "HARVEST"

    def save(self,*args,**kwargs):
        try:
            self.time = localtime(self.time)
        except:
            pass
        super().save(*args,**kwargs)

class WastageData(models.Model):
    date = models.DateField(default=now,blank=True)
    time = models.TimeField(default=now,blank=True)
    site = models.ForeignKey(Site,on_delete=models.SET_NULL,null=True)
    box = models.ForeignKey(Box,on_delete=models.SET_NULL,null=True)
    rack = models.ForeignKey(Rack,on_delete=models.SET_NULL,null=True)
    square_meter_id = models.ForeignKey(Location,on_delete=models.SET_NULL,null=True)
    wastage_kg = models.FloatField(blank=True,null=True)
    wastage_reason = models.CharField(max_length=100)
    seedling_batch_no = models.ForeignKey(Batch,on_delete=models.SET_NULL,null=True)
    staff = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        try:
            return str(self.date) + ' | ' + str(self.time) + ' | ' + self.box.name + ' | ' + self.rack.name
        except:
            return 'Missing Values'

    def get_model_type(self):
        return "WASTAGE"

    def save(self,*args,**kwargs):
        try:
            self.time = localtime(self.time)
        except:
            pass
        super().save(*args,**kwargs)

class SpoilageData(models.Model):
    date = models.DateField(default=now,blank=True)
    time = models.TimeField(default=now,blank=True)
    site = models.ForeignKey(Site,on_delete=models.SET_NULL,null=True)
    harvestdata = models.ForeignKey(HarvestData,on_delete=models.SET_NULL,null=True)
    wastage_kg = models.FloatField(blank=True,null=True)
    wastage_reason = models.CharField(max_length=100,unique=True)
    staff = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        try:
            return str(self.date) + ' | ' + str(self.time) + ' | ' + str(self.harvestdata.seedlingdata.produce_type)
        except:
            return 'Missing Values'

    def get_model_type(self):
        return "SPOILAGE"

    def save(self,*args,**kwargs):
        try:
            self.time = localtime(self.time)
        except:
            pass
        super().save(*args,**kwargs)

class LightReading(models.Model):
    date = models.DateField(default=now,blank=True)
    time = models.TimeField(default=now,blank=True)
    site = models.ForeignKey(Site,on_delete=models.SET_NULL,null=True)
    box = models.ForeignKey(Box,on_delete=models.SET_NULL,null=True)
    rack = models.ForeignKey(Rack,on_delete=models.SET_NULL,null=True)
    square_meter_id = models.ForeignKey(Location,on_delete=models.SET_NULL,null=True)
    par_reading = models.FloatField(blank=True,null=True)
    staff = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        try:
            return str(self.date) + ' | ' + str(self.time) + ' | ' + self.box.name + ' | ' + self.rack.name
        except:
            return 'Missing Values'

    def get_model_type(self):
        return "LIGHT READING"

    def save(self,*args,**kwargs):
        try:
            self.time = localtime(self.time)
        except:
            pass
        super().save(*args,**kwargs)

class AirReading(models.Model):
    date = models.DateField(default=now,blank=True)
    time = models.TimeField(default=now,blank=True)
    site = models.ForeignKey(Site,on_delete=models.SET_NULL,null=True)
    box = models.ForeignKey(Box,on_delete=models.SET_NULL,null=True)
    current_relative_humidity = models.FloatField(blank=True,null=True)
    current_temp = models.FloatField(blank=True,null=True)
    current_co2_level = models.FloatField(blank=True,null=True)
    staff = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        try:
            return str(self.date) + ' | ' + str(self.time) + ' | ' + self.box.name
        except:
            return 'Missing Values'

    def get_model_type(self):
        return "AIR READING"

    def save(self,*args,**kwargs):
        try:
            self.time = localtime(self.time)
        except:
            pass
        super().save(*args,**kwargs)

class WaterReading(models.Model):
    date = models.DateField(default=now,blank=True)
    time = models.TimeField(default=now,blank=True)
    site = models.ForeignKey(Site,on_delete=models.SET_NULL,null=True)
    box = models.ForeignKey(Box,on_delete=models.SET_NULL,null=True)
    tank = models.ForeignKey(Tank,on_delete=models.SET_NULL,null=True)
    activity = models.ForeignKey(Activity,on_delete=models.SET_NULL,null=True)
    prev_ph = models.FloatField(blank=True,null=True)
    current_ph = models.FloatField(blank=True,null=True)
    prev_ec = models.FloatField(blank=True,null=True)
    current_ec = models.FloatField(blank=True,null=True)
    acid_used_ml = models.FloatField(blank=True,null=True)
    acid_type = models.ForeignKey(Acid,on_delete=models.SET_NULL,null=True)
    nutrient_used_ml = models.FloatField(blank=True,null=True)
    nutrient_type = models.ForeignKey(Nutrient,on_delete=models.SET_NULL,null=True)
    water_level_liters = models.FloatField(blank=True,null=True)
    staff = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        try:
            return str(self.date) + ' | ' + str(self.time) + ' | ' + self.box.name
        except:
            return 'Missing Values'

    def get_model_type(self):
        return "WATER READING"

    def save(self,*args,**kwargs):
        try:
            self.time = localtime(self.time)
        except:
            pass
        super().save(*args,**kwargs)

class WeightCategory(models.Model):
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.category

class CustomerType(models.Model):
    custom_type = models.CharField(max_length=100)

    def __str__(self):
        return self.custom_type


class PackagedBy(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ProductName(models.Model):
    name = models.CharField(max_length=100)


    def __str__(self):
        return self.name

class CustomerName(models.Model):
    name = models.CharField(max_length=100)


    def __str__(self):
        return self.name
    


class PackingLog(models.Model):

    time = models.DateTimeField(auto_now_add=True)
    date_harvested = models.DateField(auto_now_add=False, null=True, blank=False, verbose_name = 'Date Harvested' )
    date_packaged = models.DateField(auto_now_add=False, null=True, blank=False, verbose_name = 'Date Packaged')
    custom_name = models.ForeignKey(CustomerName, on_delete=models.CASCADE, verbose_name='Customer Name', blank=False)
    prod_name = models.ForeignKey(ProductName, on_delete = models.SET_NULL, null=True, blank=False, verbose_name = 'Product Name')
    no_of_packs = models.PositiveIntegerField(verbose_name='Number of Packs', blank=False, null=True)
    packaged_by = models.ForeignKey(PackagedBy,on_delete=models.CASCADE , null=True, blank=False, verbose_name = 'Packaged By')

    def __str__(self):
        return self.custom_name



class ProductLog(models.Model):
    prod_name = models.ForeignKey(ProductName, on_delete = models.SET_NULL, related_name="names", null=True, blank=True)
    no_of_packs = models.PositiveIntegerField(verbose_name='Number of Packs', blank=True, null=True)
    packaged_by = models.ManyToManyField(PackagedBy, blank=True)

class DeliveryData(models.Model) :
    delivery_date = models.CharField(max_length=100)
    order_no = models.CharField(max_length=100)
    f_name = models.CharField(max_length=100)
    l_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    mop = models.CharField(max_length=100)
    delivery_fee =  models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    discount_code = models.CharField(max_length=100)
    total_price =  models.CharField(max_length=100)
    products = models.CharField(max_length=100)
    prod_weight = models.FloatField()
    prod_qty = models.CharField(max_length=100)
    prod_price =  models.CharField(max_length=100)
    order_sum = models.CharField(max_length=500)
    total_weight = models.DecimalField(max_digits=10, decimal_places=0)
    order = models.CharField(max_length=100)
