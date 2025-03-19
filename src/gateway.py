import dataclasses
import http.client
import json
import typing
import urllib.request


class Data(typing.TypedDict):
	data: list[str]


@dataclasses.dataclass
class Words:
	guessable: list[str]
	solutions: list[str]


class Gateway:
	def __init__(self) -> None:
		self.cache: dict[str, Words] = {}

	def get(self, url: str) -> str:
		response: http.client.HTTPResponse

		with urllib.request.urlopen(url) as response:
			content = response.read()

		return content.decode()

	def load(self, language: str) -> Words | None:
		match language:
			case "de":
				url = "https://raw.githubusercontent.com/caco3/wordle-de/main/other-words.json"
				data: Data = json.loads(self.get(url))
				guessable = [word for word in data["data"] if word.isascii()]

				url = "https://raw.githubusercontent.com/caco3/wordle-de/main/target-words.json"
				data: Data = json.loads(self.get(url))
				solutions = [word for word in data["data"] if word.isascii()]

				return Words(guessable, solutions)

			case "en":
				url = "https://gist.githubusercontent.com/scholtes/94f3c0303ba6a7768b47583aff36654d/raw/wordle-Ta.txt"
				guessable = self.get(url).splitlines()

				url = "https://gist.githubusercontent.com/scholtes/94f3c0303ba6a7768b47583aff36654d/raw/wordle-La.txt"
				solutions = self.get(url).splitlines()

				return Words(guessable, solutions)

			case _:
				return None

	def words(self, language: str) -> Words | None:
		if language not in self.cache:
			try:
				words = self.load(language)

				if words is None:
					return None

				self.cache[language] = words
			except Exception:
				return None

		return self.cache[language]
