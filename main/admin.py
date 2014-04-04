from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from main.models import Tshirt, BaseTshirt, Color, PrintCost, Profile, Payment

class UserProfileInline(admin.StackedInline):
    model = Profile

class UserProfileAdmin(UserAdmin):
    inlines = [ UserProfileInline, ]

class PaymentInline(admin.StackedInline):
    model = Payment
    readonly_fields = ['customer_id']

class TshirtAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'base_price', 'selling_price', 'date_created')
    inlines = [ PaymentInline, ]

class ColorInline(admin.TabularInline):
    model = Color
    extra = 3

class BaseTshirtAdmin(admin.ModelAdmin):
    inlines = [ColorInline]
    list_display = ('name', 'type', 'url',)

class PrintCostAdmin(admin.ModelAdmin):
    list_display = (
        'color',
        'quantity_range_low',
        'quantity_range_high',
        'color_1_cost',
        'color_2_cost',
        'color_3_cost',
        'color_4_cost',
        'color_5_cost',
        'color_6_cost',
        'color_additional_cost'
    )


admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)
admin.site.register(Tshirt, TshirtAdmin)
admin.site.register(BaseTshirt, BaseTshirtAdmin)
admin.site.register(PrintCost, PrintCostAdmin)
