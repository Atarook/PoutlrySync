from rest_framework import serializers
from orders.models import Order, Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'company', 'name', 'price', 'stock', 'is_active']

class OrderCreateSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()

    def validate(self, data):
        request = self.context["request"]
        user = request.user
        company = user.company

        if user.role == "viewer":
            raise serializers.ValidationError("Viewer cannot create orders.")

        try:
            product = Product.objects.get(id=data["product_id"], company=company)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product does not exist for your company.")

        if not product.is_active:
            raise serializers.ValidationError("Product is inactive.")

        if product.stock < data["quantity"]:
            raise serializers.ValidationError("Not enough stock.")

        data["product"] = product
        return data
