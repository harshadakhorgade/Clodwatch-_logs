# from django.urls import path
# from .views import test_logging_view

# urlpatterns = [
#     path('test-log/', test_logging_view),
# ]


from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('submit-form/', views.submit_form, name='submit_form'),
    path('crash/', views.crash, name='crash'),
]
