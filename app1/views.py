# import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import render
from django.core.mail import send_mail 
import random
from app1.models import Data,Blog,Myride,Rideinfo
from . serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

#create your views here

def index(request):
    try:
        request.session['email']
        user = Data.objects.get(email = request.session['email']) 
        return render(request, 'index.html', {'user_object' : user})
    except:
        return render(request, 'page_login.html')
def page_register(request):
    try:
        if request.method == 'GET':
            return render(request,'page_register.html')
        else:
            global user_data
            user_data={
                'name' : request.POST['name'],
                'phonenumber' : request.POST['phonenumber'],
                'email' : request.POST['email'],
                'password' : request.POST['password'],
            }
            if len(request.POST['password']) > 3:
                global c_otp
                c_otp = random.randint(1000,9999)
                subject = 'REGISTATION AT RIDE_HELP'
                massage = f"your otp {c_otp}"
                from_email = settings.EMAIL_HOST_USER
                send_mail(subject, massage, from_email, [request.POST['email']])
                return render(request, 'page_otp.html',{'msg':'check your inbox'})
            else:
                return render(request, 'page_register.html', {'msg':'password length more than four'})
    except:
        return render(request, 'page_register.html', {'msg':'please connect internet'})
        
def page_otp(request):
    if request.method == 'POST':
        if c_otp == int(request.POST['otp']):
            Data.objects.create(
                name = user_data['name'],
                phonenumber = user_data['phonenumber'],
                email = user_data['email'],
                password = user_data['password'],
            )   
            return render(request,'redirect.html')
        else:
            return render(request,'page_otp.html',{'msg':'worng otp'})


def page_login(request):
    if request.method == 'GET':
        return render(request,'page_login.html')
    else:
        try:
            global user
            user_object = user = Data.objects.get(email = request.POST['email'])
            if user_object.password == request.POST['password']:
                request.session['email'] = request.POST['email']
                return render(request, 'page_profile.html',{'user_object':user_object})
            else:
                return render(request,'page_login.html'),
        except:
            return render(request,'page_login.html', {'msg':"your email does't exits'"})

def redirect(request):
    return render(request, 'redirect.html')

def page_forget(request):
    # if request.method == 'GET':
    #     return render(request, 'page_forget.html')
    # else:
    #     user_email = request.POST['email']
    #     try:
    #         user_object = Data.objects.get(email = user_email)
    #         subject = 'Account Recovery'
    #         message = f"Your password is {user_object.password}."
    #         from_email = settings.EMAIL_HOST_USER
    #         rec = [user_email]
    #         send_mail(subject, message, from_email, rec)
    #         return render(request, 'page_login.html', {'msg':'check mail box'})
    #     except:
    #         return render(request, 'page_forget.html', {'msg':'Account does not exist!!!'})
    if request.method == "GET":
        return render(request,'page_forget.html')
    else:
        u_email = request.POST['email']  
        try:
            user_object = Data.objects.get(email = u_email)
            subject = 'account recovery'
            massage = f"your password is {user_object.password} and email is {user_object.email}"
            from_email = settings.EMAIL_HOST_USER
            rec = [u_email]
            send_mail(subject, massage, from_email, rec)
            return render(request, 'page_login.html',{'msg':'check inbox'})
        except:
            return render(request, 'page_forget.html', {'msg':'email not exist'})

def page_profile(request):
    try:
        user_object = Data.objects.get(email = request.session['email'])
        if request.method == 'POST':
            user_object.name = request.POST['name']
            user_object.phonenumber = request.POST['phonenumber']
            if request.FILES:
                user_object.pic = request.FILES['pic']
            user_object.save()
            return render(request, 'edit_profile.html',{'user_object':user_object})
        else:
            user_object = Data.objects.get(email = request.session['email'])
            return render(request, 'page_profile.html',{'user_object':user_object})
    except:
        return render(request, 'page_profile.html',{'user_object':user_object})

def addblog(request):
    global user_object
    user_object = Data.objects.get(email = request.session['email'])
    # return render(request,'page_addblog.html',{'user_object':user_object})
    if request.method == 'GET':
        user_object = Data.objects.get(email = request.session['email'])
        blogs = Blog.objects.filter(user = user_object)
        # return render(request, 'my_blog.html',{'blogs': blogs, 'user_object':user})
        return render(request, 'page_addblog.html', {'blog':blogs, 'user_object':user_object})
    else:
        user_object = Data.objects.get(email = request.session['email'])
        Blog.objects.create(
            title = request.POST['title'],
            user = user_object,
            content = request.POST['content'],
            pic = request.FILES['pic']
        )
        return render(request, 'page_addblog.html', {'user_object':user_object})

def viewblog(request):
    user_object = Data.objects.get(email = request.session['email'])
    all_blogs = Blog.objects.all()
    return render(request, 'page_blogs.html', {'all_blogs': all_blogs, 'user_object': user_object})

def createride(request):
    if request.method == 'GET':
        user_object = Data.objects.get(email = request.session['email'])
        all_ride = Myride.objects.filter(user = user_object)
        return render(request, 'createride.html',{'allride':all_ride, 'user_object':user_object})
    else:
        user_object = Data.objects.get(email = request.session['email'])
        Myride.objects.create(
            pickup_point = request.POST['pickup'],
            pickout_point = request.POST['drop'],
            user = user_object,
            date = request.POST['date'],
            phone_number = request.POST['phonenumber'],
            price = request.POST['price'],
            allowed_participants = request.POST['maxnumber'],
            arrival_time = request.POST['arrivaltime'],
            drop_time = request.POST['droptime']
        )
        all_ride = Myride.objects.filter(user = user_object)
        return render(request, 'createride.html',{'allride':all_ride, 'user_object':user_object})

def findride(request):
    if request.method == 'POST':
        st = request.POST['find']
        if st!=None:
            all_ride = Myride.objects.filter(pickup_point = st)
            user_object = Data.objects.get(email = request.session['email'])
            return render(request, 'allride.html', {'allrides': all_ride, 'user_object': user_object})
    else:
        user_object = Data.objects.get(email = request.session['email'])
        all_ride = Myride.objects.all()
        return render(request, 'allride.html', {'allrides': all_ride, 'user_object': user_object})

def bookride(request,pk):
    if request.method == 'GET':
        user_object = Data.objects.get(email = request.session['email'])
        all_ride = Myride.objects.get(id = pk)
        return render(request, 'bookride.html',{'allride': all_ride,'user_object':user_object, 'ride_id': pk})
    else:
        user_object = Data.objects.get(email = request.session['email'])
        all_ride = Myride.objects.get(id = pk)
        Rideinfo.objects.create(
            pickup_point = request.POST['arrivalR'],
            pickout_point = request.POST['dropR'],
            arrival_time = request.POST['arrivaltimeR'],
            drop_time = request.POST['droptimeR'],
            date = request.POST['dateR'],
            allowed_participants = request.POST['spaceleftR'],
            price = request.POST['priceR'],
            ride_id = request.POST['rideidR'],
            name = request.POST['nameR'],
            phone_number = request.POST['phonenumberR'],
    
            user = user_object,
            myride = all_ride,
        )
        user_objectt = Myride.objects.get(id = pk)
        a=int(request.POST['spaceleftR'])
        b=a - 1
        # int(b)
        if request.method == 'POST':
            user_objectt.allowed_participants  = b
            user_objectt.save()
        my_ride = Rideinfo.objects.filter(user = user_object)
        return render(request, 'myride.html',{'myrides':my_ride, 'user_object':user_object})

        # return render(request, 'myride.html', {'user_object':user_object, 'allride': all_ride, 'ride_id': pk, 'msg':'book done!!! check ride in [My Ride] option'})

def myride(request):
    # if request.method == 'POST':
    # user_objectts = Rideinfo.objects.get(id = pk)
    # del user_objectts 
    user_object = Data.objects.get(email = request.session['email'])
    my_ride = Rideinfo.objects.filter(user = user_object)
    return render(request, 'myride.html',{'myrides':my_ride, 'user_object':user_object})

def information(request,pk):
    user_object = Data.objects.get(email = request.session['email'])
    all_ride = Rideinfo.objects.filter(ride_id = pk)
    return render(request,'information.html', {'user_object': user_object, 'allrides': all_ride})

def delete(request,pk,ride_id):
    # user = Rideinfo.objects.get(id = pk)
    # ride_id = user.ride_id
    user_add = Myride.objects.get(id = ride_id)
    a=user_add.allowed_participants
    b=a + 1
    # int(b)
    if b >= 0:
        user_add.allowed_participants  = b
        user_add.save()

    user_objectts = Rideinfo.objects.get(id = pk)
    user_objectts.delete()

    user_object = Data.objects.get(email = request.session['email'])
    my_ride = Rideinfo.objects.filter(user = user_object)
    return render(request, 'myride.html',{'myrides':my_ride, 'user_object':user_object})

def reride(request,pk):
    user_objectts = Myride.objects.get(id = pk)
    user_objectts.delete()
        
    user_object = Data.objects.get(email = request.session['email'])
    all_ride = Myride.objects.filter(user = user_object)
    return render(request, 'createride.html',{'allride':all_ride, 'user_object':user_object})

def fire(request,pk,ride_id):
    # user = Rideinfo.objects.get(id = pk)
    # ride_id = user.ride_id
    user_add = Myride.objects.get(id = ride_id)
    a=user_add.allowed_participants
    b=a + 1
    # int(b)
    if b >= 0:
        user_add.allowed_participants  = b
        user_add.save()

    user_objectts = Rideinfo.objects.get(id = pk)
    user_objectts.delete()
    
    # user_object = Data.objects.get(email = request.session['email'])
    # all_ride = Myride.objects.filter(user = user_object)
    # return render(request, 'createride.html',{'allride':all_ride, 'user_object':user_object})

    user_object = Data.objects.get(email = request.session['email'])
    all_ride = Rideinfo.objects.filter(user = user_object)
    return render(request, 'information.html',{'allrides': all_ride, 'user_object':user_object})


class UserList(APIView):
    def get(self,request):
        all_data = Data.objects.all()
        ser_object = UserSerializer(all_data, many=True)
        return Response(ser_object.data)

class UserCreate(APIView):
    def post(self, request):
        p_data = request.data
        ser_object = UserSerializer(data = p_data)
        if ser_object.is_valid():
            ser_object.save()
            all_data = Data.objects.all()
            ser_object = UserSerializer(all_data, many=True)
            return Response(ser_object.data)
        else:
            return Response(ser_object.errors)
            
class UserPut(APIView):
    def put(self, request, pk):
        row_obj = Data.objects.get(id = pk)
        ser_object = UserSerializer(row_obj, data= request.data)
        if ser_object.is_valid():
            ser_object.save()
            all_data = Data.objects.all()
            ser_object = UserSerializer(all_data, many=True)
            return Response(ser_object.data)
        else:
            return Response(ser_object.errors)

        
class UserDelete(APIView):
    def delete(self,request, pk):
        row_obj = Data.objects.get(id = pk)
        row_obj.delete()
        all_data = Data.objects.all()
        ser_object = UserSerializer(all_data, many = True)
        return Response(ser_object.data)


# def remove(request,ride_id):
#     # user = Rideinfo.objects.get(id = ride_id)
#     user_add = Myride.objects.get(id = ride_id)
#     a=user_add.allowed_participants
#     b=a + 1
#     int(b)
#     if b >= 0:
#         user_add.allowed_participants  = b
#         user_add.save()

#     user_object = Data.objects.get(email = request.session['email'])
#     my_ride = Rideinfo.objects.filter(ride_id = ride_id)
    # return render(request, 'remove.html',{'myrides':my_ride, 'user_object':user_object})


# def donate(request,pk):
#     #payment
#     #donation table row create
#     myride_object = Myride.objects.get(id = pk)
#     currency = 'INR'
#     amount = 500*100  # Rs. 200
#     amount = amount * 100
#     # Create a Razorpay Order

#     razorpay_order = razorpay_client.order.create(dict(amount=amount, currency=currency, payment_capture='0'))
 
#     # order id of newly created order.
#     razorpay_order_id = razorpay_order['id']
#     callback_url = 'paymenthandler/'
 
#     # we need to pass these details to frontend.
#     global context
#     context = {}
#     context['razorpay_order_id'] = razorpay_order_id
#     context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
#     context['razorpay_amount'] = amount
#     context['currency'] = currency
#     context['callback_url'] = callback_url
#     context['myride_object'] = myride_object
#     # return render(request, 'bookride.html', context = context)


 
 
# # authorize razorpay client with API Keys.
# razorpay_client = razorpay.Client(
#     auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


 

 
 
# # we need to csrf_exempt this url as
# # POST request will be made by Razorpay
# # and it won't have the csrf token.
# @csrf_exempt
# def paymenthandler(request):
 
#     # only accept POST request.
#     if request.method == "POST":
#         try:
           
#             # get the required parameters from post request.
#             payment_id = request.POST.get('razorpay_payment_id', '')
#             razorpay_order_id = request.POST.get('razorpay_order_id', '')
#             signature = request.POST.get('razorpay_signature', '')
#             params_dict = {
#                 'razorpay_order_id': razorpay_order_id,
#                 'razorpay_payment_id': payment_id,
#                 'razorpay_signature': signature
#             }
 
#             # verify the payment signature.
#             # result = razorpay_client.utility.verify_payment_signature(
#             #     params_dict)
#             # if result is not None:
#             amount = context['razorpay_amount']  # Rs. 200
#             try:

#                 # capture the payemt
#                 razorpay_client.payment.capture(payment_id, amount)

#                 # render success page on successful caputre of payment
#                 return render(request, 'paymentsucsess.html')
#             except:

#                 # if there is an error while capturing payment.
#                 return render(request, 'paymentfail.html')
            
#         except:
 
#             # if we don't find the required parameters in POST data
#             return HttpResponseBadRequest()
#     else:
#        # if other than POST request is made.
#         return HttpResponseBadRequest()

