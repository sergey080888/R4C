from django.contrib import admin
from orders.models import Order
from customers.models import Customer
from robots.models import Robot


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['email']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'robot_serial']

@admin.register(Robot)
class RobotAdmin(admin.ModelAdmin):
    list_display = ['serial', 'serial', 'model', 'version', 'created']


