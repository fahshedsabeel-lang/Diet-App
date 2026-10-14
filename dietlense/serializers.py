from rest_framework import serializers
from dietlense.models import *

class Useraserializer(serializers.ModelSerializer):
    profile=serializers.SerializerMethodField(read_only=True)
    class Meta:
        model=CustomUser
        fields=["id","username","email","password","phone","profile"]
        read_only_field=["id"]

    def create (self,validated_data):
        return CustomUser.objects.create_user(**validated_data)

    def get_profile(self,obj):
        profile_obj=UserProfile.objects.get(owner=obj)
        serializer_instance=UseraprofileSerializer(profile_obj)
        return serializer_instance.data


class UseraprofileSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserProfile
        fields="__all__"
        read_only_fields=["id","bmr","owner"]


class FoodLogSerializer(serializers.ModelSerializer):
    class Meta:
        model=FoodLog
        fields="__all__"
        read_only_field=["id","created_at","owner"]