from rest_framework.exceptions import APIException


class ArticleAlreadyRated(APIException):
    status_code = 400
    default_detail = "You have already rated this article."
    default_code = "bad_request"
