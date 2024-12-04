from django.urls import path
from . import views

urlpatterns = [
   # path('products/',views.products_list,name='products'),
   path('products/',views.ProductList.as_view(),name='products'),
   path('products/<int:pk>',views.ProductDetail.as_view()),
   path('categories/',views.CategoryList.as_view(),name='categories'),
   path('categories/<int:pk>/',views.CategoryDetail.as_view(),name='category_detail'),
   
]
