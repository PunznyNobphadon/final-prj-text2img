# Generated by Django 4.2.7 on 2024-05-20 16:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("image_generator", "0005_generatedimage_style"),
    ]

    operations = [
        migrations.AlterField(
            model_name="generatedimage",
            name="style",
            field=models.CharField(default="Sticker", max_length=255),
        ),
    ]
