from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum

from .models import Transaction
from .serializers import TransactionSerializer


# ➕ Add transaction
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_transaction(request):
    serializer = TransactionSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data)

    return Response(serializer.errors, status=400)


# 📄 Get transactions (with filters + pagination)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_transactions(request):
    transactions = Transaction.objects.filter(user=request.user)

    # 🔹 Filter by type
    type_param = request.GET.get('type')
    if type_param:
        transactions = transactions.filter(type=type_param)

    # 🔹 Filter by category
    category = request.GET.get('category')
    if category:
        transactions = transactions.filter(category_id=category)

    # 🔹 Filter by date range
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        transactions = transactions.filter(date__range=[start_date, end_date])

    # 🔹 Sorting
    sort_by = request.GET.get('sort_by', 'date')   # default = date
    order = request.GET.get('order', 'desc')       # asc / desc

    if order == 'desc':
        sort_by = f'-{sort_by}'

    transactions = transactions.order_by(sort_by)

    # 🔹 Pagination (safe handling)
    try:
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 5))
    except ValueError:
        return Response({"error": "page and limit must be integers"}, status=400)

    if page < 1 or limit < 1:
        return Response({"error": "page and limit must be > 0"}, status=400)

    start = (page - 1) * limit
    end = start + limit

    total = transactions.count()
    transactions = transactions[start:end]

    serializer = TransactionSerializer(transactions, many=True)

    return Response({
        "total": total,
        "page": page,
        "limit": limit,
        "data": serializer.data
    })

# 📊 Monthly summary
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def monthly_summary(request):
    month_param = request.GET.get('month')  # format: YYYY-MM

    if not month_param:
        return Response({"error": "Month is required"}, status=400)

    year, month = map(int, month_param.split('-'))

    transactions = Transaction.objects.filter(
        user=request.user,
        date__year=year,
        date__month=month
    )

    total_income = transactions.filter(type='income').aggregate(
        Sum('amount')
    )['amount__sum'] or 0

    total_expense = transactions.filter(type='expense').aggregate(
        Sum('amount')
    )['amount__sum'] or 0

    return Response({
        "total_income": total_income,
        "total_expense": total_expense
    })


# 📊 Category-wise breakdown
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def category_breakdown(request):
    transactions = Transaction.objects.filter(
        user=request.user,
        type='expense'
    )

    data = transactions.values('category__name').annotate(
        total=Sum('amount')
    )

    result = [
        {
            "category": item["category__name"],
            "total": item["total"]
        }
        for item in data
    ]

    return Response(result)