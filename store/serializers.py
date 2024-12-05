from decimal import Decimal
from rest_framework import serializers
from .models import Category, Product, Comment
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
   
