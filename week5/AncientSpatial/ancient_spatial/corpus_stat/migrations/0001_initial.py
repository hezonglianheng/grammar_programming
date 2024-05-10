# Generated by Django 4.2.11 on 2024-05-10 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="PatternStat",
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
                ("stat_type", models.CharField(default="", max_length=200)),
                ("all_cases", models.IntegerField(default=0)),
                ("place", models.IntegerField(default=0)),
                ("departure", models.IntegerField(default=0)),
                ("destination", models.IntegerField(default=0)),
                ("orientation", models.IntegerField(default=0)),
                ("direction", models.IntegerField(default=0)),
                ("path", models.IntegerField(default=0)),
                ("part", models.IntegerField(default=0)),
            ],
            options={"abstract": False,},
        ),
        migrations.CreateModel(
            name="PrepStat",
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
                ("stat_type", models.CharField(default="", max_length=200)),
                ("all_cases", models.IntegerField(default=0)),
                ("place", models.IntegerField(default=0)),
                ("departure", models.IntegerField(default=0)),
                ("destination", models.IntegerField(default=0)),
                ("orientation", models.IntegerField(default=0)),
                ("direction", models.IntegerField(default=0)),
                ("path", models.IntegerField(default=0)),
                ("part", models.IntegerField(default=0)),
            ],
            options={"abstract": False,},
        ),
        migrations.CreateModel(
            name="SpatialTypeStat",
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
                ("spatial_type", models.CharField(default="", max_length=200)),
                ("all_cases", models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name="VerbStat",
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
                ("stat_type", models.CharField(default="", max_length=200)),
                ("all_cases", models.IntegerField(default=0)),
                ("place", models.IntegerField(default=0)),
                ("departure", models.IntegerField(default=0)),
                ("destination", models.IntegerField(default=0)),
                ("orientation", models.IntegerField(default=0)),
                ("direction", models.IntegerField(default=0)),
                ("path", models.IntegerField(default=0)),
                ("part", models.IntegerField(default=0)),
            ],
            options={"abstract": False,},
        ),
    ]
