from rest_framework import mixins
from django.db import transaction, connection
from django.db.models import F, ExpressionWrapper, DecimalField
from django.shortcuts import get_object_or_404, redirect
from .serializers import ProductSerializer, CategorySerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Category, Comment, Product, Customer, OrderItem, Order
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView,GenericAPIView

# @api_view(["GET", "POST"])
# def products_list(request):
#     if request.method == "POST":
#         serializer = ProductSerializer(data=request.data)
#         # if serializer.is_valid():
#         #     serializer.save()
#         serializer.is_valid(raise_exception=True)
#         print(serializer.validated_data)
#         serializer.save()
#         return Response(serializer.data)

#     all_products = Product.objects.select_related("category").all()
#     serializer = ProductSerializer(
#         all_products, many=True, context={"request": request}
#     )
#     return Response(serializer.data)


# class ProductList(APIView):
#     def get(self, request):
#         all_products = Product.objects.select_related("category").all()
#         serializer = ProductSerializer(
#             all_products, many=True, context={"request": request}
#         )
#         return Response(serializer.data)
#     def post(self,request):
#         serializer = ProductSerializer(data=request.data)
#         # if serializer.is_valid():
#         #     serializer.save()
#         serializer.is_valid(raise_exception=True)
#         print(serializer.validated_data)
#         serializer.save()
#         return Response(serializer.data)

class ProductList(ListCreateAPIView):
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer


# @api_view(["GET", "PUT", "PATCH", "DELETE"])
# def product_detail(request, pk):
#     product = get_object_or_404(Product.objects.select_related("category"), pk=pk)
#     if request.method == "GET":
#         serializer = ProductSerializer(product, context={"request": request})
#         return Response(serializer.data)

#     elif request.method == "PUT":
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == "DELETE":
#         if not OrderItem.objects.filter(product=product.id):
#             product.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         else:
#             return Response("this is related to the orderitem, delete it first")


# class ProductDetail(APIView):
#     def get(self,request,pk):
#         product = get_object_or_404(Product.objects.select_related("category"), pk=pk)
#         serializer = ProductSerializer(product, context={"request": request})
#         return Response(serializer.data)
#     def put(self,request,pk):
#         product = get_object_or_404(Product.objects.select_related("category"), pk=pk)
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     def delete(self,request):
#         product = get_object_or_404(Product.objects.select_related("category"), pk=pk)
#         if not OrderItem.objects.filter(product=product.id):
#             product.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         else:
#             return Response("this is related to the orderitem, delete it first")

class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset= Product.objects.all()
    serializer_class = ProductSerializer

    


    

# @api_view(["GET", "POST"])
# def category_list(request):
#     if request.method == "GET":
#         categories = Category.objects.all()
#         serializer = CategorySerializer(categories, many=True)
#         return Response(serializer.data)
#     elif request.method == "POST":
#         serializer = CategorySerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)



# class CategoryList(APIView):
#     def get(self,request):
#         categories = Category.objects.all()
#         serializer = CategorySerializer(categories, many=True)
#         return Response(serializer.data)
#     def post(self,request):
#         serializer = CategorySerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)

class CategoryList(ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


# @api_view(["GET", "PUT", "DELETE"])
# def category_detail(request, pk):

#     category_detail = get_object_or_404(Category, id=pk)
#     if request.method == "GET":
#         serializer = CategorySerializer(category_detail)
#         return Response(serializer.data)

#     elif request.method == "PUT":
#         serializer = CategorySerializer(category_detail, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

#     elif request.method == "DELETE":
#         if not Product.objects.filter(category=category_detail.id):
#             category_detail.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         else:
#             return Response(
#                 "You Cannot Remove This Category, Due TO , its dependency to product object",
#                 status=status.HTTP_400_BAD_REQUEST,
#             )


# class CategoryDetail(APIView):

#     def get(self,request,pk):
#         category_detail = get_object_or_404(Category, id=pk)
#         serializer = CategorySerializer(category_detail)
#         return Response(serializer.data)
#     def put(self,request,pk):
#         category_detail = get_object_or_404(Category, id=pk)
#         serializer = CategorySerializer(category_detail, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     def delete(self,request,pk):
#         category_detail = get_object_or_404(Category, id=pk)
#         if not Product.objects.filter(category=category_detail.id):
#             category_detail.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         else:
#             return Response(
#                 "You Cannot Remove This Category, Due TO , its dependency to product object",
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
        

class CategoryDetail(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    def delete(self,request,pk):
        category_detail = get_object_or_404(Category, id=pk)
        if not Product.objects.filter(category=category_detail.id):
            category_detail.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                "You Cannot Remove This Category, Due TO , its dependency to product object",
                status=status.HTTP_400_BAD_REQUEST,
            )








