from django.contrib import admin

from shipping.models import Customer, Job


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    raw_id_fields = ('customer',)
    list_display = ('customer', 'status', 'created_at', 'updated_at')
