from rest_framework import serializers
from .models import Media, Color, Category, Type, Ambiance, Revetement, FurnitureType, Furniture, Option, Question, Order, Palette, UserImage

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = '__all__'

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'
        
class PaletteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Palette
        fields = '__all__'

class AmbianceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ambiance
        fields = '__all__'

class RevetementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Revetement
        fields = '__all__'

class FurnitureTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FurnitureType
        fields = '__all__'

class FurnitureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Furniture
        fields = '__all__'

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class UserImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserImage
        fields = '__all__'