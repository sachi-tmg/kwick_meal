from django.urls import path
from django.views.generic import TemplateView

from customer_orders.views import HomePage,Menu,LoginPage,SignupPage,AboutPage, filter_food, order,logout_view,Cart_view,Reservation,verify_payment,Blog

urlpatterns = [
    path('',LoginPage,name='login'),
    path('signup/',SignupPage,name='signup'),
    path('home',HomePage,name='home'),
    path('menu/',Menu,name='menu'), 
    path('about/',AboutPage,name='about'), 
    path('filter-food/<int:id>/',filter_food,name='filter_food'),  
    path('order/<int:id>/',order,name='order'),  
    path('logout/', logout_view, name='logout'),
    path('cart/', Cart_view, name='cart'),
    path('reservation/', Reservation, name='reservation'),
    path('blog/', Blog, name='blog'),
    path('api/verify_payment',verify_payment,name='verify_payment'),
    path('menu.html', TemplateView.as_view(template_name='about.html'), name='about_html'),
    
    
    




]