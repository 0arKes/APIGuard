import requests
from celery import shared_task
from django.db import transaction

from monitoring.choices import APIStatus

from .models import API, History


@shared_task
def verify_api(api_id):
    api = API.objects.get(id=api_id)

    response_dict = {
        "api_response": None,
        "status_code": None,
        "response_time": "",
        "api": api,
        "timeout": api.timeout_count,
        "api_status": api.api_status,
    }

    try:
        response = requests.get(api.url, timeout=10)
        response_time = int(response.elapsed.total_seconds() * 1000)
        response_api_status = (
            APIStatus.UP
            if response.status_code >= 200 and response.status_code < 400
            else APIStatus.DOWN
        )

        response_dict.update(
            {
                "api_response": response.reason,
                "status_code": response.status_code,
                "response_time": response_time,
                "api_status": response_api_status,
            }
        )

    except requests.exceptions.Timeout:
        response_dict.update({"timeout": response_dict["timeout"] + 1})

        if response_dict["timeout"] >= 3:
            response_dict["api_status"] = APIStatus.DOWN

    except requests.exceptions.ConnectionError:
        response_dict["api_status"] = APIStatus.DOWN

    if response_dict["api_status"] == APIStatus.UP:
        response_dict["timeout"] = 0

    with transaction.atomic():
        History.objects.create(
            api_response=response_dict["api_response"],
            status_code=response_dict["status_code"],
            response_time=response_dict["response_time"],
            api=response_dict["api"],
        )
        api.api_status = response_dict["api_status"]
        api.timeout_count = response_dict["timeout"]

        api.save()


@shared_task
def check_api():
    apis = API.objects.all()

    for api in apis:
        verify_api.delay(api.id)
