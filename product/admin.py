from django.contrib import admin
from django.http import HttpResponse, HttpResponseRedirect

from .models import *

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'quantity', 'rating']
    search_fields = ['title', 'bullet_points']
    actions = ['export_products']

    def export_products(self, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        return HttpResponseRedirect("/export_products/?ids=%s" % (",".join(selected)))

    export_products.short_description = "Export products as CSV file"  


admin.site.register(Product, ProductAdmin)
