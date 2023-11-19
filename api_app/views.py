from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
import rest_framework.status as api_status
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated


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

