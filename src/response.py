import dataclasses
import http
import json


class Encoder(json.JSONEncoder):
	def default(self, o: object) -> object:
		if dataclasses.is_dataclass(o):
			return vars(o)

		return super().default(o)


@dataclasses.dataclass
class Response:
	code: http.HTTPStatus
	data: object


def error(message: str, code: http.HTTPStatus = http.HTTPStatus.BAD_REQUEST) -> Response:
	return Response(code, {"code": code, "message": message})


def success(data: object, code: http.HTTPStatus = http.HTTPStatus.OK) -> Response:
	return Response(code, data)
