from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CountrySerializer, StateSerializer, CitySerializer, UserSerializer
import json
from django.http import HttpResponse, Http404
from .models import Country,State,City,User, UserManager
from django.db import IntegrityError
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from .constant import STATUS





# Create your views here.
class AllCountry(APIView):
    def get(self,request):
        try:
            country_instance = Country.objects.all()
            
            serializer = CountrySerializer(country_instance, many = True)
            
            #print('abcd',str(serializer.data))
            Dict = {
                    'status' : STATUS[0],
                    'message' : 'Following countries found',
                    'country' : serializer.data
                    }
            return HttpResponse(json.dumps(Dict), content_type = 'application/json' ,status = 200)
        
        except:
            Dict = {
                'status' : STATUS[1],
                'message' : 'No country with that id exist'
            }
            return HttpResponse(json.dumps(Dict), content_type = 'application/json' ,status = 404)


class CountryView(APIView):
    def get(self,request,id):
        try:
            country_instance = Country.objects.get(id = id)
            serializer = CountrySerializer(country_instance, many = False)
            Dict = {
                    'status' : 'success',
                    'message' : 'Following countries found',
                    'country' : serializer.data
                    }
            return HttpResponse(json.dumps(Dict), content_type = 'application/json' ,status = 200)
        
        except:
            Dict = {
                'status' : 'Fail',
                'message' : 'No country with that id exist'
            }
            return HttpResponse(json.dumps(Dict), content_type = 'application/json' ,status = 404)


    def post(self,request):
        try:
            json_data = request.read()
            data = json.loads(json_data)
            country_name = data['country_name']
            country_code = data['country_code']
            country_instance = {"country_name" : country_name, "country_code" : country_code}
            serializer = CountrySerializer(data = country_instance)
            if serializer.is_valid():
                serializer.save()
                Dict = {
                    'status' : 'success',
                    'message' : 'New Country is succesfully created',
                    'country' : serializer.data
                }
                return HttpResponse(json.dumps(Dict), content_type = 'application/json' ,status = 201)
            return HttpResponse(status = 400)
        
        except ValueError:
            Dict = {
                    'status' : 'fail',
                    'message' : 'Decoding JSON has failed'
                }
            return HttpResponse(json.dumps(Dict), content_type = 'application/json' ,status = 400)
        except KeyError:
            Dict = {
                    'status' : 'fail',
                    'message' : 'country parameters are unknown'
                }
            return HttpResponse(json.dumps(Dict), content_type = 'application/json' ,status = 406)
        except:
            Dict = {
                    'status' : 'fail',
                    'message' : 'Country creation failed'
                }
            return HttpResponse(json.dumps(Dict), content_type = 'application/json' ,status = 406)


class StateView(APIView):
    def get(self,request,id):
        try:
            country_instance = Country.objects.get(id = id)
            print(str(country_instance),'abcd')
            state_instance = State.objects.filter(country_id = id)
            if bool(state_instance):
                serializer = StateSerializer(state_instance, many = True)
                Dict = {
                    'status' : 'success',
                    'message' : 'States comes under given country id',
                    'country' : serializer.data
                }
                return HttpResponse(json.dumps(Dict), content_type = 'application/json' ,status = 200)
            Dict = {
                'status' : 'success',
                'message' : 'Country with that id not having any states'
            }
            return HttpResponse(json.dumps(Dict), content_type = 'application/json' ,status = 404)

        except:
            Dict = {
                'status' : 'Fail',
                'message' : 'No country with that id exist'
            }
            return HttpResponse(json.dumps(Dict), content_type = 'application/json' ,status = 404)


    def post(self,request,id):
        try:
            country_instance = Country.objects.get(id = id)
            json_data = request.read()
            data = json.loads(json_data)
            state_name = data['state_name']
            state_instance = {"state_name" : state_name, "country_id" : id}
            serializer = StateSerializer(data = state_instance)
            if serializer.is_valid():
                serializer.save()
                Dict = {
                    'status' : 'success',
                    'message' : 'New state is successfully created',
                    'country' : serializer.data
                }
                return HttpResponse(json.dumps(Dict), content_type = 'application/json' ,status = 201)
            return HttpResponse(status = 406)
        except ValueError:
            Dict = {
                    'status' : 'fail',
                    'message' : 'Decoding JSON has failed'
                }
            return HttpResponse(json.dumps(Dict), content_type = 'application/json' ,status = 406)
        except KeyError:
            Dict = {
                    'status' : 'fail',
                    'message' : 'state_name is unknown'
                }
            return HttpResponse(json.dumps(Dict), content_type = 'application/json' ,status = 406)
        except:
            Dict = {
                    'status' : 'fail',
                    'message' : 'No Country with that id is found'
                }
            return HttpResponse(json.dumps(Dict), content_type = 'application/json' ,status = 404)


class CityView(APIView):
    def get(self,request,id):
        try:
            state_instance = State.objects.get(id = id)
            city_instance = City.objects.filter(state_id = id)
            if bool(city_instance):
                serializer = CitySerializer(city_instance, many = True)
                Dict = {
                    'status' : 'success',
                    'message' : 'Following Cities comes under given state id',
                    'country' : serializer.data
                }
                return HttpResponse(json.dumps(Dict), content_type = 'application/json' ,status = 200)
            Dict = {
                'status' : 'success',
                'message' : 'State with that id not having any cities'
            }
            return HttpResponse(json.dumps(Dict), content_type = 'application/json' ,status = 404)
        except:
            Dict = {
                'status' : 'Fail',
                'message' : 'No State with that id exists'
            }
            return HttpResponse(json.dumps(Dict), content_type = 'application/json' ,status = 404)


    def post(self,request,id):
        try:
            state_instance = State.objects.get(id = id)
            json_data = request.read()
            data = json.loads(json_data)
            city_name = data['city_name']
            city_instance = {"city_name" : city_name, "state_id" : id}
            serializer = CitySerializer(data = city_instance)
            if serializer.is_valid():
                serializer.save()
                Dict = {
                    'status' : 'success',
                    'message' : 'New city is succesfully created',
                    'country' : serializer.data
                }
                return HttpResponse(json.dumps(Dict), content_type = 'application/json' ,status = 201)
            
            Dict = {
                'status' : 'fail',
                'message' : 'City not created'
            }
            return HttpResponse(jsoc.dumps(Dict) , content_type = 'application/json',status = 406)

        except ValueError:
            Dict = {
                    'status' : 'fail',
                    'message' : 'Decoding JSON has failed'
                }
            return HttpResponse(json.dumps(Dict), content_type = 'application/json' ,status = 406)
        except KeyError:
            Dict = {
                    'status' : 'fail',
                    'message' : 'city_name is unknown'
                }
            return HttpResponse(json.dumps(Dict), content_type = 'application/json' ,status = 406)
        except:
            Dict = {
                    'status' : 'fail',
                    'message' : 'No State with that id is found'
                }
            return HttpResponse(json.dumps(Dict),content_type = 'application/json',status = 404)


class UserView(APIView):
    
    def get(self,request,id):
        try:
            user = User.objects.get(id = id)
            serializer = UserSerializer(user, many = False)
            Data = serializer.data
            city_id = Data['city_id']
            state_id = Data['state_id']
            country_id = Data['country_id']
            city_name = City.objects.get(id = city_id).city_name
            state_name = State.objects.get(id = state_id).state_name
            country_name = Country.objects.get(id = country_id).country_name
            Doc = {
                'status' : 'success',
                'message' : 'User Found',
                'id' : Data['id'],
                'name' : Data['name'],
                'business_type' : Data['business_type'],
                'phone' : Data['phone'],
                'address' : Data['address'],
                'city_name' : city_name,
                'state_name' : state_name,
                'country_name' : country_name
            }
            return HttpResponse(json.dumps(Doc), content_type = 'application/json' ,status = 200)
            
        except:
            Dict = {
                    'status' : 'fail',
                    'message' : 'No User with that id is found'
                }
            return HttpResponse(json.dumps(Dict), content_type = 'application/json' ,status = 404)


    def post(self,request):
        try:
            json_data = request.read()
            data = json.loads(json_data)
            name = data['name']
            email = data['email']
            password = data['password']
            confirm_password = data['confirm_password']
            address = data['address']
            business_type = data['business_type']
            phone = data['phone']
            city_id = data['city_id']
            state_id = data['state_id']
            country_id = data['country_id']

           
        
            str='''
        
            pass_len = len(password)
            
            if pass_len < 8 or pass_len >16:
                Dict = {
                    'status' : 'fail',
                    'message' : 'Password must contain minimum 8 charactes or maximum 16 characters'
                }
                return HttpResponse(json.dumps(Dict), content_type = 'application/json' ,status=406)

            if bool(User.objects.filter(password = password)):
                Dict = {
                    'status' : 'fail',
                    'message' : 'This password is already in use'
                }
                return HttpResponse(json.dumps(Dict), content_type = 'application/json' ,status=406)'''

            if password != confirm_password:
                Dict = {
                    'status' : 'fail',
                    'message' : 'Password fields must be same'
                }
                return HttpResponse(json.dumps(Dict), content_type = 'application/json' ,status=406)

            
            #if not(business_type in ['Individual', 'Proprietor', 'Corporate']):
            #    Dict = {
            #        'status' : 'fail',
            #        'message' : 'Enter valid business type'
            #    }
            #    return HttpResponse(json.dumps(Dict), content_type = 'application/json' ,status=406)

            s = '''phone = data['phone']
            phone_len = len(phone)
            if phone_len != 10:
                Dict = {
                    'status' : 'fail',
                    'message' : 'phone no. must contain 10 digits'
                }
                return HttpResponse(json.dumps(Dict), content_type = 'application/json' ,status=406)

            '''

            city_instance = City.objects.get(id = city_id)
            if not city_instance:
                Dict = {
                    'status' : 'fail',
                    'message' : 'City id does not exist'
                }
                return HttpResponse(json.dumps(Dict), content_type = 'application/json' , status=404)

            state_instance = State.objects.get(id = state_id)
            if not state_instance:
                Dict = {
                    'status' : 'fail',
                    'message' : 'State id does not exist'
                }
                return HttpResponse(json.dumps(Dict), content_type = 'application/json' ,status=404)

            country_instance = Country.objects.get(id = country_id)
            if not country_instance:
                Dict = {
                    'status' : 'fail',
                    'message' : 'Country id does not exist'
                }
                return HttpResponse(json.dumps(Dict), content_type = 'application/json',status=404)

            country_code = country_instance.country_code

            user = User.objects.create_staffuser(
                name = name,
                email = email,
                password = password,
                address = address,
                business_type = business_type,
                phone = phone,
                city_id = city_instance,
                state_id = state_instance,
                country_id = country_instance,
                country_code = country_code
            )
            user.save()
            
            Doc = {
                'name' : name,
                'email' : email,
                'password' : password,
                'address' : address,
                'business_type' : business_type,
                'phone' : phone,
                'city_id' : city_id,
                'state_id' : state_id,
                'country_id' : country_id,
                'country_code' : country_code
            }
            
            
            if user:
                
                Dict = {
                    'status' : 'Success',
                    'message' : 'User is successfully registered',
                    'user' : Doc
                }
                return HttpResponse(json.dumps(Dict), content_type = 'application/json' , status=201)
            
            Dict = {
                'status' : 'fail',
                'message' : 'Please fill details properly.'
            }
            return HttpResponse(jsoc.dumps(Dict) , content_type = 'application/json',status = 406)


        except ValueError as e:
            print(e)
            Dict = {
                    'status' : 'fail',
                    'message' : 'Decoding JSON has failed'
                }
            return HttpResponse(json.dumps(Dict), content_type = 'application/json' , status = 406)

        except KeyError:
            Dict = {
                    'status' : 'fail',
                    'message' : 'provide correct parameters'
                }
            return HttpResponse(json.dumps(Dict), content_type = 'application/json' , status = 406)

        except City.DoesNotExist:
            Dict = {
                    'status' : 'fail',
                    'message' : 'City does not exist'
                }
            return HttpResponse(json.dumps(Dict),content_type = 'application/json',status = 404)

        except State.DoesNotExist:
            Dict = {
                    'status' : 'fail',
                    'message' : 'State does not exist'
                }
            return HttpResponse(json.dumps(Dict), content_type = 'application/json',status = 404)

        except Country.DoesNotExist:
            Dict = {
                    'status' : 'fail',
                    'message' : 'Country does not exist'
                }
            return HttpResponse(json.dumps(Dict), content_type = 'application/json' ,status = 404)

        except IntegrityError as e: 
            Dict = {
                    'status' : 'fail',
                    'message' : e.args[0]
            }
            return HttpResponse(json.dumps(Dict), content_type = 'application/json' , status = 400)
            
                

        except :
        
            Dict = {
                    'status' : 'fail',
                    'message' : 'User not registered. This might be due to incorrect details or user already in use'
                }
            
            return HttpResponse(json.dumps(Dict), content_type = 'application/json' , status = 404)


class LoginView(APIView):
    def post(self,request):
        try:
            email = request.data['email']
            password = request.data['password']
            user = authenticate(email = email, password=password)
            if user:
                Dict = {
                    "status" : "success",
                    "message" : "You are successfully logged in"
                }
                return HttpResponse(json.dumps(Dict), content_type = 'application/json' ,status = 200)
            else:
                Dict = {
                    "status" : "fail",
                    "message" : "Log in fail"
                }
                return HttpResponse(json.dumps(Dict), content_type = 'application/json' ,status = 200)
            
        except ValueError:
            Dict = {
                    'status' : 'fail',
                    'message' : 'Decoding JSON has failed'
                }
            return HttpResponse(json.dumps(Dict), content_type = 'application/json' ,status = 406)

        except KeyError:
            Dict = {
                    'status' : 'fail',
                    'message' : 'provide correct Authentication credentials'
                }
            return HttpResponse(json.dumps(Dict), content_type = 'application/json' ,status = 406)

        except Exception as e:
            print(str(e))
            Dict = {
                    'status' : 'fail',
                    'message' : 'You need to register first'
            }
            
            return HttpResponse(json.dumps(Dict), content_type = 'application/json' ,status = 404)
            
            
