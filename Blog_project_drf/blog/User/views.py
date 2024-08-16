from django.shortcuts import render
from rest_framework.response import Response
from .models import UserSignup,UserLogin
from .serializers import SignupSerializer,LoginSerializer
from rest_framework.views import APIView
import random
from cryptography.fernet import Fernet
from rest_framework import status
from datetime import datetime
from django.core.mail import send_mail
from django.utils.decorators import method_decorator
from .decorators import require_authentication

chars = 'abcdefghijklmnopqrstuvwxyz' \
        'ABCDEFGHIJKLMNOPQRSTUVXYZ' \
        '0123456789' \
        '#()^[]-_*%&=+/'

digits='0123456789'
# Create your views here.

key = b'lCg_aLx7Eblj3OkEnKx-AU20eI5Q9x_GN6IHTOtfCws='
fernet = Fernet(key)

class UserApi(APIView):

    def get(self,request):
        users=UserSignup.objects.all()
        serializer=SignupSerializer(users,many=True)
        return Response({'payload':serializer.data},status=status.HTTP_200_OK)

    def post(self,request):
        data=request.data
        pwd=data['password']
        if len(pwd)>=3:
            data['password'] = (fernet.encrypt(pwd.encode())).decode('utf-8')
        else:
            return Response({'message':'password should atleast 3 characters long!'}, status=status.HTTP_400_BAD_REQUEST)
        if 'secretkey' not in data.keys():
            secret_key = ''.join([random.SystemRandom().choice(chars) for i in range(50)])
            data['secretkey']=secret_key    
        serializer=SignupSerializer(data=data)
        if not serializer.is_valid():
            return Response({'error':serializer.errors,'message':'Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({'message':'User created successfully!!'},status=status.HTTP_200_OK)

    
    @method_decorator(require_authentication, name="dispatch")
    def delete(self,request, *args, **kwargs):
        try:
            user_obj=UserSignup.objects.get(id=request.data['id'])
            if request.session['username']==user_obj.username and kwargs["auth_status"]:
                user_obj.delete()
                request.session.clear()
                return Response({'message':'Record deleted!!'}, status=status.HTTP_200_OK)
            else:
                return Response({'message':'You can not delete other user!!'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({'message':'Invalid id'}, status=status.HTTP_400_BAD_REQUEST)


class LoginApi(APIView):

    def get(self,request):
        user=UserSignup.objects.get(username=request.data['username'])
        decrypted_password = fernet.decrypt(bytes(user.password, 'utf-8')).decode('utf-8')
        if request.data['password']==decrypted_password:
            otp=''.join(random.choices(digits,k=6))
            send_mail(
            'Your OTP Code',
            f'Your OTP code is {otp}. It is valid for 10 minutes.',
            'shivangi.royalbrothers@gmail.com',
            [user.email],
            fail_silently=False,
            )
            request.session['otp']=otp
            request.session['username']=user.username
            request.session['secretkey']=user.secretkey
            return Response({'message':"OTP sent to your mail, please add OTP and username for verification"},status=status.HTTP_200_OK)
        else:
            return Response({'message':'Entered data is incorrect!!'}, status=status.HTTP_400_BAD_REQUEST)


    def post(self,request):
        if request.session['otp']==request.data['otp']:
            user=UserSignup.objects.get(username=request.data['username'])
            if user.secretkey==request.session['secretkey']:
                login_data={
                    "user":user.id,
                    "otp":request.data['otp'],
                    "login_session":datetime.now()
                }
                serializer=LoginSerializer(data=login_data)
                if not serializer.is_valid():
                    return Response({'error':serializer.errors,'message':'Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)
                serializer.save()
            return Response({'payload':login_data,'message':'User logged in successfully..'},status=status.HTTP_200_OK)
        else:
            return Response({'message':'OTP is not correct, Please try again'}, status=status.HTTP_400_BAD_REQUEST)

    
@method_decorator(require_authentication, name="dispatch")
class LogoutApi(APIView):
    def get(self,request, *args, **kwargs):
        if kwargs["auth_status"]:
            request.session.clear()
            kwargs["auth_status"]=False
            return Response({'message':"Logged out!!"}, status=status.HTTP_200_OK)
        return Response({"message":"Not logged in"}, status=status.HTTP_400_BAD_REQUEST)
    
@method_decorator(require_authentication,name="dispatch")
class UserDetails(APIView):

    def get(self,request, *args, **kwargs):
        if kwargs["auth_status"]:
            user_obj=UserSignup.objects.get(username=request.session['username'])
            details={
                "username":user_obj.username,
                "email":user_obj.email,
                "contact":user_obj.contact
            } 
            return Response({'User details':details}, status=status.HTTP_200_OK)
        return Response({"message":"For see details first you need to login!"}, status=status.HTTP_400_BAD_REQUEST)
    
@method_decorator(require_authentication,name="dispatch")
class ChangePassword(APIView):

    def patch(self,request, *args, **kwargs):
        if kwargs["auth_status"]:
            user_obj=UserSignup.objects.get(username=request.data['username'])
            decrypted_password=fernet.decrypt(bytes(user_obj.password, 'utf-8')).decode('utf-8')
            if request.data['password']==decrypted_password and request.data['new_password']==request.data['confirm_new_password'] and len(request.data['new_password'])>=3:
                pwd=request.data['new_password']
                encrypted_pwd=(fernet.encrypt(pwd.encode())).decode('utf-8')
                updated_data={
                    "username":user_obj.username,
                    "password":encrypted_pwd,
                    "email":user_obj.email,
                    "contact":user_obj.contact
                }
                serializer=SignupSerializer(user_obj,data=updated_data,partial=True)
                if not serializer.is_valid():
                    return Response({'status':403,'error':serializer.errors,'message':'Something went wrong!'})
                serializer.save()
                return Response({'status':200,'message':'Your password is updated now!!'})
        return Response({"message":"First you have to login then you can change your password!"}, status=status.HTTP_400_BAD_REQUEST)