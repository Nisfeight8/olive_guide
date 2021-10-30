from django import forms
from .models import *
from leaflet.forms.widgets import LeafletWidget
from material import Layout, Row ,Column
from django.utils.translation import ugettext_lazy as _

class CoordinatesForm(forms.Form):
    x=forms.FloatField(required=True,widget=forms.NumberInput(attrs={'step': 'any'}))
    y=forms.FloatField(required=True,widget=forms.NumberInput(attrs={'step': 'any'}))
    layout = Layout(Row(Column('x'), Column('y')))
from django.forms.formsets import formset_factory

CoordinatesFormSet = formset_factory(form=CoordinatesForm, extra=0,
min_num=4, validate_min=True,)


class OliveGroveForm(forms.ModelForm):
    class Meta:
        model = OliveGrove
        fields = ('name','srid')
class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        exclude = ('created_by','created_at','olive_grove',)
