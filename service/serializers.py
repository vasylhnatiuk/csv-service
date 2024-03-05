from rest_framework import serializers
from .models import Client, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Client
        fields = '__all__'
