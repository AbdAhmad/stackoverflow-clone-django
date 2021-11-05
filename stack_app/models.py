from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import pre_save
from .utils import unique_slug_generator


class Tags(models.Model): 
    tag_word = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.tag_word


class Question(models.Model):
    title = models.CharField(max_length=200, unique=True)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=250, null=True, blank=True)
    tags = models.ManyToManyField(Tags, blank=True)
    views = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title[:50]


def pre_save_receiver(sender, instance, *args, **kwargs):
   if not instance.slug:
       instance.slug = unique_slug_generator(instance)

pre_save.connect(pre_save_receiver, sender=Question)
    

class Answer(models.Model):
    ans = models.TextField()
    answered_by = models.ForeignKey(User, on_delete=models.CASCADE)
    question_to_ans = models.ForeignKey(Question, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.ans[:20]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, default='NA')
    email = models.EmailField(max_length=254, default='NA')
    location = models.CharField(max_length=100, default='NA')
    about_me = models.TextField(default='NA')
    ques_asked = models.ManyToManyField('stack_app.Question', blank = True)
    ans_given = models.ManyToManyField('stack_app.Answer', blank = True)
    date_joined = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return self.user.username


class Questionvote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    upvote = models.BooleanField(default=False)
    downvote = models.BooleanField(default=False)

    def __str__(self):
        return str(self.question) + ' votes'


class Answervote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    upvote = models.BooleanField(default=False)
    downvote = models.BooleanField(default=False)

    def __str__(self):
        return str(self.answer) + ' votes'
