import requests
from django.db import transaction

from monitoring.choices import APIStatus
from monitoring.models import API, History
from monitoring.services.api_verification_class_services import APIResult


def verify_api_response(api: API) -> APIResult:

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
        result.timeout_count = 0

    except requests.exceptions.Timeout:
        result.api_response = "Timeout"
        result.timeout_count += 1

        if result.timeout_count >= 3:
            result.api_status = APIStatus.DOWN

    except requests.exceptions.ConnectionError:
        result.api_response = "Connection Error"
        result.api_status = APIStatus.DOWN
        result.timeout_count = 0

    return result


def save_history(result: APIResult, api: API) -> None:
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
