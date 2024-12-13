from decimal import Decimal
from rest_framework import serializers
from django.contrib.auth import get_user_model
from config import settings
from .models import Category, Customer, Product, Comment, Cart, CartItem, Order,OrderItem
from django.utils.text import slugify

# class CategorySerializer(serializers.Serializer):
# id = serializers.IntegerField()
# title = serializers.CharField(max_length=255)
# description = serializers.CharField(max_length=500)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "title", "description"]


# class ProductSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     name = serializers.CharField(max_length=255)
#     category = serializers.HyperlinkedRelatedField(
#         queryset = Category.objects.all(),
#         view_name = 'category_detail',
#     )
#     unit_price = serializers.DecimalField(max_digits=6, decimal_places=2)
#     inventory = serializers.IntegerField()
#     unit_price_after_tax = serializers.SerializerMethodField()


#     def get_unit_price_after_tax(self,product):
#         return round(product.unit_price * Decimal(1.09),4)


class ProductSerializer(serializers.ModelSerializer):
    # category = serializers.StringRelatedField()

    class Meta:
        model = Product

        fields = [
            "id",
            "name",
            "category",
            "unit_price",
            "inventory",
            "unit_price_after_tax",
        ]
       
    unit_price_after_tax = serializers.SerializerMethodField(read_only=True)
    def get_unit_price_after_tax(self, product):
        return round(product.unit_price * Decimal(1.09), 4)

    def validate(self, data):

        self.unit_price = int(data["unit_price"])
        if self.unit_price > 32:
            raise serializers.ValidationError("unit price must be less than 32")
        else:
            return data

    def create(self, validated_data):
        self.name = validated_data.get("name")
        slug = slugify(self.name)
        new_product = Product.objects.create(slug=slug, **validated_data)
        return new_product
    
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment 
        fields = ['id','product','name','body','status']
        read_only_fields = ['id','product','status']
    product =ProductSerializer(read_only=True)

    def create(self, validated_data):
        product_pk = self.context['product_pk']
        comment = Comment.objects.create(product_id=product_pk,**validated_data)
        # comment.product_id = product_pk
        # comment.name = validated_data['name']
        # comment.body = validated_data['body']
        # comment.save()
        return comment
   
class ProductCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name','unit_price']



class CreateCartItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CartItem
        fields = ['id','product','quantity']

    def create(self, validated_data):
        quantity = validated_data.get('quantity')
        cart_pk = self.context.get('cart_pk')
        product = validated_data.get('product')
        if CartItem.objects.filter(cart_id=cart_pk,product_id = product.id).exists():
            cart_item = CartItem.objects.get(product_id = product.id,cart_id=cart_pk)
            cart_item.quantity += quantity
            cart_item.save()
            return cart_item
        else:
            return CartItem.objects.create(cart_id=cart_pk,**validated_data)
        


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductCartItemSerializer(read_only=True)
    class Meta:
        model = CartItem
        fields =['id','product','quantity','item_price']
    item_price = serializers.SerializerMethodField()
    def get_item_price(self,item):
        return (item.product.unit_price * item.quantity)

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True,read_only=True)
    class Meta:
        model = Cart
        fields = ['id','items','total_price']
        read_only_fields=['id',]
    total_price = serializers.SerializerMethodField()
    
    def get_total_price(self,cart):
        return sum([item.product.unit_price*item.quantity for item in cart.items.all()])
        
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id','first_name','last_name','email']

class CustomerSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    class Meta:
        model = Customer
        fields = ['id','user','birth_date','phone_number']
        read_only_fields = ['id','user']

class ProductOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name']

class OrderItemSerializer(serializers.ModelSerializer):
    
    product = ProductOrderItemSerializer()
    class Meta:
        model = OrderItem
        fields = ['id','order','product','quantity','unit_price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    customer = CustomerSerializer()
    class Meta:
        model = Order
        fields = ['id','customer','status','items']


class OrderCreateSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self,cart_id):
        if not Cart.objects.filter(id=cart_id).exists():
            raise serializers.ValidationError('the cart id you entered does not exist')
        elif Cart.objects.filter(id=cart_id).count() == 0:
            raise serializers.ValidationError('the cart is empty')
        return cart_id
    
    def save(self, **kwargs):
        cart_id = self.validated_data['cart_id']
        user_id = self.context.get('user_id')

        order = Order()
        customer = Customer.objects.get(user_id = user_id)
        order.customer = customer
        order.save()
        cart = Cart(id=cart_id)
        items = cart.items.all()
        order_items = list()
        for cart_item in items:
            order_item = OrderItem()
            order_item.product_id = cart_item.product_id
            order_item.order=order
            order_item.quantity = cart_item.quantity
            order_item.unit_price = cart_item.product.unit_price
            order_items.append(order_item)
            cart_item.delete()
        Cart.objects.get(id=cart_id).delete()
        OrderItem.objects.bulk_create(order_items)
        return order
        
        


    


