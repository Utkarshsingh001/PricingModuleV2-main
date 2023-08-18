from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404, render , redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from datetime import datetime
import math
from authentication.models import Pricing_Module, Week_Table ,TMF
import os
import csv
import zipfile


# Create your views here.
def home(request):
    return render(request ,"authentication/index.html")

def signup(request):
    if request.method == 'POST':
        username = request.POST["username"]
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

 

        if User.objects.filter(username=username):
            messages.error(request , "Username already exist ! Please try some other username")
            return redirect(home)
        if User.objects.filter(email=email):
            messages.error(request ,"Email already exist " )
            return redirect(home)

        if pass1 != pass2:
            messages.error(request , "Passswords do not match , Please check the passowrd and try again")
            return redirect('home')

        if not username.isalnum():
            messages.error(request , "Username must be alpha numeric")
            return redirect(home)

        myuser = User.objects.create_user(username , email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request , "Your account has been succesfully created")
        return redirect("signin")
    return render(request ,"authentication/signup.html")


def signin(request):

    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username = username ,password=pass1)
        global x
        x = user.first_name
        if user is not None:
            login(request,user)
            fname = user.first_name
            
            return render(request , "authentication/index.html" ,{'fname':fname})

        else:
            messages.error(request ,"Bad Credentials!")
    return render(request ,"authentication/signin.html")

def signout(request):
    logout(request)
    messages.success(request,"logged out successfully")
    return redirect('home')
    
def dashboard(request):
    query_results = Pricing_Module.objects.all()
    fullobj={}
    activequeue=[]
    for item in query_results:
        objdict={
            "mod_id":item.mod_id,
            "dbp_price":item.dbp_price,
            "dbp_km":item.dbp_km,
            "dap":item.dap,
            "waiting_time":item.waiting_time,
            "waiting_charge":item.waiting_charge,
            "status":item.status,
            "usermodifiedby":item.usermodifiedby,
            "timestamp":item.created_at,
            }
        if item.status == True:
            activequeue.append(item.mod_id)
        days = Week_Table.objects.filter(mod_id=item.mod_id)
        dayarray=[]
        for day in days:
            dayarray.append(day.weekday)
        objdict["weekdays"]=dayarray
        tmf = TMF.objects.filter(mod_id=item.mod_id)
        timearray =[]
        timedictionary={}
        for t in tmf:
            timedictionary={
                t.hour:t.factor,
            }
            timearray.append(timedictionary)
        objdict["TMF"] = timearray
        fullobj[f"{item.mod_id}"]=objdict
    #active/nonactive
    print(activequeue)
    
    return render(request , 'authentication/dashboard.html',{"fullobj":fullobj})

def addform(request):
    if request.method == "POST":
        new_instance = Pricing_Module()
        new_instance.dbp_price = request.POST['dbp_price']
        new_instance.dbp_km = request.POST['dbp_km']
        weekdays = request.POST.getlist('option')
        new_instance.dap = request.POST['dap']
        TMF_time = request.POST.getlist('time[]')
        TMF_factor = request.POST.getlist('factor[]')
        new_instance.waiting_time = request.POST['waiting_time']
        new_instance.waiting_charge = request.POST['waiting_charge']
        new_instance.status = False
        if request.user.is_authenticated:
            user = request.user
        new_instance.usermodifiedby = user.first_name
        new_instance.save()
        instances = []
        for day in weekdays:
            instances.append(Week_Table(mod_id = new_instance , weekday = day))
        Week_Table.objects.bulk_create(instances)
        secondinstances = []
        for item1,item2 in zip(TMF_time, TMF_factor):
            secondinstances.append(TMF(mod_id = new_instance, hour = item1, factor = item2))
        TMF.objects.bulk_create(secondinstances)
        return redirect('dashboard')
    return render(request , "authentication/addform.html")

def edit_object(request,pk):
    obj = get_object_or_404(Pricing_Module,pk=pk)
    if request.user.is_authenticated:
        user = request.user
        if request.method == "POST":
            obj.delete()
            new_instance = Pricing_Module()
            new_instance.dbp_price = request.POST['dbp_price']
            new_instance.dbp_km = request.POST['dbp_km']
            weekdays = request.POST.getlist('option')
            new_instance.dap = request.POST['dap']
            TMF_time = request.POST.getlist('time[]')
            TMF_factor = request.POST.getlist('factor[]')
            new_instance.waiting_time = request.POST['waiting_time']
            new_instance.waiting_charge = request.POST['waiting_charge']
            new_instance.created_at = datetime.now()
            new_instance.status = False
            if request.user.is_authenticated:
                user = request.user
            new_instance.usermodifiedby = user.first_name
            new_instance.save()
            instances = []
            for day in weekdays:
                instances.append(Week_Table(mod_id = new_instance , weekday = day))
            Week_Table.objects.bulk_create(instances)
            secondinstances = []
            for item1,item2 in zip(TMF_time, TMF_factor):
                secondinstances.append(TMF(mod_id = new_instance, hour = item1, factor = item2))
            TMF.objects.bulk_create(secondinstances)
            return redirect('dashboard')
    return render(request, 'authentication/editform.html')

def delete_object(request,pk):
    obj = get_object_or_404(Pricing_Module,pk=pk)
    print("inside obj")
    if request.user.is_authenticated:
        user = request.user
        print("inside user")
        if request.method == "POST":
            print(request.POST['confirmation'])
            if request.POST['confirmation'] == 'yes':
                obj.delete()
            return redirect('dashboard')
    return render(request,"authentication/deleteconfirmation.html")


def deactivate_item(request,pk):
    if request.method == "POST":
        if request.POST['confirmation'] == 'yes':
            querry = Pricing_Module.objects.get(mod_id = pk)
            new_status = False
            querry.status = new_status
            querry.save()
            return redirect('dashboard')
        else:
            return redirect('dashboard')
    
    return render(request,"authentication/deactivate.html")

def activate_item(request,pk):

    if request.method == "POST":
        if request.POST['confirmation'] == 'yes':
            querys = Pricing_Module.objects.filter(status=True)
            actives_object = []
            for query in querys:
                actives_object.append(query)

            # lets create active objects list of days
            weeklist1 =[]
            for object in actives_object:
                q = Week_Table.objects.filter(mod_id = object.mod_id)
                for i in q :
                    weeklist1.append(i.weekday)
            q2 = Week_Table.objects.filter(mod_id = pk)
            weeklist2 = []
            for item in q2:
                weeklist2.append(item.weekday)
            
            
            #merge and compare the list now 
            going_to_active_queue = weeklist1 + weeklist2
            print(going_to_active_queue)
            if len(going_to_active_queue) == len(set(going_to_active_queue)):
                change = Pricing_Module.objects.get(mod_id = pk)
                new_status = True
                change.status = new_status
                change.save()
                return redirect('dashboard')
            else:
                messages.error(request , "The Pricing Module Is Already Active On The Given Day ")
                return redirect('dashboard')
        else:
            return redirect('dashboard')

    return render(request,"authentication/activate.html")


def drivers(request):
    if request.method == "POST":
        foundid = 0
        totaldistance = float(request.POST['total_dist'])
        day_of_week =request.POST['day']
        total_time = float(request.POST['time'])
        waiting_total_time = float(request.POST['waiting_time'])
        active_object = Pricing_Module.objects.filter(status=True)
        for items in active_object:
            qid = Week_Table.objects.filter(mod_id= items.mod_id)
            for i in qid:
                if i.weekday == day_of_week.title():
                   fid = i.mod_id
                   foundid = fid.mod_id
        moduleused = Pricing_Module.objects.get( mod_id= foundid)
        dbp_km = float(moduleused.dbp_km)
        dbp_price = float(moduleused.dbp_price)
        dap = float(moduleused.dap)
        waiting_time = moduleused.waiting_time
        waiting_charge = moduleused.waiting_charge
        
        #filter the TMF Table and get the dictionary
        tmf = TMF.objects.filter(mod_id=foundid)
        timearray =[]
        timedictionary={}
        thour = []
        tfactor = []
        for t in tmf:
            thour.append(t.hour)
            tfactor.append(t.factor)
        lowertimevalue = math.floor(float(total_time)) 
        if lowertimevalue == 0:
            tmfvalue = 1
        elif lowertimevalue in thour:
            tmfvalue = tfactor[thour.index(lowertimevalue)]
        else :
            tmfvalue = tfactor[thour.index(max(thour))]
        Dn = totaldistance - dbp_km
        quotient = waiting_total_time // waiting_time
        quotient -= 1
        final_pricing = ( dbp_price + (Dn * dap) + (total_time * tmfvalue ) + waiting_charge*quotient) 
        print(f"The Final Pricing is {final_pricing}")
        
    return render(request , "authentication/drivers.html")



@api_view(['POST'])
def calculation_price_api(request):
    foundid = 0
    totaldistance = float(request.data['total_dist'])
    day_of_week =request.data['day']
    total_time = float(request.data['time'])
    waiting_total_time = float(request.data['waiting_time'])
    active_object = Pricing_Module.objects.filter(status=True)
    for items in active_object:
        qid = Week_Table.objects.filter(mod_id= items.mod_id)
        for i in qid:
            if i.weekday == day_of_week.title():
                fid = i.mod_id
                foundid = fid.mod_id
    moduleused = Pricing_Module.objects.get( mod_id= foundid)
    dbp_km = float(moduleused.dbp_km)
    dbp_price = float(moduleused.dbp_price)
    dap = float(moduleused.dap)
    waiting_time = moduleused.waiting_time
    waiting_charge = moduleused.waiting_charge
    
    #filter the TMF Table and get the dictionary
    tmf = TMF.objects.filter(mod_id=foundid)
    timearray =[]
    timedictionary={}
    thour = []
    tfactor = []
    for t in tmf:
        thour.append(t.hour)
        tfactor.append(t.factor)
    lowertimevalue = math.floor(float(total_time)) 
    if lowertimevalue == 0:
        tmfvalue = 1
    elif lowertimevalue in thour:
        tmfvalue = tfactor[thour.index(lowertimevalue)]
    else :
        tmfvalue = tfactor[thour.index(max(thour))]
    Dn = totaldistance - dbp_km
    quotient = waiting_total_time // waiting_time
    quotient -= 1
    print(quotient)
    
    final_pricing = ( dbp_price + (Dn * dap) + (total_time * tmfvalue ) + waiting_charge*quotient)      
    print(final_pricing)
    return Response({'Pricing' , final_pricing})

def fetch_data(start_index, chunk_size):
    return Pricing_Module.objects.all()[start_index:start_index + chunk_size]

def generate_csv_chunk(data):
    rows = []
    for row in data:
        rows.append({
            'mod_id': row.mod_id,
            'dbp_price': row.dbp_price,
            'dbp_km':row.dbp_km,
            'dap':row.dap,
            'waiting_charge':row.waiting_charge,
            'waiting_time':row.waiting_time,
            'status':row.status,
            'usermodifiedby':row.usermodifiedby,
            'created_at':row.created_at
            # Add more fields as needed
        })
    return rows

def generate_csv_file(data, filename):
    with open(filename, mode='w', newline='') as file:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def clean_temp_directory(temp_dir):
    for root, _, files in os.walk(temp_dir):
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(root, file)
                os.remove(file_path)

def combine_csv_files(temp_dir):
    combined_data = []

    for root, _, files in os.walk(temp_dir):
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as csv_file:
                    reader = csv.DictReader(csv_file)
                    for row in reader:
                        combined_data.append(row)

    return combined_data

def download_combined_csv(request):
    temp_dir = 'temp_csv'
    combined_data = combine_csv_files(temp_dir)

    combined_csv_file = os.path.join(temp_dir, 'combined_data.csv')
    generate_csv_file(combined_data, combined_csv_file)

    with open(combined_csv_file, 'rb') as csv_file:
        response = HttpResponse(csv_file.read(), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=combined_data.csv'
        return response

def generate_and_download_csv(request):
    chunk_size = 3000
    total_rows = Pricing_Module.objects.count()

    # Create a temporary directory to store CSV files
    temp_dir = 'temp_csv'
    os.makedirs(temp_dir, exist_ok=True)

    clean_temp_directory(temp_dir)  # Clean the directory before generating CSVs

    for start_index in range(0, total_rows, chunk_size):
        data = fetch_data(start_index, chunk_size)
        csv_data = generate_csv_chunk(data)

        filename = os.path.join(temp_dir, f'data_{start_index}.csv')
        generate_csv_file(csv_data, filename)

    return download_combined_csv(request)

def download_page(request):
    return render(request, 'authentication/download.html')
