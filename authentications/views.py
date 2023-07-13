from django.shortcuts import render, redirect
from authentications.forms import *
from authentications.models import CustomUser, ChooseGroup
from django.contrib import messages
 
from django.contrib.auth import authenticate, login,logout


def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            
            user = form.save()
            user.save()
            return redirect('authentications:loggin')
    else:
        form = UserRegistrationForm()
    return render(request, 'authentications/signup.html', {'form': form})


def loggin(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_group_leader or user.is_staff:
                login(request, user)
                messages.info(request, 'Login successful')
                return redirect('authentications:group_leader_instructions')
            elif user is not None and user.is_group_member:
                login(request, user)
                messages.info(request, 'Login successful')
                return redirect('authentications:group_member_instructions')
            elif user is not None and user.is_personal:
                login(request, user)
                messages.info(request, 'Login successful')
                return redirect('authentications:personal_user_instructions')
            
            messages.info(request, 'Invalid data')
            return redirect('authentications:loggin')
    else:
        form = LoginForm(request)
    return render(request, 'authentications/login.html', {'form': form})

def register_company(request):
    user=request.user
    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            save_group= form.save(commit = False)
            save_group.created_by=user
            save_group.save()
            
            return redirect('index')
    else:
        form = CompanyRegistrationForm()
    return render(request, 'authentications/companyform.html', {'form': form})

def editgroup(request, group_id):
    group = CompanyModel.objects.get(id=group_id)
    user = request.user
    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST, request.FILES, instance=group)
        if form.is_valid():
            
            save_group = form.save(commit=False)
            save_group.created_by = user
            save_group.save()
            return redirect('index')
   
       
    form = CompanyRegistrationForm(instance=group)
    return render(request, 'authentications/edit_group.html', {'form': form})



def choose_your_group(request):
    user = request.user
    if request.method == 'POST':
        form = GroupSelectionForm(request.POST)
        if form.is_valid():
            if user.is_group_member:
                group = form.cleaned_data['group']
                ChooseGroup.objects.get_or_create(group = group, user = user)
                messages.info(request, f'{group} choosed!!!')
                return redirect('index')
            messages.error(request, 'You dont belong to any group.')
            return redirect('index')
        form.save()
        messages.success(request, f'{group} added register successful')
        return redirect('index')
    form = GroupSelectionForm()
    context ={
        'form':form
    }
    return render(request, 'authentications/choosegroupform.html', context)
           

def signout(request):
    logout(request)
    messages.info(request, 'You just logged out, login again!')
    return redirect('authentications:loggin')


def personal_user_instructions(request):
    return render(request, 'authentications/personal_user_instruction.html', {})

def group_leader_instructions(request):
    return render(request, 'authentications/group_leader_instruction.html', {})

def group_member_instructions(request):
    return render(request, 'authentications/group_members.html', {})

# def list_of_people_in_group(request, group_id):
    
    
