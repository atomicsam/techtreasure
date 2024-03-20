import datetime
import os
from math import ceil

from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render

from login.models import Merchandise, HistoryRecord
from team_project import settings


def change_password(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        old_pwd = request.POST.get('old_pwd')
        new_pwd = request.POST.get('new_pwd')
        user_obj = User.objects.filter(username=name, password=old_pwd).values("id", "username", "password").first()
        if user_obj:
            User.objects.filter(id=user_obj.get("id", None)).update(password=new_pwd)
            return JsonResponse({"message": "Password updated successfully", "code": 200})
        else:
            return JsonResponse({"message": "User does not exist", "code": 400})

    return render(request, 'techtreasure/password_change_form.html')


def history_views(request):
    return render(request, 'techtreasure/listing.html')


def history_data(request):
    page = request.GET.get("page", 1)
    limit = request.GET.get("limit", 10)

    ordered_records = HistoryRecord.objects.select_related('merchandise').order_by('creation_time')

    paginator = Paginator(ordered_records, limit)
    page_1 = paginator.get_page(page)
    response_data = {"page": page, "limit": limit, "count": paginator.count, "data": [],
                     "count_num": ceil(paginator.count / int(limit))}
    for record in page_1:
        response_data["data"].append({
            "id": record.merchandise.id,
            "name": record.merchandise.title,
            "price": float(record.merchandise.price),
            "file_image": str(record.merchandise.file_image)
        })

    return JsonResponse(response_data)


def make_listing(request):
    if request.method == "POST":
        title = request.POST.get("title")
        describe = request.POST.get("describe")
        price = request.POST.get("describe")
        file_image = request.FILES['image']
        now_time = datetime.datetime.now()
        now_timestamp = int(now_time.timestamp())
        file_name = str(now_timestamp) + "_" + str(file_image.name)
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)

        with default_storage.open(file_path, 'wb+') as destination:
            for chunk in file_image.chunks():
                destination.write(chunk)
        #         user_id=user_id, user_name=user_name
        Merchandise.objects.create(title=title, describe=describe, price=price, file_image=file_name,
                                   creation_time=now_time)
        return JsonResponse({"message": "Operation successful", "code": 200})
    return render(request, 'techtreasure/makelisting.html')