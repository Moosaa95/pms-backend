# Generated by Django 5.0.3 on 2024-03-16 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0002_remove_project_members_delete_member"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="due_date",
            field=models.DateTimeField(),
        ),
    ]