# Generated by Django 3.2.6 on 2021-11-01 16:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ans', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('answered_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True)),
                ('body', models.TextField()),
                ('slug', models.SlugField(blank=True, max_length=250, null=True)),
                ('views', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_word', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Questionvote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upvote', models.BooleanField(default=False)),
                ('downvote', models.BooleanField(default=False)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stack_app.question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='tags',
            field=models.ManyToManyField(blank=True, to='stack_app.Tags'),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Name', max_length=200)),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('about_me', models.TextField(default='Apparently, this user prefers to keep an air of mystery about them.')),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='user_profile_pic')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('ans_given', models.ManyToManyField(blank=True, to='stack_app.Answer')),
                ('ques_asked', models.ManyToManyField(blank=True, to='stack_app.Question')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Answervote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upvote', models.BooleanField(default=False)),
                ('downvote', models.BooleanField(default=False)),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stack_app.answer')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='question_to_ans',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stack_app.question'),
        ),
    ]
