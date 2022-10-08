from django.contrib import admin

from shipping.models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)
