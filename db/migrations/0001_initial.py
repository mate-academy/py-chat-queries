# Generated by Django 4.0.2 on 2022-10-26 07:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=63)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=63)),
                ('last_name', models.CharField(max_length=63)),
                ('username', models.CharField(max_length=63, unique=True)),
                ('bio', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('sent', models.DateTimeField(auto_now_add=True)),
                ('is_delivered', models.BooleanField()),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.chat')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.user')),
            ],
        ),
        migrations.AddField(
            model_name='chat',
            name='users',
            field=models.ManyToManyField(to='db.User'),
        ),
    ]
