# Generated by Django 4.2.7 on 2024-02-17 15:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("projectapp", "0024_alter_appointment_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="appointment",
            name="status",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Одобрен", "Одобрен"),
                    ("Преглежда се", "Преглежда се"),
                    ("Отказано", "Отказано"),
                    ("Пропуснат", "Пропуснат"),
                    ("Изпълнен", ""),
                ],
                default="Преглежда се",
                max_length=20,
                null=True,
            ),
        ),
    ]
