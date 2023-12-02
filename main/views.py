from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Media, Color, Category, Type, Ambiance, Revetement, FurnitureType, Furniture, Option, Question, Order, Palette, UserImage
from .serializers import MediaSerializer, ColorSerializer, CategorySerializer, TypeSerializer, AmbianceSerializer, RevetementSerializer, FurnitureTypeSerializer, FurnitureSerializer, OptionSerializer, QuestionSerializer, OrderSerializer, PaletteSerializer, UserImageSerializer

@api_view(['GET'])
def media_list(request):
    media = Media.objects.all()
    serializer = MediaSerializer(media, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def color_list(request):
    colors = Color.objects.all()
    serializer = ColorSerializer(colors, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def category_list(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def type_list(request):
    types = Type.objects.all()
    serializer = TypeSerializer(types, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def palette_list(request):
    types = Palette.objects.all()
    serializer = PaletteSerializer(types, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def ambiance_list(request):
    ambiances = Ambiance.objects.all()
    serializer = AmbianceSerializer(ambiances, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def revetement_list(request):
    revetements = Revetement.objects.all()
    serializer = RevetementSerializer(revetements, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def furniture_type_list(request):
    furniture_types = FurnitureType.objects.all()
    serializer = FurnitureTypeSerializer(furniture_types, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def furniture_list(request):
    furnitures = Furniture.objects.all()
    serializer = FurnitureSerializer(furnitures, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def option_list(request):
    options = Option.objects.all()
    serializer = OptionSerializer(options, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def question_list(request):
    questions = Question.objects.all()
    serializer = QuestionSerializer(questions, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
def order_list(request):
    if request.method == 'GET':
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def user_image_list(request):
    if request.method == 'GET':
        user_images = UserImage.objects.all()
        serializer = UserImageSerializer(user_images, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UserImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
