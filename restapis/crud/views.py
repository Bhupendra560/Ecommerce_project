import json
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from .models import ProductModel
from rest_framework.renderers import JSONRenderer
from django.db.utils import IntegrityError
from datetime import datetime

class PRODUCTMODELVIEW(APIView):
    class ProductSerializer(serializers.ModelSerializer):
        class Meta:
            model = ProductModel
            fields = "__all__"

    def post(self, request):
        serializer = self.ProductSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.data
        try:
            new_product = ProductModel(
                name = validated_data['name'],
                brand = validated_data['brand'],
                price = validated_data['price'],
                category = validated_data['category'],
            )
            # checking optional fields for data if provided by user, also save them
            if 'description' in validated_data:
                new_product.description = validated_data['description']
            if 'is_available' in validated_data:
                new_product.is_available = validated_data['is_available']

            new_product.save()
            return Response({'message': 'Product created successfully'}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({'message': 'Duplicate Entry.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, pk=None):
        if pk is not None:
            try:
                product = ProductModel.objects.get(id=pk)
                serializer = self.ProductSerializer(product).data
                return Response(serializer)
            except ProductModel.DoesNotExist:
                return Response({'message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'message': e}, status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                all_products = ProductModel.objects.all()
                if all_products:
                    serializer = self.ProductSerializer(all_products, many=True).data
                    return Response(serializer)
                else:
                    return Response({'message': 'Data not found'}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            

    def put(self, request, pk):
        try:
            existing_product = ProductModel.objects.get(id=pk)
        except ProductModel.DoesNotExist:
            return Response({'message': 'Product with id {} not found'.format(pk)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
               
        if not request.data:
            return Response({'message': 'No fields were modified'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.ProductSerializer(existing_product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        existing_product.last_updated = datetime.now()
        existing_product.save()
        return Response({'message': 'Product updated successfully'}, status=status.HTTP_200_OK)


    def delete(self, request, pk):
        try:
            del_product = ProductModel.objects.get(id=pk)
        except ProductModel.DoesNotExist:
            return Response({'message': 'Product with id {} not found'.format(pk)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
               
        del_product.delete()
        return Response({'message': 'Product with id {} deleted successfully'.format(pk)}, status=status.HTTP_200_OK)
