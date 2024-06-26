# Generated by Django 4.2.11 on 2024-06-03 08:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ReplacePair",
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
                ("rp_pair", models.CharField(max_length=100, verbose_name="替换对")),
            ],
        ),
        migrations.CreateModel(
            name="SentencePair",
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
                ("context1", models.TextField(verbose_name="句子1")),
                (
                    "context1_filepath",
                    models.CharField(max_length=200, verbose_name="句子1文件路径"),
                ),
                ("context2", models.TextField(verbose_name="句子2")),
                (
                    "context2_filepath",
                    models.CharField(max_length=200, verbose_name="句子2文件路径"),
                ),
                (
                    "rp_pair",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="show.replacepair",
                    ),
                ),
            ],
        ),
    ]
