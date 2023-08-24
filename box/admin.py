from django.contrib import admin
from box.models import Box


# Register your models here.

@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = ["created_by", "length", "breadth", "height"]
    raw_id_field = "created_by"

