# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from orders.models import Order, Product
from .serializers import ProductSerializer , OrderCreateSerializer
import csv
from django.http import HttpResponse


class ProductListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        company = request.user.company
        products = Product.objects.filter(company=company, is_active=True, is_deleted=False)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ProductDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        ids = request.data.get("ids", [])
        company = request.user.company

        Product.objects.filter(
            id__in=ids,
            company=company
        ).update(is_active=False, is_deleted=True)

        return Response({"message": "Products soft-deleted"})

class OrderCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        product = serializer.validated_data["product"]
        quantity = serializer.validated_data["quantity"]
        user = request.user

        # Create the order
        order = Order.objects.create(
            company=user.company,
            product=product,
            quantity=quantity,
            created_by=user
        )

        # Reduce stock
        product.stock -= quantity
        product.save()

        return Response({"message": "Order created", "order_id": order.id})




class OrderExportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        company = request.user.company
        orders = Order.objects.filter(company=company)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="orders.csv"'

        writer = csv.writer(response)
        writer.writerow(["ID", "Product", "Quantity", "Status", "Created By", "Created At"])

        for order in orders:
            writer.writerow([
                order.id,
                order.product.name,
                order.quantity,
                order.status,
                order.created_by.username if order.created_by else "",
                order.created_at,
            ])

        return response


from datetime import date

class OrderUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        order = Order.objects.get(id=pk, company=request.user.company)

        user = request.user

        if user.role == "viewer":
            return Response({"error": "Viewer cannot edit orders"}, status=403)

        if user.role == "operator":
            if order.created_at.date() != date.today():
                return Response({"error": "Operators may edit only today's orders"}, status=403)
