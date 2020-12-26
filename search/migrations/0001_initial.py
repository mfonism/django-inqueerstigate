# Generated by Django 3.1.4 on 2020-12-26 11:47

import cloudinary.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import search.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Scum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=128)),
                ('location', models.CharField(max_length=64)),
                ('ext_url', models.URLField(max_length=256)),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ScumShot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('shot', cloudinary.models.CloudinaryField(max_length=255, verbose_name='scum_shot')),
                ('encoding', search.fields.NumpyArrayField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='scum_shots', to='search.scum')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SearchResult',
            fields=[
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('in_shot', cloudinary.models.CloudinaryField(max_length=255, verbose_name='in_shot')),
                ('out_scum_shots', models.ManyToManyField(related_name='search_results', to='search.ScumShot')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
    ]
