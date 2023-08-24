from .models import Box
from .serializers import BoxSerializer
from django.db.models import Avg, Count, F, Sum
from django.utils import timezone
from datetime import timedelta

A1 = 100
V1 = 1000
L1 = 100
L2 = 50


def check_area(length=0.0, breadth=0.0):
    total_area_dict = Box.objects.aggregate(Sum('area'))
    total_area = total_area_dict['area__sum']
    total_count = Box.objects.all().count()
    if (total_area + (length * breadth)) / (total_count + 1) > A1:
        return False
    return True


def check_volume(user,length=0.0, breadth=0.0, height=0.0):
    total_volume_dict = Box.objects.filter(created_by=user).aggregate(Sum('volume'))
    total_volume = total_volume_dict['volume__sum']
    total_count = Box.objects.filter(created_by=user).count()
    if (total_volume + (length * breadth * height)) / (total_count + 1) > V1:
        return False
    return True


def check_last_week_boxes():
    current_week_start = timezone.now() - timedelta(days=timezone.now().weekday())
    current_week_boxes = Box.objects.filter(created_at__gte=current_week_start).count()
    if current_week_boxes > L1:
        return False
    return True


def check_user_last_week_boxes(user):
    current_week_start = timezone.now() - timedelta(days=timezone.now().weekday())
    current_week_boxes = Box.objects.filter(created_by=user, created_at__gte=current_week_start).count()
    if current_week_boxes > L2:
        return False
    return True


class BoxFilter:
    def __init__(self, data):
        self.length_more_than = data.get('length_more_than', 0.0)
        self.length_less_than = data.get('length_less_than', 10000000000)
        self.breadth_more_than = data.get('breadth_more_than', 0.0)
        self.breadth_less_than = data.get('breadth_less_than', 10000000000)
        self.height_more_than = data.get('height_more_than', 0.0)
        self.height_less_than = data.get('height_less_than', 10000000000)
        self.area_more_than = data.get('area_more_than', 0.0)
        self.area_less_than = data.get('area_less_than', 10000000000000000)
        self.volume_more_than = data.get('volume_more_than', 0.0)
        self.volume_less_than = data.get('volume_less_than', 100000000000000)

    def get_data(self, user=None):
        box_data = Box.objects.filter(length__gt=self.length_more_than, length__lt=self.length_less_than,
                                      breadth__gt=self.breadth_more_than, breadth__lt=self.breadth_less_than,
                                      height__gt=self.height_more_than, height__lt=self.height_less_than,
                                      area__gt=self.area_more_than, area__lt=self.area_less_than,
                                      volume__gt=self.volume_more_than, volume__lt=self.volume_less_than)

        if user is not None:
            box_data.filter(created_by=user)
        ser_box_data = BoxSerializer(box_data, many=True)
        result = []
        for data in ser_box_data.data:
            temp = dict(Box_Id=data.get('id'), Length=data.get('length'), Breadth=data.get('breadth'),
                        Height=data.get('height'), Area=data.get('area'), Volume=data.get('volume'))
            result.append(temp)
        return result
