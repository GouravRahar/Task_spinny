from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from .serializers import BoxIdSerializer, BoxSerializer, DisplayBoxSerializer, BoxDimensionSerializer
from .services import BoxFilter, check_area, check_volume, check_last_week_boxes, check_user_last_week_boxes
from .models import Box
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.decorators import action


class BoxViewSet(viewsets.ModelViewSet):

    @action(detail=False, methods=["post"], permission_classes=[IsAdminUser], url_path='add')
    def perform_create(self, request):
        data = request.data
        ser_data = BoxDimensionSerializer(data=data)
        if ser_data.is_valid():
            length = ser_data.validated_data.get('length')
            breadth = ser_data.validated_data.get('breadth')
            height = ser_data.validated_data.get('height')
            if not check_area(length, breadth):
                return Response(data="Please Provide Dimensions with Less Area!", status=status.HTTP_406_NOT_ACCEPTABLE)
            if not check_volume(request.user, length, breadth, height):
                return Response(data="Please Provide Dimensions with Less Volume!",
                                status=status.HTTP_406_NOT_ACCEPTABLE)
            if not check_last_week_boxes():
                return Response(data="Quota for this week has been fulfilled, Add Data Tomorrow!",
                                status=status.HTTP_406_NOT_ACCEPTABLE)
            if not check_user_last_week_boxes(request.user):
                return Response(data="Quota for You, For this week has been fulfilled, Add Data Tomorrow!",
                                status=status.HTTP_406_NOT_ACCEPTABLE)
            box = Box.objects.create(length=length, height=height, breadth=breadth, created_by=request.user,
                                     area=length * breadth, volume=length * breadth * height)
            return Response(data=dict(id=box.id, length=box.length), status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["put"], detail=False, permission_classes=[IsAdminUser], url_path='update')
    def perform_update(self, request):
        data = request.data
        ser_data = BoxIdSerializer(data=data)
        if ser_data.is_valid():
            id = ser_data.validated_data.get('id')
            length = ser_data.validated_data.get('length')
            breadth = ser_data.validated_data.get('breadth')
            height = ser_data.validated_data.get('height')
            if length is not None and breadth is not None and not check_area(length, breadth):
                return Response(data="Please Provide Dimensions with Less Area!", status=status.HTTP_406_NOT_ACCEPTABLE)
            if length is not None and breadth is not None and height is not None and not check_volume(request.user, length, breadth, height):
                return Response(data="Please Provide Dimensions with Less Volume!",
                                status=status.HTTP_406_NOT_ACCEPTABLE)
            if not check_last_week_boxes():
                return Response(data="Quota for this week has been fulfilled, Add Data Tomorrow!",
                                status=status.HTTP_406_NOT_ACCEPTABLE)
            if not check_user_last_week_boxes(request.user):
                return Response(data="Quota for You, For this week has been fulfilled, Add Data Tomorrow!",
                                status=status.HTTP_406_NOT_ACCEPTABLE)
            try:
                box = Box.objects.get(id=id)
                if length:
                    box.length = length
                if breadth:
                    box.breadth = breadth
                if height:
                    box.height = height
                if length and breadth:
                    box.area = length * breadth
                if length and breadth and height:
                    box.volume = length * breadth * height
                box.save()
                return Response(data="Box Details has been Updated", status=status.HTTP_200_OK)
            except Box.DoesNotExists:
                return Response(data="Box does not exist", status=status.HTTP_400_BAD_REQUEST)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"], permission_classes=[AllowAny], url_path='display')
    def display_box(self, request):
        data = request.GET
        ser_data = DisplayBoxSerializer(data=data)
        if ser_data.is_valid():
            result = BoxFilter(ser_data.validated_data).get_data()
            return Response(data=result, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["get"], detail=False, permission_classes=[IsAdminUser], url_path='display/my')
    def display_boxes(self, request):
        data = request.GET
        ser_data = DisplayBoxSerializer(data=data)
        if ser_data.is_valid():
            result = BoxFilter(ser_data.validated_data).get_data(user=request.user)
            return Response(data=result, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["post"], detail=False, permission_classes=[IsAdminUser], url_path='delete')
    def delete_box(self, request):
        data = request.data
        ser_data = BoxIdSerializer(data=data)
        if ser_data.is_valid():
            id = ser_data.validated_data.get('id')
            try:
                box = Box.objects.get(id=id, created_by=request.user)
                box.delete()
                return Response(data="Box Deleted SuccessFully", status=status.HTTP_200_OK)
            except Box.DoesNotExists:
                return Response(data="Please Enter a Valid Id of box Created by You!",
                                status=status.HTTP_400_BAD_REQUEST)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
