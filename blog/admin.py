from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(UserInfo)
admin.site.register(Blog)
admin.site.register(Tag)
admin.site.register(Classify)
admin.site.register(Article)
admin.site.register(UpAndDown)
admin.site.register(Comment)