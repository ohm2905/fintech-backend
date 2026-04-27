from django.shortcuts import render
from .utils import get_stock_price

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Portfolio
from .serializers import PortfolioSerializer


# ➕ Add Stock
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_stock(request):
    stock_name = request.data.get('stock_name').upper()
    quantity = int(request.data.get('quantity'))
    buy_price = float(request.data.get('buy_price'))

    existing_stock = Portfolio.objects.filter(
        user=request.user,
        stock_name=stock_name
    ).first()

    if existing_stock:
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
            "avg_price": round(avg_price, 2)
        })

    serializer = PortfolioSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(user=request.user, stock_name=stock_name)
        return Response(serializer.data)

    return Response(serializer.errors, status=400)


# 📊 Portfolio Summary
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def portfolio_summary(request):
    stocks = Portfolio.objects.filter(user=request.user)

    result = []
    total_investment = 0
    total_current_value = 0

    profits = []

    for stock in stocks:
        current_price = get_stock_price(stock.stock_name)

        investment = stock.quantity * stock.buy_price
        current_value = stock.quantity * current_price
        profit_loss = current_value - investment

        total_investment += investment
        total_current_value += current_value

        profits.append({
            "stock": stock.stock_name,
            "profit": profit_loss
        })

        result.append({
            "id": stock.id,
            "stock": stock.stock_name,
            "quantity": stock.quantity,
            "buy_price": round(stock.buy_price, 2),
            "current_price": round(current_price, 2),
            "investment": round(investment, 2),
            "current_value": round(current_value, 2),
            "profit_loss": round(profit_loss, 2)
        })

    # 🔥 Top gainer / loser
    top_gainer = None
    top_loser = None

    if len(profits) >= 2:
        profits_sorted = sorted(profits, key=lambda x: x["profit"])
        top_loser = profits_sorted[0]["stock"]
        top_gainer = profits_sorted[-1]["stock"]

    elif len(profits) == 1:
        top_gainer = profits[0]["stock"]
        top_loser = None

    # 🔥 Overall calculation
    overall_profit = total_current_value - total_investment

    growth_percent = (
        (overall_profit / total_investment) * 100
        if total_investment > 0 else 0
    )

    return Response({
        "total_investment": round(total_investment, 2),
        "total_current_value": round(total_current_value, 2),
        "overall_profit_loss": round(overall_profit, 2),
        "growth_percent": round(growth_percent, 2),
        "top_gainer": top_gainer,
        "top_loser": top_loser,
        "stocks": result
    })


# ❌ Delete Stock
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_stock(request, id):
    try:
        stock = Portfolio.objects.get(id=id, user=request.user)
        stock.delete()
        return Response({"message": "Stock deleted successfully"})
    except Portfolio.DoesNotExist:
        return Response({"error": "Stock not found"}, status=404)