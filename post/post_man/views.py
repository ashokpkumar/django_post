from django.shortcuts import render
from django.views import View
from .models import UserModel, OrderModel    
from django.shortcuts import render
from django.shortcuts import render
import jwt
from datetime import datetime, timedelta

# Create your views here.
class PostManView(View):
    def get(self, request):
        return render(request, 'post_man.html')
    
class AuthView(View):
    def token_required(self,view_func):
        def wrapper(request, *args, **kwargs):
            token = request.POST.get('token')
            if token:
                try:
                    payload = jwt.decode(token, 'secret_key', algorithms=['HS256'])
                    username = payload['username']
                    password = payload['password']
                    # Get the name from username and password
                    name = f"{username} {password}"
                    request.name = name
                except jwt.ExpiredSignatureError:
                    return render(request, 'token_expired.html')
                except jwt.InvalidTokenError:
                    return render(request, 'invalid_token.html')
            else:
                return render(request, 'token_required.html')
            
            return view_func(request, *args, **kwargs)
        
        return wrapper

    def generate_token(self, username, password):
        try:
            user = UserModel.objects.get(username=username)
            if user.check_password(password):
                payload = {
                    'username': username,
                    'password': password,
                    'exp': datetime.utcnow() + timedelta(days=1)  # Token expiration time
                }
                token = jwt.encode(payload, 'secret_key', algorithm='HS256')
                return token
            else:
                return None
        except UserModel.DoesNotExist:
            return None
        
    def get_items(self):
        items = OrderModel.objects.all()
        item_list = []
        for item in items:
            item_dict = {
                'order_id': item.order_id,
                'location': item.location,
                'street_address': item.street_address,
                'landmark': item.landmark,
                'priority': item.priority,
                'phone_number': item.phone_number,
                'door_number': item.door_number,
                'order_weight': item.order_weight,
                'order_status': item.order_status
            }
            item_list.append(item_dict)
        return item_list
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        token = self.generate_token(username, password)
        if token is not None:
            context = {
                'token': token,
                'items': self.get_items()
            }
            # items = self.get_items()
            return render(request, 'main_page.html', context)
        else:
            context = {
                "invalid_credentials":True
            }
            return render(request, 'invalid_credentials.html',context)

    # def get(self, request):
    #     user1 = UserModel(username='user1', password='password1', email='user1@email.com')
    #     user1.save()
    #     user2 = UserModel(username='user2', password='password2', email='user2@email.com')
    #     user2.save()
    #     return render(request, 'post_man.html')

    def get(self, request):
        context = {
                'token': request.POST.get('token'),
                'items': self.get_items()
            }
        return render(request, 'main_page.html', context)
        # items = [{
        #     'order_id':"1234",
        #     'location':"Bangalore",
        #     'street_address':"MG Road",
        #     'landmark':"Opposite to MG Mall",
        #     'priority':1,
        #     'phone_number':"9999999999",
        #     'door_number':"1",
        #     'order_weight':10,
        #     'order_status':"delivered"
        # },
        # {
        #     'order_id':"XXXX",
        #     'location':"Bangalore",
        #     'street_address':"MG Road",
        #     'landmark':"Opposite to MG Mall",
        #     'priority':1,
        #     'phone_number':"9999999999",
        #     'door_number':"1",
        #     'order_weight':10,
        #     'order_status':"delivered"
        # },
        # {
        #     'order_id':"YYYY",
        #     'location':"Bangalore",
        #     'street_address':"MG Road",
        #     'landmark':"Opposite to MG Mall",
        #     'priority':1,
        #     'phone_number':"9999999999",
        #     'door_number':"1",
        #     'order_weight':10,
        #     'order_status':"delivered"
        # },
        # {
        #     'order_id':"ZZZZ",
        #     'location':"Bangalore",
        #     'street_address':"MG Road",
        #     'landmark':"Opposite to MG Mall",
        #     'priority':1,
        #     'phone_number':"9999999999",
        #     'door_number':"1",
        #     'order_weight':10,
        #     'order_status':"delivered"
        # }
        
        # ]  # List of items to add to OrderModel
        
        # for item in items:
        #     order = OrderModel(order_id=item['order_id'], 
        #                        location=item['location'], 
        #                        street_address=item['street_address'], 
        #                        landmark=item['landmark'],
        #                        priority = item['priority'],
        #                        phone_number = item['phone_number'],
        #                        door_number = item['door_number'],
        #                        order_weight = item['order_weight'],
        #                        order_status = item['order_status']
        #                        )  
        #     order.save()
        # return render(request, 'post_man.html')
    

class Logout(View):
    def get(self, request):
        return render(request,'post_man.html')
    
class Delivery(View):
    def get(self, request):
        return render(request, 'delivery.html')