import pandas as pd
from django.http import FileResponse
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from .models import Robot


def add_to_excel(request):
    # Получение текущей даты и времени
    now = timezone.now()
    # Получение даты и времени одной недели назад
    week_ago = now - timedelta(days=7)
    model_set = set(list(Robot.objects.values_list('model', flat=True)))
    made_week_ago = Robot.objects.filter(created__gte=week_ago)
    list_dict = []
    for model_value in model_set:
        filter_set = made_week_ago.filter(model=model_value)
        if filter_set:
            count_list = filter_set.values_list('serial').annotate(count=Count('id'))
            model_list = count_list.values_list('model', flat=True)
            version_list = count_list.values_list('version', flat=True)
            data_set = {
                'Модель': model_list,
                'Версия': version_list,
                'Количество за неделю': [count[1] for count in count_list],
            }

            df = pd.DataFrame(data_set)
            list_dict.append({model_value: df})

    with pd.ExcelWriter('report.xlsx') as writer:
        for dict_df in list_dict:
            list(dict_df.values())[0].to_excel(writer, index=False, sheet_name=list(dict_df.keys())[0])
    return FileResponse(open('report.xlsx', 'rb'), as_attachment=True)
