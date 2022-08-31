from rest_framework import serializers
from .models import Country,State,City,User
#from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

            
class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

#class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#    def get(cls, user):
#        print('yos')

#        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
#        print('yoss')
#        token['email'] =  user.email
#        return token
