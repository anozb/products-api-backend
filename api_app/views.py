from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
import rest_framework.status as api_status
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
import api_app.serializers as api_serializers
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import authenticate
from api_app.models import User, Products
from drf_yasg.utils import swagger_auto_schema


# Create your views here.
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def home(request):
    """
    This is simple APIs for testing purpose

    :param request:
    :return: dictionary containing message as key and value as Hello, world!
    """
    name = request.GET.get("name")
    if name:
        message = f"Hello, {name}"
    else:
        message = "Hello, world!"
    return Response({"message": message}, status=api_status.HTTP_200_OK)


class UserRegistration(generics.GenericAPIView):
    """"
    This API is used to register a user

    """
    serializer_class = api_serializers.UserRegisterSerializer

    @swagger_auto_schema(tags=["User"], operation_summary="Register API")
    def post(self, request, *args, **kwargs):
        request_data = request.data
        serializer = self.serializer_class(data=request_data)
        if serializer.is_valid(raise_exception=True):
            print("Validated data", serializer.validated_data)
            user = serializer.create(serializer.validated_data)
            return JsonResponse({"user_id": user.pk,
                                 "message": "User registered successfully"},
                                status=api_status.HTTP_201_CREATED)

        else:
            return JsonResponse({"message": "User registration failed", "errors": serializer.errors},
                                status=api_status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    """
    This API is used to log in a user
    """
    serializer_class = api_serializers.LoginSerializer

    @swagger_auto_schema(tags=["User"], operation_summary="Login API")
    def post(self, request, *args, **kwargs):
        request_data = request.data
        serializer = self.serializer_class(data=request_data)
        if serializer.is_valid(raise_exception=True):
            print("Validated data", serializer.validated_data)
            user = authenticate(username=serializer.validated_data['username'],
                                password=serializer.validated_data['password'])
            if user:
                access_token = AccessToken.for_user(user)
                return JsonResponse({"user_id": user.pk,
                                     "token": str(access_token)},
                                    status=api_status.HTTP_200_OK)

            else:
                return JsonResponse({"message": "Invalid user credentials"},
                                    status=api_status.HTTP_400_BAD_REQUEST)

        else:
            return JsonResponse({"message": "User login failed", "errors": serializer.errors},
                                status=api_status.HTTP_400_BAD_REQUEST)


class UserProfile(generics.GenericAPIView):
    """
    This API is used to et user profile
    """
    serializer_class = api_serializers.UserRegisterSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=["User"], operation_summary="Profile API")
    def get(self, request):
        user = User.objects.get(pk=request.user.pk)
        user_data = self.serializer_class(user).data
        if "password" in user_data:
            del user_data["password"]
        return JsonResponse(user_data, status=api_status.HTTP_200_OK)


# instead of using serializer
# class UserProfile(generics.GenericAPIView):
#     """
#     This API is used to et user profile
#     """
#     permission_classes = [IsAuthenticate]
#
#     def get(self, request):
#         user = User.objects.get(pk=request.user.pk)
#         user_data = {
#             "User_id": user.pk,
#             "username": user.username,
#             "email": user.email,
#             "first_name": user.first_name,
#             "last_name": user.last_name
#         }
#         return JsonResponse(user_data, status=api_status.HTTP_200_OK)


class ProductCreateView(generics.GenericAPIView):
    """
    This API is used to create a product
    """
    serializer_class = api_serializers.ProductModelSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=["Products"], operation_summary="product create API")
    def post(self, request):
        request_data = request.data
        serializer = self.serializer_class(data=request_data)
        if serializer.is_valid(raise_exception=True):
            serializer.validated_data["user_id"] = request.user.pk
            product = serializer.create(serializer.validated_data)
            return JsonResponse({"product_id": product.pk,
                                 "messages": "Product created successfully"},
                                status=api_status.HTTP_201_CREATED)
        else:
            return JsonResponse({"message": "Product creation failed", "errors": serializer.errors},
                                status=api_status.HTTP_400_BAD_REQUEST)


class ProductListView(generics.GenericAPIView):
    """
    This API is used to get all products
    """
    serializer_class = api_serializers.ProductModelSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=["Products"], operation_summary="product list API")
    def get(self, request):
        products = Products.objects.all()
        product_data = self.serializer_class(products, many=True).data
        return JsonResponse(product_data, status=api_status.HTTP_200_OK, safe=False)


class ProductDetailView(generics.GenericAPIView):
    """
    This API is used to get single product detail
    """
    serializer_class = api_serializers.ProductModelSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=["Products"], operation_summary="product detail API")
    def get(self, request, product_id):
        try:
            product = Products.objects.get(pk=product_id)
            product_data = self.serializer_class(product).data
            return JsonResponse(product_data, status=api_status.HTTP_200_OK, safe=False)
            # to return in dictionary format## return JsonResponse(dict(data=product_data),
            # status=api_status.HTTP_200_OK, safe=False)
        except Products.DoesNotExist:
            return JsonResponse({"message": "Product does not exist"},
                                status=api_status.HTTP_404_NOT_FOUND)


class ProductUpdateView(generics.GenericAPIView):
    """
    This API is used to update a product
    """
    serializer_class = api_serializers.ProductModelSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=["Products"], operation_summary="product update API")
    def put(self, request, product_id):
        try:
            request_data = request.data
            serializer = self.serializer_class(data=request_data)
            if serializer.is_valid(raise_exception=True):
                product = Products.objects.get(pk=product_id)
                product = serializer.update(product, serializer.validated_data)
                return JsonResponse({"product_id": product.pk, "message": "Product updated successfully"},
                                    status=api_status.HTTP_200_OK)
            else:
                return JsonResponse({"message": "Product update failed", "errors": serializer.errors},
                                    status=api_status.HTTP_400_BAD_REQUEST)
        except Products.DoesNotExist:
            return JsonResponse({"message": "Product does not exist"},
                                status=api_status.HTTP_404_NOT_FOUND)


class ProductDeleteView(generics.GenericAPIView):
    """
    This API is used to delete product
    """
    serializer_class = api_serializers.ProductModelSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=["Products"], operation_summary="product delete API")
    def delete(self, request, product_id):
        try:
            product = Products.objects.get(pk=product_id)
            Products.objects.filter(pk=product_id).delete()
            return JsonResponse({"product_id": product_id, "message": "product deleted successfully"},
                                status=api_status.HTTP_200_OK, safe=False)

        except Products.DoesNotExist:
            return JsonResponse({"message": "Product does not exist"},
                                status=api_status.HTTP_404_NOT_FOUND)
