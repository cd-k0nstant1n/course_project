# Generated by Django 4.2.7 on 2023-12-13 19:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("projectapp", "0003_customuser_delete_doctor_delete_patient"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="password",
            field=models.CharField(default="sth", max_length=500),
        ),
    ]
