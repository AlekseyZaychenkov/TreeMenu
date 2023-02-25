from django.urls import path
from menu import views


urlpatterns = [
    path('', views.home, name='home'),

    path('<str:active_item_url>', views.home),

    path('<str:ancestor_url_1>/<str:active_item_url>', views.home),

    path('<str:ancestor_url_2>/<str:ancestor_url_1>/<str:active_item_url>', views.home),

    path('<str:ancestor_url_3>/<str:ancestor_url_2>/<str:ancestor_url_1>/<str:active_item_url>', views.home),

    path('<str:ancestor_url_4>/<str:ancestor_url_3>/<str:ancestor_url_2>/<str:ancestor_url_1>/'
         '<str:active_item_url>', views.home),

    path('<str:ancestor_url_5>/<str:ancestor_url_4>/<str:ancestor_url_3>/<str:ancestor_url_2>/'
         '<str:ancestor_url_1>/<str:active_item_url>', views.home),

    path('<str:ancestor_url_6>/<str:ancestor_url_5>/<str:ancestor_url_4>/<str:ancestor_url_3>/'
         '<str:ancestor_url_2>/<str:ancestor_url_1>/<str:active_item_url>', views.home),

    path('<str:ancestor_url_7>/<str:ancestor_url_6>/<str:ancestor_url_5>/<str:ancestor_url_4>/'
         '<str:ancestor_url_3>/<str:ancestor_url_2>/<str:ancestor_url_1>/<str:active_item_url>', views.home),

    path('<str:ancestor_url_8>/<str:ancestor_url_7>/<str:ancestor_url_6>/<str:ancestor_url_5>/'
         '<str:ancestor_url_4>/<str:ancestor_url_3>/<str:ancestor_url_2>/<str:ancestor_url_1>/'
         '<str:active_item_url>', views.home),

    path('<str:ancestor_url_9>/<str:ancestor_url_8>/<str:ancestor_url_7>/<str:ancestor_url_6>/'
         '<str:ancestor_url_5>/<str:ancestor_url_4>/<str:ancestor_url_3>/<str:ancestor_url_2>/'
         '<str:ancestor_url_1>/<str:active_item_url>', views.home),
]
