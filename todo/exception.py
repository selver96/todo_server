from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    # error = exc
    # if response is not None:
    #     if error['code'] == 401:
    #         authentication_failed(error['message'], 401, response)
    return response


def authentication_failed(error, status_code, response):
    # import pdb
    # pdb.set_trace()
    response.data = {
        'error': str(error),
        'status': status_code
    }
    response.status_code = status_code
    return response
