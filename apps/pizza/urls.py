from django.urls import path

from apps.pizza.views import PizzaListCreateView, PizzaRetrieveUpdateDestroyAPIView

urlpatterns = [
    path("", PizzaListCreateView.as_view()),
    path("/<int:pk>", PizzaRetrieveUpdateDestroyAPIView.as_view()),
]