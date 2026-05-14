from rest_framework.response import Response


def success_response(data=None, message=None, status=200):
    payload = {"success": True}
    if message is not None:
        payload["message"] = message
    if data is not None:
        payload["data"] = data
    return Response(payload, status=status)
