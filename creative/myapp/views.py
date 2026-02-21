from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.db.models import Q
import datetime

# --- AUTHENTICATION ---

def index(request):
    return render(request, 'index.html')

def login_view(request):
    msg = ""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.user_type == 'admin':
                login(request, user)
                return redirect('/admin_home/')
                
            elif user.user_type == 'seller':
                try:
                    seller = Seller.objects.get(login=user)
                    if seller.status == 'approve':
                        login(request, user)
                        request.session['sid'] = seller.id
                        return redirect('/seller_home/')
                    elif seller.status == 'reject':
                        msg = "Your account is rejected"
                    elif seller.status == 'block':
                        msg = "Your account is blocked"
                    else:
                        msg = "Wait for approval"
                except Seller.DoesNotExist:
                    msg = "Seller profile not found"
            
            elif user.user_type == 'user':
                try:
                    u_obj = User.objects.get(login=user)
                    login(request, user)
                    request.session['uid'] = u_obj.id
                    return redirect('/user_home/')
                except User.DoesNotExist:
                    msg = "User profile not found"

        else:
            msg = "Invalid Credentials"
    return render(request, 'login.html', {'msg': msg})

def user_reg(request):
    msg = ""
    if request.method == 'POST':
        name = request.POST.get('name')
        place = request.POST.get('place')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        u = request.POST.get('username')
        p = request.POST.get('password')
        if Login.objects.filter(username=u).exists():
            msg = "Username already exists"
        else:
            user = Login.objects.create_user(username=u, password=p, user_type='user', view_password=p)
            User.objects.create(login=user, name=name, place=place, phone=phone, email=email)
            return redirect('/login/')
    return render(request, 'user_reg.html', {'msg': msg})

def seller_reg(request):
    msg = ""
    if request.method == 'POST':
        name = request.POST.get('name')
        place = request.POST.get('place')
        contact = request.POST.get('contact')
        email = request.POST.get('email')
        u = request.POST.get('username')
        p = request.POST.get('password')
        image = request.FILES.get('image')
        if Login.objects.filter(username=u).exists():
            msg = "Username already exists"
        else:
            user = Login.objects.create_user(username=u, password=p, user_type='seller', view_password=p)
            Seller.objects.create(login=user, name=name, place=place, contact_number=contact, email=email, image=image)
            return redirect('/login/')
    return render(request, 'seller_reg.html', {'msg': msg})

def logout_view(request):
    logout(request)
    return redirect('/login/')

# --- ADMIN VIEWS ---

def admin_home(request):
    if request.user.is_authenticated and request.user.user_type == 'admin':
        return render(request, 'admin/home.html')
    return redirect('/login/')

def manage_sellers(request):
    if request.user.is_authenticated and request.user.user_type == 'admin':
        action = request.GET.get('action')
        id = request.GET.get('id')
        if action and id:
            try:
                sl = Seller.objects.get(id=id)
                if action == 'approve':
                    sl.status = 'approve'
                elif action == 'reject':
                    sl.status = 'reject'
                elif action == 'block':
                    sl.status = 'block'
                elif action == 'unblock':
                    sl.status = 'approve'
                sl.save()
                return redirect('/manage_sellers/')
            except:
                pass
        
        sellers = Seller.objects.all()
        return render(request, 'admin/manage_sellers.html', {'sellers': sellers})
    return redirect('/login/')

def admin_view_users(request):
    if request.user.is_authenticated and request.user.user_type == 'admin':
        users = User.objects.all()
        return render(request, 'admin/view_users.html', {'users': users})
    return redirect('/login/')

def admin_view_payments(request):
    if request.user.is_authenticated and request.user.user_type == 'admin':
        payments = Payment.objects.all().order_by('-date')
        return render(request, 'admin/view_payments.html', {'payments': payments})
    return redirect('/login/')

# --- SELLER VIEWS ---

def seller_home(request):
    if 'sid' in request.session:
        return render(request, 'seller/home.html')
    return redirect('/login/')

def add_design(request):
    msg = ""
    if 'sid' in request.session:
        if request.method == 'POST':
            title = request.POST.get('title')
            description = request.POST.get('description')
            price = request.POST.get('price')
            image = request.FILES.get('image')
            seller = Seller.objects.get(id=request.session['sid'])
            Design.objects.create(seller=seller, title=title, description=description, price=price, image=image)
            return redirect('/manage_design/')
        return render(request, 'seller/add_design.html', {'msg': msg})
    return redirect('/login/')

def manage_design(request):
    if 'sid' in request.session:
        seller = Seller.objects.get(id=request.session['sid'])
        designs = Design.objects.filter(seller=seller)
        return render(request, 'seller/manage_design.html', {'designs': designs})
    return redirect('/login/')

def edit_design(request):
    msg = ""
    if 'sid' in request.session:
        id = request.GET.get('id')
        design = Design.objects.get(id=id)
        if request.method == 'POST':
            design.title = request.POST.get('title')
            design.description = request.POST.get('description')
            design.price = request.POST.get('price')
            if request.FILES.get('image'):
                design.image = request.FILES.get('image')
            design.save()
            return redirect('/manage_design/')
        return render(request, 'seller/edit_design.html', {'design': design, 'msg': msg})
    return redirect('/login/')

def delete_design(request):
    if 'sid' in request.session:
        id = request.GET.get('id')
        Design.objects.filter(id=id).delete()
        return redirect('/manage_design/')
    return redirect('/login/')

def seller_view_bookings(request):
    if 'sid' in request.session:
        seller = Seller.objects.get(id=request.session['sid'])
        bookings = Booking.objects.filter(design__seller=seller).order_by('-date')
        return render(request, 'seller/view_bookings.html', {'bookings': bookings})
    return redirect('/login/')

def manage_booking_status(request):
    if 'sid' in request.session:
        id = request.GET.get('id')
        action = request.GET.get('action')
        try:
            booking = Booking.objects.get(id=id)
            if action == 'approve':
                booking.status = 'approved'
            elif action == 'reject':
                booking.status = 'rejected'
            elif action == 'ship':
                booking.status = 'shipped'
            elif action == 'deliver':
                booking.status = 'delivered'
            booking.save()
        except:
            pass
        return redirect('/seller_view_bookings/')
    return redirect('/login/')

# --- USER VIEWS ---

def user_home(request):
    if 'uid' in request.session:
        return render(request, 'user/home.html')
    return redirect('/login/')

def browse_designs(request):
    if 'uid' in request.session:
        search = request.GET.get('search')
        if search:
            designs = Design.objects.filter(
                Q(title__icontains=search) | 
                Q(seller__name__icontains=search)
            )
        else:
            designs = Design.objects.all()
        return render(request, 'user/browse_designs.html', {'designs': designs})
    return redirect('/login/')

def design_details(request):
    if 'uid' in request.session:
        id = request.GET.get('id')
        design = Design.objects.get(id=id)
        if request.method == 'POST':
            text = request.POST.get('text')
            color = request.POST.get('color')
            image = request.FILES.get('image')
            user = User.objects.get(id=request.session['uid'])
            
            booking = Booking.objects.create(
                user=user, 
                design=design, 
                custom_text=text, 
                custom_color=color, 
                custom_image=image
            )
            return redirect('/my_orders/')
            
        return render(request, 'user/design_details.html', {'design': design})
    return redirect('/login/')

def my_orders(request):
    if 'uid' in request.session:
        user = User.objects.get(id=request.session['uid'])
        bookings = Booking.objects.filter(user=user).order_by('-date')
        return render(request, 'user/my_orders.html', {'bookings': bookings})
    return redirect('/login/')

def user_make_payment(request):
    if 'uid' in request.session:
        id = request.GET.get('id')
        booking = Booking.objects.get(id=id)
        if request.method == 'POST':
            booking.payment_status = 'paid'
            booking.save()
            Payment.objects.create(booking=booking, user=booking.user, amount=booking.design.price)
            return redirect('/my_orders/')
        return render(request, 'user/payment.html', {'booking': booking})
    return redirect('/login/')
