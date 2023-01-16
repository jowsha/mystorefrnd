from rest_framework import serializers
from api.models import Products,Review,Cart


class ProductsSerializer(serializers.Serializer):
    name=serializers.CharField()
    description=serializers.CharField()
    category=serializers.CharField()
    price=serializers.IntegerField()
    image=serializers.ImageField()


class ProductModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=Products
        fields=["name","description","category","price","image"]

class ReviewSerializer(serializers.ModelSerializer):
    user=serializers.CharField(read_only=True)
    product_name=serializers.CharField(read_only=True)
    class Meta:
        model=Review
        fields=["review","product_name","user","rating"]

    def create(self,validated_data):
        user=self.context.get("user")
        product=self.context.get("product")
        return Review.objects.create(**validated_data,user=user,product_name=product)

class CartSerialzer(serializers.ModelSerializer):
    user=serializers.CharField(read_only=True)
    product=serializers.CharField(read_only=True)
    date=serializers.CharField(read_only=True)
    class Meta:
        model=Cart
        fields=[
            "user",
            "product",
            "date"
        ]
    
    def create(self, validated_data):
        user=self.context.get("user")
        product=self.context.get("product")
        return Cart.objects.create(**validated_data,user=user,product=product)