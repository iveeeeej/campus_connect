from django.contrib import admin

from .models import Organization


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "organization_type", "is_active")
    list_filter = ("organization_type", "is_active")
    search_fields = ("code", "name")
