from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import modelformset_factory
from . import models

from .models import PackingLog, WeightCategory
from bootstrap_modal_forms.forms import BSModalModelForm


class UserCreateForm(UserCreationForm):
    class Meta:
        fields = ("username", "email", "password1", "password2")
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Display name"
        self.fields["email"].label = "Email address"

class SiteForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = models.Site
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control'
                }
            )
        }

class BoxForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = models.Box
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control'
                }
            )
        }

class RackForm(forms.ModelForm):
    class Meta:
        model = models.Rack
        fields = ('name', )
        labels = {
            'name': 'Box'
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter rack name here'
                }
            )
        }

class ProduceTypeForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = models.ProduceType

class LocationForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = models.Location
        labels = {
            'name': 'SQM ID',
            'x_cor': 'X-coor',
            'y_cor': 'Y-coor'
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control'
                }
            ),
            'x_cor': forms.NumberInput(attrs={
                'class': 'form-control'
                }
            ),
            'y_cor': forms.NumberInput(attrs={
                'class': 'form-control'
                }
            ),
            'is_open': forms.Select(attrs={
                'class': 'form-control'
            })
        }

class AcidForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = models.Acid

class NutrientForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = models.Nutrient

class ActivityForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = models.Activity

class GrowMediumForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = models.GrowMedium

class TrayForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = models.Tray

class ActivityForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = models.Activity

class TankForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = models.Tank

class BatchForm(forms.ModelForm):
    class Meta:
        fields = ('num',)
        model = models.Batch
        labels={'num':'Batch no.',}
        widgets={
            'num': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                }
                )
            }

class PlantingDataSingleForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = models.PlantingData

class TransplantDataSingleForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = models.TransplantData

class SeedlingWastageDataSingleForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = models.SeedlingWastageData

class WastageDataSingleForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = models.WastageData

class HarvestDataSingleForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = models.HarvestData

class LightReadingForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = models.LightReading

class AirReadingForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = models.AirReading

class WaterReadingForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = models.WaterReading

class ChooseBatchForm(forms.Form):
    batch = forms.ModelChoiceField(queryset=models.Batch.objects.all())

class ChooseSiteBoxForm(forms.Form):
    site = forms.ModelChoiceField(queryset=models.Site.objects.all())
    box = forms.ModelChoiceField(queryset=models.Box.objects.all())

class ChooseSiteBoxRackForm(forms.Form):
    site = forms.ModelChoiceField(queryset=models.Site.objects.all())
    box = forms.ModelChoiceField(queryset=models.Box.objects.all())
    rack = forms.ModelChoiceField(queryset=models.Rack.objects.all())

class WaterConsumptionForSiteDataForm(forms.ModelForm):
    class Meta:
        exclude = ('site','staff',)
        model = models.WaterConsumption

class EnergyConsumptionForBoxDataForm(forms.ModelForm):
    class Meta:
        exclude = ('box','staff',)
        model = models.EnergyConsumption

class BoxModelForm(forms.ModelForm):
    class Meta:
        model = models.Box
        fields = ('site','name', )
        labels = {
            'site': 'Site',
            'name': 'Box'
        }
        widgets = {
            'site': forms.Select(attrs={
                'class': 'form-control'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Box Name here'
                }
            )
        }
RackFormset = modelformset_factory(
    models.Rack,
    fields=('name', ),
    extra=1,
    labels={'name':'Rack'},
    widgets={
        'name': forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter Rack Name here'
            }
        )
    }
)

ProduceTypeFormset = modelformset_factory(
    models.ProduceType,
    fields=('name','variety','seed_brand'),
    extra=1,
    labels={'name':'Produce','variety':'Variety','seed_brand':'Seed Brand'},
    widgets={
        'name': forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter produce type here'
            }
        ),
        'variety': forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter variety here'
            }
        ),
        'seed_brand': forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter seed brand here'
            }
        ),
    }
)

LocationFormset = modelformset_factory(
    models.Location,
    fields=('name','x_cor','y_cor','is_open'),
    extra=1,
    labels={'name':'Location','x_cor':'X-coor','y_cor':'Y-coor'},
    widgets={
        'name': forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter SQM ID'
            }
        ),
        'x_cor': forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '(optional)'
            }
        ),
        'y_cor': forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '(optional)'
            }
        ),
        'is_open': forms.Select(attrs={
            'class': 'form-control'
        })
    }
)

AcidFormset = modelformset_factory(
    models.Acid,
    fields=('name', ),
    extra=1,
    labels={'name':'Acid'},
    widgets={
        'name': forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter acid here'
            }
        )
    }
)

NutrientFormset = modelformset_factory(
    models.Nutrient,
    fields=('name', ),
    extra=1,
    labels={'name':'Nutrient'},
    widgets={
        'name': forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter nutrient here'
            }
        )
    }
)

ActivityFormset = modelformset_factory(
    models.Activity,
    fields=('name', ),
    extra=1,
    labels={'name':'Activity'},
    widgets={
        'name': forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter activity here'
            }
        )
    }
)

GrowMediumFormset = modelformset_factory(
    models.GrowMedium,
    fields=('name', ),
    extra=1,
    labels={'name':'Grow Medium'},
    widgets={
        'name': forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter grow medium here'
            }
        )
    }
)

TrayFormset = modelformset_factory(
    models.Tray,
    fields=('name', ),
    extra=1,
    labels={'name':'Tray'},
    widgets={
        'name': forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter tray here'
            }
        )
    }
)

TankFormset = modelformset_factory(
    models.Tank,
    fields=('name', ),
    extra=1,
    labels={'name':'Tank'},
    widgets={
        'name': forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter tank here'
            }
        )
    }
)

class PlantingDataForm(forms.ModelForm):
    class Meta:
        exclude = ('date','time','square_meter_id','staff')
        model = models.PlantingData
        labels = {
            'seedling_batch_no':'Batch',
            'growmedium':'Grow Medium',
            'produce_type':'Produce Type'
        }
        widgets = {
            'site': forms.Select(attrs={
                'class': 'form-control'
            }),
            'box': forms.Select(attrs={
                'class': 'form-control'
            }),
            'rack': forms.Select(attrs={
                'class': 'form-control'
            }),
            'seedling_batch_no': forms.Select(attrs={
                'class': 'form-control'
            }),
            'growmedium': forms.Select(attrs={
                'class': 'form-control'
            }),
            'tray': forms.Select(attrs={
                'class': 'form-control'
            }),
            'produce_type': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

class PlantingDataBatchForm(forms.ModelForm):
    class Meta:
        fields = ('growmedium','tray','produce_type',)
        model = models.PlantingData
        labels={'growmedium':'Grow Medium','tray':'Tray','produce_type':'Produce'}
        widgets={
            'growmedium': forms.Select(attrs={
                'class': 'form-control'
            }),
            'tray': forms.Select(attrs={
                'class': 'form-control'
            }),
            'produce_type': forms.Select(attrs={
                'class': 'form-control'
            })
        }

class PlantingDataForLocForm(forms.ModelForm):
    class Meta:
        fields = ('growmedium','tray','produce_type',)
        model = models.PlantingData
        labels={'growmedium':'Grow Medium','tray':'Tray','produce_type':'Produce'}
        widgets={
            'growmedium': forms.Select(attrs={
                'class': 'form-control'
            }),
            'tray': forms.Select(attrs={
                'class': 'form-control'
            }),
            'produce_type': forms.Select(attrs={
                'class': 'form-control'
            })
        }

PlantingDataFormset = modelformset_factory(
    models.PlantingData,
    fields=('square_meter_id','growmedium','tray','produce_type'),
    extra=1,
    labels={'square_meter_id':'SQM ID','growmedium':'Grow Medium','tray':'Tray','produce_type':'Produce'},
    widgets = {
        'square_meter_id': forms.Select(attrs={
            'class': 'form-control'
        }),
        'growmedium': forms.Select(attrs={
            'class': 'form-control'
        }),
        'tray': forms.Select(attrs={
            'class': 'form-control'
        }),
        'produce_type': forms.Select(attrs={
            'class': 'form-control'
        }),
    }
)

class TransplantBatchForm(forms.ModelForm):
    class Meta:
        fields = ('seedling_batch_no','box','rack',)
        model = models.TransplantData
        labels = {
            'seedling_batch_no': 'Which batch were these?'
        }
        widgets={
            'seedling_batch_no': forms.Select(attrs={
                'class': 'form-control'
            }),
            'box': forms.Select(attrs={
                'class': 'form-control'
            }),
            'rack': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

class SeedlingWastageDataForm(forms.ModelForm):
    class Meta:
        fields = ('seedling_batch_no','wastage_reason',)
        model = models.SeedlingWastageData
        labels = {
            'seedling_batch_no': 'Which batch were these?',
            'wastage_reason': 'Reason for wastage'
        }
        widgets={
            'seedling_batch_no': forms.Select(attrs={
                'class': 'form-control'
            }),
            'wastage_reason': forms.TextInput(attrs={
                'class': 'form-control',
                }
            ),
        }

SeedlingWastageDataFormset = modelformset_factory(
    models.SeedlingWastageData,
    fields=('square_meter_id',),
    extra=1,
    labels={'square_meter_id':'SQM ID',},
    widgets={
        'square_meter_id': forms.Select(attrs={
            'class': 'form-control'
        }),
    }
)

class HarvestDataForm(forms.ModelForm):
    class Meta:
        exclude = ('date','time','square_meter_id','harvest_weight_kg','no_of_heads','produce_type','staff')
        model = models.HarvestData
        widgets = {
            'site': forms.Select(attrs={
                'class': 'form-control'
            }),
            'box': forms.Select(attrs={
                'class': 'form-control'
            }),
            'rack': forms.Select(attrs={
                'class': 'form-control'
            }),
            'seedling_batch_no': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
        }

class HarvestDataForLocForm(forms.ModelForm):
    class Meta:
        fields = ('harvest_weight_kg','seedling_batch_no','no_of_heads')
        model = models.HarvestData
        labels={'harvest_weight_kg':'Weight','seedling_batch_no':'Batch','no_of_heads':'Number of heads (if lettuce)'}
        widgets={
            'harvest_weight_kg': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Kg'
                }
            ),
            'seedling_batch_no': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'no_of_heads': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '(optional)'
                }
            ),
        }

HarvestDataFormset = modelformset_factory(
    models.HarvestData,
    fields=('square_meter_id','harvest_weight_kg','no_of_heads'),
    extra=1,
    labels={'square_meter_id':'SQM ID','harvest_weight_kg':'Weight'},
    widgets={
        'square_meter_id': forms.Select(attrs={
            'class': 'form-control'
        }),
        'harvest_weight_kg': forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Kg'
            }
        ),
        'no_of_heads': forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': '(optional)'
            }
        ),
    }
)

class WastageDataForm(forms.ModelForm):
    class Meta:
        fields = ('seedling_batch_no','wastage_reason',)
        model = models.WastageData
        labels = {
            'seedling_batch_no': 'Which batch were these?',
            'wastage_reason': 'Reason for wastage'
        }
        widgets={
            'seedling_batch_no': forms.Select(attrs={
                'class': 'form-control'
            }),
            'wastage_reason': forms.TextInput(attrs={
                'class': 'form-control',
                }
            ),
        }

WastageDataFormset = modelformset_factory(
    models.WastageData,
    fields=('square_meter_id','wastage_kg'),
    extra=1,
    labels={'square_meter_id':'SQM ID','wastage_kg':'Wastage'},
    widgets={
        'square_meter_id': forms.Select(attrs={
            'class': 'form-control'
        }),
        'wastage_kg': forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Kg'
            }
        ),
    }
)

class LightReadingDataForm(forms.ModelForm):
    class Meta:
        exclude = ('date','time','square_meter_id','par_reading','staff')
        model = models.LightReading
        widgets = {
            'site': forms.Select(attrs={
                'class': 'form-control'
            }),
            'box': forms.Select(attrs={
                'class': 'form-control'
            }),
            'rack': forms.Select(attrs={
                'class': 'form-control'
            })
        }

class LightReadingDataForLocForm(forms.ModelForm):
    class Meta:
        fields = ('par_reading',)
        model = models.LightReading
        labels={'par_reading':'PAR',}
        widgets={
            'par_reading': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                }
            ),
        }

LightReadingDataFormset = modelformset_factory(
    models.LightReading,
    fields=('square_meter_id','par_reading'),
    extra=1,
    labels={'square_meter_id':'SQM ID','par_reading':'PAR Reading'},
    widgets={
        'square_meter_id':  forms.Select(attrs={
            'class': 'form-control'
        }),
        'par_reading': forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'PAR reading'
            }
        )
    }
)

class AirReadingDataForm(forms.ModelForm):
    class Meta:
        exclude = ('date','time','staff',)
        model = models.AirReading
        labels = {'current_relative_humidity': 'Relative humidity', 'current_temp': 'Temperature', 'current_co2_level': 'CO2 level'}
        widgets = {
            'site': forms.Select(attrs={
                'class': 'form-control'
            }),
            'box': forms.Select(attrs={
                'class': 'form-control'
            }),
            'current_relative_humidity': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'current_temp': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'current_co2_level': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
        }

class AirReadingForBoxDataForm(forms.ModelForm):
    class Meta:
        exclude = ('box','staff',)
        model = models.AirReading
        labels = {'current_relative_humidity': 'Relative humidity', 'current_temp': 'Temperature', 'current_co2_level': 'CO2 level'}
        widgets = {
            'current_relative_humidity': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'current_temp': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'current_co2_level': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
        }

class WaterReadingDataForm(forms.ModelForm):
    class Meta:
        exclude = ('date','time','tank','activity','prev_ph','current_ph','prev_ec','current_ec','acid_used_ml','acid_type','nutrient_used_ml','nutrient_type','water_level_liters','staff')
        model = models.WaterReading
        widgets= {
            'site': forms.Select(attrs={
                'class': 'form-control'
            }),
            'box': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

class WaterReadingForTankDataForm(forms.ModelForm):
    class Meta:
        model = models.WaterReading
        fields = ('activity','prev_ph','current_ph','prev_ec','current_ec','acid_used_ml','acid_type','nutrient_used_ml','nutrient_type','water_level_liters')
        labels = {'activity':'Activity','prev_ph':'Prev. pH','current_ph':'Current pH','prev_ec':'Prev. EC','current_ec':'Current EC','acid_used_ml':'Acid Amount',
                'acid_type':'Acid','nutrient_used_ml':'Nutrient Amount','nutrient_type':'Nutrient','water_level_liters':'Water Level'},
        widgets={
            'activity': forms.Select(attrs={
                'class': 'form-control'
            }),
            'acid_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'nutrient_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'prev_ph': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'pH'
                }
            ),
            'current_ph': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'pH'
                }
            ),
            'prev_ec': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'current_ec': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'acid_used_ml': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'mL'
                }
            ),
            'nutrient_used_ml': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'mL'
                }
            ),
            'water_level_liters': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'L'
                }
            )
        }

WaterReadingDataFormset = modelformset_factory(
    models.WaterReading,
    fields=('tank','activity','prev_ph','current_ph','prev_ec','current_ec','acid_used_ml','acid_type','nutrient_used_ml','nutrient_type','water_level_liters'),
    extra=1,
    labels={'tank':'Tank','activity':'Activity','prev_ph':'Prev. pH','current_ph':'Current pH','prev_ec':'Prev. EC','current_ec':'Current EC','acid_used_ml':'Acid Amount',
            'acid_type':'Acid','nutrient_used_ml':'Nutrient Amount','nutrient_type':'Nutrient','water_level_liters':'Water Level'},
    widgets={
        'tank': forms.Select(attrs={
            'class': 'form-control'
        }),
        'acid_type': forms.Select(attrs={
            'class': 'form-control'
        }),
        'nutrient_type': forms.Select(attrs={
            'class': 'form-control'
        }),
        'activity': forms.Select(attrs={
            'class': 'form-control'
        }),
        'acid_type': forms.Select(attrs={
            'class': 'form-control'
        }),
        'nutrient_type': forms.Select(attrs={
            'class': 'form-control'
        }),
        'prev_ph': forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'pH'
            }
        ),
        'current_ph': forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'pH'
            }
        ),
        'prev_ec': forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        ),
        'current_ec': forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        ),
        'acid_used_ml': forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'mL'
            }
        ),
        'nutrient_used_ml': forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'mL'
            }
        ),
        'water_level_liters': forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'L'
            }
        )
    }
)
class DateInput(forms.DateInput):
    input_type = 'date'

class PackingLogForm(forms.ModelForm):
    
    class Meta:
        model = PackingLog
        exclude = ('date', 'time', 'prod_name' , 'no_of_packs')
        fields = ['custom_name', 'date_packaged', 'date_harvested', 'packaged_by']
        widgets = {
            'date_packaged' : DateInput(),
            'date_harvested' : DateInput(),
            
          }

PackingLogFormset = modelformset_factory(
    models.PackingLog,
    fields= ('prod_name' , 'no_of_packs'),
    # widgets= {
    #       'packaged_by' : forms.CheckboxSelectMultiple(),
    # #     #  'harvest': forms.Select(attrs={
    # #     #      'class' : 'form-control'
    # #     # }),
    # # #     'no_of_packs' : forms.NumberInput(attrs={
    # # #         'class' : 'form-control'
    # # #     }),
    # # #     'packaging_used' : forms.Select(attrs={
    # # #         'class' : 'form-control'
    # # #     }),
    # # #     'weight_in_grams' : forms.NumberInput(attrs={
    # # #         'class' : 'form-control'
    # # #     }),
    # }
)

class ProductNameForm(forms.ModelForm):
    class Meta:
        model = models.ProductName  
        fields = '__all__'



class WeightCategoryForm(forms.ModelForm):
    class Meta:
        model = WeightCategory
        fields = '__all__'



class WeightCategoryModal(BSModalModelForm):
    class Meta:
        model = WeightCategory
        fields = "__all__"


class PackagedByForm(forms.ModelForm):
    class Meta:
        model = models.PackagedBy
        fields = "__all__"
