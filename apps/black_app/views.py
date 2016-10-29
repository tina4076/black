from django.shortcuts import render, redirect
from .models import User, Appointment
from django.contrib import messages
from django.core.urlresolvers import reverse


# Create your views here.
def index(request):
    return redirect(reverse('users:main'))

def main(request):
    return render(request, 'black_app/main.html')

# def filter1(myWish, otherWish):
#     myItems = []
#     for w in myWish:
#         myItems.append(w.item.name)
#
#     reduced_wishList = []
#     for o in otherWish:
#         if o.name not in myItems:
#             reduced_wishList.append(o)
#     return reduced_wishList
#
#
def appointments(request):
    # myWish = WishList.objects.getWishList(request.session['user_id'])
    # otherWish = Item.objects.getOtherList(request.session['user_id'])
    # reducedWish = filter1(myWish, otherWish)
    #list1 = Appointment.objects.getAll()
    list1 = User.objects.getTodayAppointments(request.session['user_id'])
    #list2 = User.objects.getFutureAppointmennts(request.session['user_id'])
    for l in list1:
        print l.tasks, l.status, l.date, l.time

    context = {
          'appointments': list1,
    #      'otherWish': reducedWish
    }
    return render(request, 'black_app/appointments.html', context)

def register(request):
    if request.method == 'POST':
        print request.POST
        validation = User.objects.register(request.POST)
        if validation[0]:
            return log_user_in(request, validation[1])
        else:
            for error in validation[1]:
                messages.error(request, error)
            return redirect(reverse('users:main'))
    return redirect(reverse('users:main'))

def login(request):
    if request.method == 'POST':
        validation = User.objects.login(request.POST)
        if validation[0]:
            return log_user_in(request, validation[1])
        else:
            messages.error(request, validation[1])
    return redirect(reverse('users:main'))

def log_user_in(request, user):
    print("running log_user_in function")
    request.session['user_id'] = user.id
    request.session['name'] = user.name
    # add user to success flash message
    messages.success(request, "Hello, {}!".format(user.name))
    return redirect(reverse('users:appointments'))

def logout(request):
    if 'user_id' in request.session:
        request.session.modified = True
        for k in request.session.keys():
            del request.session[k]
        messages.success(request, "You have been successfully logged out")
        return redirect(reverse('users:index'))
    else:
        messages.error(request, "You were not logged in")
    return redirect(reverse('users:index'))

def edit(request, id):
    appointment = Appointment.objects.getApp(id)
    context = {"appointment": appointment}
    return render(request,'black_app/edit.html', context)


def update_app(request, id):
    return redirect(reverse('users:appointments'))


def add(request):
    if request.method == 'POST':
        print request.POST
        validation = Appointment.objects.register(request.POST)
        if validation[0]:
            user = User.objects.addAppointments(request.session['user_id'], validation[1])
            return redirect(reverse('users:appointments'))
        else:
            messages.error(request, validation[1])
            return redirect(reverse('users:appointments'))


# def add_with_name(request, name):
#     user_id = request.session["user_id"]
#     wish = WishList.objects.register(name, user_id)
#     return redirect(reverse('users:dashboard'))
#
#

def delete_app(request, id):
    Appointment.objects.delete(id)
    return redirect(reverse('users:appointments'))
#
# def remove_wish_item(request,wish_id):
#     WishList.objects.delete(wish_id)
#     return redirect(reverse('users:dashboard'))
#
#
# def wish_items(request, id):
#     wish = WishList.objects.getWishListItemID(id)
#     if wish:
#         context = {
#             'name' : wish[0].item.name,
#             'wish' : wish
#         }
#     else:
#         context ={}
#     return render(request, 'wish2_app/wish_items.html', context)
