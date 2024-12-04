from django.db import transaction, connection
from django.db.models import F, ExpressionWrapper, DecimalField
from django.shortcuts import get_object_or_404, redirect
from .serializers import ProductSerializer,CategorySerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Category, Comment, Product, Customer, OrderItem, Order
from rest_framework import status


@api_view(['GET','POST'])
def products_list(request):
    if request.method == 'POST':
        serializer = ProductSerializer(data= request.data)
        # if serializer.is_valid():
        #     serializer.save()
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        serializer.save()
        return Response(serializer.data)
       
        
    all_products = Product.objects.select_related('category').all()
    serializer = ProductSerializer(all_products, many=True,context={'request':request})
    return Response(serializer.data)

@api_view(['GET','PUT','PATCH','DELETE'])
def product_detail(request,pk):
    product = get_object_or_404(Product.objects.select_related('category'),pk=pk)
    if request.method == 'GET':
        serializer = ProductSerializer(product,context={'request':request})
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = ProductSerializer(product,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)






@api_view()
def category_list(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories,many= True)
    return Response(serializer.data)

@api_view()
def category_detail(request,pk):
    category_detail = get_object_or_404(Category,id=pk)
    serializer = CategorySerializer(category_detail)
    return Response(serializer.data)
