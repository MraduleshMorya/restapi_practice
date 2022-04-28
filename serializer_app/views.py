
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Employee, Employee2
from serializer_app.serializers import EmployeeSerializer,Employee2Serializer,EmployeeSerializer2
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from .authentication import is_token_expired, token_expire_handler, expires_in,authenticate_credentials
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from django.conf import settings
from django.core.mail import send_mail
import base64

def index(request):
    return HttpResponse("Index page ")


@csrf_exempt
def details(request):
    # permission_classes = (IsAuthenticated,)  
    # print(permission_classes)
    if request.method == 'GET':
        db_data = Employee.objects.all()
        serializer = EmployeeSerializer(db_data, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = EmployeeSerializer2(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def employee_detail(request, input_username):
    """
    Retrieve, update or delete a code data_obj.
    """
    try:
        data_obj = Employee.objects.get(username=input_username)
    except Employee.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = EmployeeSerializer(data_obj)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = EmployeeSerializer(data_obj, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        data_obj.delete()
        return HttpResponse(status=204)


##
##  class based serializers
##
@api_view(['GET', 'POST'])
def employee_list(request):
    permission_classes = (IsAuthenticated,)
    if request.method == 'GET':
        db_data = Employee2.objects.all()
        serializer = Employee2Serializer(db_data, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = Employee2Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def employee_detail(request, input_username):
    """
    Retrieve, update or delete a code data_obj.
    """
    try:
        data_obj = Employee2.objects.get(username=input_username)
    except Employee2.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = Employee2Serializer(data_obj)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = Employee2Serializer(data_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        data_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

##
##
##
#@custom_decorator()
class Employee2List(APIView):
    """
    List all db_data, or create a new data_obj.
    """
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        print("user = ", request.user)
        authenticate_credentials(request.auth)
        db_data = Employee2.objects.all()
        serializer = Employee2Serializer(db_data, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        authenticate_credentials(request.auth)
        serializer = Employee2Serializer(data=request.data)
        print("serializer", serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class Employee2Detail(APIView):
    """
    Retrieve, update or delete a data_obj instance.
    """
    def get_object(self, input_username):
        try:
            return Employee2.objects.get(username=input_username)
        except Employee2.DoesNotExist:
            raise Http404

    def get(self, request, input_username, format=None):
        data_obj = self.get_object(input_username)
        serializer = Employee2Serializer(data_obj)
        return Response(serializer.data)

    def put(self, request, input_username, format=None):
        data_obj = self.get_object(input_username)
        serializer = Employee2Serializer(data_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, input_username, format=None):
        data_obj = self.get_object(input_username)
        data_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))   
@csrf_exempt
def user_login(request):
    input_username = request.data.get("username")
    input_password = request.data.get("password")
    
    print("username", input_username)
    print("password", input_password)
    if input_username is None or input_password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=input_username, password=input_password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)

    token, _ = Token.objects.get_or_create(user=user)
    is_expired, token = token_expire_handler(token)
    return Response({'token': token.key},
                    status=HTTP_200_OK)
    
@api_view(["GET"])
def user_info(request):
    return Response({
        'user': request.user.username,
        'expires_in': expires_in(request.auth)
    }, status=HTTP_200_OK)
    


class create_user(APIView):
    """
    List all db_data, or create a new data_obj.
    """
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        db_data = Employee2.objects.all()
        serializer = Employee2Serializer(db_data, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = Employee2Serializer(data=request.data)
        ran = dict(request.data)
        print("passed email",ran["email"])
        message = str(ran["email"])
        message_bytes = message.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        encoded_email = base64_bytes.decode('ascii')
        try:
            subject = 'set your password'
            message = f"""Hi {ran["username"]}, click on this link to set your password  http://127.0.0.1:8000/set_user/{encoded_email}/."""
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [str(ran["email"])]
            send_mail( subject, message, email_from, recipient_list )
        except:
            print("an exception occurrred")
            
        print(encoded_email)
        print("decoded email ", encoded_email)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class set_user(APIView):
    """
    List all db_data, or create a new data_obj.
    """
    def post(self, request, id, format=None):
        serializer = Employee2Serializer(data=request.data)
        print("serializer", serializer)
        try:
            
            base64_message = id
            base64_bytes = base64_message.encode('ascii')
            message_bytes = base64.b64decode(base64_bytes)
            message = message_bytes.decode('ascii')

            print("decoded email",message)
            Employee2.objects.get(email=message)
        except:
            print("an exception occurred ")
        data_obj = Employee2.objects.get(email=message)
        # print("serialized data")
        # temp = Employee2Serializer(data_obj)
        # print(temp.data)

        # print(data_obj)
        ser_data = Employee2Serializer(data_obj)
        print("ser data ",ser_data.data['email'])
        serializer = Employee2Serializer(data_obj, data=request.data)  
        print("printing serializer ", serializer)
          
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)