from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from .models import Property,Unit,Tenant,RentalInformation
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    pro=Property.objects.all()
    context={'pro':pro }
    return render(request,"home.html",context)

def register(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('pass1')
        confirm_password = request.POST.get('pass2')

        if password != confirm_password:
            messages.warning(request, "Passwords do not match")
            return render(request, "user/register.html")

        try:
            if User.objects.get(username=email):
                messages.warning(request, "Email is already taken")
                return render(request, 'user/register.html')
        except User.DoesNotExist:
            pass

        user = User.objects.create_user(username=email, password=password)
        messages.success(request, "Account created successfully. Please log in.")
        return redirect('login')

    return render(request, "user/register.html")


def handlelogin(request):
    if request.method=="POST":
        username=request.POST['email']
        userpassword=request.POST['pass1']
        myuser=authenticate(username=username,password=userpassword)
        if myuser is not None:
            login(request,myuser)
            messages.success(request,"Login Success")
            return redirect('home')
        else:
            messages.error(request,"something went wrong")
            return redirect('login')
        
    return render(request,"user/login.html")

def handlelogout(request):
    logout(request)
    messages.success(request,"Logout Success")
    return redirect('login')






@login_required(login_url="/login/")
def property_details(request,id):
    pro=Property.objects.filter(id=id).first()
    uni=Unit.objects.filter(id=id).first()
    context={'pro':pro,
             'uni':uni}
    return render(request,'user/single_property.html',context)

def admin_login(request):
    if request.method == 'POST':
        username=request.POST['email']
        userpassword=request.POST['pass1']
        user = authenticate(request, username=username, password=userpassword)
        if user is not None:
            login(request,user)
            messages.success(request,"Login Success")
            return redirect('sellproperty')
        else:
            messages.error(request, 'Invalid admin credentials.')
    return render(request, 'admin/admin_login.html')



def sellproperty(request):
    if request.method == 'POST':
        name = request.POST['name']
        address = request.POST['address']
        location = request.POST['location']
        features = request.POST['features']
        image = request.FILES.get('image') 

        property = Property(name=name,address=address,location=location,features=features,image=image)
        property.save()

        return redirect('home')
    return render(request,'admin/sellproperty.html')


def byproperty(request,id):
    return render(request,'user/byproperty.html')






@login_required(login_url="/login/")
def profile(request):
    return render(request, 'user/profile.html')


@login_required(login_url="/login/")  
def addprofile(request):
    if request.method == 'POST':
        name = request.POST['name']
        address = request.POST['address']
        document_proofs = request.POST['document_proofs']
        user = request.user
        profile = Tenant(name=name, address=address, document_proofs=document_proofs, user=user)
        profile.save()
    return render(request, 'user/addprofile.html')


def profiledetails(request):
    profile = Tenant.objects.all()
    context = {'profile': profile}
    return render(request, 'user/profiledetails.html', context)


def assigntenantunit(request):
    if request.method == 'POST':
        property_id = request.POST.get('property')
        unit_number = request.POST.get('unit_number')
        rent_cost = request.POST.get('rent_cost')
        unit_type = request.POST.get('unit_type')
        tenant_id = request.POST.get('tenant')

        property_instance = get_object_or_404(Property, id=property_id)
        tenant_instance = get_object_or_404(Tenant, id=tenant_id)

        unit = Unit.objects.create(
            property=property_instance,
            unit_number=unit_number,
            rent_cost=rent_cost,
            unit_type=unit_type,
            tenant=tenant_instance
        )

        agreement_end_date = request.POST.get('agreement_end_date')
        monthly_rent_date = request.POST.get('monthly_rent_date')

        RentalInformation.objects.create(
            unit=unit,
            agreement_end_date=agreement_end_date,
            monthly_rent_date=monthly_rent_date
        )

        return redirect('tenantprofile', id=tenant_instance.id)

    properties = Property.objects.all()
    tenants = Tenant.objects.all()
    return render(request, 'tenant_profile.html', {'properties': properties, 'tenants': tenants})






@login_required(login_url="/login/") 
def tenantprofile(request, id):
    tenant = get_object_or_404(Tenant, id=id, user=request.user)

    try:
        unit = Unit.objects.get(tenant=tenant)
        rental_info = RentalInformation.objects.get(unit=unit)
    except Unit.DoesNotExist:
        rental_info = None
    except RentalInformation.DoesNotExist:
        rental_info = None
    return render(request, 'tenantprofile.html', {'tenant': tenant, 'rental_info': rental_info})


def search(request):
    feature = request.GET.get('feature')
    units = Unit.objects.filter(property__features__icontains=feature)
    properties = Property.objects.filter(features__icontains=feature)
    return render(request, 'search.html', {'units': units, 'properties': properties})




def about(request):
    return render(request,'about.html')

def contactus(request):
    return render(request,'contact.html')

