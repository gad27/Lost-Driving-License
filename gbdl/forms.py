from django.forms import ModelForm
from django.forms import HiddenInput
from .filters import LicenseFilter
from .models import *
from django import forms
from django.forms import CharField
from django.forms import Textarea
from django.forms import EmailField
from django.forms import TextInput
from django.forms import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re

class CreateForm(ModelForm):
    class Meta:
        model = License
        fields = ['dln', 'name', 'dob', 'class1', 'sex']
        exclude = ['place', 'group1', 'status', 'phone', 'action', 'date_added_on', 'declared_on', 'returned_on', 'found_on', 'expd']

        widgets = {
            'dob': TextInput(attrs={'class':'form-control', 'type':'date'}),
            #'expd': TextInput(attrs={'class':'form-control', 'type':'date'}),
            'class1': TextInput(attrs={'class':'form-control', 'placeholder':'Hint: A,B,...'})
        }

        labels = {
            'dln': 'Driving License Number',
            'name':'Name',
            'dob': 'Date of Birth',
            'class1': 'Class',
            'sex': 'Gender',
            #'expd': 'Expiration Date',
        }
    
    def clean_dob(self):
        data = self.cleaned_data.get('dob')
        if str(data) > str(datetime.datetime.today().date()):
            raise forms.ValidationError(
                'you can\'t add future date')
        elif (datetime.datetime.today().date() - data) < datetime.timedelta(days=18*365):
            raise forms.ValidationError(
                'Driving License owner must be 18 years old and above')
        return data

    #def clean_expd(self):
        #data = self.cleaned_data.get('expd')
        #if str(data) < str(datetime.datetime.today().date()):
       #     raise forms.ValidationError(
      #          'your driving license has expired')
     #   return data

    def clean_dln(self): 
        data1 = self.cleaned_data.get('dln')
        if len(data1) != 16:
            raise forms.ValidationError(
                'Driving license number must be 16 numbers')
        #data2 = data1.isdecimal()
        if data1.isdecimal() == False:
            raise forms.ValidationError(
                'Driving license number must contain numbers only')
        for instance in License.objects.all().filter(status='NOT DECLARED', group1='FOUND'):
            if instance.dln == data1: 
                raise forms.ValidationError(
                    'License having D.L.No ' +data1+ ' have been already added, Check it in Submitted Licenses')
        for instance in License.objects.all().filter(status='NOT DECLARED', group1='LOST'):
            if instance.dln == data1: 
                raise forms.ValidationError(
                    'License having D.L.No ' +data1+ ' have been reported as missing, Check it in Lost Licenses')
        return data1
    
    def clean_class1(self):
        data1 = self.cleaned_data.get('class1')
        check1 = bool(re.match('^[A,B,C,D,D1,E,F]+$', data1))
        if check1 == False:
            raise forms.ValidationError(
                'The valid classes are: "A","B","C","D","D1","E","F"')
        return data1

class AdminDeclareForm(ModelForm):
    class Meta:
        model = License
        fields = ['dln', 'name', 'dob', 'class1', 'sex', 'phone']
        exclude = ['place', 'group1', 'status', 'action', 'date_added_on', 'declared_on', 'returned_on', 'found_on', 'expd']

        widgets = {
            'dob': TextInput(attrs={'class':'form-control', 'type':'date'}),
           # 'expd': TextInput(attrs={'class':'form-control', 'type':'date'}),
            'class1': TextInput(attrs={'class':'form-control', 'placeholder':'Hint: A,B,...'})
        }

        labels = {
            'dln': 'Driving License Number',
            'name':'Name',
            'dob': 'Date of Birth',
            'class1': 'Class',
            'sex': 'Gender',
           # 'expd': 'Expiration Date',
            'phone': 'Phone Number',
        }

    def clean_dob(self):
        data = self.cleaned_data.get('dob')
        if str(data) > str(datetime.datetime.today().date()):
            raise forms.ValidationError(
                'you can\'t add future date')
        elif (datetime.datetime.today().date() - data) < datetime.timedelta(days=18*365):
            raise forms.ValidationError(
                'Driving License owner must be 18 years old and above')
        return data
    
    def clean_dln(self):
        data1 = self.cleaned_data.get('dln')
        if len(data1) != 16:
            raise forms.ValidationError(
                'Driving license number must be 16 numbers')
        if data1.isdecimal() == False:
            raise forms.ValidationError(
                'Driving license number must contain numbers only')
        for instance in License.objects.all().filter(status='DECLARED', group1='FOUND', action='IN STOCK'):
            if instance.dln == data1: 
                raise forms.ValidationError(
                    'License having D.L.No ' +data1+ ' have already been declared')
        return data1
    
    def clean_class1(self):
        data1 = self.cleaned_data.get('class1')
        check1 = bool(re.match('^[A,B,C,D,D1,E,F]+$', data1))
        if check1 == False:
            raise forms.ValidationError(
                'The valid classes are: "A","B","C","D","D1","E","F"')
        return data1
    
    def clean_phone(self):
        data1 = self.cleaned_data.get('phone')
        check1 = bool(re.match('^+?250?7?[0-9]+$', data1))
        if check1 == False:
            raise forms.ValidationError(
                'Write your phone number correctly')
        return data1

class DeclareForm(ModelForm):
    class Meta:
        model = License
        fields = ['dln', 'name', 'dob', 'class1', 'sex', 'phone']
        exclude = ['place', 'group1', 'status', 'action', 'date_added_on', 'declared_on', 'returned_on', 'found_on', 'expd']

        widgets = {
            'dob': TextInput(attrs={'class':'form-control', 'type':'date'}),
           # 'expd': TextInput(attrs={'class':'form-control', 'type':'date'}),
            'class1': TextInput(attrs={'class':'form-control', 'placeholder':'Hint: A,B,...'})
        }

        labels = {
            'dln': 'Driving License Number',
            'name':'Name',
            'dob': 'Date of Birth',
            'class1': 'Class',
            'sex': 'Gender',
           # 'expd': 'Expiration Date',
            'phone': 'Phone Number',
        }

    def clean_dob(self):
        data = self.cleaned_data.get('dob')
        if str(data) > str(datetime.datetime.today().date()):
            raise forms.ValidationError(
                'you can\'t add future date')
        elif (datetime.datetime.today().date() - data) < datetime.timedelta(days=18*365):
            raise forms.ValidationError(
                'Driving License owner must be 18 years old and above')
        return data
    
    def clean_dln(self):
        data1 = self.cleaned_data.get('dln')
        if len(data1) != 16:
            raise forms.ValidationError(
                'Driving license number must be 16 numbers')
        if data1.isdecimal() == False:
            raise forms.ValidationError(
                'Driving license number must contain numbers only')
        for instance in License.objects.all().filter(status='DECLARED', group1='FOUND', action='IN STOCK'):
            if instance.dln == data1: 
                raise forms.ValidationError(
                    'Uruhushya rwo gutwara rufite numero ' +data1+ ' rwamaze kumenyekanishwa, gana sitasiyo ya police ikwegereye bagufashe.')
        return data1
    
    def clean_class1(self):
        data1 = self.cleaned_data.get('class1')
        check1 = bool(re.match('^[A,B,C,D,D1,E,F]+$', data1))
        if check1 == False:
            raise forms.ValidationError(
                'The valid classes are: "A","B","C","D","D1","E","F"')
        return data1

class AdminLostForm(ModelForm):
    class Meta:
        model = License
        fields = ['dln', 'name', 'dob', 'class1', 'sex', 'phone']
        exclude = ['group1', 'expd', 'place', 'action', 'status', 'date_added_on', 'declared_on', 'returned_on', 'found_on']

        widgets = {
            'dob': TextInput(attrs={'class':'form-control', 'type':'date'}),
            'class1': TextInput(attrs={'class':'form-control', 'placeholder':'Hint: A,B,...'}),
            'name': TextInput(attrs={'class':'form-control', 'placeholder':'add your name'})
        }

        labels = {
            'dln': 'Driving License Number',
            'name':'Name',
            'dob': 'Date of Birth',
            'class1': 'Class',
            'sex': 'Gender',
            'phone': 'Phone Number',
        }
        
    def clean_dob(self):
        data = self.cleaned_data.get('dob')
        if str(data) > str(datetime.datetime.today().date()):
            raise forms.ValidationError(
                'you can\'t add future date')
        elif (datetime.datetime.today().date() - data) < datetime.timedelta(days=18*365):
            raise forms.ValidationError(
                'Driving License owner must be 18 years old and above')
        return data
    
    def clean_dln(self):
        data1 = self.cleaned_data.get('dln')
        if len(data1) != 16:
            raise forms.ValidationError(
                'Driving license number must be 16 numbers')
        if data1.isdecimal() == False:
            raise forms.ValidationError(
                'Driving license number must contain numbers only')
        for instance in License.objects.all().filter(status='NOT DECLARED', group1='LOST'):
            if instance.dln == data1: 
                raise forms.ValidationError(
                    'License with D.L.No ' +data1+ ' have already been signaled as a lost one; Check it in Lost Licenses.')
        return data1
    
    def clean_class1(self):
        data1 = self.cleaned_data.get('class1')
        check1 = bool(re.match('^[A,B,C,D,D1,E,F]+$', data1))
        if check1 == False:
            raise forms.ValidationError(
                'The valid classes are: "A","B","C","D","D1","E","F"')
        return data1


class LostForm(ModelForm):
    class Meta:
        model = License
        fields = ['dln', 'name', 'dob', 'class1', 'sex', 'phone']
        exclude = ['group1', 'expd', 'place', 'action', 'status', 'date_added_on', 'declared_on', 'returned_on', 'found_on']

        widgets = {
            'dob': TextInput(attrs={'class':'form-control', 'type':'date'}),
            'class1': TextInput(attrs={'class':'form-control', 'placeholder':'Hint: A,B,...'}),
            'name': TextInput(attrs={'class':'form-control', 'placeholder':'add your name'})
        }

        labels = {
            'dln': 'Driving License Number',
            'name':'Name',
            'dob': 'Date of Birth',
            'class1': 'Class',
            'sex': 'Gender',
            'phone': 'Phone Number',
        }
        
    def clean_dob(self):
        data = self.cleaned_data.get('dob')
        if str(data) > str(datetime.datetime.today().date()):
            raise forms.ValidationError(
                'you can\'t add future date')
        elif (datetime.datetime.today().date() - data) < datetime.timedelta(days=18*365):
            raise forms.ValidationError(
                'Driving License owner must be 18 years old and above')
        return data
    
    def clean_dln(self):
        data1 = self.cleaned_data.get('dln')
        if len(data1) != 16:
            raise forms.ValidationError(
                'Driving license number must be 16 numbers')
        if data1.isdecimal() == False:
            raise forms.ValidationError(
                'Driving license number must contain numbers only')
        for instance in License.objects.all().filter(status='NOT DECLARED', group1='LOST'):
            if instance.dln == data1: 
                raise forms.ValidationError(
                    'Uruhushya rwo gutwara rufite numero ' +data1+ ' rwamaze kumenyekanishwa ko rwatakaye, niba warubuze mu mpushya zabonetse, gana sitasiyo ya police ikwegereye bagufashe.')
        return data1
    
    def clean_class1(self):
        data1 = self.cleaned_data.get('class1')
        check1 = bool(re.match('^[A,B,C,D,D1,E,F]+$', data1))
        if check1 == False:
            raise forms.ValidationError(
                'The valid classes are: "A","B","C","D","D1","E","F"')
        return data1

class FoundForm(ModelForm):
    class Meta:
        model = License
        fields = ['dln', 'name', 'dob', 'class1', 'sex', 'phone']
        exclude = ['group1', 'place', 'status', 'action', 'date_added_on', 'declared_on', 'returned_on', 'found_on', 'expd']

        widgets = {
            'dob': TextInput(attrs={'class':'form-control', 'type':'date'}),
           # 'expd': TextInput(attrs={'class':'form-control', 'type':'date'}),
            'class1': TextInput(attrs={'class':'form-control', 'placeholder':'Hint: A,B,...'})
        }

        labels = {
            'dln': 'Driving License Number',
            'name':'Name',
            'dob': 'Date of Birth',
            'class1': 'Class',
            'sex': 'Gender',
           # 'expd': 'Expiration Date',
        }

    def clean_dob(self):
        data = self.cleaned_data.get('dob')
        if str(data) > str(datetime.datetime.today().date()):
            raise forms.ValidationError(
                'you can\'t add future date')
        elif (datetime.datetime.today().date() - data) < datetime.timedelta(days=18*365):
            raise forms.ValidationError(
                'Driving License owner must be 18 years old and above')
        return data
    
    def clean_dln(self):
        data1 = self.cleaned_data.get('dln')
        if len(data1) != 16:
            raise forms.ValidationError(
                'Driving license number must be 16 numbers')
        if data1.isdecimal() == False:
            raise forms.ValidationError(
                'Driving license number must contain numbers only')
        for instance in License.objects.all().filter(status='DECLARED', group1='FOUND'):
            if instance.dln == data1: 
                raise forms.ValidationError(
                    'License with D.L.No ' +data1+ ' have already been found.')
        
        return data1
    
    def clean_class1(self):
        data1 = self.cleaned_data.get('class1')
        check1 = bool(re.match('^[A,B,C,D,D1,E,F]+$', data1))
        if check1 == False:
            raise forms.ValidationError(
                'The valid classes are: "A","B","C","D","D1","E","F"')
        return data1

class UpdateForm(ModelForm):
    class Meta:
        model = License
        fields = ['dln', 'name', 'dob', 'class1', 'sex', 'phone','group1']
        exclude = ['place', 'status', 'action', 'date_added_on', 'declared_on', 'returned_on', 'found_on', 'expd']

        widgets = {
            'dob': TextInput(attrs={'class':'form-control', 'type':'date'}),
           # 'expd': TextInput(attrs={'class':'form-control', 'type':'date'}),
            'class1': TextInput(attrs={'class':'form-control', 'placeholder':'Hint: A,B,...'})
        }

        labels = {
            'dln': 'Driving License Number',
            'name':'Name',
            'dob': 'Date of Birth',
            'class1': 'Class',
            'sex': 'Gender',
            #'expd': 'Expiration Date',
            'phone': 'Phone Number',
            'group1': 'Group',
        }

    def clean_dob(self):
        data = self.cleaned_data.get('dob')
        if str(data) > str(datetime.datetime.today().date()):
            raise forms.ValidationError(
                'you can\'t add future date')
        elif (datetime.datetime.today().date() - data) < datetime.timedelta(days=18*365):
            raise forms.ValidationError(
                'Driving License owner must be 18 years old and above')
        return data

   # def clean_expd(self):
    #    data = self.cleaned_data.get('expd')
     #   if str(data) < str(datetime.datetime.today().date()):
      #      raise forms.ValidationError(
       #         'your driving license has expired')
        #return data
    
    def clean_dln(self):
        data1 = self.cleaned_data.get('dln')
        if len(data1) != 16:
            raise forms.ValidationError(
                'Driving license number must be 16 numbers')
        if data1.isdecimal() == False:
            raise forms.ValidationError(
                'Driving license number must contain numbers only')
        return data1
    
    def clean_class1(self):
        data1 = self.cleaned_data.get('class1')
        check1 = bool(re.match('^[A,B,C,D,D1,E,F]+$', data1))
        if check1 == False:
            raise forms.ValidationError(
                'The valid classes are: "A","B","C","D","D1","E","F"')
        return data1

class UpdateForm1(ModelForm):
    class Meta:
        model = License
        fields = ['dln', 'name', 'dob', 'class1', 'sex', 'phone', 'status']
        exclude = ['place', 'group1', 'action', 'date_added_on', 'declared_on', 'returned_on', 'found_on', 'expd']

        widgets = {
            'dob': TextInput(attrs={'class':'form-control', 'type':'date'}),
         #   'expd': TextInput(attrs={'class':'form-control', 'type':'date'}),
            'class1': TextInput(attrs={'class':'form-control', 'placeholder':'Hint: A,B,...'})
        }

        labels = {
            'dln': 'Driving License Number',
            'name':'Name',
            'dob': 'Date of Birth',
            'class1': 'Class',
            'sex': 'Gender',
         #   'expd': 'Expiration Date',
            'phone': 'Phone Number',
            'status': 'Status',
        }

    def clean_dob(self):
        data = self.cleaned_data.get('dob')
        if str(data) > str(datetime.datetime.today().date()):
            raise forms.ValidationError(
                'you can\'t add future date')
        elif (datetime.datetime.today().date() - data) < datetime.timedelta(days=18*365):
            raise forms.ValidationError(
                'Driving License owner must be 18 years old and above')
        return data

   # def clean_expd(self):
    #    data = self.cleaned_data.get('expd')
     #   if str(data) < str(datetime.datetime.today().date()):
      #      raise forms.ValidationError(
       #         'your driving license has expired')
        #return data
    
    def clean_dln(self):
        data1 = self.cleaned_data.get('dln')
        if len(data1) != 16:
            raise forms.ValidationError(
                'Driving license number must be 16 numbers')
        if data1.isdecimal() == False:
            raise forms.ValidationError(
                'Driving license number must contain numbers only')
        return data1
    
    def clean_class1(self):
        data1 = self.cleaned_data.get('class1')
        check1 = bool(re.match('^[A,B,C,D,D1,E,F]+$', data1))
        if check1 == False:
            raise forms.ValidationError(
                'The valid classes are: "A","B","C","D","D1","E","F"')
        return data1

class UpdateForm2(ModelForm):
    class Meta:
        model = License
        fields = ['dln', 'name', 'dob', 'class1', 'sex', 'phone', 'action']
        exclude = ['place','group1', 'status', 'date_added_on', 'declared_on', 'returned_on', 'found_on', 'expd']

        widgets = {
            'dob': TextInput(attrs={'class':'form-control', 'type':'date'}),
           # 'expd': TextInput(attrs={'class':'form-control', 'type':'date'}),
            'class1': TextInput(attrs={'class':'form-control', 'placeholder':'Hint: A,B,...'})
        }

        labels = {
            'dln': 'Driving License Number',
            'name':'Name',
            'dob': 'Date of Birth',
            'class1': 'Class',
            'sex': 'Gender',
           # 'expd': 'Expiration Date',
            'phone': 'Phone Number',
            'action': 'Action',
        }

    def clean_dob(self):
        data = self.cleaned_data.get('dob')
        if str(data) > str(datetime.datetime.today().date()):
            raise forms.ValidationError(
                'you can\'t add future date')
        elif (datetime.datetime.today().date() - data) < datetime.timedelta(days=18*365):
            raise forms.ValidationError(
                'Driving License owner must be 18 years old and above')
        return data

    #def clean_expd(self):
     #   data = self.cleaned_data.get('expd')
      #  if str(data) < str(datetime.datetime.today().date()):
       #     raise forms.ValidationError(
        #        'your driving license has expired')
        #return data
    
    def clean_dln(self):
        data1 = self.cleaned_data.get('dln')
        if len(data1) != 16:
            raise forms.ValidationError(
                'Driving license number must be 16 numbers')
        if data1.isdecimal() == False:
            raise forms.ValidationError(
                'Driving license number must contain numbers only')
        return data1
    
    def clean_class1(self):
        data1 = self.cleaned_data.get('class1')
        check1 = bool(re.match('^[A,B,C,D,D1,E,F]+$', data1))
        if check1 == False:
            raise forms.ValidationError(
                'The valid classes are: "A","B","C","D","D1","E","F"')
        return data1

class ReturnForm(ModelForm):
    class Meta:
        model = License
        fields = ['dln', 'name', 'dob', 'class1', 'sex', 'declared_on', 'phone']
        exclude = ['group1', 'place', 'status', 'action', 'date_added_on', 'returned_on', 'found_on', 'expd']

        widgets = {
            'dob': TextInput(attrs={'class':'form-control', 'type':'date'}),
            #'expd': TextInput(attrs={'class':'form-control', 'type':'date'}),
            'class1': TextInput(attrs={'class':'form-control', 'placeholder':'Hint: A,B,...'})
        }

        labels = {
            'dln': 'Driving License Number',
            'name':'Name',
            'dob': 'Date of Birth',
            'class1': 'Class',
            'sex': 'Gender',
          #  'expd': 'Expiration Date',
            'declared_on': 'Declared on',
            'phone': 'Phone Number',
        }

    def clean_dob(self):
        data = self.cleaned_data.get('dob')
        if str(data) > str(datetime.datetime.today().date()):
            raise forms.ValidationError(
                'you can\'t add future date')
        elif (datetime.datetime.today().date() - data) < datetime.timedelta(days=18*365):
            raise forms.ValidationError(
                'Driving License owner must be 18 years old and above')
        return data

   # def clean_expd(self):
    #    data = self.cleaned_data.get('expd')
     #   if str(data) < str(datetime.datetime.today().date()):
      #      raise forms.ValidationError(
       #         'your driving license has expired')
        #return data
    
    def clean_dln(self):
        data1 = self.cleaned_data.get('dln')
        if len(data1) != 16:
            raise forms.ValidationError(
                'Driving license number must be 16 numbers')
        if data1.isdecimal() == False:
            raise forms.ValidationError(
                'Driving license number must contain numbers only')
        return data1

    def clean_class1(self):
        data1 = self.cleaned_data.get('class1')
        check1 = bool(re.match('^[A,B,C,D,D1,E,F]+$', data1))
        if check1 == False:
            raise forms.ValidationError(
                'The valid classes are: "A","B","C","D","D1","E","F"')
        return data1        

class signupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_username(self):
        data1 = self.cleaned_data.get('username')
        for instance in User.objects.all():
            if instance.username == data1: 
                raise forms.ValidationError(
                    'Police station name: ' +data1+ ' exists for another account, give another name.')
        return data1

    def clean_email(self):
        data1 = self.cleaned_data.get('email')
        for instance in User.objects.all():
            if instance.email == data1: 
                raise forms.ValidationError(
                    'Email: ' +data1+ ' exists for another account, give another email.')
        return data1
class ContactForm(forms.Form):
    from_email = EmailField(widget=TextInput(attrs={'class': 'form-control', 'placeholder':'Injiza imeyili yanyu (email) *'}), required=True, label='')
    subject = CharField(widget=TextInput(attrs={'class': 'form-control', 'placeholder':'Injiza icyo ugendereye (subject) *'}), required=True, label='')
    message = CharField(widget=Textarea(attrs={'cols': 80, 'rows': 5, 'class': 'form-control','placeholder':'Injiza ubutumwa*'}), required=True, label='')