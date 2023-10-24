import json
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from .models import ProductModel
from rest_framework.renderers import JSONRenderer
from django.db.utils import IntegrityError

class PRODUCTMODELVIEW(APIView):
    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(required=True)
        brand = serializers.CharField(required=True)
        price = serializers.CharField(required=True)
        category = serializers.CharField(required=True)
        # optional fields for user
        description = serializers.CharField(required=False)
        is_available = serializers.CharField(required=False)

    def post(self, request):

        serializer = self.InputSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        if validated_data is not None:
            try:
                new_product = ProductModel(
                    name = validated_data['name'],
                    brand = validated_data['brand'],
                    price = validated_data['price'],
                    category = validated_data['category'],
                )
                # checking optional fields for data if provided by user save them
                if 'description' in validated_data:
                    new_product.description = validated_data['description']
                if 'is_available' in validated_data:
                    new_product.is_available = validated_data['is_available']

                new_product.save()
                return Response({'message': 'Product created successfully'}, status=status.HTTP_201_CREATED)
            
            except IntegrityError:
                return Response({'message': 'Database Integrity error.'}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'message': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'message': 'Validated data is None'}, status=status.HTTP_400_BAD_REQUEST)




