from django.shortcuts import render, redirect, get_list_or_404
from . models import Task, TaskProject, Statusholder
from task.forms import CreatProjectForm, CreateTaskForm
from django.contrib import messages
from django.contrib.auth import logout
from task.tasks import send_reminder_emails
from authentications.models import ChooseGroup, CompanyModel, CustomUser

def index(request):
    user = request.user
    projects = TaskProject.objects.filter(user=user)
    tasks = Task.objects.filter(created_by=user)
    assigned_tasks = Task.objects.filter(assigned_to=user)

    if request.method == 'POST':
        task_id = request.POST.get('task_id', None)
        status = request.POST.get('status', None)
        
        if task_id and status in [choice[0] for choice in Task.STATUS_CHOICES]:
            try:
                task = Task.objects.get(id=task_id, assigned_to=user)
                task.status = status
                task.save()
                messages.success(request, 'Task status updated successfully.')
            except Task.DoesNotExist:
                messages.error(request, 'Task not found.')

    context = {
        'tasks': tasks,
        'projects': projects,
        'assigned': assigned_tasks,
    }
    return render(request, 'task/home.html', context)

def viewtask(request):
    user = request.user
    assigned = Task.objects.filter(assigned_to=user)
    assign= assigned.first()

    if request.method == 'POST':
        task_id = request.POST.get('task_id', None)
        status = request.POST.get('status', None)
        if task_id and status in [choice[0] for choice in Task.STATUS_CHOICES]:
            try:
                task = Task.objects.get(id=task_id, assigned_to=user)
                task.status = status
                task.save()
                messages.success(request, 'Task status updated successfully.')
            except Task.DoesNotExist:
                messages.error(request, 'Task not found.')
                
    # assigned_tasks = Task.objects.filter(assigned_to=user) 
    tasks = Task.objects.filter(created_by=user)       
    get_groups = CompanyModel.objects.filter(created_by=user)
    get_all_groups = []
    for group in get_groups:
        members = ChooseGroup.objects.filter(group=group)
        group.members = members
        get_all_groups.append(group)
        
    groupmember = ChooseGroup.objects.filter(user=user)
    

    context = {
        'assigned': assigned,
        'assign':assign,
        'all_groups':get_groups,
        'members':groupmember,
        'tasks':tasks
    }
    return render(request, 'task/dashboard.html', context)



def projectform(request):
    user = request.user
    if request.method == 'POST':
        form = CreatProjectForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            due_date = form.cleaned_data['due_date']
            
            create_project = TaskProject(name = name, description = description, 
                                         due_date=due_date, user=user)
            create_project.save()
            messages.success(request, f'You have add {name} successfully')
            return redirect('index')
        messages.error(request, 'Project not save')
        return redirect('projectform')
    form = CreatProjectForm()
    context = {
        'form':form,
    }
    return render(request, 'task/create_project.html', context)

def editproject(request, project_id):
    user = request.user
    projectid = TaskProject.objects.get(id = project_id)
    if request.method == 'POST':
        
        form = CreatProjectForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            due_date = form.cleaned_data['due_date']
            
            projectid.name=name
            projectid.description=description
            projectid.due_date =due_date
            projectid.user = user
            
            projectid.save()
           
            messages.success(request, f'You have updated {name} successfully')
            return redirect('index')
        messages.error(request, 'Project not save')
        return redirect('projectform')
    initial_data={
        'name':projectid.name,
        'description':projectid.description,
        'due_date':projectid.due_date,
    }
    form = CreatProjectForm(initial=initial_data)
    context = {
        'form':form,
    }
    return render(request, 'task/edit_project.html', context)

 
def assigntask(request, project_id):
    user = request.user
    project = TaskProject.objects.get(id=project_id)
    customusers = ChooseGroup.objects.filter(user=project.user)
    # send_reminder_emails.apply_async(countdown=60)
    
    if request.method == 'POST':
        form = CreateTaskForm(request.POST)
        if form.is_valid():
            assign_to = form.cleaned_data['assigned_to']
            task = form.save(commit=False)
            task.project = project
            task.assigned_to = assign_to
            task.created_by = user
            task.save()
            messages.success(request, 'You assigned a task successfully')
            return redirect('assigntask', project.id)

        else:
            messages.error(request, 'Form is not valid. Please check the errors.')
    else:
        initial_data = {
            'title': project.name,
            'description': project.description,
            'project': project
            
        }
        form = CreateTaskForm(initial=initial_data)
        # ass_task = project.task_set.all()
        form.fields['assigned_to'].queryset = CustomUser.objects.filter(choosegroup__group__created_by=project.user)

        form.fields['project'].queryset = TaskProject.objects.filter(user=user)

    context = {
        'form': form,
        'project': project,
    }
    return render(request, 'task/assignproject.html', context)
       
def deletetask(request, task_id):
    task_id = Task.objects.get(id = task_id)
    task_id.delete()
    messages.info(request, 'deleted!')
    
    return redirect('index')

def deleteproject(request, project_id):
    project_id = TaskProject.objects.get(id = project_id)
    project_id.delete()
    messages.info(request, 'deleted!')
    
    return redirect('index')

def groupdetail(request, group_id):
    group =  CompanyModel.objects.get(id=group_id)
    context = {
        'groups':group,
    }
    return render(request, 'task/group_details.html', context)

