from rest_framework import status
from rest_framework.generics import *
from rest_framework.response import Response
from .serializers import *
from rest_framework.permissions import IsAuthenticated


class CategoryListEndPoint(ListAPIView):
    queryset = Category.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = CategorySerializer

    def listr(self, *args, **kwargs):
        q = self.get_queryset()
        ser = self.serializer_class(q, many=True, context={'request': self.request})
        if q.exists():
            return Response(ser.data, status=status.HTTP_200_OK)
        return Response({"msg": "not found"}, status=status.HTTP_404_NOT_FOUND)


class ProductListEndPoint(ListAPIView):
    queryset = Product.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductSerializer

    def list(self, *args, **kwargs):
        q = self.get_queryset()
        ser = self.serializer_class(q, many=True, context={'request': self.request})
        if q.exists():
            return Response(ser.data, status=status.HTTP_200_OK)
        return Response({"msg": "not found"}, status=status.HTTP_404_NOT_FOUND)
