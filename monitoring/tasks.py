from celery import shared_task

from monitoring.services.api_response_services import save_history, verify_api_response

from .models import API


@shared_task
def verify_api(api_id):
    api = API.objects.get(id=api_id)

    result = verify_api_response(api)

    save_history(result, api)


@shared_task
def check_apis():
    apis = API.objects.all()

    for api in apis:
        verify_api.delay(api.id)
