from django.urls import path
from .views import AccountView

 
app_name = 'account'
urlpatterns = [
    # CBV url path
    path("signup/", AccountView.as_view()),
]