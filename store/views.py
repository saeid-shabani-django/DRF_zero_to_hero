from django.db import transaction, connection
from django.db.models import F, ExpressionWrapper, DecimalField
from django.shortcuts import get_object_or_404
from .serializers import ProductSerializer,CategorySerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Category, Comment, Product, Customer, OrderItem, Order
from rest_framework import status


@api_view()
def products_list(request):
    all_products = Product.objects.select_related('category').all()
    serializer = ProductSerializer(all_products, many=True,context={'request':request})
    return Response(serializer.data)

@api_view()
def product_detail(request,pk):
    # product = get_object_or_404(Product,id=pk)
    try:
        product = Product.objects.select_related('category').get(id=pk)
    except Product.DoesNotExist:
        return Response('this product is not exist anymore',status= status.HTTP_404_NOT_FOUND)
    serializer = ProductSerializer(product)
    return Response(serializer.data)

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
