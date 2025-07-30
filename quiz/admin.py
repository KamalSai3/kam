from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .models import Quiz, Question, Option, Submission, Answer

admin.site.register(User, UserAdmin)

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(Submission)
admin.site.register(Answer)