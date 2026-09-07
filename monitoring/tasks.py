import requests
from celery import shared_task
from django.db import transaction

from monitoring.choices import APIStatus
from monitoring.services.api_verification import APIResult

from .models import API, History


@shared_task
def verify_api(api_id):
    api = API.objects.get(id=api_id)

    result = APIResult(
        api_response=None,
        status_code=None,
        response_time=None,
        timeout_count=api.timeout_count,
        api_status=APIStatus(api.api_status),
    )

    try:
        response = requests.get(api.url, timeout=10)
        response_time = int(response.elapsed.total_seconds() * 1000)
        response_api_status = (
            APIStatus.UP
            if response.status_code >= 200 and response.status_code < 400
            else APIStatus.DOWN
        )

        result.api_response = response.reason
        result.status_code = response.status_code
        result.response_time = response_time
        result.api_status = response_api_status

    except requests.exceptions.Timeout:
        result.api_response = "Timeout"
        result.timeout_count += 1

        if result.timeout_count >= 3:
            result.api_status = APIStatus.DOWN

    except requests.exceptions.ConnectionError:
        result.api_response = "Connection Error"
        result.api_status = APIStatus.DOWN

    if result.api_status == APIStatus.UP:
        result.timeout_count = 0

    with transaction.atomic():
        History.objects.create(
            api_response=result.api_response,
            status_code=result.status_code,
            response_time=result.response_time,
            api=api,
        )
        api.api_status = result.api_status
        api.timeout_count = result.timeout_count

        api.save()


@shared_task
def check_api():
    apis = API.objects.all()

    for api in apis:
        verify_api.delay(api.id)
