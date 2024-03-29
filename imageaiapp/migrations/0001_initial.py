# Generated by Django 4.1 on 2023-10-10 13:57

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Prompt",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("prompt", models.CharField(max_length=4000)),
                (
                    "result",
                    models.ImageField(
                        blank=True, null=True, upload_to="diffuse-result"
                    ),
                ),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
