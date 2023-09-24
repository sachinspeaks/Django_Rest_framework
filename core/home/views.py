from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from home.models  import *
from home.serializer import *
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator


class LoginAPI(APIView):

    def post(self,request):
        data=request.data
        serializer=LoginSerializer(data=data)
        if not serializer.is_valid():
            return Response({"status":False,"message":serializer.errors},status.HTTP_401_UNAUTHORIZED)
        
        
        user=authenticate(username=serializer.data['username'],password=serializer.data['password'])
        if not user:
            return Response({"status":False,"message":"Invalid Credentials"},status.HTTP_401_UNAUTHORIZED)

        token=Token.objects.create(user=user)
        return Response({'status':True,'message':'user login successful','token':str(token)},status.HTTP_201_CREATED)



class RegisterAPI(APIView):
    def post(self,request):
        data=request.data
        serializer=RegisterSerializer(data=data)
        if not serializer.is_valid():
            return Response({"status":False,"message":serializer.errors},status.HTTP_401_UNAUTHORIZED)
        
        serializer.save()

        return Response({"status":True,"message":"User Created"},status.HTTP_201_CREATED)




class PersonAPI(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get(self,request):
        try:
            objs=Person.objects.filter()
            page=request.GET.get('page',1)
            page_size=3
            paginator=Paginator(objs,page_size)
            print(paginator.page(page))
            serializer=PersonSerializer(paginator.page(page),many=True)   
        except Exception as e:
            return Response({"status":False,"message":"Invalid Page Number"""})     


        
        return Response(serializer.data)
    def post(self,request):
        data=request.data
        serializer=PersonSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)
    def put(self,request):
        data=request.data
        serializer=PersonSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)
    def patch(self,request):
        data=request.data
        obj=Person.objects.get(id=data['id'])
        serializer=PersonSerializer(obj,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)
    def delete(self,request):
        data=request.data
        obj=Person.objects.get(id=data['id'])
        obj.delete()
        return Response({"Messsage":"Person Deleted"})





@api_view(['GET','POST'])
def index(request):
    courses={
    'course_name':"Python",
    'learn':["flask","django","tornado","fast-api"],
    'course_provider':'Scalar'
    }
    if request.method=='GET':
        print("Get called")
        print(request.GET.get('search'))
        return Response(courses)
    elif request.method=='POST':
        data=request.data
        print("Post called")
        print(data)
        return Response(courses)


@api_view(['POST','PUT','PATCH','DELETE'])
def login(request):
    data=request.data
    serializer=LoginSerializer(data=data)

    if serializer.is_valid():
        data=serializer.validated_data
        print(data)
        return Response({"message":"Login successful"})

    return Response(serializer.errors)


    
@api_view(['GET','POST','PUT','PATCH','DELETE'])
def person(request):
    if request.method=='GET':
        objs=Person.objects.filter(color__isnull=False)
        serializer=PersonSerializer(objs,many=True)
        return Response(serializer.data)
    
    elif request.method=='POST':
        data=request.data
        serializer=PersonSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)
    
    elif request.method=='PUT':
        data=request.data
        serializer=PersonSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)
    
    elif request.method=='PATCH':
        data=request.data
        obj=Person.objects.get(id=data['id'])
        serializer=PersonSerializer(obj,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)

    else:
        data=request.data
        obj=Person.objects.get(id=data['id'])
        obj.delete()
        return Response({"Messsage":"Person Deleted"})




class PersonViewSet(viewsets.ModelViewSet):
    serializer_class=PersonSerializer
    queryset=Person.objects.all()

    def  list(self,request):
        search=request.GET.get('search')
        queryset=self.queryset
        if search:
            queryset=queryset.filter(name__startswith=search)
        serializers=PersonSerializer(queryset,many=True)
        return Response({"Status":200,"data":serializers.data},status=status.HTTP_204_NO_CONTENT)