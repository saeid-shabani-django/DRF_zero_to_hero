from decimal import Decimal
from rest_framework import serializers
from .models import Category

# class CategorySerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)
#     description = serializers.CharField(max_length=500)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','title','description']


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    category = serializers.HyperlinkedRelatedField(
        queryset = Category.objects.all(),
        view_name = 'category_detail',
    )
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2)
    inventory = serializers.IntegerField()
    unit_price_after_tax = serializers.SerializerMethodField()
    

    def get_unit_price_after_tax(self,product):
        return round(product.unit_price * Decimal(1.09),4)


