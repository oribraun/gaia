from django.http import HttpResponse, JsonResponse

from new_app.models import ExampleModel
from new_app.serializers import ExampleModelSerializer

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def get_data(request, number=None):
    data = ExampleModel.objects.all()
    if request.method == 'GET':
        serializer = ExampleModelSerializer(data, many=True)
        return JsonResponse({'res':serializer.data, 'number': number}, safe=False)