import abc
import dataclasses
import http

import database


@dataclasses.dataclass
class Result:
	code: http.HTTPStatus
	response: dict[str, object]


def error(message: str, code: http.HTTPStatus = http.HTTPStatus.BAD_REQUEST) -> Result:
	return Result(code, {"code": code, "message": message})


def success(data: dict[str, object], code: http.HTTPStatus = http.HTTPStatus.OK) -> Result:
	return Result(code, {"code": code, "data": data})


class Endpoint(abc.ABC):
	method: http.HTTPMethod
	path: str

	def __init__(self, database: database.Database) -> None:
		self.database = database

	@abc.abstractmethod
	def run(self, data: database.RequestData) -> Result:
		pass
