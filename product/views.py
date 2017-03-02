import os
import csv
import datetime
import mimetypes

from django.shortcuts import render
from django.utils.encoding import smart_str
from wsgiref.util import FileWrapper
from django.contrib.contenttypes.models import ContentType
from django.forms.models import model_to_dict
from django.http import HttpResponse

from .models import *

def export_products(request):
    if request.method == "POST":
        product_ids = request.GET.get('ids').split(',')
        result_csv_fields = request.POST.getlist('props[]')

        path = datetime.datetime.now().strftime("/tmp/.costco_products_%Y_%m_%d_%H_%M_%S.csv")
        result = open(path, 'w')
        result_csv = csv.DictWriter(result, fieldnames=result_csv_fields)
        result_csv.writeheader()

        queryset = Product.objects.filter(id__in=product_ids)

        for product in queryset:
            product_ = model_to_dict(product, fields=result_csv_fields)
            if 'bullet_points' in result_csv_fields:
                product_['bullet_points'] = product.bullet_points.encode('utf-8')
            if 'details' in result_csv_fields:
                product_['details'] = product.details.encode('utf-8')
            result_csv.writerow(product_)

        result.close()

        wrapper = FileWrapper( open( path, "r" ) )
        content_type = mimetypes.guess_type( path )[0]

        response = HttpResponse(wrapper, content_type = content_type)
        response['Content-Length'] = os.path.getsize( path ) # not FileField instance
        response['Content-Disposition'] = 'attachment; filename=%s/' % smart_str( os.path.basename( path ) ) # same here        
        return response

    return render(request, 'product_properties.html')    