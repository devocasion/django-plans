from django.contrib import admin
from django.core import urlresolvers
from models import UserPlan, Plan, PlanQuota, Quota, PlanPricing, Pricing, Order, BillingInfo
from ordered_model.admin import OrderedModelAdmin
from plans.models import Invoice

class UserLinkMixin(object):
    def user_link(self, obj):
        change_url = urlresolvers.reverse('admin:auth_user_change', args=(obj.user.id,))
        return '<a href="%s">%s</a>' % (change_url, obj.user.username)

    user_link.short_description = 'User'
    user_link.allow_tags = True

class PlanQuotaInline(admin.TabularInline):
    model = PlanQuota

class PlanPricingInline(admin.TabularInline):
    model = PlanPricing

class QuotaAdmin(OrderedModelAdmin):
    list_display = ('codename', 'name', 'description', 'unit', 'is_boolean',  'move_up_down_links', )

class PlanAdmin(OrderedModelAdmin):
    search_fields = ('customized__username', 'customized__email', )
    list_filter = ( 'available',  )
    list_display = ('name',   'description', 'customized', 'default', 'available', 'created', 'move_up_down_links')
    inlines = (PlanPricingInline, PlanQuotaInline)
    list_select_related = True

    def queryset(self, request):
        return super(PlanAdmin, self).queryset(request).select_related('customized')


class BillingInfoAdmin(UserLinkMixin, admin.ModelAdmin):
    search_fields = ('user__username', 'user__email')
    list_display = ('user', 'tax_number', 'name', 'street', 'zipcode', 'city', 'country')
    list_select_related = True
    readonly_fields = ('user_link',)
    exclude = ('user',)

class OrderAdmin(admin.ModelAdmin):
    list_filter = ('status', "plan")
    search_fields = ('id', 'user__username', 'user__email')
    list_display = ("id", "name", "created", "user", "status", "completed", "tax", "amount", "currency", "plan", "pricing")
    def queryset(self, request):
        return super(OrderAdmin, self).queryset(request).select_related('plan', 'pricing', 'user')


class InvoiceAdmin(admin.ModelAdmin):
    search_fields = ('full_number',  'buyer_tax_number', 'user__username', 'user__email')
    list_filter = ('type', )
    list_display = ('full_number', "issued", "total_net", "currency", 'user', "tax", "buyer_name", "buyer_city", "buyer_tax_number")
    list_select_related = True
    raw_id_fields = ('user', 'order')

class UserPlanAdmin(UserLinkMixin, admin.ModelAdmin):
    list_filter = ('active', 'expire')
    search_fields = ('user__username', 'user__email')
    list_display = ('user', 'plan', 'expire', 'active')
    list_select_related = True
    readonly_fields = ['user_link']
    fields = ('user_link', 'plan', 'expire', 'active' )



admin.site.register(Quota, QuotaAdmin)
admin.site.register(Plan, PlanAdmin)
admin.site.register(UserPlan, UserPlanAdmin)
admin.site.register(Pricing)
admin.site.register(Order, OrderAdmin)
admin.site.register(BillingInfo, BillingInfoAdmin)
admin.site.register(Invoice, InvoiceAdmin)


