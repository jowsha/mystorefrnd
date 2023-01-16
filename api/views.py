from django.shortcuts import render
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.response import Response
from api.serialize import ProductsSerializer,ProductModelSerializer,ReviewSerializer,CartSerialzer
from api.models import Products,Review,Cart
from rest_framework.decorators import action
from rest_framework import authentication,permissions
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.parsers import FileUploadParser
from rest_framework.parsers import MultiPartParser, FormParser


# Create your views here.

# list() create() retrieve() update() destroy()
class ProductsView(ModelViewSet):
    # parser_class = (MultiPartParser, FormParser)
    serializer_class=ProductModelSerializer
    queryset=Products.objects.all()
    # authentication_classes=[authentication.BasicAuthentication]
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    # def list(self,request,*args,**kwargs):
    #     qs=Products.objects.all()
    #     serialzer=ProductModelSerializer(qs,many=True) #deserializer
    #     return Response(data=serialzer.data)

    # def create(self,request,*args,**kwargs):
    #     serialzer=ProductModelSerializer(data=request.data)
    #     if serialzer.is_valid():
    #         serialzer.save()
    #         # Products.objects.create(**serialzer.validated_data)
    #         return Response(data=serialzer.data)
    #     else:
    #         return Response(data=serialzer.errors)

    # def retrieve(self,request,*args,**kwargs):
    #     id=kwargs.get("pk")
    #     qs=Products.objects.get(id=id)
    #     serialzer=ProductModelSerializer(qs)
    #     return Response(data=serialzer.data)

    # def update(self,request,*args,**kwargs):
    #     id=kwargs.get("pk")
    #     qs=Products.objects.get(id=id)
    #     serialzer=ProductModelSerializer(data=request.data,instance=qs)
    #     if serialzer.is_valid():
    #         serialzer.save()
    #         return Response(data=serialzer.data)
    #     else:
    #         return Response(data=serialzer.errors)

    # def destroy(self,request,*args,**kwargs):
    #     id=kwargs.get("id")
    #     Products.objects.get(id=id).delete()
    #     return Response(data="deleted")
        
    # def partial_update(self,request,*args,**kw):
    #      id=kw.get("pk")
    #      qs=Products.objects.get(id=id)
    #      serialzer=ProductModelSerializer(data=request.data,instance=qs)
    #      if serialzer.is_valid():
    #         serialzer.save()
    #         return Response(data=serialzer.data)
    #      else:
    #         return Response(data=serialzer.errors)

    @action(methods=["get"],detail=False) #custom methods call cheyannn,first action import cheyannm,detail id pass cheyannn True
    def categories(self,request,*args,**kw):
        categories=Products.objects.values_list('category',flat=True).distinct() #flat is uesd to convert tuple to list ,distinct is used to avoid dupilcte nsme
        return Response(data=categories)
    @action(methods=["post"],detail=True)
    def add_review(self,request,*args,**kw):
        user=request.user
        product=self.get_object()# get object is used to get id,product object kittaan
        serializer=ReviewSerializer(data=request.data,context={"user":user,"product":product})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
    # localhost:8000/products/1/review/
    @action(methods=["get"],detail=True)
    def reviews(self,request,*args,**kw):
        product=self.get_object()
        qs=Review.objects.filter(product_name=product)
        serialzer=ReviewSerializer(qs,many=True)
        return Response(data=serialzer.data)
    
    @action(methods=["get"],detail=True)
    def addtocart(self,request,*args,**kw):
        product=self.get_object()
        user=request.user 
        serializer=CartSerialzer(data=request.data,context={"product":product,"user":user})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

# localhost:8000/users/carts
        
class CartsView(GenericViewSet,ListModelMixin):
    serializer_class=CartSerialzer
    queryset=Cart.objects.all()
    # authentication_classes=[authentication.BasicAuthentication]
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
    