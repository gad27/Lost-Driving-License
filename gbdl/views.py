from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import * 
from .forms import *
from .filters import LicenseFilter
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import *
from django.forms import forms
import datetime
from .utils import *
from django.template.loader import get_template
from gbdl.models import License
from django.contrib.auth import get_user_model
from django.core.mail import send_mail, BadHeaderError
from GBDL1.utils.email_utils import send_simple_text_email
from GBDL1.settings import EMAIL_HOST_USER
from django.core.paginator import Paginator

# Create your views here.

@login_required(login_url='login')
@allowed_users(allowed_roles=['super admin', 'admin'])
def homeAdmin(request):
    licenses = License.objects.all()
    total_licenses = licenses.count()
    non_declared = licenses.filter(status='NOT DECLARED', group1='FOUND').count()
    non_declared_list = licenses.filter(status='NOT DECLARED', group1='FOUND')
    paginator = Paginator(non_declared_list, 2)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    declared = licenses.filter(status='DECLARED', action='IN STOCK').count()
    declared_list = licenses.filter(status='DECLARED', action='IN STOCK')
    paginator = Paginator(declared_list, 2)
    page = request.GET.get('page')
    posts1 = paginator.get_page(page)
    lost = licenses.filter(group1='LOST', status='NOT DECLARED').count()
    lost_list = licenses.filter(group1='LOST', status='NOT DECLARED')
    paginator = Paginator(lost_list, 2)
    page = request.GET.get('page')
    posts2 = paginator.get_page(page)
    returned = licenses.filter(action='RETURNED').count()
    returned_list = licenses.filter(action='RETURNED')
    paginator = Paginator(lost_list, 2)
    page = request.GET.get('page')
    posts3 = paginator.get_page(page)
    context = {'licenses':licenses, 'total_licenses':total_licenses, 'non_declared':non_declared, 'non_declared_list':posts, 'declared':declared,
     'declared_list':posts1, 'lost':lost, 'lost_list':posts2, 'returned':returned, 'returned_list':posts3}
    return render(request, 'gbdl/dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['super admin', 'admin'])
def license(request):
    licenses = License.objects.all().order_by('name')
    non_declared_list = licenses.filter(status='NOT DECLARED', group1='FOUND')
    myFilter = LicenseFilter(request.GET, queryset=non_declared_list)
    licenses = myFilter.qs
    paginator = Paginator(licenses, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    context = {'non_declared_list':posts, 'myFilter':myFilter}
    return render(request, 'gbdl/license.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['super admin', 'admin'])
def license1(request):
    licenses = License.objects.all().order_by('declared_on')
    declared_list = licenses.filter(status='DECLARED', action='IN STOCK')
    myFilter = LicenseFilter(request.GET, queryset=declared_list)
    licenses = myFilter.qs
    paginator = Paginator(licenses, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    context = {'declared_list':posts, 'myFilter':myFilter}
    return render(request, 'gbdl/license1.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['super admin', 'admin'])
def license2(request):
    licenses = License.objects.all().order_by('name')
    lost_list = licenses.filter(group1='LOST', status='NOT DECLARED')
    myFilter = LicenseFilter(request.GET, queryset=lost_list)
    licenses = myFilter.qs
    paginator = Paginator(licenses, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    context = {'lost_list':posts, 'myFilter':myFilter}
    return render(request, 'gbdl/license2.html', context)

#@login_required(login_url='login')
#@allowed_users(allowed_roles=['super admin', 'admin'])
#def license3(request):
 #   licenses = License.objects.all()
  #  found_list = licenses.filter(group1='FOUND', status='DECLARED')
   # myFilter = LicenseFilter(request.GET, queryset=found_list)
   # licenses = myFilter.qs
    #paginator = Paginator(licenses, 10)
    #page = request.GET.get('page')
    #posts = paginator.get_page(page)
    #context = {'found_list':posts, 'myFilter':myFilter}
    #return render(request, 'gbdl/license3.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['super admin', 'admin'])
def license4(request):
    licenses = License.objects.all().order_by('returned_on')
    returned_list = licenses.filter(action='RETURNED')
    myFilter = LicenseFilter(request.GET, queryset=returned_list)
    licenses = myFilter.qs
    paginator = Paginator(licenses, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    context = {'returned_list':posts, 'myFilter':myFilter}
    return render(request, 'gbdl/license4.html', context)

#Create
@login_required(login_url='login')
@allowed_users(allowed_roles=['super admin', 'admin'])
def create(request):
    # initial_data = {
    #     'status':"NOT DECLARED" 
    #     }
    form = CreateForm()
    if request.method == 'POST':
        form = CreateForm(request.POST)
        if form.is_valid():
            create_doc = form.save(commit=False)
            create_doc.user = request.user
            create_doc.group1 = 'FOUND'
            create_doc.place = 'Kigali'
            create_doc.status = 'NOT DECLARED'
            create_doc.action = 'IN STOCK'
            create_doc.date_added_on =  datetime.datetime.now()
            create_doc.found_on =  datetime.datetime.now()
            create_doc.save()
            messages.success(request, 'You have successfully added the found license')
            return redirect('license')
    context = {'form':form}
    return render(request, 'gbdl/create.html', context)

#Details
@login_required(login_url='login')
@allowed_users(allowed_roles=['super admin', 'admin'])
def details(request, pk):
    licenses = License.objects.get(id=pk)
    i = licenses
    context = {'i':i}
    return render(request, 'gbdl/details.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['super admin', 'admin'])
def details_declared(request, pk):
    licenses = License.objects.get(id=pk)
    i = licenses
    context = {'i':i}
    return render(request, 'gbdl/details_declared.html', context)

#@login_required(login_url='login')
#@allowed_users(allowed_roles=['super admin', 'admin'])
#def review1(request, pk):
 #   licenses = License.objects.get(id=pk)
  #  i = licenses
   # context = {'i':i}
    #return render(request, 'gbdl/review.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['super admin', 'admin'])
def details_lost(request, pk):
    licenses = License.objects.get(id=pk)
    i = licenses
    context = {'i':i}
    return render(request, 'gbdl/details_lost.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['super admin', 'admin'])
def details_returned(request, pk):
    licenses = License.objects.get(id=pk)
    i = licenses
    context = {'i':i}
    return render(request, 'gbdl/details_returned.html', context)

def home(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                # send_simple_text_email(subject, '%s message is: %s' %(from_email, message), ['tusifu@yopmail.com'])
                send_mail(subject, '%s message is: %s' %(from_email, message), from_email, ['niyongadgsinai@gmail.com'],fail_silently=False,)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return render(request, "gbdl/home_layout.html")
    return render(request, "gbdl/home_layout.html", {'form': form})

def details_declared_user(request, pk):
    licenses = License.objects.get(id=pk)
    i = licenses
    context = {'i':i}
    return render(request, 'gbdl/details_user_declare.html', context)

#Update
@login_required(login_url='login')
@allowed_users(allowed_roles=['super admin', 'admin'])
def update_license(request, pk):
    licenses = License.objects.get(id=pk)
    form = UpdateForm(instance=licenses)
    if request.method == 'POST':
        form = UpdateForm(request.POST, instance=licenses)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully Updated the license with name of ' + licenses.name)
            return redirect('dashboard')
    context = {'form': form}
    return render(request, 'gbdl/updateForm.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['super admin', 'admin'])
def update_license_status(request, pk):
    licenses = License.objects.get(id=pk)
    form = UpdateForm1(instance=licenses)
    if request.method == 'POST':
        form = UpdateForm1(request.POST, instance=licenses)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully Updated the license with name of ' + licenses.name)
            return redirect('dashboard')
    context = {'form': form}
    return render(request, 'gbdl/updateStatusForm.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['super admin', 'admin'])
def update_license_action(request, pk):
    licenses = License.objects.get(id=pk)
    form = UpdateForm2(instance=licenses)
    if request.method == 'POST':
        form = UpdateForm2(request.POST, instance=licenses)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully Updated the license with name of ' + licenses.name)
            return redirect('dashboard')
    context = {'form': form}
    return render(request, 'gbdl/updateActionForm.html', context)    

@login_required(login_url='login')
@allowed_users(allowed_roles=['super admin', 'admin'])
def delete(request, pk):
    licenses = License.objects.get(id=pk)
    if request.method == "POST":
        licenses.delete()
        messages.success(request, 'You have successfully Deleted the license')
        return redirect('dashboard')
    context = {'item':licenses}
    return render(request, 'gbdl/delete.html', context)

def user(request):
    licenses = License.objects.all().order_by('name')
    user_list = licenses.filter(group1='FOUND', status='NOT DECLARED')
    myFilter = LicenseFilter(request.GET, queryset=user_list)
    licenses = myFilter.qs
    paginator = Paginator(licenses, 20)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    context = {'user_list':posts, 'myFilter':myFilter}
    return render(request, 'gbdl/userlist.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['super admin', 'admin'])
def declare_license(request, pk):
    licenses = License.objects.get(id=pk)
    userName = request.user.username
    form = AdminDeclareForm(instance=licenses)
    if licenses.group1 == 'FOUND':
        licenses.status = "DECLARED"
        #form = DeclareForm(instance=licenses)
        if request.method == 'POST':
            form = DeclareForm(request.POST, instance=licenses)
            receiverNumber = request.POST['phone']
            receiverName = request.POST['name']
            receiverDln = request.POST['dln']
            if form.is_valid():
                licenses.declared_on = datetime.datetime.now()
                send_sms_to_reporter(receiverNumber, receiverName, receiverDln, userName )
                form.save()
                messages.success(request, 'You have successfully Declared the license')
                return redirect('declared')
    else:
       messages.info(request, 'LICENSE THAT IS NOT YET BEEN FOUND CAN NOT BE DECLARED')
    context = {'form': form}
    return render(request, 'gbdl/declareForm.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['super admin', 'admin'])
def return_license(request, pk):
    licenses = License.objects.get(id=pk)
    userName = request.user.username
    form = ReturnForm(instance=licenses)
    if licenses.group1 == 'FOUND':
        if licenses.status == 'DECLARED':
            licenses.action = "RETURNED"
            if request.method == 'POST':
                form = ReturnForm(request.POST, instance=licenses)
                receiverNumber = request.POST['phone']
                receiverName = request.POST['name']
                receiverDln = request.POST['dln']
                if form.is_valid():
                    licenses.returned_on = datetime.datetime.now()
                    send_sms_to_owner(receiverNumber, receiverName, receiverDln, userName )
                    form.save()
                    messages.success(request, 'You have successfully Returned the license')
                    return redirect('returned')
        else:
           messages.info(request, 'LICENSE THAT IS NOT YET DECLARED CAN NOT BE RETURNED')
        context = {'form': form}
        return render(request, 'gbdl/returnForm.html', context)
    else:
       messages.info(request, 'LICENSE THAT IS NOT YET FOUND CAN NOT BE DECLARED')
    context = {'form': form}
    return render(request, 'gbdl/returnForm.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['super admin', 'admin'])
def lost_license(request):
    # initial_data = {
    #     'status':"LOST" 
    #     }
    userName = request.user.username
    form = LostForm()
    if request.method == 'POST':
        form = AdminLostForm(request.POST)
        receiverNumber = request.POST['phone']
        receiverName = request.POST['name']
        receiverDln = request.POST['dln']
        if form.is_valid():
            lost_doc = form.save(commit=False)
            lost_doc.group1 = 'LOST'
            lost_doc.place = 'Kigali'
            lost_doc.status = 'NOT DECLARED'
            lost_doc.action = 'IN STOCK'
            lost_doc.date_added_on = datetime.datetime.now()
            send_sms_to_owner1(receiverNumber, receiverName, receiverDln, 'Muhima Traffic Police' )
            lost_doc.save()
            messages.success(request, 'You have successfully added a Lost license')
            return redirect('dashboard')
    context = {'form':form}
    return render(request, 'gbdl/lostForm.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['super admin', 'admin'])
def found_license(request, pk):
    licenses = License.objects.get(id=pk)
    userName = request.user.username
    licenses.group1 = "FOUND"
    form = FoundForm(instance=licenses)
    if request.method == 'POST':
        form = FoundForm(request.POST, instance=licenses)
        receiverNumber = request.POST['phone']
        receiverName = request.POST['name']
        receiverDln = request.POST['dln']
        if form.is_valid():
            found_doc = form.save(commit=False)
            found_doc.status = 'DECLARED'
            found_doc.found_on = datetime.datetime.now()
            found_doc.declared_on = datetime.datetime.now()
            send_sms_to_owner2(receiverNumber, receiverName, receiverDln, userName )
            form.save()
            messages.success(request, 'You have successfully added the license in submitted licenses')
            return redirect('declared')
    context = {'form': form}
    return render(request, 'gbdl/foundForm.html', context)

def declare_license_user(request, pk):
    licenses = License.objects.get(id=pk)
    userName = request.user.username
    form = DeclareForm(instance=licenses)
    if licenses.group1 == 'FOUND':
        licenses.status = "DECLARED"
        #form = DeclareForm(instance=licenses)
        if request.method == 'POST':
            form = DeclareForm(request.POST, instance=licenses)
            receiverNumber = request.POST['phone']
            receiverName = request.POST['name']
            receiverDln = request.POST['dln']
            if form.is_valid():
                licenses.declared_on = datetime.datetime.now()
                send_sms_to_reporter(receiverNumber, receiverName, receiverDln, userName )
                form.save()
                messages.success(request, 'Urakoze kumenyekanisha ko uru ruhushya rwo gutwara burundu ari urwanyu mu kanya murabona ubutumwa bugufi kuri telefone, bubamenyesha andi mabwiriza.')
                return redirect('user')
    else:
       messages.info(request, 'LICENSE THAT IS NOT YET FOUND CAN NOT BE DECLARED')
    context = {'form': form}
    return render(request, 'gbdl/declaretionFormUser.html', context)

def lost_license_user(request):
    # initial_data = {
    #     'status':"LOST" 
    #     }
    userName = request.user.username
    form = LostForm()
    if request.method == 'POST':
        form = LostForm(request.POST)
        receiverNumber = request.POST['phone']
        receiverName = request.POST['name']
        receiverDln = request.POST['dln']
        if form.is_valid():
            lost_doc = form.save(commit=False)
            lost_doc.group1 = 'LOST'
            lost_doc.place = 'Kigali'
            lost_doc.status = 'NOT DECLARED'
            lost_doc.action = 'IN STOCK'
            lost_doc.date_added_on = datetime.datetime.now()
            send_sms_to_owner1(receiverNumber, receiverName, receiverDln, 'Muhima Traffic Police' )
            lost_doc.save()
            messages.success(request, 'Murakoze kumenyekanisha uruhushya rwo gutwara burundu rwabuze, murabona ubutumwa bugufi kuri telefone bubabwira andi mabwiriza.')
            return redirect('user')
    context = {'form':form}
    return render(request, 'gbdl/lostFormUser.html', context)


    #Login & SignUp
    #AUTHENTICATION
@unaunthenticated_user
def login_view(request): 
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, 'Police Station Name OR password is Incorrect')
    context = {}
    return render(request, 'gbdl/login.html', context)


@login_required(login_url='login')
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')

@login_required(login_url='login')
@allowed_users(allowed_roles=['super admin'])
def signup_view(request):
    form = signupForm()
    if request.method == 'POST':
        form = signupForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='admin')
            user.groups.add(group)
            messages.success(request, 'Account was created for ' + username)
            return redirect('login')
    context = {'form':form}
    return render(request, 'gbdl/signup.html', context)

#Report
@login_required(login_url='login')
@allowed_users(allowed_roles=['super admin', 'admin'])
def report(request):
   # licenses = License.objects.all().order_by('name')
    try:
        type1 = request.GET.get('s')
        fromdate = request.GET.get('fromdate')
        todate = request.GET.get('todate')
        fromdate1 = request.GET.get('fromdate1')
        todate1 = request.GET.get('todate1')
        fromdate2 = request.GET.get('fromdate2')
        todate2 = request.GET.get('todate2')
    
    except:
        type1 = None
    if type1:
        q = str(type1)
        if type1 == 'NOT DECLARED':
            results = License.objects.raw('select id,dln,name,class1,status,date_added_on from gbdl_license where status = "NOT DECLARED" and group1= "FOUND" and date_added_on between "'+fromdate+'" and "'+todate+'"')
        #return render(request, 'gbdl/nondReport.html', {"results":results})
        if type1 == 'DECLARED':
            if fromdate:
                results = License.objects.raw('select id,dln,name,class1,status,date_added_on from gbdl_license where status = "DECLARED" and action = "IN STOCK" and date_added_on between "'+fromdate+'" and "'+todate+'"')

        if type1 == 'DECLARED':
            if fromdate1:
                results = License.objects.raw('select id,dln,name,class1,status,date_added_on from gbdl_license where status = "DECLARED" and action = "IN STOCK" and declared_on between "'+fromdate1+'" and "'+todate1+'"') 
        
        if type1 == 'DECLARED':
            if fromdate:
                if fromdate1:
                    results = License.objects.raw('select id,dln,name,class1,status,date_added_on from gbdl_license where status = "DECLARED" and date_added_on between "'+fromdate+'" and "'+todate+'" and declared_on between "'+fromdate1+'" and"'+todate1+'" ')
        if type1 == 'LOST':
            results = License.objects.raw('select id,dln,name,class1,status,date_added_on from gbdl_license where group1 = "LOST" and date_added_on between "'+fromdate+'" and "'+todate+'"')
        
        if type1 == 'RETURNED':
            if fromdate:
                results = License.objects.raw('select id,dln,name,class1,status,date_added_on from gbdl_license where action = "RETURNED" and date_added_on between "'+fromdate+'" and "'+todate+'"')

        if type1 == 'RETURNED':
            if fromdate:
                if fromdate1:
                    results = License.objects.raw('select id,dln,name,class1,status,date_added_on from gbdl_license where action = "RETURNED" and date_added_on between "'+fromdate+'" and "'+todate+'" and declared_on between "'+fromdate1+'" and"'+todate1+'"')

        if type1 == 'RETURNED':
            if fromdate:
                if fromdate2:
                    results = License.objects.raw('select id,dln,name,class1,status,date_added_on from gbdl_license where action = "RETURNED" and date_added_on between "'+fromdate+'" and "'+todate+'" and returned_on between "'+fromdate2+'" and "'+todate2+'"')
        if type1 == 'RETURNED':
            if fromdate:
                if fromdate1:
                    if fromdate2:
                        results = License.objects.raw('select id,dln,name,class1,status,date_added_on from gbdl_license where action = "RETURNED" and date_added_on between "'+fromdate+'" and "'+todate+'" and declared_on between "'+fromdate1+'" and"'+todate1+'" and returned_on between "'+fromdate2+'" and "'+todate2+'"')

        if type1 == 'RETURNED':
            if fromdate1:
                results = License.objects.raw('select id,dln,name,class1,status,date_added_on from gbdl_license where action = "RETURNED" and declared_on between "'+fromdate1+'" and"'+todate1+'"')

        if type1 == 'RETURNED':
            if fromdate1:
                if fromdate2:
                    results = License.objects.raw('select id,dln,name,class1,status,date_added_on from gbdl_license where action = "RETURNED" and declared_on between "'+fromdate1+'" and"'+todate1+'" and returned_on between "'+fromdate2+'" and "'+todate2+'"')

        if type1 == 'RETURNED':
            if fromdate2:
                results = License.objects.raw('select id,dln,name,class1,status,date_added_on from gbdl_license where action = "RETURNED" and returned_on between "'+fromdate2+'" and "'+todate2+'"')
        
        #return render(request, 'gbdl/fullReport.html', {"results":results})
        date1 = datetime.datetime.now()
        context = {'results':results, 'date1':date1, 'userName':request.user.username, 'type1':type1, 'fromdate':fromdate, 'todate':todate, 'fromdate1':fromdate1, 'todate1':todate1, 'fromdate2':fromdate2, 'todate2':todate2}
        template = get_template('gbdl/testpdf.html')
        html = template.render(context)
        pdf= render_to_pdf('gbdl/testpdf.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            file_name = "GDBL Report for %s Licenses" %(type1)
            content = "inline; filename='%s'" %(file_name)
            download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(file_name)
        response['Content-Disposition'] = content
        return response
        return HttpResponse*"Not found"
    else:
       return render(request, 'gbdl/report.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['super admin', 'admin'])
def report1(request):
    try: 
        type1 = request.GET.get('c')
        #type2 = request.GET.get('lost')
        #type3 = request.GET.get('d')
        #type4 = request.GET.get('return')
        fromdate = request.GET.get('fromdate')
        todate = request.GET.get('todate')
        fromdate1 = request.GET.get('fromdate1')
        todate1 = request.GET.get('todate1')
        fromdate2 = request.GET.get('fromdate2')
        todate2 = request.GET.get('todate2')
    except:
        fromdate = None
    if type1 == 'NOT DECLARED':
        if type1 == 'LOST':
            if type1 == 'DECLARED':
                if type1 == 'RETURNED':
                    results = License.objects.raw('select id,dln,name,class1,status,date_added_on from gbdl_license where date_added_on between "'+fromdate+'" and "'+todate+'"')

    if type1 == 'NOT DECLARED':
        if type1 == 'LOST':
            results = License.objects.raw('select id,dln,name,class1,status,date_added_on from gbdl_license where status = "NOT DECLARED" or group1= "LOST" and date_added_on between "'+fromdate+'" and "'+todate+'"')

    if type1 == 'NOT DECLARED':
        if type1 == 'LOST':
            if type1 == 'DECLARED':
                results = License.objects.raw('select id,dln,name,class1,status,date_added_on from gbdl_license where action = "IN STOCK" and date_added_on between "'+fromdate+'" and "'+todate+'"')

    if type1 == 'NOT DECLARED':
        if type1 == 'DECLARED':
                results = License.objects.raw('select id,dln,name,class1,status,date_added_on from gbdl_license where status = "NOT DECLARED" or status = "DECLARED" and action = "IN STOCK" and date_added_on between "'+fromdate+'" and "'+todate+'"')

    if type1 == 'NOT DECLARED':
        if type1 == 'RETURNED':
            results = License.objects.raw('select id,dln,name,class1,status,date_added_on from gbdl_license where (status = "NOT DECLARED" and group1 = "FOUND") or action= "RETURNED" and date_added_on between "'+fromdate+'" and "'+todate+'"')

    if type1 == 'LOST':
        if type1 == 'DECLARED':
            if type1 == 'RETURNED':
                results = License.objects.raw('select id,dln,name,class1,status,date_added_on from gbdl_license where (action = "IN STOCK" and group1 = "LOST") or action= "RETURNED" or (action = "IN STOCK" and status = "DECLARED") and date_added_on between "'+fromdate+'" and "'+todate+'"')

    if type1 == 'LOST':
        if type1 == 'DECLARED':
            results = License.objects.raw('select id,dln,name,class1,status,date_added_on from gbdl_license where (status = "NOT DECLARED" and group1= "LOST") or (status = "DECLARED" and action = "IN STOCK" and date_added_on between "'+fromdate+'" and "'+todate+'"')

    if type1 == 'LOST':
        if type1 == 'RETURNED':
            results = License.objects.raw('select id,dln,name,class1,status,date_added_on from gbdl_license where (status = "NOT DECLARED" and group1= "LOST") or action = "RETURNED" and date_added_on between "'+fromdate+'" and "'+todate+'"')

    if type1 == 'NOT DECLARED':
        results = License.objects.raw('select id,dln,name,class1,status,date_added_on from gbdl_license where (status = "NOT DECLARED" and group1= "FOUND") and date_added_on between "'+fromdate+'" and "'+todate+'"')

    if type1 == 'LOST':
        results = License.objects.raw('select id,dln,name,class1,status,date_added_on from gbdl_license where (status = "NOT DECLARED" and group1= "LOST") and date_added_on between "'+fromdate+'" and "'+todate+'"')

    if type1 == 'DECLARED':
        results = License.objects.raw('select id,dln,name,class1,status,date_added_on from gbdl_license where (status = "DECLARED" or action= "IN STOCK" and date_added_on between "'+fromdate+'" and "'+todate+'"')

    if type1 == 'RETURNED':
        results = License.objects.raw('select id,dln,name,class1,status,date_added_on from gbdl_license where action = "RETURNED" and date_added_on between "'+fromdate+'" and "'+todate+'"')

        date1 = datetime.datetime.now()
        context = {'results':results, 'date1':date1, 'userName':request.user.username, 'type1':type1, 'fromdate':fromdate, 'todate':todate, 'fromdate1':fromdate1, 'todate1':todate1, 'fromdate2':fromdate2, 'todate2':todate2}
        template = get_template('gbdl/testpdf.html')
        html = template.render(context)
        pdf= render_to_pdf('gbdl/testpdf.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            file_name = "GDBL Report for %s Licenses" %(type1)
            content = "inline; filename='%s'" %(file_name)
            download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(file_name)
        response['Content-Disposition'] = content
        return response
        return HttpResponse*"Not found"
    else:
       return render(request, 'gbdl/report.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['super admin', 'admin'])
def chart(request):
    licenses = License.objects.all()
    total_licenses = licenses.count()
    non_declared = licenses.filter(status='NOT DECLARED', group1='FOUND').count()
    declared = licenses.filter(status='DECLARED', action='IN STOCK').count()
    lost = licenses.filter(group1='LOST', status='NOT DECLARED').count()
    returned = licenses.filter(action='RETURNED').count()
    context = {'licenses':licenses, 'total_licenses':total_licenses, 'non_declared':non_declared, 'declared':declared, 
    'lost':lost, 'returned':returned}
    return render(request, 'gbdl/charts.html', context)


def send_sms_to_reporter(receiver, name, dln, username):   
    message = f'Kuri ' + name +',' \
        ' Mumaze kumenyekanisha ko uruhushya rwo gutwara burundu rwari rwarabuze rufite numero ' + dln + ' ari urwanyu,gana ' + username + ' ubone icyangombwa cyawe.'\
        ' Murakoze.'    
    print(username)
    License.send_sms(receiver, message)

def send_sms_to_owner(receiver, name, dln, username):
    message = f'Kuri ' + name +',' \
        ' Uruhushya rwo gutwara burundu wamenyekanishije ko ari urwawe rufite numero ' + dln + ' wamaze kurufata kuri ' + username + ' Murakoze.'
    License.send_sms(receiver, message)

def send_sms_to_owner1(receiver, name, dln, username):
    message = f'Kuri ' + name +',' \
        ' Murakoze kumenyekanisha ko uruhushya rwo gutwara burundu  rufite numero ' + dln + ' rwatakaye, niruboneka muzohererezwa ubutumwa bugufi bubabwira Station Ya Police rubitseho. gana ' + username +\
        ' Kubundi bufasha.'
    License.send_sms(receiver, message)

def send_sms_to_owner2(receiver, name, dln, username):
    message = f'Kuri ' + name +',' \
        ' Uruhushya rwo gutwara burundu mwari mwaramenyekanishije ko rwabuze rufite numero ' + dln + ' rwabonetse, gana ' + username + ' ubone icyangombwa cyawe.'
    License.send_sms(receiver, message)
  