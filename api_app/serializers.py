from datetime import datetime

from rest_framework import serializers
from django.contrib.auth.models import User
from api_app.models import Products, User


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User(first_name=validated_data['first_name'],
                    last_name=validated_data['last_name'],
                    email=validated_data['email'],
                    username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)


class ProductModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ["user_id", "category", "title", "description", "price",
                  "quantity", "product_img", "created_at"]

    def create(self, validated_data):
        product = Products.objects.create(**validated_data)
        return product


def update(self, instance, validated_data):
    instance.category = validated_data.get("category", instance.category)
    instance.title = validated_data.get("title", instance.title)
    instance.description = validated_data.get("description", instance.description)
    instance.price = validated_data.get("price", instance.price)
    instance.quantity = validated_data.get("quantity", instance.quantity)
    instance.product_img = validated_data.get("product_img", instance.product_img)
    instance.updated_at = datetime.now()
    instance.save()
    return instance
