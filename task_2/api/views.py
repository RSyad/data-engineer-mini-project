from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import PriceData
from .serializers import PriceDataSerializer

# Create your views here.
class PriceDataView(APIView):
    def get(self, request):
        query = PriceData.objects.all()

        # Get parameters
        item_category = request.query_params.get('item_category')
        year = request.query_params.get('year')
        month = request.query_params.get('month')
        day = request.query_params.get('day')

        # Apply filters if got parameters
        if item_category:
            query = query.filter(item_category=item_category)
        if year:
            query = query.filter(date__year=int(year))
        if month:
            query = query.filter(date__month=int(month))
        if day:
            query = query.filter(date__day=int(day))

        serializer = PriceDataSerializer(query, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PriceDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)