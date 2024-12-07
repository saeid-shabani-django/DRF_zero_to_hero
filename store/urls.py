from django.urls import path
from . import views
from rest_framework_nested import routers


router = routers.DefaultRouter()

router.register('products',views.ProductViewSet,basename='products')
product_router = routers.NestedDefaultRouter(router,'products',lookup='product')
product_router.register('comments',views.CommentViewSet,basename='product_comment')
router.register('categories',views.CategoryViewSet,basename='category')

router.register('carts',views.CartViewSet,basename='cart')
cart_router = routers.NestedDefaultRouter(router,'carts',lookup='cart')
cart_router.register('items',views.CartItemViewSet,basename='cartitem')


urlpatterns = [
   # path('products/',views.products_list,name='products'),
   # path('products/',views.ProductList.as_view(),name='products'),
   # path('products/<int:pk>',views.ProductDetail.as_view()),
   # path('categories/',views.CategoryList.as_view(),name='categories'),
   # path('categories/<int:pk>/',views.CategoryDetail.as_view(),name='category_detail'),
   
] + router.urls + product_router.urls + cart_router.urls
