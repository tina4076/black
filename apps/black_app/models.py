from __future__ import unicode_literals
from django.db import models
from django.db.models import Q
import bcrypt
import re
import datetime
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
name_regex = re.compile(r'^[a-zA-Z]+$')


class AppointmentManager(models.Manager):
    def getAll(self):
        return Appointment.objects.all()

    def register(self, form_data):
        # Validation portion. Pushes all errors to an array that is returned if there are errors
        errors = []
        dateString = form_data['date']

        tokens = dateString.split('-')
        if len(tokens) != 3:
            errors.append("Invalid Date. format is yyyy-mm-dd.")
        else:
            try:
                n_tokens = [int(t) for t in tokens]
                new_date = datetime.date(n_tokens[0], n_tokens[1], n_tokens[2])
            except:
                errors.append("Invalid Date. yyyy, mm, dd should be integer.")
                return (False, errors)

            if new_date < datetime.date.today():
                errors.append("Invalid Date. The date has to be after today.")

        if not len(form_data['tasks'])>=1:
            errors.append("tasks must be 1 or more characters.")
        if len(errors) is not 0:
            return (False, errors)
        else:
            print("passed validations")
            # create the hashed password using bcrypt. Remember to encode
            appointment = Appointment.objects.create(tasks=form_data['tasks'], status = "Pending", date = new_date,  time=form_data['time'])
            return (True, appointment)
#
    def getApp(self, id):
        apps = Appointment.objects.filter(id = id)
        return apps[0]

#     def getOtherWishList(self, id):
#         user = User.objects.getUser(id)
#         wish = WishList.objects.filter(~Q(user = user))
#         return wish
#
#     def getWishListItemID(self, item_id):
#         item = Item.objects.getItem(item_id)
#         wish = WishList.objects.filter(item = item)
#         return wish
#
    def delete(self, id):
        Appointment.objects.filter(id = id).delete()
        print "Appointment %s deleted" %(id)

class Appointment(models.Model):
     tasks = models.CharField(max_length=255)
     status = models.CharField(max_length=20)
     date = models.DateField(auto_now=False)
     time = models.TimeField(auto_now=False)
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)
     objects = AppointmentManager()



class UserManager(models.Manager):

    def getUser(self, id):
        users = User.objects.filter(id = id)
        return users[0]

    def getAppointments(self, id):
        users = User.objects.filter(id = id)
        user = users[0]
        app =  user.appointments.all()
        print app
        return app

    def getTodayAppointments(self, id):
        users = User.objects.filter(id = id)
        user = users[0]
        app =  user.appointments.filter(date = datetime.date.today())
        print app
        return app

    def getFutureAppointmennts(self, id):
        users = User.objects.filter(id = id)
        user = users[0]
        app =  user.appointments.filter(date > datetime.date.today())
        print app
        return app


    def addAppointments(self, id, appointment):
        users = User.objects.filter(id = id)
        user = users[0]
        user.appointments.add(appointment)

    def login(self, form_data):
        print("Validating login")
        user = User.objects.filter(email=form_data['email'])
        if user:
            print('Email found in database')
            user = user[0]
            if bcrypt.checkpw(form_data['pw'].encode(), user.pw_hash.encode()):
                print("passwords match")
                # returning user object to views
                return (True, user)
        return (False, "Invalid email or password")

    def register(self, form_data):
        # Validation portion. Pushes all errors to an array that is returned if there are errors
        errors = []
        if not name_regex.match(form_data['name']):
            errors.append("Invalid name")
        if not email_regex.match(form_data['email']):
            errors.append("Invalid email")
        if not len(form_data['name'])>=2:
            errors.append("name must be 2 or more characters.")
        if len(form_data['pw']) < 8:
            errors.append("Password must be 8 or more characters in length")
        if form_data['pw'] != form_data['pw_confirmation']:
            errors.append("Password must match password confirmation")
        user = User.objects.filter(email=form_data['email'])
        if user:
            errors.append("email has already been registered")
        # checks if there were any errors
        if len(errors) is not 0:
            return (False, errors)
        else:
            print("passed validations")
            # create the hashed password using bcrypt. Remember to encode
            pw_hash = bcrypt.hashpw(form_data['pw'].encode(), bcrypt.gensalt().encode())
            # create() method in objects returns newly entered entry in your db
            user = User.objects.create(name=form_data['name'], email=form_data['email'],  pw_hash=pw_hash)
            return (True, user)

class User(models.Model):
     name = models.CharField(max_length=255)
     email = models.CharField(max_length=255)
     pw_hash = models.CharField(max_length=255)
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)
     appointments = models.ManyToManyField(Appointment)
     objects = UserManager()


#
# class ItemManager(models.Manager):
#
#     def register(self, name, user):
#         items = Item.objects.filter(name = name)
#         if items:
#             item = items[0]
#         else:
#             item  = Item.objects.create(name = name, add_by = user)
#         return (True, item)
#
#     def getItem(self, id):
#         items = Item.objects.filter(id = id)
#         return items[0]
#
#     def getOtherList(self, id):
#         user = User.objects.getUser(id)
#         items =Item.objects.filter(~Q(add_by = user))
#         return items
#
#     def deleteAll(self):
#         Item.objects.all().delete()
#
#     def deleteItem(self,id):
#         Item.objects.filter(id = id).delete()
#
#
#class Item(models.Model):
#     name = models.CharField(max_length=255)
#     add_by = models.ForeignKey(User, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     objects = ItemManager()
#
