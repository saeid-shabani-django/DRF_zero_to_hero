from rest_framework import mixins
from django.db import transaction, connection
from django.db.models import F, ExpressionWrapper, DecimalField, Prefetch
from django.shortcuts import get_object_or_404, redirect
from rest_framework.decorators import action

from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
    DjangoModelPermissions,
)

from store.permissions import (
    CustomDjangoModelPermission,
    IsAdminOrReadOnly,
    SendPrivateEmail,
)
from .serializers import (
    OrderCreateSerializer,
    ProductSerializer,
    CategorySerializer,
    CommentSerializer,
    CartSerializer,
    CartItemSerializer,
    CreateCartItemSerializer,
    UpdateCartItemSerializer,
    CustomerSerializer,
    OrderSerializer,
    OrderItemSerializer,
    OrderUpdateSerializer,
)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import (
    Category,
    Comment,
    Product,
    Customer,
    OrderItem,
    Order,
    Cart,
    CartItem,
)
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    GenericAPIView,
)
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter

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

# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     queryset= Product.objects.all()
#     serializer_class = ProductSerializer

# class ProductList(ListCreateAPIView):
#     queryset = Product.objects.select_related('category').all()
#     serializer_class = ProductSerializer


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

# class CategoryList(ListCreateAPIView):
#     serializer_class = CategorySerializer
#     queryset = Category.objects.all()

# class CategoryDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
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


class ProductViewSet(ModelViewSet):
    # queryset = Product.objects.select_related("category").all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    # filterset_fields =['category_id','name']
    ordering_fields = ["inventory", "unit_price"]
    search_fields = [
        "name",
    ]
    # permission_classes = [CustomDjangoModelPermission,]
    filterset_class = ProductFilter

    def get_queryset(self):
        queryset = Product.objects.select_related("category").all()
        category_id = self.request.query_params.get("category_id")
        if category_id is not None:
            return queryset.filter(category_id=category_id)
        else:
            return queryset

    def destroy(self, request, pk):
        product = get_object_or_404(Product.objects.select_related("category"), pk=pk)
        if not OrderItem.objects.filter(product=product.id):
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("this is related to the orderitem, delete it first")


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.prefetch_related("products").all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

    def destory(self, request, pk):

        category_detail = get_object_or_404(Category, pk=pk)

        if len(Product.objects.filter(category=category_detail.id)) > 0:

            return Response(
                "You Cannot Remove This Category, Due TO , its dependency to product object"
            )
        else:

            category_detail.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        product_pk = self.kwargs["product_pk"]
        comments = Comment.objects.filter(product_id=product_pk)
        return comments

    def get_serializer_context(self):
        product_pk = self.kwargs["product_pk"]
        return {"product_pk": product_pk}


class CartViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    # permission_classes=[IsAdminUser]
    queryset = Cart.objects.prefetch_related("items__product").all()
    serializer_class = CartSerializer
    # lookup_value_regex = "^[0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12}$"


class CartItemViewSet(ModelViewSet):
    http_method_names = ["get", "patch", "delete", "head", "options", "post"]

    def get_queryset(self):
        cart_pk = self.kwargs["cart_pk"]
        return CartItem.objects.select_related("product").filter(cart_id=cart_pk).all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateCartItemSerializer
        elif self.request.method == "PATCH":
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        cart_pk = self.kwargs["cart_pk"]
        return {"cart_pk": cart_pk}


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]

    @action(detail=False, methods=["get", "put"], permission_classes=[IsAuthenticated])
    def me(self, request):
        user_id = request.user.id
        customer = Customer.objects.get(id=user_id)

        if request.method == "GET":
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)

        elif request.method == "PUT":
            all_data = request.data
            serializer = CustomerSerializer(customer, data=all_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

    @action(detail=True, permission_classes=[SendPrivateEmail])
    def send_private_email(self, request, pk):
        return Response(f"everythins is ok you are number of {pk}")


class OrderViewSet(ModelViewSet):
    http_method_names = ['post','get','head','options','patch','delete']
    def get_permissions(self):
        if self.request.method in ['DELETE','PATCH']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return OrderCreateSerializer
        if self.request.method == 'PATCH':
            return OrderUpdateSerializer
        return OrderSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return (
                Order.objects.select_related("customer")
                .prefetch_related(
                    Prefetch(
                        "items", queryset=OrderItem.objects.select_related("product")
                    )
                )
                .all()
            )

        return Order.objects.filter(customer__user_id=self.request.user.id)

    def get_serializer_context(self):
        user_id = self.request.user.id
        return {"user_id": user_id}

    def create(self, request, *args, **kwargs):
        created_serializer = OrderCreateSerializer(
            data=request.data, context={"user_id": self.request.user.id}
        )
        created_serializer.is_valid(raise_exception=True)
        final_serializer = created_serializer.save()
        return Response(OrderSerializer(final_serializer).data)
