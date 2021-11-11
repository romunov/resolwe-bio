# Generated by Django 3.1.7 on 2021-10-13 07:52

import os

import django.contrib.postgres.fields
import django.contrib.postgres.indexes
import django.contrib.postgres.search
from django.db import connection, migrations, models


def load_triggers(apps, schema_editor):
    file_names = [
        "triggers_feature.sql",
        # "triggers_mapping.sql",
    ]
    with connection.cursor() as c:
        for file_name in file_names:
            file_path = os.path.join(os.path.dirname(__file__), file_name)
            with open(file_path) as fh:
                sql_statement = fh.read()
            c.execute(sql_statement)


class Migration(migrations.Migration):

    replaces = [
        ("resolwe_bio_kb", "0001_initial"),
        ("resolwe_bio_kb", "0002_alter_field_max_length"),
        ("resolwe_bio_kb", "0003_add_map_index"),
        ("resolwe_bio_kb", "0004_add_unique_together"),
        ("resolwe_bio_kb", "0005_species"),
        ("resolwe_bio_kb", "0006_feature_fullname_300"),
        ("resolwe_bio_kb", "0007_feature_fullname_350"),
        ("resolwe_bio_kb", "0008_callable_defaults"),
        ("resolwe_bio_kb", "0009_full_text_search"),
        ("resolwe_bio_kb", "0010_update_indexes_constraints"),
        ("resolwe_bio_kb", "0011_feature_type_index"),
        ("resolwe_bio_kb", "0012_update_feature_search"),
    ]

    dependencies = [
        ("flow", "0001_squashed_0043_full_text_search"),
    ]

    operations = [
        migrations.CreateModel(
            name="Feature",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("source", models.CharField(max_length=20)),
                ("feature_id", models.CharField(max_length=50)),
                ("species", models.CharField(max_length=50)),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("gene", "Gene"),
                            ("transcript", "Transcript"),
                            ("exon", "Exon"),
                            ("probe", "Probe"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "sub_type",
                    models.CharField(
                        choices=[
                            ("protein-coding", "Protein-coding"),
                            ("pseudo", "Pseudo"),
                            ("rRNA", "rRNA"),
                            ("ncRNA", "ncRNA"),
                            ("snRNA", "snRNA"),
                            ("snoRNA", "snoRNA"),
                            ("tRNA", "tRNA"),
                            ("asRNA", "asRNA"),
                            ("other", "Other"),
                            ("unknown", "Unknown"),
                        ],
                        max_length=20,
                    ),
                ),
                ("name", models.CharField(max_length=1024)),
                ("full_name", models.CharField(blank=True, max_length=350)),
                ("description", models.TextField(blank=True)),
                (
                    "aliases",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=256),
                        blank=True,
                        default=list,
                        size=None,
                    ),
                ),
                ("search", django.contrib.postgres.search.SearchVectorField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Mapping",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "relation_type",
                    models.CharField(
                        choices=[
                            ("crossdb", "Crossdb"),
                            ("ortholog", "Ortholog"),
                            ("transcript", "Transcript"),
                            ("exon", "Exon"),
                        ],
                        max_length=20,
                    ),
                ),
                ("source_db", models.CharField(max_length=20)),
                ("source_id", models.CharField(max_length=50)),
                ("source_species", models.CharField(max_length=50)),
                ("target_db", models.CharField(max_length=20)),
                ("target_id", models.CharField(max_length=50)),
                ("target_species", models.CharField(max_length=50)),
            ],
        ),
        migrations.AddIndex(
            model_name="mapping",
            index=models.Index(
                fields=[
                    "source_db",
                    "source_id",
                    "source_species",
                    "target_db",
                    "target_species",
                ],
                name="idx_feature_source_target",
            ),
        ),
        migrations.AddIndex(
            model_name="mapping",
            index=models.Index(
                fields=["target_db", "target_id", "target_species"],
                name="idx_feature_target",
            ),
        ),
        migrations.AddConstraint(
            model_name="mapping",
            constraint=models.UniqueConstraint(
                fields=(
                    "source_db",
                    "source_id",
                    "source_species",
                    "target_db",
                    "target_id",
                    "target_species",
                    "relation_type",
                ),
                name="uniq_mapping_source_target_type",
            ),
        ),
        migrations.AddIndex(
            model_name="feature",
            index=models.Index(fields=["source"], name="idx_feature_source"),
        ),
        migrations.AddIndex(
            model_name="feature",
            index=models.Index(fields=["species"], name="idx_feature_species"),
        ),
        migrations.AddIndex(
            model_name="feature",
            index=models.Index(fields=["feature_id"], name="idx_feature_feature_id"),
        ),
        migrations.AddIndex(
            model_name="feature",
            index=models.Index(fields=["type"], name="idx_feature_type"),
        ),
        migrations.AddIndex(
            model_name="feature",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["search"], name="idx_feature_search"
            ),
        ),
        migrations.AddConstraint(
            model_name="feature",
            constraint=models.UniqueConstraint(
                fields=("source", "feature_id", "species"),
                name="uniq_feature_source_feature_id_species",
            ),
        ),
        migrations.RunPython(load_triggers),
        # Update existing entries.
        migrations.RunSQL("UPDATE resolwe_bio_kb_feature SET id=id;"),
    ]