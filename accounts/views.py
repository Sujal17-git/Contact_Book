from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from .models import CustomUser,Contact
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        dob = request.POST.get('date_of_birth')
        gender = request.POST.get('gender')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        # Create user with password
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password1,  # correct key
            date_of_birth=dob,
            gender=gender
        )

        return redirect('login')

    return render(request, 'accounts/register.html')
def login_view(request):
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request,username=username,password=password)

        if user:
            login(request,user)
            return redirect('dashboard')
        else:
            messages.error(request,'Invalid username or password')
            return redirect('login')

    return render(request,'accounts/login.html') 

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    if request.method =='POST':
        name = request.POST.get('name')
        mobile_no = request.POST.get('mobile_no')
        email = request.POST.get('email')
        city = request.POST.get('city')

        if name and mobile_no and email and city:
            Contact.objects.create(
                user = request.user,
                name = name,
                mobile_no= mobile_no,
                email = email,
                city = city,
            )
            return redirect('dashboard')
        
    contacts = Contact.objects.filter(user=request.user)
    return render(request,'accounts/dashboard.html',{'contacts':contacts})

@login_required
def update_contact(request,pk):
    contact = get_object_or_404(Contact,pk=pk)

    if request.method =='POST':
        contact.name = request.POST.get('name')
        contact.mobile_no = request.POST.get('mobile_no')
        contact.email = request.POST.get('email')
        contact.city = request.POST.get('city')
        contact.save()
        return redirect('dashboard')
    
    return render(request,'accounts/update_contact.html',{'contact':contact})


@login_required
def delete_contact(request,pk):
    contact = get_object_or_404(Contact,pk=pk,user=request.user)
    contact.delete()
    return redirect('dashboard')

def index(request):
    return render(request,'accounts/index.html')


