

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response

class FirstView(APIView):
    def get(self, *args, **kwargs):
        print(self.request.query_params.dict())
        return Response("Hello from get")
    #витягування даних
    def post(self, *args, **kwargs):
        print(self.request.data)
        return Response("Hello from post")

    def put(self, *args, **kwargs):
        print(self.request.data)
        print(self.request.query_params.dict())
        return Response("Hello from put")

    def patch(self, *args, **kwargs):
        return Response("Hello from patch")

    def delete(self, *args, **kwargs):
        return Response("Hello from delete")

class SecondView(APIView):
    def get(self, *args, **kwargs):
        print(kwargs)
        return Response(kwargs["age"])
