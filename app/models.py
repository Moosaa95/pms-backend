from datetime import timezone
from django.core.validators import MaxValueValidator
from django.db import models

class Project(models.Model):
    STATUS_CHOICES = [
        ('TODO', 'To Do'),
        ('PROGRESS', 'Progress'),
        ('DONE', 'Done'),
    ]

    name = models.CharField(max_length=100)
    created_at = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    progress = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(100)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='TODO')
    # members = models.ManyToManyField('Member', related_name='projects')

    def __str__(self):
        return self.name
    
    @classmethod
    def create_project(cls, **kwargs):
        return cls.objects.create(**kwargs)

    @classmethod
    def get_projects(cls):
        return cls.objects.all().values()
    

    @classmethod
    def get_project(cls, project_id):
        try:
            return cls.objects.values().get(id=project_id)
        except cls.DoesNotExist:
            return None
    
    @classmethod
    def update_project(cls, project_id, **kwargs):
        project = cls.objects.get(pk=project_id)
        for key, value in kwargs.items():
            setattr(project, key, value)
        project.save()
        return project
    
    @classmethod
    def delete_project(cls, project_id):
        project = cls.objects.get(pk=project_id)
        if project:
            project.delete()
            return True
        else:
            return False


    @classmethod
    def fetch_filter_projects(cls, conditions=None):
        queryset = None
        fields = [
            "id",
            "name",
            "due_date",
            "status",
            "progress",
            "created_at",
        ]

        if conditions:
            queryset = (
                cls.objects.filter(conditions)
                .order_by("-created_at")
                .values(*fields)
            )

        return list(queryset)

    

class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    description = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=Project.STATUS_CHOICES, default='TODO')

    def __str__(self):
        return self.description

    @classmethod
    def create_task(cls, project_id, **kwargs):
        project = Project.objects.get(pk=project_id)
        task = cls.objects.create(project=project, **kwargs)
        return task
    
    @classmethod
    def get_tasks(cls):
        return cls.objects.all().values()
    
    @classmethod
    def get_task(cls, task_id):
        try:
            return cls.objects.values().get(id=task_id)
        except cls.DoesNotExist:
            return None

    @classmethod
    def update_task(cls, task_id, **kwargs):
        task = cls.objects.get(pk=task_id)
        for key, value in kwargs.items():
            setattr(task, key, value)
        task.save()
        return task

    @classmethod
    def delete_task(cls, task_id):
        task = cls.objects.get(pk=task_id)
        if task:
            task.delete()
            return True
        else:
            return False

    @classmethod
    def fetch_filter_tasks(cls, conditions=None):
        queryset = None
        fields = [
            "id",
            "description",
            "status",
            "project__name",
        ]

        if conditions:
            queryset = (
                cls.objects.filter(conditions)
                .order_by("-id")
                .values(*fields)
            )

        return list(queryset)


