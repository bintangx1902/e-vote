from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
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
    permission_classes = (IsAuthenticated,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def list(self, *args, **kwargs):
        query = self.get_queryset()
        ser = self.serializer_class(query, many=True, context={'request': self.request})
        if query.exists():
            for item in ser.data:
                item['category_img'] = item['category_img'].replace('https', 'http')
            return Response(ser.data, status=status.HTTP_200_OK)
        return Response({"msg": "not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def add_new_product(request):
    if request.method == 'POST':
        data = request.data
        serializer = AddProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Berhasil Tambah Produk"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response()


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def add_new_category(request):
    if request.method == 'POST':
        data = request.data
        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Berhasil Tambah Kategori"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response()
