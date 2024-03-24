from django.contrib import admin

# Register your models here.
from .models import OriginalText, TextInfo, SpaceInfo

admin.site.register(OriginalText)
admin.site.register(TextInfo)
admin.site.register(SpaceInfo)
