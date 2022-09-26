from collections import Counter
from datetime import datetime

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import *


# show images of hotel rooms and direct to index.html
def index(request):
    images = []
    types = Type.objects.all()
    for type in types:
        images.append(type.images_set.first())

    rooms = zip(types, images)
    return render(request, "web/index.html", {'rooms': rooms})


# load facilities page
def facilities(request):
    return render(request, "web/facilities.html", {})


#load restuarant page
def restaurant(request):
    return render(request, "web/restaurant.html", {})


# registered users can review the hotel
@login_required
def review(request):
    # get details entered for review and save them (review is associated with each user)
    if request.method == 'POST':
        rating = request.POST['rating']
        review = request.POST['review_text']
        rev = Review(user_id=request.user.profile, rating=rating, review=review)
        rev.save()
        return redirect('index')
    else:
        return render(request, "web/review.html", {})


# logout from hotel
@login_required
def my_logout(request):
    logout(request)
    return render(request, "web/index.html", {})


# this view will only be accessed if the user is logged in
@login_required
def profile(request):
    # Get changes in profile and save them in model
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        email = request.POST['email']
        address = request.POST['address']
        new_pic = request.FILES.get('newProfilePic')

        #check for changes, only save changed data
        if first_name is not None:
            request.user.first_name = first_name
        if last_name is not None:
            request.user.last_name = last_name
        if password is not None and password != "":
            request.user.set_password(password)
        if email is not None:
            request.user.email = email
        if new_pic is not None:
            request.user.profile.profile_pic = new_pic
        if address is not None:
            request.user.profile.address = address

        request.user.save()
        return redirect('profile')
    else:
        # get the persons previous reviews and bookings to show on template (view)
        return render(request, "web/profile.html", {'reviews': request.user.profile.review_set.all()})


# Login for the user. Authenticate user and if valid, redirect it to main page
def my_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        #if valid user
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('/admin/')
            return redirect('index')
        else:
            return redirect('login')  #if invalid
    else:
        return render(request, "web/login.html")


# signup for the user
def signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        username = request.POST['username']
        profile_pic = request.FILES.get('profile_pic')
        name_arr = name.split(' ')
        firstname = name_arr[0]

        # if valid user
        if len(name_arr) > 1:
            lastname = name_arr[1]
            user = User.objects.create_user(username=username, email=email,
                                            first_name=firstname, last_name=lastname)
            # if user is created save it in database
            if user is not None:
                user.set_password(password)

                if profile_pic is not None:
                    user.profile.profile_pic = profile_pic
                user.save()
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('index')
            else:
                return redirect('signup')
        else:
            return redirect('signup')
    else:
        return render(request, "web/signup.html")


@login_required
def check(request):
    if request.method == 'POST':
        check_in_date = request.POST['check_in']
        check_in = datetime.strptime(check_in_date, "%Y-%m-%d")
        check_out_date = request.POST['check_out']
        check_out = datetime.strptime(check_out_date, "%Y-%m-%d")

        # all these rooms cannot be shown
        # those regs that start before checkin and end within
        reg_lte = list(
            Registration.objects.filter(check_in_date__lte=check_in, check_out_date__range=(check_in, check_out)))

        # those regs that start between checkin and checkout, and end after checkout
        reg_gte = list(
            Registration.objects.filter(check_in_date__range=(check_in, check_out), check_out_date__gte=check_out))

        # those regs that start and end within checkin and checkout
        reg_in = list(Registration.objects.filter(check_in_date__gte=check_in, check_out_date__lte=check_out))

        # those regs that start and end outside checkin and checkout
        reg_out = list(Registration.objects.filter(check_in_date__lte=check_in, check_out_date__gte=check_out))

        unavailable_room_bookings = list(set(reg_gte + reg_lte + reg_in + reg_out))

        # get the unavailable rooms
        unavailable_rooms = []
        for reg in unavailable_room_bookings:
            for detail in list(reg.details.all()):
                unavailable_rooms.append(detail.room_id.id)

        # get available rooms
        available_rooms = list(set(list(Room.objects.all().exclude(id__in=unavailable_rooms))))

        # get type and number of rooms associated with that type, they will be available to user
        available_types = []
        for room in available_rooms:
            available_types.append(room.room_type)

        available_types = Counter(available_types)

        # get type, room count and first image into a single zipped list and send to view
        ty = []
        count = []
        images = []
        for item in available_types:
            ty.append(item)
            count.append(available_types[item])
            images.append(item.images_set.first())

        return render(request, "web/booking.html",
                      {'available': zip(ty, count, images), 'check_in': check_in_date, 'check_out': check_out_date})

    else:
        return redirect('booking')


# book the room according to the user selections
@login_required
def booking(request):
    if request.method == 'POST':
        # get required data
        type_id = int(request.POST['type_id'])
        qty = int(request.POST['quantity'])
        check_in = datetime.strptime(request.POST['check_in'], "%Y-%m-%d")
        check_out = datetime.strptime(request.POST['check_out'], "%Y-%m-%d")

        room_type = Type.objects.get(id=type_id)
        total_cost = qty * room_type.price
        available_rooms = list(room_type.room_set.all().filter(status='a'))[:qty]

        # calculate costs and save registration information
        book = Registration(user=request.user.profile, occupants=qty * room_type.capacity, check_in_date=check_in,
                            check_out_date=check_out, payment=total_cost)
        book.save()

        for room in available_rooms:
            room.status = 'r'
            room.save()
            detail = RegistrationDetails(registration_id=book, room_id=room)
            detail.save()

        return redirect('index')
    else:
        return render(request, "web/booking.html", {})
