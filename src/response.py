import dataclasses
import http
import typing

type ResponseBody = ErrorBody | SuccessBody
type ResponseData = dict[str, object] | list[dict[str, object]]


class ErrorBody(typing.TypedDict):
	code: http.HTTPStatus
	message: str


class SuccessBody(typing.TypedDict):
	code: http.HTTPStatus
	data: ResponseData


@dataclasses.dataclass
class Response:
	body: ResponseBody
	code: http.HTTPStatus


def error(message: str, code: http.HTTPStatus = http.HTTPStatus.BAD_REQUEST) -> Response:
	return Response({"code": code, "message": message}, code)


def success(data: ResponseData, code: http.HTTPStatus = http.HTTPStatus.OK) -> Response:
	return Response({"code": code, "data": data}, code)
