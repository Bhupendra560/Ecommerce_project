from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from .models import ProductModel
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404
from datetime import datetime

class PRODUCTMODELVIEW(APIView):
    class InputSerializer(serializers.ModelSerializer):
        name = serializers.CharField(required=True)
        brand = serializers.CharField(required=True)
        price = serializers.CharField(required=True)
        category = serializers.CharField(required=True)
        description = serializers.CharField(required=True)
        # optional field
        is_available = serializers.BooleanField(required=False)
        class Meta:
            model = ProductModel
            exclude = ["created_at", "last_updated"]

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = ProductModel
            fields = "__all__"


    def post(self, request):
        # creating new product in db with exception handling
        serializer = self.InputSerializer(data= request.data)
        if serializer.is_valid():
            validated_data = serializer.data
            try:
                new_product = ProductModel(
                    name=validated_data.get('name'),
                    brand=validated_data.get('brand'),
                    price=validated_data.get('price'),
                    category=validated_data.get('category'),
                    description=validated_data.get('description')
                )

                if 'is_available' in validated_data:
                    new_product.is_available = validated_data.get('is_available')

                new_product.save()

                return Response({'message': 'Product created successfully'}, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({'message': 'Duplicate Entry.'}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None):
        if pk is not None:
            try:
                # fetching particular product
                product = ProductModel.objects.get(id=pk)
                serializer = self.OutputSerializer(product).data
                return Response(serializer)
            except ProductModel.DoesNotExist:
                return Response({'message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                # fetching all products from db
                all_products = ProductModel.objects.all()
                if all_products:
                    serializer = self.OutputSerializer(all_products, many=True).data
                    return Response(serializer)
                else:
                    return Response({'message': 'Data not found'}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, pk):
        try:
            # checking if product exist, then update it
            existing_product = ProductModel.objects.get(id=pk)
        except ProductModel.DoesNotExist:
            return Response({'message': 'Product with id {} not found'.format(pk)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if not request.data:
            return Response({'message': 'No fields were modified'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.InputSerializer(existing_product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        existing_product.last_updated = datetime.now()
        existing_product.save()
        return Response({'message': 'Product updated successfully'}, status=status.HTTP_200_OK)


    def delete(self, request, pk):
        if pk is not None:
            try:
                # deleting particular product
                product = get_object_or_404(ProductModel, id=pk)
                product.delete()
                return Response({'message': 'Product with id {} deleted successfully'.format(pk)}, status=status.HTTP_200_OK)
            except ProductModel.DoesNotExist:
                return Response({'message': 'Product with id {} not found'.format(pk)}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'message': 'please specify product id to delete'}, status=status.HTTP_400_BAD_REQUEST)
