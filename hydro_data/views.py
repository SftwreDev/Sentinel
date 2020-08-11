# IMPORT CLASS BASED VIEWS

from django.views.generic import TemplateView, CreateView, DetailView, ListView, RedirectView, UpdateView, DeleteView

# OTHER IMPORTS

import csv, io
from django.shortcuts import render
from django.contrib.auth import login, logout
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.db import IntegrityError
from django.db.models import Q,F
import datetime as dt
import django.apps

# IMPORT FORMS AND MODELS

from . import forms, models
from . models import PackingLog
from .forms import PackingLogForm, WeightCategoryForm, PackingLogFormset
# GET USER MODEL

from django.contrib.auth import get_user_model
User = get_user_model()
############ BOOTSTRAP MODAL ###################

from bootstrap_modal_forms.generic import (
    BSModalCreateView,
)
from .forms import WeightCategoryModal, WeightCategoryForm
#################################################
##########################################################
#############      DECORATORS                #############
##########################################################

from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test,login_required



# SUPERUSER CHECKER
def superuser_required():
    def wrapper(wrapped):
        class WrappedClass(UserPassesTestMixin, wrapped):
            def test_func(self):
                return self.request.user.is_superuser

        return WrappedClass
    return wrapper

##########################################################
#############      SPECIAL FUNCTIONS         #############
##########################################################

def time_passed_calculator(duration_in_s):
    if duration_in_s >= 31536000:
        t = round(divmod(duration_in_s, 31536000)[0])
        if t == 1:
            time_passed = str(t) + ' year'
        else:
            time_passed = str(t) + ' years'
    elif duration_in_s < 31536000 and duration_in_s >= 86400:
        t = round(divmod(duration_in_s, 86400)[0])
        if t == 1:
            time_passed = str(t) + ' day'
        else:
            time_passed = str(t) + ' days'
    elif duration_in_s < 86400 and duration_in_s >= 3600:
        t = round(divmod(duration_in_s, 3600)[0])
        if t == 1:
            time_passed = str(t) + ' hour'
        else:
            time_passed = str(t) + ' hours'
    elif duration_in_s < 3600 and duration_in_s >= 60:
        t = round(divmod(duration_in_s, 60)[0])
        if t == 1:
            time_passed = str(t) + ' minute'
        else:
            time_passed = str(t) + ' minutes'
    else:
        if duration_in_s == 1:
            time_passed = str(round(duration_in_s)) + ' second'
        else:
            time_passed = str(round(duration_in_s)) + ' seconds'
    return time_passed

##########################################################
#############      TEMPLATE VIEWS            #############
##########################################################

class HomePage(TemplateView):
    template_name = 'index.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Home'
        return context

class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("login")
    template_name = "signup.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Sign Up'
        return context

class TestPage(TemplateView):
    template_name = 'test.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Signed in'
        return context

class ThanksPage(TemplateView):
    template_name = 'thanks.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Thanks'
        return context

@superuser_required()
class ItemsPage(LoginRequiredMixin, TemplateView):
    template_name = 'hydro_data/items.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        produce_types = models.ProduceType.objects.all()
        acids = models.Acid.objects.all()
        nutrients = models.Nutrient.objects.all()
        activities = models.Activity.objects.all()
        growmediums = models.GrowMedium.objects.all()
        trays = models.Tray.objects.all()
        context['produce_types'] = produce_types
        context['acids'] = acids
        context['nutrients'] = nutrients
        context['activities'] = activities
        context['growmediums'] = growmediums
        context['trays'] = trays
        context['page_title'] = 'Items'
        return context

@superuser_required()
class BatchesPage(LoginRequiredMixin, TemplateView):
    template_name = 'hydro_data/batches.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        return context

##########################################################
#############      CREATE CLASS BASED VIEWS  #############
##########################################################

@superuser_required()
class SiteForm(LoginRequiredMixin, CreateView):
    form_class = forms.SiteForm
    success_url = reverse_lazy("home")
    template_name = "hydro_data/create_site.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Create Site'
        return context

class BatchForm(LoginRequiredMixin, CreateView):
    form_class = forms.BatchForm
    success_url = reverse_lazy("home")
    template_name = "hydro_data/create_batch.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Start Batch'
        return context

@superuser_required()
class AirReadingForm(LoginRequiredMixin, CreateView):
    form_class = forms.AirReadingDataForm
    success_url = reverse_lazy("home")
    template_name = "hydro_data/create_airreading.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Create Air Reading'
        return context

##########################################################
#############      CREATE FUNCTION VIEWS     #############
##########################################################

@user_passes_test(lambda u: u.is_superuser)
def create_box_with_racks(request):
    template_name = 'hydro_data/create_box_with_racks.html'
    if request.method == 'GET':
        boxform = forms.BoxModelForm(request.GET or None)
        formset = forms.RackFormset(queryset=models.Rack.objects.none())
    elif request.method == 'POST':
        boxform = forms.BoxModelForm(request.POST)
        formset = forms.RackFormset(request.POST)
        if boxform.is_valid() and formset.is_valid():
            box = boxform.save()
            for form in formset:
                rack = form.save(commit=False)
                rack.box = box
                rack.save()
                boxrack, created = models.BoxRack.objects.get_or_create(box=box,rack=rack)
                if created: print(f'Created connection between {box} and {rack}')
                else:  print(f'Connection between {box} and {rack} already present')

            return HttpResponseRedirect(reverse('home'))
    return render(request, template_name, {
        'page_title': 'Create Box & Racks',
        'boxform': boxform,
        'formset': formset,
    })

@user_passes_test(lambda u: u.is_superuser)
def create_producetype(request):
    template_name = 'hydro_data/create_producetype.html'
    if request.method == 'GET':
        formset = forms.ProduceTypeFormset(queryset=models.ProduceType.objects.none())
    elif request.method == 'POST':
        formset = forms.ProduceTypeFormset(request.POST)
        if formset.is_valid():
            for form in formset:
                name = form.cleaned_data['name']
                variety = form.cleaned_data['variety']
                seed_brand = form.cleaned_data['seed_brand']
                producetype = models.ProduceType.objects.create(
                    name=name,
                    variety=variety,
                    seed_brand=seed_brand
                    )

            return HttpResponseRedirect(reverse('hydro_data:produce_type_list'))
    return render(request, template_name, {
        'page_title': 'Create Produce Type',
        'formset': formset,
    })

@user_passes_test(lambda u: u.is_superuser)
def create_location(request):
    template_name = 'hydro_data/create_location.html'
    if request.method == 'GET':
        rackform = forms.ChooseSiteBoxRackForm()
        formset = forms.LocationFormset(queryset=models.Location.objects.none())
    elif request.method == 'POST':
        rackform = forms.ChooseSiteBoxRackForm(request.POST)
        formset = forms.LocationFormset(request.POST)
        if rackform.is_valid() and formset.is_valid():
            site = rackform.cleaned_data['site']
            box = rackform.cleaned_data['box']
            rack = rackform.cleaned_data['rack']
            for form in formset:
                name = form.cleaned_data['name']
                x_cor = form.cleaned_data['x_cor']
                y_cor = form.cleaned_data['y_cor']
                location, created = models.Location.objects.get_or_create(rack=rack,name=name)
                if x_cor or y_cor:
                    if x_cor:
                        location.x_cor = x_cor
                    if y_cor:
                        location.y_cor = y_cor
                    location.save()
                if created: print(f'Created location {name} for rack {rack}')
                else:  print(f'Location {name} already present in {rack}')
                racklocation, rlcreated = models.RackLocation.objects.get_or_create(rack=rack,location=location)
                if rlcreated: print(f'Created connection between {rack} and {location}')
                else:  print(f'Connection between {rack} and {location} already present')
            return HttpResponseRedirect(reverse('home'))
    return render(request, template_name, {
        'page_title': 'Create SQM ID',
        'rackform': rackform,
        'formset': formset,
    })

@user_passes_test(lambda u: u.is_superuser)
def create_acid(request):
    template_name = 'hydro_data/create_acid.html'
    if request.method == 'GET':
        formset = forms.AcidFormset(queryset=models.Acid.objects.none())
    elif request.method == 'POST':
        formset = forms.AcidFormset(request.POST)
        if formset.is_valid():
            for form in formset:
                name = form.cleaned_data['name']
                acid, created = models.Acid.objects.get_or_create(name=name)
                if created: print(f'Created {name} as acid')
                else:  print(f'Acid {name} already present')

            return HttpResponseRedirect(reverse('hydro_data:acid_list'))
    return render(request, template_name, {
        'page_title': 'Create Acid',
        'formset': formset,
    })

@user_passes_test(lambda u: u.is_superuser)
def create_nutrient(request):
    template_name = 'hydro_data/create_nutrient.html'
    if request.method == 'GET':
        formset = forms.NutrientFormset(queryset=models.Nutrient.objects.none())
    elif request.method == 'POST':
        formset = forms.NutrientFormset(request.POST)
        if formset.is_valid():
            for form in formset:
                name = form.cleaned_data['name']
                nutrient, created = models.Nutrient.objects.get_or_create(name=name)
                if created: print(f'Created {name} as nutrient')
                else:  print(f'Nutrient {name} already present')

            return HttpResponseRedirect(reverse('hydro_data:nutrient_list'))
    return render(request, template_name, {
        'page_title': 'Create Nutrient',
        'formset': formset,
    })

@user_passes_test(lambda u: u.is_superuser)
def create_activity(request):
    template_name = 'hydro_data/create_activity.html'
    if request.method == 'GET':
        formset = forms.ActivityFormset(queryset=models.Activity.objects.none())
    elif request.method == 'POST':
        formset = forms.ActivityFormset(request.POST)
        if formset.is_valid():
            for form in formset:
                name = form.cleaned_data['name']
                producetype, created = models.Activity.objects.get_or_create(name=name)
                if created: print(f'Created {name} as activity')
                else:  print(f'Activity {name} already present')

            return HttpResponseRedirect(reverse('hydro_data:activity_list'))
    return render(request, template_name, {
        'page_title': 'Create Activity',
        'formset': formset,
    })

@user_passes_test(lambda u: u.is_superuser)
def create_growmedium(request):
    template_name = 'hydro_data/create_growmedium.html'
    if request.method == 'GET':
        formset = forms.GrowMediumFormset(queryset=models.GrowMedium.objects.none())
    elif request.method == 'POST':
        formset = forms.GrowMediumFormset(request.POST)
        if formset.is_valid():
            for form in formset:
                name = form.cleaned_data['name']
                growmedium, created = models.GrowMedium.objects.get_or_create(name=name)
                if created: print(f'Created {name} as grow medium')
                else:  print(f'Grow medium {name} already present')

            return HttpResponseRedirect(reverse('hydro_data:growmedium_list'))
    return render(request, template_name, {
        'page_title': 'Create Grow Medium',
        'formset': formset,
    })

@user_passes_test(lambda u: u.is_superuser)
def create_tray(request):
    template_name = 'hydro_data/create_tray.html'
    if request.method == 'GET':
        formset = forms.TrayFormset(queryset=models.Tray.objects.none())
    elif request.method == 'POST':
        formset = forms.TrayFormset(request.POST)
        if formset.is_valid():
            for form in formset:
                name = form.cleaned_data['name']
                tray, created = models.Tray.objects.get_or_create(name=name)
                if created: print(f'Created {name} as tray')
                else:  print(f'Tray {name} already present')

            return HttpResponseRedirect(reverse('hydro_data:tray_list'))
    return render(request, template_name, {
        'page_title': 'Create Tray',
        'formset': formset,
    })

@user_passes_test(lambda u: u.is_superuser)
def create_tank(request):
    template_name = 'hydro_data/create_tank.html'
    if request.method == 'GET':
        boxform = forms.ChooseSiteBoxForm()
        formset = forms.TankFormset(queryset=models.Tank.objects.none())
    elif request.method == 'POST':
        boxform = forms.ChooseSiteBoxForm(request.POST)
        formset = forms.TankFormset(request.POST)
        if boxform.is_valid() and formset.is_valid():
            site = boxform.cleaned_data['site']
            box = boxform.cleaned_data['box']
            for form in formset:
                name = form.cleaned_data['name']
                tank, created = models.Tank.objects.get_or_create(box=box,name=name)
                if created: print(f'Created tank {name} for box {box}')
                else:  print(f'Tank {name} already present in {box}')
            return HttpResponseRedirect(reverse('home'))
    return render(request, template_name, {
        'page_title': 'Create Tank',
        'boxform': boxform,
        'formset': formset,
    })

@login_required
def create_plantingdata(request):
    template_name = 'hydro_data/create_plantingdata.html'
    if request.method == 'GET':
        plantingdataform = forms.PlantingDataForm()
    elif request.method == 'POST':
        plantingdataform = forms.PlantingDataForm(request.POST)
        if plantingdataform.is_valid():
            plantingdata = plantingdataform.cleaned_data
            site = plantingdata['site']
            box = plantingdata['box']
            rack = plantingdata['rack']
            batch = plantingdata['seedling_batch_no']
            growmedium = plantingdata['growmedium']
            tray = plantingdata['tray']
            produce_type = plantingdata['produce_type']
            locations = models.Location.objects.filter(rack=rack)
            for loc in locations:
                plantdata = models.PlantingData.objects.create(
                    site=site,
                    box=box,
                    rack=rack,
                    square_meter_id=loc,
                    seedling_batch_no=batch,
                    growmedium=growmedium,
                    tray=tray,
                    produce_type=produce_type,
                    staff=request.user
                )
                loc.plant()
            return HttpResponseRedirect(reverse('home'))
    return render(request, template_name, {
        'page_title': 'Create Seedling Batch',
        'plantingdataform': plantingdataform,
    })

@login_required
def create_harvestdata(request):
    template_name = 'hydro_data/create_harvestdata.html'
    if request.method == 'GET':
        harvestdataform = forms.HarvestDataForm()
        formset = forms.HarvestDataFormset(queryset=models.HarvestData.objects.none())
    elif request.method == 'POST':
        harvestdataform = forms.HarvestDataForm(request.POST)
        formset = forms.HarvestDataFormset(request.POST)
        if harvestdataform.is_valid() and formset.is_valid():
            harvestdata = harvestdataform.cleaned_data
            site = harvestdata['site']
            box = harvestdata['box']
            rack = harvestdata['rack']
            batch = harvestdata['seedling_batch_no']
            for form in formset:
                harvest = form.cleaned_data
                sqm_id = form.cleaned_data['square_meter_id']
                weight = form.cleaned_data['harvest_weight_kg']
                no_of_heads = form.cleaned_data['no_of_heads']
                harvestdata = models.HarvestData.objects.create(
                    site=site,
                    box=box,
                    rack=rack,
                    square_meter_id=sqm_id,
                    seedling_batch_no=batch,
                    harvest_weight_kg=weight,
                    no_of_heads=no_of_heads,
                    staff=request.user
                )
                sqm_id.harvest()
            return HttpResponseRedirect(reverse('home'))
    return render(request, template_name, {
        'page_title': 'Create Harvest Data',
        'harvestdataform': harvestdataform,
        'formset': formset,
    })

@user_passes_test(lambda u: u.is_superuser)
def create_lightreading(request):
    template_name = 'hydro_data/create_lightreading.html'
    if request.method == 'GET':
        lightreadingdataform = forms.LightReadingDataForm()
        formset = forms.LightReadingDataFormset(queryset=models.LightReading.objects.none())
    elif request.method == 'POST':
        lightreadingdataform = forms.HarvestDataForm(request.POST)
        formset = forms.LightReadingDataFormset(request.POST)
        if lightreadingdataform.is_valid() and formset.is_valid():
            lightreadingdata = lightreadingdataform.cleaned_data
            site = lightreadingdata['site']
            box = lightreadingdata['box']
            rack = lightreadingdata['rack']
            for form in formset:
                print('Creating new light reading')
                lightreading = form.cleaned_data
                sqm_id = lightreading['square_meter_id']
                par_reading = lightreading['par_reading']
                lreading = models.LightReading.objects.create(
                    site=site,
                    box=box,
                    rack=rack,
                    square_meter_id=sqm_id,
                    par_reading=par_reading,
                    staff=request.user
                )
            return HttpResponseRedirect(reverse('home'))
    return render(request, template_name, {
        'page_title': 'Create Light Reading',
        'lightreadingdataform': lightreadingdataform,
        'formset': formset,
    })

@user_passes_test(lambda u: u.is_superuser)
def create_waterreading(request):
    template_name = 'hydro_data/create_waterreading.html'
    if request.method == 'GET':
        waterreadingdataform = forms.WaterReadingDataForm()
        formset = forms.WaterReadingDataFormset(queryset=models.WaterReading.objects.none())
    elif request.method == 'POST':
        waterreadingdataform = forms.WaterReadingDataForm(request.POST)
        formset = forms.WaterReadingDataFormset(request.POST)
        if waterreadingdataform.is_valid() and formset.is_valid():
            waterreadingdata = waterreadingdataform.cleaned_data
            site = waterreadingdata['site']
            box = waterreadingdata['box']
            for form in formset:
                waterreading = form.cleaned_data
                tank = waterreading['tank']
                activity = waterreading['activity']
                prev_ph = waterreading['prev_ph']
                current_ph = waterreading['current_ph']
                prev_ec = waterreading['prev_ec']
                current_ec = waterreading['current_ec']
                acid_used_ml = waterreading['acid_used_ml']
                acid_type = waterreading['acid_type']
                nutrient_used_ml = waterreading['nutrient_used_ml']
                nutrient_type = waterreading['nutrient_type']
                water_level_liters = waterreading['water_level_liters']
                wreading = models.WaterReading.objects.create(
                    site=site,
                    box=box,
                    tank = tank,
                    activity = activity,
                    prev_ph = prev_ph,
                    current_ph = current_ph,
                    prev_ec = prev_ec,
                    current_ec = current_ec,
                    acid_used_ml = acid_used_ml,
                    acid_type = acid_type,
                    nutrient_used_ml = nutrient_used_ml,
                    nutrient_type = nutrient_type,
                    water_level_liters = water_level_liters,
                    staff=request.user
                )
            return HttpResponseRedirect(reverse('home'))
    return render(request, template_name, {
        'page_title': 'Create Water Reading',
        'waterreadingdataform': waterreadingdataform,
        'formset': formset,
    })

##########################################################
#############      ADD FUNCTION VIEWS        #############
###########similar to CREATEVIEW but modified#############
##########################################################

@user_passes_test(lambda u: u.is_superuser)
def add_rack(request,**kwargs):
    template_name = 'hydro_data/add_racks.html'
    instance = get_object_or_404(models.Box,slug=kwargs['slug'])

    if request.method == 'GET':
        formset = forms.RackFormset(queryset=models.Rack.objects.none())
    elif request.method == 'POST':
        formset = forms.RackFormset(request.POST)
        if formset.is_valid():
            for form in formset:
                rack = form.save(commit=False)
                rack.box = instance
                rack.save()
                boxrack, created = models.BoxRack.objects.get_or_create(box=instance,rack=rack)
                if created: print(f"Created connection between {instance} and {rack}")
                else:  print(f"Connection between {instance} and {rack} already present")

            return HttpResponseRedirect(reverse('hydro_data:rack_tank_per_box',kwargs={'slug': instance.slug}))
    return render(request, template_name, {
        'page_title': 'Add Rack',
        'box': instance,
        'formset': formset,
    })

@user_passes_test(lambda u: u.is_superuser)
def add_tank(request,**kwargs):
    template_name = 'hydro_data/add_tanks.html'
    instance = get_object_or_404(models.Box,slug=kwargs['slug'])

    if request.method == 'GET':
        formset = forms.TankFormset(queryset=models.Tank.objects.none())
    elif request.method == 'POST':
        formset = forms.TankFormset(request.POST)
        if formset.is_valid():
            for form in formset:
                tank = form.save(commit=False)
                tank.box = instance
                tank.save()

            return HttpResponseRedirect(reverse('hydro_data:rack_tank_per_box',kwargs={'slug': instance.slug}))
    return render(request, template_name, {
        'page_title': 'Add Tank',
        'box': instance,
        'formset': formset,
    })

@user_passes_test(lambda u: u.is_superuser)
def add_location(request,**kwargs):
    template_name = 'hydro_data/add_locations.html'
    instance = get_object_or_404(models.Rack,box__slug=kwargs['boxslug'],slug=kwargs['slug'])

    if request.method == 'GET':
        formset = forms.LocationFormset(queryset=models.Location.objects.none())
    elif request.method == 'POST':
        formset = forms.LocationFormset(request.POST)
        if formset.is_valid():
            rack = instance
            for form in formset:
                name = form.cleaned_data['name']
                x_cor = form.cleaned_data['x_cor']
                y_cor = form.cleaned_data['y_cor']
                is_open = form.cleaned_data['is_open']
                location, created = models.Location.objects.get_or_create(rack=rack,name=name)
                if x_cor or y_cor:
                    if x_cor:
                        location.x_cor = x_cor
                    if y_cor:
                        location.y_cor = y_cor
                    location.save()
                if is_open:
                    if is_open == '1':
                        location.harvest()
                    else:   location.plant()
                    location.save()
                if created: print(f'Created location {name} for rack {rack}')
                else:  print(f'Location {name} already present in {rack}')
                racklocation, rlcreated = models.RackLocation.objects.get_or_create(rack=rack,location=location)
                if rlcreated: print(f'Created connection between {rack} and {location}')
                else:  print(f'Connection between {rack} and {location} already present')
            return HttpResponseRedirect(reverse('hydro_data:loc_per_rack',kwargs={'boxslug':instance.box.slug,'rackslug': instance.slug}))
    return render(request, template_name, {
        'page_title': 'Add SQM ID',
        'rack': instance,
        'formset': formset,
    })

@login_required
def add_seedlingbatch(request,**kwargs):
    template_name = 'hydro_data/add_seedlingbatch.html'
    instance = get_object_or_404(models.Rack,pk=kwargs['pk'])

    if request.method == 'GET':
        batchform = forms.BatchForm()
        form = forms.PlantingDataBatchForm()
    elif request.method == 'POST':
        batchform = forms.BatchForm(request.POST)
        form = forms.PlantingDataBatchForm(request.POST)
        if batchform.is_valid() and form.is_valid():
            seedling_batch, created = models.Batch.objects.get_or_create(num=batchform.cleaned_data['num'])
            if created:print(f'New batch #{batchform.cleaned_data["num"]}')
            else: print('Batch exists')
            site = instance.box.site
            box = instance.box
            rack = instance
            growmedium = form.cleaned_data['growmedium']
            tray = form.cleaned_data['tray']
            produce_type = form.cleaned_data['produce_type']
            locations = models.Location.objects.filter(rack=rack)
            for loc in locations:
                preading = models.PlantingData.objects.create(
                    site=site,
                    box=box,
                    rack=rack,
                    square_meter_id=loc,
                    seedling_batch_no=seedling_batch,
                    growmedium=growmedium,
                    tray=tray,
                    produce_type=produce_type,
                    staff=request.user
                )
                loc.plant()
            return HttpResponseRedirect(reverse('hydro_data:rack_tank_per_box',kwargs={'slug':box.slug}))
    return render(request, template_name, {
        'page_title': f"Add Batch for Rack {instance.name}",
        'rack': instance,
        'batchform': batchform,
        'form': form,
    })

@login_required
def add_transplantbatch(request,**kwargs):
    template_name = 'hydro_data/add_transplantbatch.html'
    instance = get_object_or_404(models.Rack,pk=kwargs['pk'])
    locations = models.Location.objects.filter(rack=instance)

    if request.method == 'GET':
        transplantform = forms.TransplantBatchForm()
    elif request.method == 'POST':
        transplantform = forms.TransplantBatchForm(request.POST)
        if transplantform.is_valid():
            batch = transplantform.cleaned_data['seedling_batch_no']
            new_rack = transplantform.cleaned_data['rack']
            new_box = transplantform.cleaned_data['box']
            site = new_box.site
            new_locations = models.Location.objects.filter(rack=new_rack)
            for loc in locations:
                if loc.is_open == '0':
                    try:
                        treading = models.TransplantData.objects.create(
                            site=site,
                            box=new_box,
                            rack=new_rack,
                            square_meter_id=models.Location.objects.get(rack=new_rack,name=loc.name),
                            seedling_batch_no=batch,
                            staff=request.user
                        )
                        models.Location.objects.get(rack=new_rack,name=loc.name).put_transplant()
                        loc.transplant()
                    except:
                        print("Can't transplant")
            return HttpResponseRedirect(reverse('hydro_data:rack_tank_per_box',kwargs={'slug':instance.box.slug}))
    return render(request, template_name, {
        'page_title': f"Transplant Batch for Rack {instance.name}",
        'rack': instance,
        'transplantform': transplantform,
    })

@user_passes_test(lambda u: u.is_superuser)
def add_seedlingwastage(request,**kwargs):
    template_name = 'hydro_data/add_seedlingwastage.html'
    instance = get_object_or_404(models.Rack,pk=kwargs['pk'])

    if request.method == 'GET':
        seedlingwastagedataform = forms.SeedlingWastageDataForm()
        formset = forms.SeedlingWastageDataFormset(queryset=models.SeedlingWastageData.objects.none())
    elif request.method == 'POST':
        seedlingwastagedataform = forms.SeedlingWastageDataForm(request.POST)
        formset = forms.SeedlingWastageDataFormset(request.POST)
        if seedlingwastagedataform.is_valid() and formset.is_valid():
            seedlingwastagedata = seedlingwastagedataform.cleaned_data
            batch = seedlingwastagedata['seedling_batch_no']
            reason = seedlingwastagedata['wastage_reason']
            rack = instance
            box = rack.box
            site = box.site
            for form in formset:
                loc = form.cleaned_data['square_meter_id']
                swastage = models.SeedlingWastageData.objects.create(
                    site=site,
                    box=box,
                    rack = rack,
                    square_meter_id=loc,
                    seedling_batch_no=batch,
                    wastage_reason=reason,
                    staff=request.user
                )
                loc.wasted()
            return HttpResponseRedirect(reverse('hydro_data:rack_tank_per_box',kwargs={'slug':box.slug}))
    return render(request, template_name, {
        'page_title': 'Add Seedling Wastage',
        'rack': instance,
        'seedlingwastagedataform': seedlingwastagedataform,
        'formset': formset,
    })

@user_passes_test(lambda u: u.is_superuser)
def add_wastagedata(request,**kwargs):
    template_name = 'hydro_data/add_wastagedata.html'
    instance = get_object_or_404(models.Rack,pk=kwargs['pk'])

    if request.method == 'GET':
        wastagedataform = forms.WastageDataForm()
        formset = forms.WastageDataFormset(queryset=models.SeedlingWastageData.objects.none())
    elif request.method == 'POST':
        wastagedataform = forms.WastageDataForm(request.POST)
        formset = forms.WastageDataFormset(request.POST)
        if wastagedataform.is_valid() and formset.is_valid():
            wastagedata = wastagedataform.cleaned_data
            batch = wastagedata['seedling_batch_no']
            reason = wastagedata['wastage_reason']
            rack = instance
            box = rack.box
            site = box.site
            for form in formset:
                loc = form.cleaned_data['square_meter_id']
                wastage_kg = form.cleaned_data['wastage_kg']
                wastage = models.WastageData.objects.create(
                    site=site,
                    box=box,
                    rack = rack,
                    square_meter_id=loc,
                    wastage_kg=wastage_kg,
                    seedling_batch_no=batch,
                    wastage_reason=reason,
                    staff=request.user
                )
                loc.wasted()
            return HttpResponseRedirect(reverse('hydro_data:rack_tank_per_box',kwargs={'slug':box.slug}))
    return render(request, template_name, {
        'page_title': 'Add Seedling Wastage',
        'rack': instance,
        'wastagedataform': wastagedataform,
        'formset': formset,
    })

##########################################################
#############     ADD-FOR FUNCTION VIEWS     #############
###########similar to CREATEVIEW but modified#############
##########################################################

@user_passes_test(lambda u: u.is_superuser)
def add_waterconsumption_for_site(request,**kwargs):
    template_name = 'hydro_data/add_waterconsumption_for_site.html'
    instance = get_object_or_404(models.Site,slug=kwargs['slug'])

    if request.method == 'GET':
        form = forms.WaterConsumptionForSiteDataForm()
    elif request.method == 'POST':
        form = forms.WaterConsumptionForSiteDataForm(request.POST)
        if form.is_valid():
            site = instance
            wcdata = models.WaterConsumption.objects.create(
                site=site,
                water_reading=form.cleaned_data['water_reading'],
                staff=request.user
                )
            return HttpResponseRedirect(reverse('hydro_data:box_list',kwargs={'slug': instance.slug}))
    return render(request, template_name, {
        'page_title': f"Add Water Consumption for {instance.name}",
        'site': instance,
        'form': form,
    })

@user_passes_test(lambda u: u.is_superuser)
def add_energyconsumption_for_box(request,**kwargs):
    template_name = 'hydro_data/add_energyconsumption_for_box.html'
    instance = get_object_or_404(models.Box,slug=kwargs['slug'])

    if request.method == 'GET':
        form = forms.EnergyConsumptionForBoxDataForm()
    elif request.method == 'POST':
        form = forms.EnergyConsumptionForBoxDataForm(request.POST)
        if form.is_valid():
            ecdata = models.EnergyConsumption.objects.create(
                box=instance,
                electrical_reading=form.cleaned_data['electrical_reading'],
                staff=request.user
                )
            return HttpResponseRedirect(reverse('hydro_data:rack_tank_per_box',kwargs={'slug': instance.slug}))
    return render(request, template_name, {
        'page_title': f"Add Energy Consumption for {instance.name}",
        'box': instance,
        'form': form,
    })

@login_required
def add_plantdata_for_loc(request,**kwargs):
    template_name = 'hydro_data/add_plantingdata_for_loc.html'
    instance = get_object_or_404(models.Location,pk=kwargs['pk'])

    if request.method == 'GET':
        batchform = forms.ChooseBatchForm()
        form = forms.PlantingDataForLocForm()
    elif request.method == 'POST':
        batchform = forms.ChooseBatchForm(request.POST)
        form = forms.PlantingDataForLocForm(request.POST)
        if batchform.is_valid() and form.is_valid():
            batch = batchform.cleaned_data['batch']
            site = instance.rack.box.site
            box = instance.rack.box
            rack = instance.rack
            pdata = models.PlantingData.objects.create(
                site=site,
                box=box,
                rack=rack,
                seedling_batch_no=batch,
                square_meter_id=instance,
                growmedium=form.cleaned_data['growmedium'],
                tray=form.cleaned_data['tray'],
                produce_type=form.cleaned_data['produce_type'],
                staff=request.user
                )
            instance.plant()
            return HttpResponseRedirect(reverse('hydro_data:single_location',kwargs={'boxslug':box.slug,'rackslug':rack.slug,'slug': instance.slug}))
    return render(request, template_name, {
        'page_title': f"Add Planting Data for SQM ID {instance.name}",
        'location': instance,
        'batchform': batchform,
        'form': form,
    })

@login_required
def add_harvestdata_for_loc(request,**kwargs):
    template_name = 'hydro_data/add_harvestdata_for_loc.html'
    instance = get_object_or_404(models.Location,pk=kwargs['pk'])

    if request.method == 'GET':
        batchform = forms.ChooseBatchForm()
        form = forms.HarvestDataForLocForm()
    elif request.method == 'POST':
        batchform = forms.ChooseBatchForm(request.POST)
        form = forms.HarvestDataForLocForm(request.POST)
        if batchform.is_valid() and form.is_valid():
            batch = batchform.cleaned_data['batch']
            site = instance.rack.box.site
            box = instance.rack.box
            rack = instance.rack
            hdata = models.HarvestData.objects.create(
                site=site,
                box=box,
                rack=rack,
                square_meter_id=instance,
                seedling_batch_no=batch,
                harvest_weight_kg=form.cleaned_data['harvest_weight_kg'],
                wastage_kg=form.cleaned_data['wastage_kg'],
                seedlingdata=models.PlantingData.objects.filter(site=site,box=box,rack=rack).order_by('-pk')[0],
                staff=request.user
                )
            instance.harvest()
            return HttpResponseRedirect(reverse('hydro_data:single_location',kwargs={'boxslug':box.slug,'rackslug':rack.slug,'slug': instance.slug}))
    return render(request, template_name, {
        'page_title': f"Add Harvest Data for SQM ID {instance.name}",
        'location': instance,
        'batchform':batchform,
        'form': form,
    })

@user_passes_test(lambda u: u.is_superuser)
def add_lightdata_for_loc(request,**kwargs):
    template_name = 'hydro_data/add_lightdata_for_loc.html'
    instance = get_object_or_404(models.Location,pk=kwargs['pk'])

    if request.method == 'GET':
        form = forms.LightReadingDataForLocForm()
    elif request.method == 'POST':
        form = forms.LightReadingDataForLocForm(request.POST)
        if form.is_valid():
            box = instance.rack.box
            rack = instance.rack
            ldata = models.LightReading.objects.create(
                box=box,
                rack=rack,
                square_meter_id=instance,
                par_reading=form.cleaned_data['par_reading'],
                staff=request.user
                )
            return HttpResponseRedirect(reverse('hydro_data:single_location',kwargs={'boxslug':box.slug,'rackslug':rack.slug,'slug': instance.slug}))
    return render(request, template_name, {
        'page_title': f"Add Light Reading for SQM ID {instance.name}",
        'location': instance,
        'form': form,
    })

@user_passes_test(lambda u: u.is_superuser)
def add_waterdata_for_tank(request,**kwargs):
    template_name = 'hydro_data/add_waterdata_for_tank.html'
    instance = get_object_or_404(models.Tank,pk=kwargs['pk'])

    if request.method == 'GET':
        form = forms.WaterReadingForTankDataForm()
    elif request.method == 'POST':
        form = forms.WaterReadingForTankDataForm(request.POST)
        if form.is_valid():
            box = instance.box
            tank = instance
            wdata = models.WaterReading.objects.create(
                box=box,
                tank=tank,
                activity=form.cleaned_data['activity'],
                prev_ph=form.cleaned_data['prev_ph'],
                current_ph=form.cleaned_data['current_ph'],
                prev_ec=form.cleaned_data['prev_ec'],
                current_ec=form.cleaned_data['prev_ec'],
                acid_used_ml=form.cleaned_data['acid_used_ml'],
                acid_type=form.cleaned_data['acid_type'],
                nutrient_used_ml=form.cleaned_data['nutrient_used_ml'],
                nutrient_type=form.cleaned_data['nutrient_type'],
                water_level_liters=form.cleaned_data['water_level_liters'],
                staff=request.user
                )
            return HttpResponseRedirect(reverse('hydro_data:single_tank',kwargs={'boxslug':box.slug,'slug': instance.slug}))
    return render(request, template_name, {
        'page_title': f"Add Water Reading for Tank {instance.name}",
        'tank': instance,
        'form': form,
    })

@user_passes_test(lambda u: u.is_superuser)
def add_airdata_for_box(request,**kwargs):
    template_name = 'hydro_data/add_airdata_for_box.html'
    instance = get_object_or_404(models.Box,slug=kwargs['slug'])

    if request.method == 'GET':
        form = forms.AirReadingForBoxDataForm()
    elif request.method == 'POST':
        form = forms.AirReadingForBoxDataForm(request.POST)
        if form.is_valid():
            site = instance.site
            box = instance
            adata = models.AirReading.objects.create(
                site=site,
                box=box,
                current_relative_humidity=form.cleaned_data['current_relative_humidity'],
                current_temp=form.cleaned_data['current_temp'],
                current_co2_level=form.cleaned_data['current_co2_level'],
                staff=request.user
                )
            return HttpResponseRedirect(reverse('hydro_data:rack_tank_per_box',kwargs={'slug': instance.slug}))
    return render(request, template_name, {
        'page_title': f"Add Air Reading for Box {instance.name}",
        'box': instance,
        'form': form,
    })


##########################################################
#############   ADD-MULTIPLE FUNCTION VIEWS  #############
###########similar to CREATEVIEW but modified#############
##########################################################

@login_required
def add_multiple_plantdata(request,**kwargs):
    template_name = 'hydro_data/add_multiple_plantdata.html'
    instance = get_object_or_404(models.Rack,pk=kwargs['pk'])

    if request.method == 'GET':
        formset = forms.PlantingDataFormset(queryset=models.PlantingData.objects.none())
    elif request.method == 'POST':
        formset = forms.PlantingDataFormset(request.POST)
        if formset.is_valid():
            site = instance.box.site
            box = instance.box
            rack = instance
            for form in formset:
                plantdata = form.cleaned_data
                sqm_id = plantdata['square_meter_id']
                growmedium = plantdata['growmedium']
                tray = plantdata['tray']
                produce_type = plantdata['produce_type']
                preading = models.PlantingData.objects.create(
                    site=site,
                    box=box,
                    rack=rack,
                    square_meter_id=sqm_id,
                    growmedium=growmedium,
                    tray=tray,
                    produce_type=produce_type,
                    staff=request.user
                )
                sqm_id.plant()
            return HttpResponseRedirect(reverse('hydro_data:loc_per_rack',kwargs={'boxslug':box.slug,'rackslug':rack.slug}))
    return render(request, template_name, {
        'page_title': f"Add Multiple Planting Data for Rack {instance.name}",
        'rack': instance,
        'formset': formset,
    })

@login_required
def add_multiple_harvestdata(request,**kwargs):
    template_name = 'hydro_data/add_multiple_harvestdata.html'
    instance = get_object_or_404(models.Rack,pk=kwargs['pk'])

    if request.method == 'GET':
        batchform = forms.ChooseBatchForm()
        formset = forms.HarvestDataFormset(queryset=models.HarvestData.objects.none())
    elif request.method == 'POST':
        batchform = forms.ChooseBatchForm(request.POST)
        formset = forms.HarvestDataFormset(request.POST)
        if batchform.is_valid() and formset.is_valid():
            site = instance.box.site
            box = instance.box
            rack = instance
            batch = batchform.cleaned_data['batch']
            for form in formset:
                harvestdata = form.cleaned_data
                sqm_id = harvestdata['square_meter_id']
                harvest_weight_kg = harvestdata['harvest_weight_kg']
                no_of_heads = harvestdata['no_of_heads']
                hreading = models.HarvestData.objects.create(
                    site=site,
                    box=box,
                    rack=rack,
                    square_meter_id=sqm_id,
                    harvest_weight_kg=harvest_weight_kg,
                    seedling_batch_no=batch,
                    no_of_heads=no_of_heads,
                    staff=request.user
                )
                sqm_id.harvest()
            return HttpResponseRedirect(reverse('hydro_data:rack_tank_per_box',kwargs={'slug':box.slug}))
    return render(request, template_name, {
        'page_title': f"Add Multiple Harvest Data for Rack {instance.name}",
        'rack': instance,
        'batchform': batchform,
        'formset': formset,
    })

@user_passes_test(lambda u: u.is_superuser)
def add_multiple_lightreading(request,**kwargs):
    template_name = 'hydro_data/add_multiple_lightreading.html'
    instance = get_object_or_404(models.Rack,pk=kwargs['pk'])

    if request.method == 'GET':
        formset = forms.LightReadingDataFormset(queryset=models.LightReading.objects.none())
    elif request.method == 'POST':
        formset = forms.LightReadingDataFormset(request.POST)
        if formset.is_valid():
            box = instance.box
            rack = instance
            for form in formset:
                lightreading = form.cleaned_data
                sqm_id = lightreading['square_meter_id']
                par_reading = lightreading['par_reading']
                lreading = models.LightReading.objects.create(
                    box=box,
                    rack=rack,
                    square_meter_id=sqm_id,
                    par_reading=par_reading,
                    staff=request.user
                )
            return HttpResponseRedirect(reverse('hydro_data:loc_per_rack',kwargs={'boxslug':box.slug,'rackslug':rack.slug}))
    return render(request, template_name, {
        'page_title': f"Add Multiple Light Reading for Rack {instance.name}",
        'rack': instance,
        'formset': formset,
    })

@user_passes_test(lambda u: u.is_superuser)
def add_multiple_waterreading(request,**kwargs):
    template_name = 'hydro_data/add_multiple_waterreading.html'
    instance = get_object_or_404(models.Box,slug=kwargs['slug'])

    if request.method == 'GET':
        formset = forms.WaterReadingDataFormset(queryset=models.WaterReading.objects.none())
    elif request.method == 'POST':
        formset = forms.WaterReadingDataFormset(request.POST)
        if formset.is_valid():
            box = instance
            for form in formset:
                wdata = models.WaterReading.objects.create(
                    box=box,
                    tank=form.cleaned_data['tank'],
                    activity=form.cleaned_data['activity'],
                    prev_ph=form.cleaned_data['prev_ph'],
                    current_ph=form.cleaned_data['current_ph'],
                    prev_ec=form.cleaned_data['prev_ec'],
                    current_ec=form.cleaned_data['prev_ec'],
                    acid_used_ml=form.cleaned_data['acid_used_ml'],
                    acid_type=form.cleaned_data['acid_type'],
                    nutrient_used_ml=form.cleaned_data['nutrient_used_ml'],
                    nutrient_type=form.cleaned_data['nutrient_type'],
                    water_level_liters=form.cleaned_data['water_level_liters'],
                    staff=request.user
                    )
            return HttpResponseRedirect(reverse('hydro_data:rack_tank_per_box',kwargs={'slug': instance.slug}))
    return render(request, template_name, {
        'page_title': f"Add Multiple Water Reading for Box {instance.name}",
        'box': instance,
        'formset': formset,
    })

##########################################################
#############     LIST CLASS BASED VIEWS     #############
##########################################################

class ListSite(LoginRequiredMixin, ListView):
    model = models.Site
    template_name = 'hydro_data/site_list.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Sites'
        return context

class ListBox(LoginRequiredMixin, ListView):
    model = models.Box

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        site = get_object_or_404(models.Site, slug=self.kwargs['slug'])
        boxes = models.Box.objects.filter(site=site)
        racks = {}
        for box in boxes:
            racks[box] = models.Rack.objects.filter(box=box)
        context['site'] = site
        context['boxes'] = boxes
        context['boxrack'] = racks
        context['page_title'] = 'Boxes'

        box_last_activity_list = {}
        for box in boxes:
            pdata = models.PlantingData.objects.filter(box__id=box.id).order_by('-id')
            hdata = models.HarvestData.objects.filter(box__id=box.id).order_by('-id')
            lreadings = models.LightReading.objects.filter(box__id=box.id).order_by('-id')
            areadings = models.AirReading.objects.filter(box__id=box.id).order_by('-id')
            wreadings = models.WaterReading.objects.filter(box__id=box.id).order_by('-id')
            rdata = list(pdata) + list(hdata) + list(lreadings) + list(areadings) + list(wreadings)
            bactivities = sorted(rdata,key = lambda x: (x.date, x.time), reverse=True)
            if bactivities:
                last_activity = bactivities[0]
                combined = dt.datetime.combine(last_activity.date, last_activity.time)
                duration = dt.datetime.now() - combined
                duration_in_s = duration.total_seconds()
                time_passed = time_passed_calculator(duration_in_s)
            else:
                time_passed = None
            box_last_activity_list[box] = time_passed
        context['box_last_activity_list'] = box_last_activity_list

        waterconsumption = models.WaterConsumption.objects.filter(site=site).order_by('-date','-time')
        context['site_activities'] = waterconsumption
        return context

class ListRackTankPerBox(LoginRequiredMixin, ListView):
    model = models.Rack
    template_name = 'hydro_data/rack_tank_per_box.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        box = get_object_or_404(models.Box, slug=self.kwargs['slug'])
        racks = models.Rack.objects.filter(box=box)
        tanks = models.Tank.objects.filter(box=box)
        rack_with_locs = []
        for rack in racks:
            rack_loc = {}
            locs = models.Location.objects.filter(rack=rack)
            rack_loc[rack] = locs
            rack_with_locs.append(rack_loc)

        context['box'] = box
        context['rack_list'] = rack_with_locs
        context['tank_list'] = tanks

        rack_last_activity_list = {}
        for rack in racks:
            pdata = models.PlantingData.objects.filter(box__id=rack.box.id,rack__id=rack.id).order_by('-id')
            hdata = models.HarvestData.objects.filter(box__id=rack.box.id,rack__id=rack.id).order_by('-id')
            lreadings = models.LightReading.objects.filter(box__id=rack.box.id,rack__id=rack.id).order_by('-id')
            rdata = list(pdata) + list(hdata) + list(lreadings)
            ractivities = sorted(rdata,key = lambda x: (x.date, x.time), reverse=True)
            if ractivities:
                last_activity = ractivities[0]
                combined = dt.datetime.combine(last_activity.date, last_activity.time)
                duration = dt.datetime.now() - combined
                duration_in_s = duration.total_seconds()
                time_passed = time_passed_calculator(duration_in_s)
            else:
                time_passed = None
            rack_last_activity_list[rack] = time_passed

        tank_last_activity_list = {}
        for tank in tanks:
            wreadings = models.WaterReading.objects.filter(box__id=tank.box.id,tank__id=tank.id).order_by('-id')
            if wreadings:
                last_activity = wreadings[0]
                combined = dt.datetime.combine(last_activity.date, last_activity.time)
                duration = dt.datetime.now() - combined
                duration_in_s = duration.total_seconds()
                time_passed = time_passed_calculator(duration_in_s)
            else:
                time_passed = None
            tank_last_activity_list[tank] = time_passed

        airdata = models.AirReading.objects.filter(box=box).order_by('-date','-time')
        waterdata = models.WaterReading.objects.filter(box=box).order_by('-date','-time')
        energyconsumption = models.EnergyConsumption.objects.filter(box=box).order_by('-date','-time')
        context['air_activities'] = airdata
        context['water_activities'] = waterdata
        context['energyconsumption'] = energyconsumption
        context['rack_last_activity_list'] = rack_last_activity_list
        context['tank_last_activity_list'] = tank_last_activity_list
        context['page_title'] = f'Box {box.name}'
        return context

class ListLocPerRack(LoginRequiredMixin, ListView):
    model = models.Location
    template_name = 'hydro_data/sqm_id_per_rack.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        box = get_object_or_404(models.Box,slug=self.kwargs['boxslug'])
        rack = get_object_or_404(models.Rack,box=box,slug=self.kwargs['rackslug'])
        loc_list = models.Location.objects.filter(rack=rack)
        context['rack'] = rack
        context['loc_list'] = loc_list
        last_activity_list = {}
        for location in loc_list:
            pdata = models.PlantingData.objects.filter(square_meter_id__id=location.id).order_by('-id')
            hdata = models.HarvestData.objects.filter(square_meter_id__id=location.id).order_by('-id')
            lreadings = models.LightReading.objects.filter(square_meter_id__id=location.id).order_by('-id')
            tdata = models.TransplantData.objects.filter(square_meter_id__id=location.id).order_by('-id')
            swdata = models.SeedlingWastageData.objects.filter(square_meter_id__id=location.id).order_by('-id')
            wdata = models.WastageData.objects.filter(square_meter_id__id=location.id).order_by('-id')
            ldata = list(pdata) + list(hdata) + list(lreadings) + list(tdata) + list(swdata) + list(wdata)
            lactivities = sorted(ldata,key = lambda x: (x.date, x.time), reverse=True)
            if lactivities:
                last_activity = lactivities[0]
                combined = dt.datetime.combine(last_activity.date, last_activity.time)
                duration = dt.datetime.now() - combined
                duration_in_s = duration.total_seconds()
                time_passed = time_passed_calculator(duration_in_s)
            else:
                time_passed = None
            last_activity_list[location] = time_passed
        plantdata = models.PlantingData.objects.filter(box=box,rack=rack)
        harvestdata = models.HarvestData.objects.filter(box=box,rack=rack)
        light_readings = models.LightReading.objects.filter(box=box,rack=rack)
        transplantdata = models.TransplantData.objects.filter(box=box,rack=rack)
        seedlingswastage = models.SeedlingWastageData.objects.filter(box=box,rack=rack)
        wastage = models.WastageData.objects.filter(box=box,rack=rack)
        data = list(plantdata) + list(harvestdata) + list(light_readings) + list(transplantdata) + list(seedlingswastage) + list(wastage)
        activities = sorted(data,key = lambda x: (x.date, x.time),reverse=True)
        context['activities'] = activities
        context['last_activity_list'] = last_activity_list
        context['page_title'] = f'Rack {rack.name}'
        return context

@superuser_required()
class ListProduceType(LoginRequiredMixin, ListView):
    model = models.ProduceType

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Produce Types'
        return context

@superuser_required()
class ListAcid(LoginRequiredMixin, ListView):
    model = models.Acid

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Acids'
        return context

@superuser_required()
class ListNutrient(LoginRequiredMixin, ListView):
    model = models.Nutrient

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Nutrients'
        return context

@superuser_required()
class ListActivity(LoginRequiredMixin, ListView):
    model = models.Activity

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Activities'
        return context

@superuser_required()
class ListGrowMedium(LoginRequiredMixin, ListView):
    model = models.GrowMedium

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Grow Mediums'
        return context

@superuser_required()
class ListTray(LoginRequiredMixin, ListView):
    model = models.Tray

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Trays'
        return context

##########################################################
#############    DETAIL CLASS BASED VIEWS    #############
##########################################################

class LocationDetail(LoginRequiredMixin, DetailView):
    models.Location

    def get_queryset(self):
        return models.Location.objects.filter(rack__slug=self.kwargs['rackslug'],slug=self.kwargs['slug'])

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        plantdata = models.PlantingData.objects.filter(square_meter_id__id=context['location'].id)
        harvestdata = models.HarvestData.objects.filter(square_meter_id__id=context['location'].id)
        light_readings = models.LightReading.objects.filter(square_meter_id__id=context['location'].id)
        transplantdata = models.TransplantData.objects.filter(square_meter_id__id=context['location'].id)
        seedlingwastage = models.SeedlingWastageData.objects.filter(square_meter_id__id=context['location'].id)
        wastage = models.WastageData.objects.filter(square_meter_id__id=context['location'].id)
        data = list(plantdata) + list(harvestdata) + list(light_readings) + list(transplantdata) + list(seedlingwastage) + list(wastage)
        activities = sorted(data,key = lambda x: (x.date, x.time),reverse=True)
        context['activities'] = activities
        context['page_title'] = f"SQM ID {context['location'].name}"
        return context

class TankDetail(LoginRequiredMixin, DetailView):
    models.Location

    def get_queryset(self):
        return models.Tank.objects.filter(box__slug=self.kwargs['boxslug'],slug=self.kwargs['slug'])

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        box = get_object_or_404(models.Box, slug=self.kwargs['boxslug'])
        tank = get_object_or_404(models.Tank, box=box, slug=self.kwargs['slug'])
        waterdata = models.WaterReading.objects.filter(box=box,tank=tank).order_by('-date','-time')
        context['water_activities'] = waterdata
        context['page_title'] = f'Tank {tank.name}'
        return context

@superuser_required()
class ProduceTypeDetail(LoginRequiredMixin, DetailView):
    model = models.ProduceType

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = context['producetype'].name
        return context

@superuser_required()
class AcidDetail(LoginRequiredMixin, DetailView):
    model = models.Acid

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = context['acid'].name
        return context

@superuser_required()
class NutrientDetail(LoginRequiredMixin, DetailView):
    model = models.Nutrient

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = context['nutrient'].name
        return context

@superuser_required()
class ActivityDetail(LoginRequiredMixin, DetailView):
    model = models.Activity

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = context['activity'].name
        return context

@superuser_required()
class GrowMediumDetail(LoginRequiredMixin, DetailView):
    model = models.GrowMedium

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = context['growmedium'].name
        return context

@superuser_required()
class TrayDetail(LoginRequiredMixin, DetailView):
    model = models.Tray

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = context['tray'].name
        return context

class PlantingDataDetail(LoginRequiredMixin, DetailView):
    model = models.PlantingData

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Planting Data #{context['plantingdata'].pk}"
        return context

class TransplantDataDetail(LoginRequiredMixin, DetailView):
    model = models.TransplantData

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Transplant Data #{context['transplantdata'].pk}"
        return context

class SeedlingWastageDataDetail(LoginRequiredMixin, DetailView):
    model = models.SeedlingWastageData

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Seedling Wastage Data #{context['seedlingwastagedata'].pk}"
        return context

class WastageDataDetail(LoginRequiredMixin, DetailView):
    model = models.WastageData

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Wastage Data #{context['wastagedata'].pk}"
        return context

class HarvestDataDetail(LoginRequiredMixin, DetailView):
    model = models.HarvestData

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Harvest Data #{context['harvestdata'].pk}"
        return context

class LightReadingDetail(LoginRequiredMixin, DetailView):
    model = models.LightReading

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Light Reading #{context['lightreading'].pk}"
        return context

class AirReadingDetail(LoginRequiredMixin, DetailView):
    model = models.AirReading

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Air Reading #{context['airreading'].pk}"
        return context

class WaterReadingDetail(LoginRequiredMixin, DetailView):
    model = models.WaterReading

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Water Reading #{context['waterreading'].pk}"
        return context

##########################################################
############# UPDATE-DELETE CLASS BASED VIEWS#############
##########################################################

@superuser_required()
class SiteUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    form_class = forms.SiteForm
    model = models.Site

    def get_success_url(self):
        view_name = 'hydro_data:box_list'
        return reverse_lazy(view_name, kwargs={'slug': self.kwargs['slug']})

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Edit {context['site'].name}"
        return context

@superuser_required()
class SiteDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Site
    success_url = reverse_lazy('hydro_data:site_list')

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Remove {context['site'].name}"
        return context

@superuser_required()
class BoxUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    form_class = forms.BoxForm
    model = models.Box

    def get_success_url(self):
        view_name = 'hydro_data:rack_tank_per_box'
        return reverse_lazy(view_name, kwargs={'slug': self.kwargs['slug']})

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Edit {context['box'].name}"
        return context

@superuser_required()
class BoxDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Box
    success_url = reverse_lazy('hydro_data:box_list')

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Remove {context['box'].name}"
        return context

@superuser_required()
class RackUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    form_class = forms.RackForm
    model = models.Rack

    def get_success_url(self):
        view_name = 'hydro_data:loc_per_rack'
        rack = models.Rack.objects.get(pk=self.kwargs['pk'])
        return reverse_lazy(view_name, kwargs={'boxslug': self.kwargs['boxslug'],'rackslug': rack.slug})

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Edit {context['rack'].name}"
        return context

@superuser_required()
class RackDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Rack

    def get_success_url(self):
        return reverse_lazy('hydro_data:rack_tank_per_box', kwargs={'slug': self.kwargs['boxslug']})

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Remove {context['rack'].name}"
        return context

@superuser_required()
class TankUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    form_class = forms.TankForm
    model = models.Tank

    def get_success_url(self):
        view_name = 'hydro_data:single_tank'
        tank = models.Tank.objects.get(pk=self.kwargs['pk'])
        return reverse_lazy(view_name, kwargs={'boxslug': self.kwargs['boxslug'],'slug': tank.slug})

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Edit {context['tank'].name}"
        return context

@superuser_required()
class TankDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Tank

    def get_success_url(self):
        return reverse_lazy('hydro_data:rack_tank_per_box', kwargs={'slug': self.kwargs['boxslug']})

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Remove {context['tank'].name}"
        return context

@superuser_required()
class LocationUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    form_class = forms.LocationForm
    model = models.Location

    def get_success_url(self):
        view_name = 'hydro_data:single_location'
        location = models.Location.objects.get(pk=self.kwargs['pk'])
        return reverse_lazy(view_name, kwargs={'boxslug': self.kwargs['boxslug'],'rackslug': self.kwargs['rackslug'],'slug':location.slug})

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Edit {context['location'].name}"
        return context

@superuser_required()
class LocationDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Location

    def get_success_url(self):
        return reverse_lazy('hydro_data:loc_per_rack', kwargs={'boxslug': self.kwargs['boxslug'],'rackslug':self.kwargs['rackslug']})

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Remove {context['location'].name}"
        return context

@superuser_required()
class ProduceTypeUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    form_class = forms.ProduceTypeForm
    model = models.ProduceType

    def get_success_url(self):
        view_name = 'hydro_data:single_produce_type'
        produce_type = models.ProduceType.objects.get(pk=self.kwargs['pk'])
        return reverse_lazy(view_name, kwargs={'slug': produce_type.slug})

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Edit {context['producetype'].name}"
        return context

@superuser_required()
class ProduceTypeDeleteView(LoginRequiredMixin, DeleteView):
    model = models.ProduceType

    def get_success_url(self):
        return reverse_lazy('hydro_data:produce_type_list')

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Remove {context['producetype'].name}"
        return context

@superuser_required()
class AcidUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    form_class = forms.AcidForm
    model = models.Acid

    def get_success_url(self):
        view_name = 'hydro_data:single_acid'
        acid = models.Acid.objects.get(pk=self.kwargs['pk'])
        return reverse_lazy(view_name, kwargs={'slug': acid.slug})

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Edit {context['acid'].name}"
        return context

@superuser_required()
class AcidDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Acid

    def get_success_url(self):
        return reverse_lazy('hydro_data:acid_list')

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Remove {context['acid'].name}"
        return context

@superuser_required()
class NutrientUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    form_class = forms.NutrientForm
    model = models.Nutrient

    def get_success_url(self):
        view_name = 'hydro_data:single_nutrient'
        nutrient = models.Nutrient.objects.get(pk=self.kwargs['pk'])
        return reverse_lazy(view_name, kwargs={'slug': nutrient.slug})

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Edit {context['nutrient'].name}"
        return context

@superuser_required()
class NutrientDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Nutrient

    def get_success_url(self):
        return reverse_lazy('hydro_data:nutrient_list')

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Remove {context['nutrient'].name}"
        return context

@superuser_required()
class ActivityUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    form_class = forms.ActivityForm
    model = models.Activity

    def get_success_url(self):
        view_name = 'hydro_data:single_activity'
        activity = models.Activity.objects.get(pk=self.kwargs['pk'])
        return reverse_lazy(view_name, kwargs={'slug': activity.slug})

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Edit {context['activity'].name}"
        return context

@superuser_required()
class ActivityDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Activity

    def get_success_url(self):
        return reverse_lazy('hydro_data:activity_list')

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Remove {context['activity'].name}"
        return context

@superuser_required()
class GrowMediumUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    form_class = forms.GrowMediumForm
    model = models.GrowMedium

    def get_success_url(self):
        view_name = 'hydro_data:single_growmedium'
        growmedium = models.GrowMedium.objects.get(pk=self.kwargs['pk'])
        return reverse_lazy(view_name, kwargs={'slug': growmedium.slug})

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Edit {context['growmedium'].name}"
        return context

@superuser_required()
class GrowMediumDeleteView(LoginRequiredMixin, DeleteView):
    model = models.GrowMedium

    def get_success_url(self):
        return reverse_lazy('hydro_data:growmedium_list')

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Remove {context['growmedium'].name}"
        return context

@superuser_required()
class TrayUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    form_class = forms.TrayForm
    model = models.Tray

    def get_success_url(self):
        view_name = 'hydro_data:single_tray'
        tray = models.Tray.objects.get(pk=self.kwargs['pk'])
        return reverse_lazy(view_name, kwargs={'slug': tray.slug})

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Edit {context['tray'].name}"
        return context

@superuser_required()
class TrayDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Tray

    def get_success_url(self):
        return reverse_lazy('hydro_data:tray_list')

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Remove {context['tray'].name}"
        return context

@superuser_required()
class PlantingDataUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    form_class = forms.PlantingDataSingleForm
    model = models.PlantingData

    def get_success_url(self):
        view_name = 'hydro_data:single_plantingdata'
        return reverse_lazy(view_name, kwargs={'boxslug':self.kwargs['boxslug'],'rackslug':self.kwargs['rackslug'],'slug':self.kwargs['slug'],'pk': self.kwargs['pk']})

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Edit Planting Data #{context['plantingdata'].pk}"
        return context

@superuser_required()
class PlantingDataDeleteView(LoginRequiredMixin, DeleteView):
    model = models.PlantingData

    def get_success_url(self):
        return reverse_lazy('hydro_data:loc_per_rack',kwargs={'boxslug':self.kwargs['boxslug'],'rackslug':self.kwargs['rackslug']})

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Remove Planting Data #{context['plantingdata'].pk}"
        return context

@superuser_required()
class TransplantDataUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    form_class = forms.TransplantDataSingleForm
    model = models.TransplantData

    def get_success_url(self):
        view_name = 'hydro_data:single_transplantdata'
        return reverse_lazy(view_name, kwargs={'boxslug':self.kwargs['boxslug'],'rackslug':self.kwargs['rackslug'],'slug':self.kwargs['slug'],'pk': self.kwargs['pk']})

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Edit Transplant Data #{context['transplantdata'].pk}"
        return context

@superuser_required()
class TransplantDataDeleteView(LoginRequiredMixin, DeleteView):
    model = models.TransplantData

    def get_success_url(self):
        return reverse_lazy('hydro_data:loc_per_rack',kwargs={'boxslug':self.kwargs['boxslug'],'rackslug':self.kwargs['rackslug']})

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Remove Transplant Data #{context['transplantdata'].pk}"
        return context

@superuser_required()
class SeedlingWastageDataUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    form_class = forms.SeedlingWastageDataSingleForm
    model = models.SeedlingWastageData

    def get_success_url(self):
        view_name = 'hydro_data:single_seedlingwastagedata'
        return reverse_lazy(view_name, kwargs={'boxslug':self.kwargs['boxslug'],'rackslug':self.kwargs['rackslug'],'slug':self.kwargs['slug'],'pk': self.kwargs['pk']})

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Edit Seedling Wastage Data #{context['seedlingwastagedata'].pk}"
        return context

@superuser_required()
class SeedlingWastageDataDeleteView(LoginRequiredMixin, DeleteView):
    model = models.SeedlingWastageData

    def get_success_url(self):
        return reverse_lazy('hydro_data:loc_per_rack',kwargs={'boxslug':self.kwargs['boxslug'],'rackslug':self.kwargs['rackslug']})

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Remove Seedling Wastage Data #{context['seedlingwastagedata'].pk}"
        return context

@superuser_required()
class WastageDataUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    form_class = forms.WastageDataSingleForm
    model = models.WastageData

    def get_success_url(self):
        view_name = 'hydro_data:single_wastagedata'
        return reverse_lazy(view_name, kwargs={'boxslug':self.kwargs['boxslug'],'rackslug':self.kwargs['rackslug'],'slug':self.kwargs['slug'],'pk': self.kwargs['pk']})

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Edit Wastage Data #{context['wastagedata'].pk}"
        return context

@superuser_required()
class WastageDataDeleteView(LoginRequiredMixin, DeleteView):
    model = models.WastageData

    def get_success_url(self):
        return reverse_lazy('hydro_data:loc_per_rack',kwargs={'boxslug':self.kwargs['boxslug'],'rackslug':self.kwargs['rackslug']})

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Remove Wastage Data #{context['wastagedata'].pk}"
        return context

@superuser_required()
class HarvestDataUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    form_class = forms.HarvestDataSingleForm
    model = models.HarvestData

    def get_success_url(self):
        view_name = 'hydro_data:single_harvestdata'
        return reverse_lazy(view_name, kwargs={'boxslug':self.kwargs['boxslug'],'rackslug':self.kwargs['rackslug'],'slug':self.kwargs['slug'],'pk': self.kwargs['pk']})

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Edit Harvest Data #{context['harvestdata'].pk}"
        return context

@superuser_required()
class HarvestDataDeleteView(LoginRequiredMixin, DeleteView):
    model = models.HarvestData

    def get_success_url(self):
        return reverse_lazy('hydro_data:loc_per_rack',kwargs={'boxslug':self.kwargs['boxslug'],'rackslug':self.kwargs['rackslug']})

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Remove Harvest Data #{context['harvestdata'].pk}"
        return context

@superuser_required()
class LightReadingUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    form_class = forms.LightReadingForm
    model = models.LightReading

    def get_success_url(self):
        view_name = 'hydro_data:single_lightreading'
        return reverse_lazy(view_name, kwargs={'boxslug':self.kwargs['boxslug'],'rackslug':self.kwargs['rackslug'],'slug':self.kwargs['slug'],'pk': self.kwargs['pk']})

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Edit Light Reading #{context['lightreading'].pk}"
        return context

@superuser_required()
class LightReadingDeleteView(LoginRequiredMixin, DeleteView):
    model = models.LightReading

    def get_success_url(self):
        return reverse_lazy('hydro_data:loc_per_rack',kwargs={'boxslug':self.kwargs['boxslug'],'rackslug':self.kwargs['rackslug']})

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Remove Light Reading #{context['lightreading'].pk}"
        return context

@superuser_required()
class AirReadingUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    form_class = forms.AirReadingForm
    model = models.AirReading

    def get_success_url(self):
        view_name = 'hydro_data:single_airreading'
        return reverse_lazy(view_name, kwargs={'boxslug':self.kwargs['boxslug'],'pk': self.kwargs['pk']})

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Edit Air Reading #{context['airreading'].pk}"
        return context

@superuser_required()
class AirReadingDeleteView(LoginRequiredMixin, DeleteView):
    model = models.AirReading

    def get_success_url(self):
        return reverse_lazy('hydro_data:rack_tank_per_box',kwargs={'slug':self.kwargs['boxslug']})

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Remove Air Reading #{context['airreading'].pk}"
        return context

@superuser_required()
class WaterReadingUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    form_class = forms.WaterReadingForm
    model = models.WaterReading

    def get_success_url(self):
        view_name = 'hydro_data:single_waterreading'
        return reverse_lazy(view_name, kwargs={'boxslug':self.kwargs['boxslug'],'tankslug':self.kwargs['tankslug'],'pk': self.kwargs['pk']})

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Edit Water Reading #{context['waterreading'].pk}"
        return context

@superuser_required()
class WaterReadingDeleteView(LoginRequiredMixin, DeleteView):
    model = models.WaterReading

    def get_success_url(self):
        return reverse_lazy('hydro_data:rack_tank_per_box',kwargs={'slug':self.kwargs['boxslug']})

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Remove Water Reading #{context['waterreading'].pk}"
        return context

##########################################################
#############   REDIRECT CLASS BASED VIEWS   #############
##########################################################

@superuser_required()
class ClearPlants(LoginRequiredMixin,RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        rack = get_object_or_404(models.Rack,pk=kwargs['pk'])
        return reverse('hydro_data:rack_tank_per_box',kwargs={'slug':rack.box.slug})

    def get(self, request, *args, **kwargs):
        rack = get_object_or_404(models.Rack,pk=kwargs['pk'])
        locations = models.Location.objects.filter(rack=rack)
        for loc in locations:
            loc.clear()
        return super().get(request, *args, **kwargs)

##########################################################
#############         AJAX AJAX AJAX         #############
##########################################################

def load_boxes(request):
    site = request.GET.get('site')
    boxes = models.Box.objects.filter(site__id=site)
    return render(request, 'hydro_data/box_dropdown_list_options.html', {'boxes': boxes})

def load_racks(request):
    box = request.GET.get('box')
    racks = models.Rack.objects.filter(box__id=box)
    return render(request, 'hydro_data/rack_dropdown_list_options.html', {'racks': racks})

def load_locations(request):
    rack = request.GET.get('rack')
    locations = models.Location.objects.filter(rack__id=rack)
    return render(request, 'hydro_data/location_dropdown_list_options.html', {'locations': locations})

def load_locations(request):
    rack = request.GET.get('rack')
    locations = models.Location.objects.filter(rack__id=rack)
    return render(request, 'hydro_data/location_dropdown_list_options.html', {'locations': locations})

def load_open_locations(request):
    rack = request.GET.get('rack')
    locations = models.Location.objects.filter(rack__id=rack, is_open='1')
    return render(request, 'hydro_data/location_dropdown_list_options.html', {'locations': locations})

def load_occupied_locations(request):
    rack = request.GET.get('rack')
    locations = models.Location.objects.filter(rack__id=rack, is_open='0')
    return render(request, 'hydro_data/location_dropdown_list_options.html', {'locations': locations})

def load_tanks(request):
    box = request.GET.get('box')
    tanks = models.Tank.objects.filter(box__id=box)
    return render(request, 'hydro_data/tank_dropdown_list_options.html', {'tanks': tanks})

def load_prod_name(request):
    prod_name = request.GET.get('prod_name')
    product = models.ProductName.filter(name__id=name)
    return render(request, 'hydro_data/prod_name_dropdown_list_options.html', {'product': product})

########################### TEST ##############################
class PackingLogView(CreateView):
    model = models.PackingLog
    form_class = PackingLogForm
    template_name = 'hydro_data/packing_log.html'


class WeightCategoryCreate(CreateView):
    model = models.WeightCategory
    form_class = WeightCategoryForm
    template_name = 'hydro_data/create_weight_category.html'


class WeightCategoryModalCreate(BSModalCreateView):
    template_name = 'hydro_data/create_weight_category.html'
    form_class = WeightCategoryModal
    success_message = 'Weight category added'
    success_url = reverse_lazy('')

def create_packinglog(request):
    template_name =  'hydro_data/packing_log.html'
 
    if request.method == 'GET' :
        packinglogdataform = forms.PackingLogForm()
        formset = forms.PackingLogFormset(queryset=models.PackingLog.objects.none())
    elif request.method == 'POST':
        packinglogdataform = forms.PackingLogForm(request.POST)
        formset = forms.PackingLogFormset(request.POST)
        
        if packinglogdataform.is_valid() and formset.is_valid():
          
            customer = packinglogdataform.cleaned_data
            name = customer['custom_name']
            packaged = customer['date_packaged']
            harvested = customer['date_harvested']

            packagedby = customer['packaged_by']
            for form in formset:


                product = form.cleaned_data.get("prod_name")
                package = form.cleaned_data.get('no_of_packs')
                packlog = PackingLog.objects.get_or_create(
                    custom_name=name, 
                    date_packaged=packaged,
                    date_harvested=harvested,
                    prod_name=product,
                    no_of_packs=package,
                    packaged_by=packagedby
                )


            return HttpResponseRedirect(reverse('hydro_data:packing_log_list'))
    return render(request, template_name, {
        'packinglogdataform': packinglogdataform,
        'formset': formset,
    })

def create_packinglogform(request):

    template_name = 'hydro_data/packing_log.html'
    packinglogdataform = PackingLogForm(request.POST or None)




class PackingLogDataList(ListView):
    model = PackingLog
    template_name = 'hydro_data/packinglog_list.html'
    context_object_name = 'packing'


def csv_upload(request):
    template = 'hydro_data/csv_upload.html'

    prompt = {
        'order' : 'CSV file for Delivery Data'
    }

    if request.method == 'GET':
        return render(request, template, prompt)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'File format invalid')

    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=','):
        _, created = models.DeliveryData.objects.get_or_create(
            delivery_date=column[0],
            order_no=column[1],
            f_name=column[2],
            l_name=column[3],
            address=column[4],
            phone=column[5],
            email=column[6],
            mop=column[7],
            delivery_fee=column[8],
            status=column[9],
            discount_code=column[10],
            total_price=column[11],
            products=column[12],
            prod_weight=column[13],
            prod_qty=column[14],
            prod_price=column[15],
            order_sum=column[16],
            total_weight=column[17],
            order=column[18]
        )

        context = {}

        return render(request, template, context)


class DeliveryDataTable(ListView):
    template_name = 'hydro_data/deliverydata_table.html'
    model = models.DeliveryData
    context_object_name = 'delivery_data'



class AdminDashboard(TemplateView):
    template_name = 'hydro_data/dashboard.html'
    