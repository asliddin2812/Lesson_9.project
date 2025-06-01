from django.contrib import admin
from .models import Construction

@admin.register(Construction)
class ConstructionTermAdmin(admin.ModelAdmin):
    list_display = ("rus_tili", "uzbek_kiril", "uzbek_lotin", "ingliz_tili", "turk_tili")
    search_fields = ("rus_tili", "uzbek_kiril", "uzbek_lotin", "ingliz_tili", "turk_tili")
    list_filter = ("uzbek_lotin",)

