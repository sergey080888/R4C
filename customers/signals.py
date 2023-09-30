from django.db.models.signals import post_save, pre_save
from R4C.settings import EMAIL_HOST_USER
from orders.models import Order
from django.dispatch import receiver
from robots.models import Robot
from django.core import mail
from django.core.mail import EmailMessage


@receiver(post_save, sender=Robot)
def send_notification(instance, created, **kwargs):
    if created:
        robot_serial = instance.serial
        orders = Order.objects.filter(robot_serial=robot_serial)
        customer_mails = [order.customer.email for order in orders]
        model = instance.model
        version = instance.version
        subject = 'Уведомление о поступлении робота'
        mail_text = f'Добрый день!Недавно вы интересовались нашим роботом модели {model}, версии {version}. \n' \
                    f'Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами'
        email = EmailMessage(
            subject,
            mail_text,
            EMAIL_HOST_USER,
            to=customer_mails,
        )
        connection = mail.get_connection()
        connection.send_messages([email])


@receiver(pre_save, sender=Order)
def add_order(instance, **kwargs):
    if Robot.objects.filter(serial=instance.robot_serial):
        raise Exception('Этот робот есть на складе - добавить в заказ нельзя')
