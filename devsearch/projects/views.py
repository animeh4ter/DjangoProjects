from django.shortcuts import render, redirect
from .models import Project, Tag
from .forms import ProjectForm, ReviewForm
from django.contrib.auth.decorators import login_required
from .utils import search_project, paginate_projects
from django.contrib import messages


def projects(request):
    pr, search_query = search_project(request)
    custom_range, pr = paginate_projects(request, pr, 3)

    context = {'projects': pr,
               'search_query': search_query,
               'custom_range': custom_range,
               }

    return render(request, 'projects/projects.html', context)


def project(request, pk):
    project_obg = Project.objects.get(id=pk)
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = project_obg
        review.owner = request.user.profile
        review.save()

        project_obg.get_vote_count()

        messages.success(request, 'Comment was successfully added')
        return redirect('project', pk=project_obg.id)

    context = {'project': project_obg,
               'form': form,
               }

    return render(request, 'projects/single-project.html', context)


@login_required(login_url='login')
def create_project(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            form.save()
            return redirect('account')

    context = {'form': form}
    return render(request, 'projects/form-template.html', context)


@login_required(login_url='login')
def update_project(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        new_tags = request.POST.get('tags').replace(',', ' ').split()
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            # broken tag loop
            # for tag in new_tags:
            #     tag, create = Tag.objects.get_or_create(name=tag)
            #     project.tags.add(tag.name)
            return redirect('account')

    context = {'form': form}
    return render(request, 'projects/form-template.html', context)


@login_required(login_url='login')
def delete_project(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    context = {'object': project}
    return render(request, 'projects/delete.html', context)
