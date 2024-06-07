from django.shortcuts import render
from django.views import View
from .models import UserModel, Order
import jwt
from datetime import datetime, timedelta
import base64
from django.apps import AppConfig

class PostManView(View):
    def get(self, request):
        return render(request, 'post_man.html')


class AuthView(View):
    def token_required(self, view_func):
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
            return render(request, 'main_page.html', context)
        else:
            context = {
                "invalid_credentials": True
            }
            return render(request, 'invalid_credentials.html', context)

    def get(self, request):
        context = {
            'token': request.POST.get('token'),
            'items': self.get_items()
        }
        return render(request, 'main_page.html', context)


class Logout(View):
    def get(self, request):
        return render(request, 'post_man.html')


class Delivery(View):
    def get_item_details(self, start_place=None):
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
            item_details['b64_link'] = "https://maps.googleapis.com/maps/api/js?key=APIKEY&callback=initMap"
            if start_place is None:
                item_details["start_place"] = '2nd cross street velacherry, chennai, tamilnadu, india'
                item_details["end_place"] = f'{item.street_address},{item.landmark}, {item.city}, {item.state}, {item.country}'
            else:
                item_details["start_place"] = start_place
                item_details["end_place"] = f'{item.street_address},{item.landmark}, {item.city}, {item.state}, {item.country}'

            return item_details
        else:
            return None

    def get(self, request):
        item_details = self.get_item_details()
        if item_details is not None:
            context = {'item': item_details}
            return render(request, 'delivery copy.html', context)
        else:
            context = {
                'token': request.POST.get('token'),
                'items': AuthView().get_items()
            }
            return render(request, 'main_page.html', context)


class Delivered(View):
    def get(self, request, order_id):
        try:
            item = Order.objects.get(order_id=order_id)
            item.order_status = 'delivered'
            item.save()
            item_details = Delivery().get_item_details(f'{item.street_address}, {item.city}, {item.state}, {item.country}')
            if item_details is not None:
                context = {'item': item_details}
                return render(request, 'delivery copy.html', context)
            else:
                context = {
                    'token': request.POST.get('token'),
                    'items': AuthView().get_items()
                }
                return render(request, 'main_page.html', context)
        except:
            context = {
                'token': request.POST.get('token'),
                'items': AuthView().get_items()
            }
            return render(request, 'main_page.html', context)
        finally:
            item.save()


class NotReachable(View):
    def get(self, request, order_id):
        try:
            item = Order.objects.get(order_id=order_id)
            item.order_status = 'customer_not_reachable'
            item.save()
            item_details = Delivery().get_item_details(f'{item.street_address}, {item.city}, {item.state}, {item.country}')
            if item_details is not None:
                context = {'item': item_details}
                return render(request, 'delivery copy.html', context)
            else:
                context = {
                    'token': request.POST.get('token'),
                    'items': AuthView().get_items()
                }
                return render(request, 'main_page.html', context)
        except:
            context = {
                'token': request.POST.get('token'),
                'items': AuthView().get_items()
            }
            return render(request, 'main_page.html', context)
        finally:
            item.save()


class Damaged(View):
    def get(self, request, order_id):
        try:
            item = Order.objects.get(order_id=order_id)
            item.order_status = 'damaged'
            item.save()
            item_details = Delivery().get_item_details(f'{item.street_address}, {item.city}, {item.state}, {item.country}')
            if item_details is not None:
                context = {'item': item_details}
                return render(request, 'delivery copy.html', context)
            else:
                context = {
                    'token': request.POST.get('token'),
                    'items': AuthView().get_items()
                }
                return render(request, 'main_page.html', context)
        except:
            context = {
                'token': request.POST.get('token'),
                'items': AuthView().get_items()
            }
            return render(request, 'main_page.html', context)
        finally:
            item.save()


class CsRejected(View):
    def get(self, request, order_id):
        try:
            item = Order.objects.get(order_id=order_id)
            item.order_status = 'customer_rejects'
            item.save()
            item_details = Delivery().get_item_details(f'{item.street_address}, {item.city}, {item.state}, {item.country}')
            if item_details is not None:
                context = {'item': item_details}
                return render(request, 'delivery copy.html', context)
            else:
                context = {
                    'token': request.POST.get('token'),
                    'items': AuthView().get_items()
                }
                return render(request, 'main_page.html', context)
        except:
            context = {
                'token': request.POST.get('token'),
                'items': AuthView().get_items()
            }
            return render(request, 'main_page.html', context)
        finally:
            item.save()


class ResetOrder(View):
    def get(self, request):
        items = Order.objects.all()
        for item in items:
            item.order_status = 'available'
            item.save()
        return render(request, 'post_man.html')


class AddUser(View):
    def get(self, request):
        max_user = UserModel.objects.all().count()
        user1 = UserModel(username='user' + str(max_user), password='password' + str(max_user),
                          email='user' + str(max_user) + '@email.com')
        user1.save()
        return render(request, 'post_man.html')


class AddOrder(View):
    def get(self, request, street, landmark, city, state, country):
        max_order = Order.objects.all().count()
        order1 = Order(order_id='order' + str(max_order),
                       customer_name='customer' + str(max_order),
                       door_number='door' + str(max_order),
                       apartment_number='apartment' + str(max_order),
                       street_address=street,
                       city=city,
                       state=state,
                       country=country,
                       pincode='pincode' + str(max_order),
                       phone_number='phone' + str(max_order),
                       ring_bell=True,
                       google_link='google' + str(max_order),
                       landmark=landmark,
                       order_weight=100,
                       item_type='item' + str(max_order),
                       battery_included=True,
                       expected_delivery_date=datetime.now() + timedelta(days=1),
                       priority='super_fast',
                       order_status='available')
        order1.save()
        return render(request, 'post_man.html')


class DeleteOrder(View):
    def get(self, request):
        items = Order.objects.filter(landmark="landmark7")
        for item in items:
            item.delete()
        return render(request, 'post_man.html')
