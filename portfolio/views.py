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
    stock_name = request.data.get('stock_name').upper()
    quantity = int(request.data.get('quantity'))
    buy_price = float(request.data.get('buy_price'))

    # 🔍 Check if stock already exists
    existing_stock = Portfolio.objects.filter(
        user=request.user,
        stock_name=stock_name
    ).first()

    if existing_stock:
        # 🧠 Calculate new average price
        total_quantity = existing_stock.quantity + quantity

        total_cost = (
            existing_stock.quantity * existing_stock.buy_price +
            quantity * buy_price
        )

        avg_price = total_cost / total_quantity

        existing_stock.quantity = total_quantity
        existing_stock.buy_price = avg_price
        existing_stock.save()

        return Response({
            "message": "Stock updated",
            "stock": stock_name,
            "new_quantity": total_quantity,
            "avg_price": avg_price
        })

    # ➕ If not exists → create new
    serializer = PortfolioSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(user=request.user, stock_name=stock_name)
        return Response(serializer.data)

    return Response(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def portfolio_summary(request):
    stocks = Portfolio.objects.filter(user=request.user)

    result = []
    total_investment = 0
    total_current_value = 0

    max_profit = float('-inf')
    min_profit = float('inf')
    top_gainer = None
    top_loser = None

    for stock in stocks:
        current_price = get_stock_price(stock.stock_name)

        investment = stock.quantity * stock.buy_price
        current_value = stock.quantity * current_price
        profit_loss = current_value - investment

        total_investment += investment
        total_current_value += current_value

        # 🔹 Track top gainer
        if profit_loss > max_profit:
            max_profit = profit_loss
            top_gainer = stock.stock_name

        # 🔹 Track top loser
        if profit_loss < min_profit:
            min_profit = profit_loss
            top_loser = stock.stock_name

        result.append({
            "stock": stock.stock_name,
            "quantity": stock.quantity,
            "buy_price": stock.buy_price,
            "current_price": current_price,
            "investment": investment,
            "current_value": current_value,
            "profit_loss": profit_loss
        })

    overall_profit = total_current_value - total_investment

    # 🔹 % Growth
    growth_percent = (
        (overall_profit / total_investment) * 100
        if total_investment > 0 else 0
    )

    return Response({
        "total_investment": total_investment,
        "total_current_value": total_current_value,
        "overall_profit_loss": overall_profit,
        "growth_percent": round(growth_percent, 2),
        "top_gainer": top_gainer,
        "top_loser": top_loser,
        "stocks": result
    })