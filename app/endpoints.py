# views.py

import json
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Project, Task
from .forms import ProjectForms, TaskForms
from django.db.models import Q

class ProjectListCreateAPIView(APIView):
    def get(self, request):
        projects = Project.get_projects()
        return Response(data=projects)

    def post(self, request):
        form = ProjectForms(request.POST)
        print(form, 'FORM')
        if form.is_valid():
            name = form.cleaned_data.get('name', None)
            due_date = form.cleaned_data.get("due_date", None)
            progress = form.cleaned_data.get("progress", None)
            project_status = form.cleaned_data.get("status", None)
            data = dict(name=name, due_date=due_date, progress=progress, status=project_status)
            project = Project.create_project(**data)
            if project:
                print(project, 'hey')
                return Response({"success": True, "message": "Project added successfully"}, status=status.HTTP_201_CREATED)
        
        return Response({"success": False, "message": "Invalid form data"}, status=status.HTTP_400_BAD_REQUEST)


class ProjectFilter(APIView):

    def post(self, request, *args, **kwargs):
        filters = request.data.get("filters")
        print(filters, 'filter')
        and_condition = Q()
        filtered = []

        if not filters:
            return Response(data={"status": True, "data": filtered})

        filters = json.loads(filters)

        if len(filters) == 0:
            return Response(data={"status": True, "data": filtered})
        
        if "name" in filters:
            filters["name__icontains"] = filters.pop('name')
        
        if "status" in filters:
            filters["status__icontains"] = filters.pop('status')

        for key, value in filters.items():
            print('KEY', key, 'valeu', value)
            and_condition.add(Q(**{key: value}), Q.AND)

        filtered = Project.fetch_filter_projects(conditions=and_condition)

        data = {"status": True, "data": filtered}

        return Response(data=data)
    


class ProjectDetailAPIView(APIView):
    def get_object(self, pk):
        return Project.get_project(project_id=pk)

    def get(self, request, pk, format=None):
        project = self.get_object(pk)
        data = {
            "id": project.id,
            "name": project.name,
            "due_date": project.due_date,
            "progress": project.progress,
            "status": project.status,
            "created_at": project.created_at,
        }
        return Response(data)

    def put(self, request, pk, format=None):
        project_id = request.data.get('project_id')
        name = request.data.get('name')
        due_date = request.data.get('due_date')
        progress = request.data.get('progress')
        status = request.data.get('status')
        data = dict(name=name, due_date=due_date, progress=progress, status=status)
        project = Project.update_project(project_id=project_id, **data)
        return Response({"message": "Project updated successfully"})

    def delete(self, request, pk, format=None):
        project = Project.delete_project(project_id=pk)
        if project:
            return Response({"message": "Project deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "Project unable to delete"}, status=status.HTTP_403_FORBIDDEN)


class TaskListCreateAPIView(APIView):
    def get(self, request):
        tasks = Task.get_tasks()
        return Response(data=tasks)

    def post(self, request):
        form = TaskForms(request.POST)
        if form.is_valid():
            description = form.cleaned_data.get('description', None)
            project_id = form.cleaned_data.get('project_id', None)
            status = form.cleaned_data.get('status', None)
            data = dict(description=description, project_id=project_id, status=status)
            task = Task.create_task(**data)
            if task:
                return Response({"success": True, "message": "Task added successfully"}, status=status.HTTP_201_CREATED)
        return Response({"success": False, "message": "Invalid form data"}, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailAPIView(APIView):
    def get_object(self, pk):
        return Task.get_task(task_id=pk)

    def get(self, request, pk, format=None):
        task = self.get_object(pk)
        if task:
            data = {
                "id": task.id,
                "description": task.description,
                "project_id": task.project_id,
                "status": task.status,
            }
            return Response(data)
        return Response({"message": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk, format=None):
        task_id = request.data.get('task_id')
        description = request.data.get('description')
        project_id = request.data.get('project_id')
        status = request.data.get('status')
        data = dict(description=description, project_id=project_id, status=status)
        task = Task.update_task(task_id=task_id, **data)
        return Response({"message": "Task updated successfully"})

    def delete(self, request, pk, format=None):
        task = Task.delete_task(task_id=pk)
        if task:
            return Response({"message": "Task deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "Task unable to delete"}, status=status.HTTP_403_FORBIDDEN)
