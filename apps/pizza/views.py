

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.request import Request

from apps.pizza.filter import filter_pizza
from apps.pizza.models import PizzaModel
from apps.pizza.serializers import PizzaSerializer


# Create your views here.
class PizzaListCreateView(ListCreateAPIView):
    serializer_class = PizzaSerializer
    def get_queryset(self):
        request:Request = self.request
        return filter_pizza(request.query_params)
class PizzaRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = PizzaSerializer
    queryset = PizzaModel.objects.all()
    http_method_names = ['get', 'put', 'delete','patch']
