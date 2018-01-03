# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, render_to_response, HttpResponse, HttpResponseRedirect
from projects.models import project_db
from django.contrib import messages
import uuid
from projects.models import project_db, project_scan_db
from webscanners import views


# Create your views here.


def create_form(request):
    return render(request, 'project_create.html')


def create(request):
    if request.method == 'POST':
        project_id = uuid.uuid4()
        project_name = request.POST.get("projectname")
        project_date = request.POST.get("projectstart")
        project_end = request.POST.get("projectend")
        project_owner = request.POST.get("projectowner")
        project_disc = request.POST.get("project_disc")

        save_project = project_db(project_name=project_name, project_id=project_id,
                                  project_start=project_date, project_end=project_end,
                                  project_owner=project_owner, project_disc=project_disc,)
        save_project.save()

        messages.success(request, "Project Created")

        return HttpResponseRedirect("/projects/")

    return render(request, 'project_create.html')


def projects(request):
    all_projects = project_db.objects.all()

    if request.method == 'POST':
        proj_id = request.POST.get("proj_id")
        del_proj = project_db.objects.filter(project_id=proj_id)
        del_proj.delete()
        messages.success(request, "Deleted Project")
        return HttpResponseRedirect("/projects/")

    return render(request, 'projects.html', {'all_projects': all_projects})


def projects_view(request):
    if request.method == 'GET':
        project_id = request.GET['proj_id']

    else:
        project_id = ''

    print "pROJECT ID ", project_id

    if request.method == 'POST':
        project_id = request.GET['proj_id']
        scan_ids = request.POST.get("scan_id")
        print scan_ids

        del_scans = project_scan_db.objects.filter(id=scan_ids)
        del_scans.delete()
        messages.success(request, "Deleted scan")
        return HttpResponseRedirect("/projects/projects_view/?proj_id=%s" % project_id)

    project_dat = project_db.objects.filter(project_id=project_id)
    scan_dat = project_scan_db.objects.filter(project_id=project_id)

    return render(request, 'project_view.html',
                  {'project_dat': project_dat, 'scan_dat': scan_dat, 'project_id': project_id})


def add_scan_v(request):
    if request.method == 'GET':
        project_id = request.GET['proj_id']

    else:
        project_id = ''

    return render(request, 'add_scan.html', {'project_id': project_id})


def add_scan(request):
    if request.method == 'POST':
        scan_type = request.POST.get("scan_type")
        project_id = request.POST.get("project_id")
        scan_target = request.POST.get("scan_target")
        save_scan = project_scan_db(scan_type=scan_type, project_url=scan_target, project_id=project_id)
        save_scan.save()
        messages.success(request, "Scan Added")
        return HttpResponseRedirect("/projects/projects_view/?proj_id=%s" % project_id)

    return render(request, 'project_view.html')

#
# def del_scan(request):
#     if request.method == 'GET':
#         project_id = request.GET['proj_id']
#
#     else:
#         project_id = ''
#     if request.method == 'POST':
#         scan_ids = request.POST.get("scan_id")
#         print scan_ids
#
#         del_scans = project_scan_db.objects.filter(id=scan_ids)
#         del_scans.delete()
#         messages.success(request, "Deleted scan")
#         return HttpResponseRedirect("/projects/projects_view/?proj_id=%s" % project_id)
#         # return HttpResponseRedirect(reversed('project_view.html'))
#     return render(request, 'projects.html')


def launch_scan(request):
    if request.method == 'GET':
        scan = views.index(request)
        print "Scan Completed", scan
    return render(request, 'projects.html')
