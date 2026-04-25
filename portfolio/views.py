from django.shortcuts import render
from .utils import get_stock_price
# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Portfolio
from .serializers import PortfolioSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_stock(request):
    serializer = PortfolioSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data)

    return Response(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def portfolio_summary(request):
    stocks = Portfolio.objects.filter(user=request.user)

    result = []
    total_investment = 0
    total_current_value = 0

    for stock in stocks:
        current_price = get_stock_price(stock.stock_name)

        investment = stock.quantity * stock.buy_price
        current_value = stock.quantity * current_price
        profit_loss = current_value - investment

        total_investment += investment
        total_current_value += current_value

        result.append({
            "stock": stock.stock_name,
            "quantity": stock.quantity,
            "buy_price": stock.buy_price,
            "current_price": current_price,
            "investment": investment,
            "current_value": current_value,
            "profit_loss": profit_loss
        })

    return Response({
        "total_investment": total_investment,
        "total_current_value": total_current_value,
        "overall_profit_loss": total_current_value - total_investment,
        "stocks": result
    })