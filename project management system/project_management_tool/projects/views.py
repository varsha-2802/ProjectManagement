
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import ProjectForm
from .models import Project
from .models import Project, Task
from .forms import ProjectForm, TaskForm
from django.shortcuts import redirect
from django.contrib import messages


def home(request):
    context = {
        'total_projects': Project.objects.count(),
        'active_tasks': Task.objects.filter(status='active').count(),
        'team_leaders': User.objects.count(),
        
    }
    return render(request, 'home.html', context)

@login_required
def project_list(request):
    projects = Project.objects.all()  # Get all projects
    return render(request, 'project_list.html', {'projects': projects})

@login_required
def project_create(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.creator = request.user
            project.save()
            return redirect(reverse('project_detail', args=[project.id]))
    else:
        form = ProjectForm()
    return render(request, 'project_form.html', {'form': form})

@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    return render(request, 'project_detail.html', {'project': project})

@login_required
def project_edit(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if project.creator != request.user:
        return redirect('project_list')  # Prevent non-creators from editing
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect(reverse('project_detail', args=[project.id]))
    else:
        form = ProjectForm(instance=project)
    return render(request, 'project_form.html', {'form': form})

@login_required
def project_delete(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if project.creator == request.user:
        project.delete()
    return redirect('project_list')


@login_required
def task_create(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            return redirect('project_detail', project_id=project.id)
    else:
        form = TaskForm()
    return render(request, 'task_form.html', {'form': form, 'project': project})




