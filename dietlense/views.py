from django.shortcuts import render
from dietlense.models import *
from dietlense.serializers import *
from rest_framework.generics import CreateAPIView, RetrieveAPIView ,UpdateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from django.contrib.auth import backends
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from dietlense.utility_funcs import calculate_bmr
from dietlense.permissions import IsOwner
from django.utils import timezone
from rest_framework.response import Response
from django.db.models import Sum

# Create your views here.

class SignUpView(CreateAPIView):
    serializer_class=Useraserializer


class ProfileView(CreateAPIView):
    serializer_class=UseraprofileSerializer
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    def perform_create(self, serializer):
        user_object=self.request.user
        # data=serializer.validated_data
        # bmr=calculate_bmr(
        #     age=data.get('age'),
        #     height=data.get('height'),
        #     weight=data.get('weight'),
        #     gender=data.get('gender'),
        #     activity_level=data.get('activity_level'),
        # )
        # return serializer.save(owner=user_object,bmr=bmr)
        return serializer.save(owner=user_object)


class ProfileRetrieveView(RetrieveAPIView, UpdateAPIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsOwner]
    serializer_class=UseraprofileSerializer
    queryset=UserProfile.objects.all()


# class Profileupdateview(UpdateAPIView):


class UserRetrieveView(RetrieveAPIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsOwner]
    serializer_class=Useraserializer
    queryset=CustomUser.objects.all()


class FoodLogCreateListView(CreateAPIView, ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = FoodLogSerializer
    # queryset = FoodLog.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return FoodLog.objects.filter(owner=self.request.user)



class FoodLogRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsOwner]
    serializer_class=FoodLogSerializer
    queryset=FoodLog.objects.all()



class DietSummeryView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        cur_date = timezone.now().date()

        queryset = FoodLog.objects.filter(
            created_at__date=cur_date,
            owner=request.user
        )

        calories_consumed = queryset.aggregate(
            calories_sum=Sum('calories')
        )

        total_calories = calories_consumed.get('calories_sum') or 0
        daily_target = request.user.profile.bmr

        context = {
            "total_calories_consumed": total_calories,
            "daily_target": daily_target,
            "balance": daily_target - total_calories
        }

        return Response(context)

        # return Response({"msg":"scs"}) 