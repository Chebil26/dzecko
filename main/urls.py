from django.urls import path
from .views import (
    media_list, color_list, category_list, type_list,
    ambiance_list, revetement_list, furniture_type_list,
    furniture_list, option_list, question_list, order_list,
    palette_list, user_image_list
)


urlpatterns = [
    path('media/', media_list, name='media-list'),
    path('colors/', color_list, name='color-list'),
    path('categories/', category_list, name='category-list'),
    path('types/', type_list, name='type-list'),
    path('palettes/', palette_list, name='palette-list'),
    path('ambiances/', ambiance_list, name='ambiance-list'),
    path('revetements/', revetement_list, name='revetement-list'),
    path('furniture_types/', furniture_type_list, name='furniture-type-list'),
    path('furnitures/', furniture_list, name='furniture-list'),
    path('options/', option_list, name='option-list'),
    path('questions/', question_list, name='question-list'),
    path('orders/', order_list, name='order-list'),
    path('user-images/', user_image_list, name='user-image-list'),
]
