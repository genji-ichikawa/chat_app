from django.contrib import admin

from main.models import Talk, User

admin.site.register(User)
admin.site.register(Talk)
