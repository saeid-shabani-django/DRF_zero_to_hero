from django.urls import path
from . import views

urlpatterns = [
   path('products/',views.products_list,name='products'),
   path('products/<int:pk>',views.product_detail),
   path('categories/',views.category_list,name='categories'),
   path('categories/<int:pk>/',views.category_detail,name='category_detail'),
   
]
