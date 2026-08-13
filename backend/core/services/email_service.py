import os

from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

from configs.celery import app
from core.services.jwt_service import ActivateToken, JWTService

UserModel = get_user_model()


class EmailService:
    # для того щоб позначити що це завдання селері додаємо @app.task
    @app.task
    def __send_email(to: str, template_name: str, context: dict, subject: str) -> None:
        template = get_template(template_name)
        html_content = template.render(context)
        msg = EmailMultiAlternatives(
            to=[to],
            from_email=os.environ.get('EMAIL_HOST_USER'),
            subject=subject
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    @classmethod
    def register(cls, user):
        token = JWTService.create_token(user, ActivateToken)  # творення токену для активації саме цього юзера
        url = f'http://localhost/activate/{token}'  # створення посилання в листі по ньому юзер переходить попадає на обробник актівейтвю далі з кваргсів витягується токен який попадає в джвт сервіс де верифікується тобто чи є такий юзер в бд і  якщо так то активується акаунт

        # .delay()означає: не надсилати лист прямо зараз усередині Django-запиту,а передати завдання Celery.
        cls.__send_email.delay(
            to=user.email,
            template_name='register.html',
            context={'name': user.profile.name, 'url': url},
            subject="Register"
        )

    # @staticmethod
    # @app.task
    # def spam():
    #     for user in UserModel.objects.all():
    #         EmailService.__send_email(user.email, 'spam.html', {}, 'SPAM')
