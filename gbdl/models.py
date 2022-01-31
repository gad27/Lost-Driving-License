from django.db import models
import datetime
import africastalking
from django.contrib.auth import get_user_model

# Create your models here.
    
class License(models.Model):
       
    GENDER = (
			('Gabo', 'Gabo'),
			('Gore', 'Gore'),
			)

    CATEGORY = (
			('LOST', 'LOST'),
			('FOUND', 'FOUND'),
			)
    
    STATU1 = (
			('NOT DECLARED', 'NOT DECLARED'),
			('DECLARED', 'DECLARED'),
			)
    
    ACTION1 = (
			('IN STOCK', 'IN STOCK'),
			('RETURNED', 'RETURNED'),
			)
    dln = models.CharField(max_length=16, null=True, default='1')
    name = models.CharField(max_length=200, null=True)
    dob = models.DateField(auto_now_add=False, auto_now=False, null=True)
    class1 = models.CharField(max_length=14, null=True)
    sex = models.CharField(max_length=4, choices=GENDER, null=True)
    expd = models.DateField(auto_now_add=False, auto_now=False, null=True)
    place = models.CharField(max_length=6,null=True)
    phone =models.CharField(max_length=15, null=False, blank=False, default='+250')
    group1 = models.CharField(max_length=6, choices=CATEGORY, null=True)
    status = models.CharField(max_length=50, choices=STATU1, null=True)
    action = models.CharField(max_length=8, choices=ACTION1, null=True)
    date_added_on = models.DateField(auto_now_add=True, auto_now=False, null=False, editable=False)
    found_on = models.DateField(auto_now_add=False, auto_now=False, null=True, editable=False)
    declared_on = models.DateField(auto_now_add=False, auto_now=False, null=True)
    returned_on = models.DateField(auto_now_add=False, auto_now=False, null=True, editable=False)
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name='license',default=1)
    def __str__(self):
	    return self.name



    @staticmethod
    def send_sms(phone_number , message):
        username = "tusifu"  # use 'sandbox' for development in the test environment
        api_key = "c1b79e7560de16b8aa9a43b7c31123f9b2148d4bb17a6d33a1dfcf95701f08b3"  # use your sandbox app API key for development in the test environment
        africastalking.initialize(username, api_key)
        # Initialize a service e.g. SMS
        sms = africastalking.SMS

        # Or use it asynchronously
        def on_finish(error, response):
            if error is not None:
                raise error
            print(response)
        response = sms.send(message, [phone_number], callback=on_finish)
        print(response)