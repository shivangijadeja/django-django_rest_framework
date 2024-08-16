from django.shortcuts import render
from .models import Category,Blogs
from .serializers import CategorySerializer,BlogSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from User.decorators import require_authentication
from User.models import UserSignup
from django.utils.decorators import method_decorator

# Create your views here.
class CategoryApi(APIView):

    def get(self,request):
        categories=Category.objects.all()
        serializer=CategorySerializer(categories,many=True)
        return Response({'message':serializer.data},status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer=CategorySerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error':serializer.errors,'message':'Data is not valid, Please enter valid data!'}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({'payload':request.data,'message':'Category created successfully!!'},status=status.HTTP_200_OK)

class BlogApi(APIView):

    def get(self,request):
        blogs=Blogs.objects.all()
        serializer=BlogSerializer(blogs,many=True)
        return Response({'message':serializer.data},status=status.HTTP_200_OK)
    
    @method_decorator(require_authentication,name="dispatch")
    def post(self,request, *args, **kwargs):
        if kwargs["auth_status"]:
            user_obj=UserSignup.objects.get(username=request.session['username'])
            request.data['created_by']=user_obj.id
            serializer=BlogSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({'error':serializer.errors,'message':'Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({'message':'Blog created successfully!!'},status=status.HTTP_200_OK)
        else:
            return Response({'message':'First you have to login!!'},status=status.HTTP_401_UNAUTHORIZED)

    def delete(self,request):
        try:
            blog_obj=Blogs.objects.get(id=request.data['id'])
            user_obj=UserSignup.objects.get(username=request.session['username'])
            if blog_obj.created_by.id==user_obj.id:
                blog_obj.delete()
                return Response({'message':'Blog deleted!!'}, status=status.HTTP_200_OK)
            else:
                return Response({'message':'You can not delete others blogs!!'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({'message':'Invalid id!!'}, status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self,request):
        blog_obj=Blogs.objects.get(id=request.data['id'])
        user_obj=UserSignup.objects.get(username=request.session['username'])
        if blog_obj.created_by.id==user_obj.id:
            updated_data={
                "title":request.data['title'],
                "description":request.data['description'],
                "category":request.data['category'],
                "image":request.data['image'],
                "slug":blog_obj.slug,
                "created_by":blog_obj.created_by.id
            }
            serializer=BlogSerializer(blog_obj,data=updated_data,partial=True)
            if not serializer.is_valid():
                return Response({'error':serializer.errors,'message':'Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({'message':'Your blog is updated now!!'},status=status.HTTP_200_OK)
        else:
            return Response({'message':'You can not update others blogs!!'}, status=status.HTTP_400_BAD_REQUEST)
