from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from juice_service.model.Address import Address
from juice_service.model.AvailableCity import City
from juice_service.model.AvailablePincode import Pincode
from juice_service.model.Cart import Cart
from juice_service.model.ContactRequest import ContactRequest
from juice_service.model.Coupon import Coupon
from juice_service.model.ItemComment import ItemComment
from juice_service.model.Item import Item
from juice_service.model.Order import Order
from juice_service.model.PhoneOTP import PhoneOTP
from juice_service.model.MainSlideImage import MainSlideImage
from juice_service.model.PageImage import PageImage

from .forms import UserAdminCreationForm, UserAdminChangeForm

User = get_user_model()


admin.site.site_header = "Mother's Store Admin"
admin.site.index_title = ""
admin.site.site_title = "Mother's Store-Admin"



class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ['phone', 'first_name', 'last_name', 'last_login']
    list_filter = ['staff', 'active', 'admin']
    fieldsets = (
        (None, {'fields': ('phone', 'role')}),
        ('personal_info', {'fields': ('first_name', 'last_name')}),
        ('permissions', {'fields': ('admin', 'staff', 'active')})
    )

    add_fieldsets = (
        (None, {
            'classes':('wide',),
            'fields': ('phone', 'password1', 'password2')
            },
        )
    )
    search_fields = ('phone',)
    ordering = ('id',)
    filter_horizontal = ()


    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)

class AvailableCityAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'created_at',
        'updated_at',
    )
    search_fields = ['name',]

class AvailablePincodeAdmin(admin.ModelAdmin):
    list_display = (
        'pincode',
        'created_at',
        'updated_at',
    )
    search_fields = ['pincode',]

class CartAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'item',
        'count',
        'weeks',
        'is_ordered',
        'order',
        'created_at',
        'updated_at'
    )

class ContactRequestAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'email',
        'phone',
        'details',
        'created_at',
    )
    search_fields = [
        'name',
        'email',
        'phone',
    ]

class CouponAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'amount',
        'valid_upto',
    )
    search_fields = [
        'code',
        'amount'
    ]

class ItemCommentAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'item',
        'comment',
        'created_at',
    )
    search_fields = [
        'comment',
        'created_at'
    ]

class ItemAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'weight',
        'slug',
        'image',
        'is_available',
        'count_per_week',
        'rate_per_bottle',
        'rate_per_week',
        'discount_type',
        'discount',
        'total_sales_count',
        'total_sales_amount',
        'description',
        'created_at',
        'updated_at'
    )
    search_fields = [
        'name',
        'is_available',
        'description',
    ]

class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'address',
        'payment',
        'status',
        'total',
        'date',
        'time',
        'created_at',
        'updated_at'
    )
    search_fields = [
        'status',
        'total'
    ]

class PhoneOTPAdmin(admin.ModelAdmin):
    list_display = (
        'phone',
        'otp',
        'count',
        'validated',
        'created_at',
        'updated_at'
    )
    search_fields = [
        'phone',
    ]

class MainSlideImageAdmin(admin.ModelAdmin):
    list_display = (
        'image',
        'is_available',
        'created_at',
        'updated_at'
    )

class PageImageAdmin(admin.ModelAdmin):
    list_display = (
        'image',
        'is_available',
        'created_at',
        'updated_at'
    )


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Address)
admin.site.register(City, AvailableCityAdmin)
admin.site.register(Pincode, AvailablePincodeAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(ContactRequest, ContactRequestAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(ItemComment, ItemCommentAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(PhoneOTP, PhoneOTPAdmin)
admin.site.register(MainSlideImage, MainSlideImageAdmin)
admin.site.register(PageImage, PageImageAdmin)
