import json
from json import JSONDecodeError
from django.http import HttpResponse
from robots.models import Robot


def create_robot(request):
    try:
        data = json.loads(request.body)
        print(type(data))
    except JSONDecodeError:
        return HttpResponse('Данные отсвутствуют или не верны')
    field_names = [field.name for field in Robot._meta.get_fields()]

    for field_name in field_names[2:]:
        json_key = data.get(field_name)
        if not json_key:
            return HttpResponse(f'Ключ {field_name} отсутствует в JSON')

    serial = f'{data["model"]}-{data["version"]}'
    data['serial'] = serial

    Robot.objects.create(**data)

    return HttpResponse('Запись о произведенном роботе, добавлена в базу')
