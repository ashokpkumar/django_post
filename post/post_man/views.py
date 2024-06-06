from django.shortcuts import render
from django.views import View
from .models import UserModel, Order    
from django.shortcuts import render
from django.shortcuts import render
import jwt
from datetime import datetime, timedelta
import base64
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
        items = Order.objects.all()
        item_list = []
        for item in items:
            item_dict = {
                'order_id': item.order_id,
                'street_address': item.street_address,
                'city': item.city,
                'landmark': item.landmark,
                'priority': item.priority,
                'phone_number': item.phone_number,
                'order_status': item.order_status
            }
            item_list.append(item_dict)
        return item_list
    
    def get_item_details(self):
        item = Order.objects.filter(order_status='available').first()
        if item:
            item_details = {
                'order_id': item.order_id,
                'customer_name': item.customer_name,
                'door_number': item.door_number,
                'apartment_number': item.apartment_number,
                'street_address': item.street_address,
                'city': item.city,
                'state': item.state,
                'country': item.country,
                'pincode': item.pincode,
                'phone_number': item.phone_number,
                'ring_bell': item.ring_bell,
                'google_link': item.google_link,
                'landmark': item.landmark,
                'order_weight': item.order_weight,
                'item_type': item.item_type,
                'battery_included': item.battery_included,
                'expected_delivery_date': item.expected_delivery_date,
                'priority': item.priority,
                'order_status': item.order_status,

            }
            return item_details
        else:
            return None
    
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
        # items = [
        #     {
        #         'order_id': "1234511",
        #         'customer_name': "customer_1",
        #         'door_number': "123",
        #         'apartment_number': "F2",
        #         'street_address': "Nehru nagar",
        #         'city': "chennai",
        #         'state': "Tamil nadu",
        #         'country': "India",
        #         'pincode': "621232",
        #         'phone_number': "9876543210",
        #         'ring_bell': True,
        #         'google_link': "https://www.google.com/maps/dir/Chromepet+bus+stand/13.0163084,80.2006422/@12.9861492,80.1342457,14z/data=!4m9!4m8!1m5!1m1!1s0x3a525fb30e2ade37:0x37045ffcd91ec864!2m2!1d80.1400577!2d12.9515322!1m0!3e0?entry=ttu",
        #         'landmark': "chromepet",
        #         'order_weight': 300,
        #         'item_type': "mobile",
        #         'battery_included': True,
        #         'expected_delivery_date': datetime.now()+timedelta(hours=15),
        #         'priority': "one_day",
        #         'order_status': "available",

        #     },
        #      {
        #         'order_id': "2345611",
        #         'customer_name': "customer_2",
        #         'door_number': "234",
        #         'apartment_number': "F3",
        #         'street_address': "Gandhi nagar",
        #         'city': "chennai",
        #         'state': "Tamil nadu",
        #         'country': "India",
        #         'pincode': "621233",
        #         'phone_number': "9786543210",
        #         'ring_bell': True,
        #         'google_link': "https://www.google.com/maps/dir/Chromepet+bus+stand/13.0163084,80.2006422/@12.9861492,80.1342457,14z/data=!4m9!4m8!1m5!1m1!1s0x3a525fb30e2ade37:0x37045ffcd91ec864!2m2!1d80.1400577!2d12.9515322!1m0!3e0?entry=ttu",
        #         'landmark': "chromepet",
        #         'order_weight': 800,
        #         'item_type': "gift",
        #         'battery_included': False,
        #         'expected_delivery_date': datetime.now()+timedelta(days=2),
        #         'priority': "normal",
        #         'order_status': "available",

        #     },
        #     {
        #         'order_id': "3456711",
        #         'customer_name': "customer_3",
        #         'door_number': "345",
        #         'apartment_number': "F4",
        #         'street_address': "Periyar nagar",
        #         'city': "chennai",
        #         'state': "Tamil nadu",
        #         'country': "India",
        #         'pincode': "621233",
        #         'phone_number': "9785543210",
        #         'ring_bell': True,
        #         'google_link': "https://www.google.com/maps/dir/Chromepet+bus+stand/13.0163084,80.2006422/@12.9861492,80.1342457,14z/data=!4m9!4m8!1m5!1m1!1s0x3a525fb30e2ade37:0x37045ffcd91ec864!2m2!1d80.1400577!2d12.9515322!1m0!3e0?entry=ttu",
        #         'landmark': "chromepet",
        #         'order_weight': 123,
        #         'item_type': "TV",
        #         'battery_included': False,
        #         'expected_delivery_date': datetime.now()+timedelta(days=1),
        #         'priority': "one_day",
        #         'order_status': "available",

        #     },
        #     {
        #         'order_id': "4567811",
        #         'customer_name': "customer_4",
        #         'door_number': "456",
        #         'apartment_number': "F5",
        #         'street_address': "Bharathi nagar",
        #         'city': "chennai",
        #         'state': "Tamil nadu",
        #         'country': "India",
        #         'pincode': "624233",
        #         'phone_number': "9785543000",
        #         'ring_bell': True,
        #         'google_link': "https://www.google.com/maps/dir/Chromepet+bus+stand/13.0163084,80.2006422/@12.9861492,80.1342457,14z/data=!4m9!4m8!1m5!1m1!1s0x3a525fb30e2ade37:0x37045ffcd91ec864!2m2!1d80.1400577!2d12.9515322!1m0!3e0?entry=ttu",
        #         'landmark': "chromepet",
        #         'order_weight': 1200,
        #         'item_type': "Bag",
        #         'battery_included': False,
        #         'expected_delivery_date': datetime.now()+timedelta(days=1),
        #         'priority': "super_fast",
        #         'order_status': "available",

        #     },{
        #         'order_id': "5678911",
        #         'customer_name': "customer_5",
        #         'door_number': "567",
        #         'apartment_number': "F6",
        #         'street_address': "Krishnan nagar",
        #         'city': "chennai",
        #         'state': "Tamil nadu",
        #         'country': "India",
        #         'pincode': "624233",
        #         'phone_number': "9785543001",
        #         'ring_bell': True,
        #         'google_link': "https://www.google.com/maps/dir/Chromepet+bus+stand/13.0163084,80.2006422/@12.9861492,80.1342457,14z/data=!4m9!4m8!1m5!1m1!1s0x3a525fb30e2ade37:0x37045ffcd91ec864!2m2!1d80.1400577!2d12.9515322!1m0!3e0?entry=ttu",
        #         'landmark': "chromepet",
        #         'order_weight': 120,
        #         'item_type': "Pencil",
        #         'battery_included': False,
        #         'expected_delivery_date': datetime.now()+timedelta(days=3),
        #         'priority': "normal",
        #         'order_status': "available",

        #     }
       
        # ]  # List of items to add to OrderModel
        
        # for item in items:
        #     order = Order( 
        #         order_id = item['order_id'],
        #         customer_name =  item['customer_name'],
        #         door_number = item['door_number'],
        #         apartment_number = item['apartment_number'],
        #         street_address = item['street_address'],
        #         city = item['city'],
        #         state = item['state'],
        #         country = item['country'],
        #         pincode = item['pincode'],
        #         phone_number = item['phone_number'],
        #         ring_bell = item['ring_bell'],
        #         google_link = item['google_link'],
        #         landmark = item['landmark'],
        #         order_weight = item['order_weight'],
        #         item_type = item['item_type'],
        #         battery_included = item['battery_included'],
        #         expected_delivery_date = item['expected_delivery_date'],
        #         priority = item['priority'],
        #         order_status = item['order_status'],  
        #                        )  
        #     order.save()
        # return render(request, 'post_man.html')
    

class Logout(View):
    def get(self, request):
        return render(request,'post_man.html')
    
class Delivery(View):

    def get_image_b64(self,image_path):
        try:
            with open(image_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
        except:
            with open('post/post_man/maps/12345.pdf', "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
            
        return encoded_string.decode('utf-8')
    
    def get_item_details(self):
        item = Order.objects.filter(order_status='available').first()
        if item:
            item_details = {
                'order_id': item.order_id,
                'customer_name': item.customer_name,
                'door_number': item.door_number,
                'apartment_number': item.apartment_number,
                'street_address': item.street_address,
                'city': item.city,
                'state': item.state,
                'country': item.country,
                'pincode': item.pincode,
                'phone_number': item.phone_number,
                'ring_bell': item.ring_bell,
                'google_link': item.google_link,
                'landmark': item.landmark,
                'order_weight': item.order_weight,
                'item_type': item.item_type,
                'battery_included': item.battery_included,
                'expected_delivery_date': item.expected_delivery_date,
                'priority': item.priority,
                'order_status': item.order_status,

            }
            item_details['b64_link'] = self.get_image_b64(r"post/post_man/maps/"+item_details['order_id']+'.pdf')
            return item_details
        else:
            return None
        
    def get(self, request):
        context = {'item':self.get_item_details() }
        return render(request, 'delivery.html',context)
    

class Delivered(View):
    def get(self, request,order_id):
        item = Order.objects.get(order_id=order_id)
        item.order_status = 'delivered'
        item.save()
        context = {'item':Delivery().get_item_details() }
        return render(request, 'delivery.html',context)
    
class NotReachable(View):
    def get(self, request,order_id):
        item = Order.objects.get(order_id=order_id)
        item.order_status = 'customer_not_reachable'
        item.save()
        context = {'item':Delivery().get_item_details() }
        return render(request, 'delivery.html',context)
    
class Damaged(View):
    def get(self, request,order_id):
        item = Order.objects.get(order_id=order_id)
        item.order_status = 'damaged'
        item.save()
        context = {'item':Delivery().get_item_details() }
        return render(request, 'delivery.html', context)
  
    
class CsRejected(View):
    def get(self, request,order_id):
        item = Order.objects.get(order_id=order_id)
        item.order_status = 'customer_rejects'
        item.save()
        context = {'item':Delivery().get_item_details() }
        return render(request, 'delivery.html', context)
  
class AddUser(View):
    def get(self, request):
        max_user = UserModel.objects.all().count()
        user1 = UserModel(username='user'+ str(max_user), password='password'+ str(max_user), email='user'+ str(max_user)+'@email.com')
        user1.save()
        return render(request, 'post_man.html')
    
class AddOrder(View):
    def get(self, request):
        max_order = Order.objects.all().count()
        order1 = Order(order_id='order'+ str(max_order), 
                       customer_name='customer'+ str(max_order), 
                       door_number='door'+ str(max_order), 
                       apartment_number='apartment'+ str(max_order), 
                       street_address='street'+ str(max_order), 
                       city='city'+ str(max_order), 
                       state='state'+ str(max_order), 
                       country='country'+ str(max_order), 
                       pincode='pincode'+ str(max_order), 
                       phone_number='phone'+ str(max_order), 
                       ring_bell=True,
                       google_link='google'+ str(max_order), landmark='landmark'+ str(max_order), order_weight=100, item_type='item'+ str(max_order), battery_included=True, expected_delivery_date=datetime.now()+timedelta(days=1), priority='super_fast', order_status='available')
        order1.save()
        return render(request, 'post_man.html')