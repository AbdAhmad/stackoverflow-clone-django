from django.contrib import admin
from .models import Question, Answer, Tags, Profile, Questionvote, Answervote
# Register your models here.

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Tags)
admin.site.register(Profile)
admin.site.register(Questionvote)
admin.site.register(Answervote)