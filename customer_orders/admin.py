from django.contrib import admin
from .models import Order, Customer, Food_Item, Food, Reservations

# class OrderAdmin(admin.ModelAdmin):
#     readonly_fields = ('customer', 'food','quantity','total')

#     def formfield_for_foreignkey(self, db_field, request, **kwargs):
#         if db_field.name in ['customer', 'food','quantity','total']:
#             kwargs['widget'] = admin.widgets.AdminTextInputWidget(attrs={'readonly': 'readonly'})
#         return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Order)
# admin.site.register( OrderAdmin)
admin.site.register([Customer, Food_Item, Food])
admin.site.register(Reservations)
