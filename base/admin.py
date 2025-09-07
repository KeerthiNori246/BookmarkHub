from django.contrib import admin
from .models import User, Preference, Article, Board

admin.site.register(User)
admin.site.register(Preference)
admin.site.register(Article)
admin.site.register(Board)
