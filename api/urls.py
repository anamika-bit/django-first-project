from django.urls import path, re_path
from api import views
from api.views import CountryView,StateView,CityView,UserView,LoginView, AllCountry
from . import views


urlpatterns = [
    path('countries/', CountryView.as_view(), name = "Country-post-views"),
    path('countries/<int:id>/', CountryView.as_view(), name = "Country-getbyid-views"),
    path('countries/', AllCountry.as_view(), name = "Country-all-views"),

    path('state_by_country/<int:id>/', StateView.as_view(), name = "state-by-country-views"),
    path('city_by_state/<int:id>/', CityView.as_view(), name = "city-by-state-views"),
    path('users/<int:id>/', UserView.as_view(), name = "get-user-by-id"),
    path('register/', UserView.as_view(), name = "register-new-user"),
    path('login/', LoginView.as_view(), name = "user-login"),

]