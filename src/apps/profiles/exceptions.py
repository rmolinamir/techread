from rest_framework.exceptions import APIException


class NoFollowingYourself(APIException):
    status_code = 403
    default_detail = "You can't follow yourself"
    default_code = "forbidden"


class NoUnfollowingYourself(APIException):
    status_code = 403
    default_detail = "You can't unfollow yourself"
    default_code = "forbidden"
