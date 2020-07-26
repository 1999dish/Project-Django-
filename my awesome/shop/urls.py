
from django.urls import path,include
from .import views
urlpatterns = [
    path('', views.index,name="ShopHome"),
    path('about/', views.about,name="About Us"),
    path('contact/', views.contact,name="Contact Us"),
    
    path('search/', views.search,name="Search"),
    path('shop/search/', views.search,name="Search"),
    path('about/search/', views.search,name="Search"),
    path('contact/search/', views.search,name="Search"),
    path('login/search/', views.search,name="Search"),
    path('signup/search/', views.search,name="Search"),
    path('search/search/', views.search,name="Search"),
    path('login/', views.loginhandle,name="Loginhandle"),
    path('signup/', views.signup,name="SignUp"),
    path('logout/', views.handlelogout,name="handlelogout"),
    path("products/<int:myid>", views.productView, name="ProductView"),
    path('checkout/<int:myid>', views.checkout,name="Checkout"),
    
     
]