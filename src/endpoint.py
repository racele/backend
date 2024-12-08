import abc
import dataclasses
import enum

import database


class Method(enum.Enum):
	Patch = 0
	Post = 1


@dataclasses.dataclass
class Result:
	code: int
	response: dict[str, object]


def error(code: int, message: str) -> Result:
	return Result(code, {"code": code, "message": message})


class Endpoint(abc.ABC):
	method: Method
	path: str

	def __init__(self, database: database.Database) -> None:
		self.database = database

	@abc.abstractmethod
	def run(self, data: database.RequestData) -> Result:
		pass
