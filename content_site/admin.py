from django.contrib import admin
from .models import Testimony, Invitated, FAQ

# admin.site.register(MissionVision)
# admin.site.register(Banner)
admin.site.register(Testimony)
admin.site.register(Invitated)

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'is_active', 'created_date')
    list_filter = ('category', 'is_active')
    search_fields = ('question', 'answer')
    ordering = ('category', 'question')
