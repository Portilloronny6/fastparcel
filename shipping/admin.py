from django.contrib import admin

from shipping.models import Customer, Job, Transaction


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    raw_id_fields = ('customer',)
    list_display = ('customer', 'status', 'created_at', 'updated_at')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    raw_id_fields = ('job',)
    list_display = ('stripe_payment_intent_id', 'job', 'amount', 'created_at')
