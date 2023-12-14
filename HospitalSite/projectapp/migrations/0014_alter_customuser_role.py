# Generated by Django 4.2.7 on 2023-12-14 11:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("projectapp", "0013_alter_customuser_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="role",
            field=models.CharField(
                choices=[
                    ("admin", "Administrator"),
                    ("doctor", "Doctor"),
                    ("patient", "Patient"),
                ],
                max_length=7,
            ),
        ),
    ]