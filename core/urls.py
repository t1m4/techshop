from django.urls import path

from core import views, auth_views, api_views

urlpatterns = [
    path('', views.IndexView.as_view(), name='core-index'),
    path('login/', auth_views.LoginView.as_view(), name='core-login'),
    path('registration/', auth_views.RegisterView.as_view(), name='core-register'),
    path('logout/', auth_views.LogoutView.as_view(), name='core-logout'),
    path('support/', views.SupportView.as_view(), name='core-support'),
    path('reset/', auth_views.ResetView.as_view(), name='core-reset'),
    path('reset/success/', auth_views.ResetSuccessView.as_view(), name='core-reset_success'),
    path('reset/<uuid:user_uuid>/', auth_views.ResetConfirmView.as_view(), name='core-reset_confirm'),
    path('categories/', views.CategoriesView.as_view(), name='core-categories'),
    path('category/<int:id>/', views.CategoryView.as_view(), name='core-category'),
    path('product/<int:id>/', views.ProductView.as_view(), name='core-product'),
    path('basket/', views.BasketView.as_view(), name='core-basket'),
    path('account/', views.AccountView.as_view(), name='core-account'),
    path('account/orders/', views.OrdersView.as_view(), name='core-orders'),
    path('account/orders/<int:id>/', views.OrderView.as_view(), name='core-order'),
]

urlpatterns += [
    path('api/v1/basket/delete/<int:id>/', api_views.DeleteProductView.as_view(), name='core-delete_product'),
    path('api/v1/basket/products/', api_views.BasketProductView.as_view(), name='core-products'),
    path('api/v1/order/create/', api_views.OrderView.as_view(), name='core-orders'),
]