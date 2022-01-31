import django_filters
from .models import *

class LicenseFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(label='Amazina ',lookup_expr ='icontains')
    dln = django_filters.CharFilter(label='D.L.No ',lookup_expr ='icontains')
    class Meta:
        model = License
        fields = ['dln', 'name' ]
        labels = {
            'dln': 'Driving License Number',
            'name':'Name',
        }
