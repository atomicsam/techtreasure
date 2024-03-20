import datetime
import os
from math import ceil

from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response

from rest_framework.views import APIView

from login.models import Merchandise, HistoryRecord
from team_project import settings


class ChangePasswordModel(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["name", "old_pwd", "new_pwd"],
            properties={
                "name": openapi.Schema(type=openapi.TYPE_STRING, title="用户名"),
                "old_pwd": openapi.Schema(type=openapi.TYPE_STRING, title="旧密码"),
                "new_pwd": openapi.Schema(type=openapi.TYPE_STRING, title="新密码"),
            }
        ),
        responses={200: "Success"},
        tags=["用户设置修改密码"]
    )
    def post(self, request):
        data = request.data.dict()
        name = data.get("name")
        old_pwd = data.get("old_pwd")
        new_pwd = data.get("new_pwd")
        user_obj = User.objects.filter(username=name, password=old_pwd).values("id", "username", "password").first()
        if user_obj:
            User.objects.filter(id=user_obj.get("id", None)).update(password=new_pwd)
            return Response({"message": "Password updated successfully", "code": 200})
        else:
            return Response({"message": "User does not exist", "code": 400})

    def get(self, request):
        return render(request, 'techtreasure/password_change_form.html')


class GetHistoryClassModel(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["pag", "limit"],
            properties={
                "page": openapi.Schema(type=openapi.TYPE_STRING, title="当前页"),
                "limit": openapi.Schema(type=openapi.TYPE_STRING, title="每页个数"),
            }
        ),
        responses={200: "Success"},
        tags=["用户商品历史记录-页面"]
    )
    def get(self, request):
        return render(request, 'techtreasure/listing.html')



from rest_framework import serializers


class HistorySerializer(serializers.Serializer):
    page = serializers.IntegerField(default=1)
    limit = serializers.IntegerField(default=10)


class HistoryClassModel(APIView):
    @swagger_auto_schema(
        query_serializer=HistorySerializer,
        responses={200: "Success"},
        tags=["用户商品历史记录数据"]
    )
    def get(self, request):
        serializer = HistorySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        page = serializer.validated_data.get("page")
        limit = serializer.validated_data.get("limit")

        ordered_records = HistoryRecord.objects.select_related('merchandise').order_by('creation_time')
        paginator = Paginator(ordered_records, limit)
        page_1 = paginator.get_page(page)

        response_data = {"page": page, "limit": limit, "count": paginator.count, "data": [],"count_num":ceil(paginator.count / limit)}
        for record in page_1:
            response_data["data"].append({
                "id":record.merchandise.id,
                "name": record.merchandise.title,
                "price": float(record.merchandise.price),
                "file_image": str(record.merchandise.file_image)
            })

        return JsonResponse(response_data)


class MakeListingModel(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["title", "describe", "price", "image"],
            properties={
                "title": openapi.Schema(type=openapi.TYPE_STRING, title="标题"),
                "describe": openapi.Schema(type=openapi.TYPE_STRING, title="商品描述信息"),
                "price": openapi.Schema(type=openapi.TYPE_STRING, title="商品价格"),
                "image": openapi.Schema(type=openapi.TYPE_FILE, title="图片"),
            }
        ),
        responses={200: "Success"},
        tags=["商品上架"]
    )
    def post(self, request):
        # 在此处添加处理POST请求的逻辑
        try:
            title = request.data.get("title")
            describe = request.data.get("describe")
            price = request.data.get("describe")
            file_image = request.FILES.get("image")
            # 获取当前时间戳
            now_time = datetime.datetime.now()
            now_timestamp = int(now_time.timestamp())
            # 构建文件名
            file_name = str(now_timestamp) + "_" + str(file_image.name)
            # 构建文件路径
            file_path = os.path.join(settings.MEDIA_ROOT, file_name)
            # 将文件写入到目标路径
            with default_storage.open(file_path, 'wb+') as destination:
                for chunk in file_image.chunks():
                    destination.write(chunk)
            #         user_id=user_id, user_name=user_name
            Merchandise.objects.create(title=title, describe=describe, price=price, file_image=file_name,
                                       creation_time=now_time)
            return Response({"message": "Operation successful", "code": 200})
        except Exception as e:
            print(e)

            return Response({"message": "operation failed1111", "code": 400})

    def get(self, request):
        return render(request, 'techtreasure/makelisting.html')
