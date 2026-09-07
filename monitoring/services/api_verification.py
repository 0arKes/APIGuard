from monitoring.choices import APIStatus


class APIResult:
    def __init__(
        self,
        api_response: str | None,
        status_code: int | None,
        response_time: int | None,
        timeout_count: int,
        api_status: APIStatus,
    ):
        self.api_response = api_response
        self.status_code = status_code
        self.response_time = response_time
        self.timeout_count = timeout_count
        self.api_status = api_status
