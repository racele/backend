import dataclasses
import urllib.error
import urllib.request


@dataclasses.dataclass
class Words:
	guessable: list[str]
	solutions: list[str]


class Gateway:
	def __init__(self) -> None:
		self.cache: dict[str, str] = {}

	def get(self, url: str) -> str | None:
		if url not in self.cache:
			try:
				with urllib.request.urlopen(url) as response:
					content: bytes = response.read()

				self.cache[url] = content.decode()
			except urllib.error.URLError:
				return None

		return self.cache[url]

	def words(self) -> Words | None:
		url = "https://gist.githubusercontent.com/scholtes/94f3c0303ba6a7768b47583aff36654d/raw/wordle-Ta.txt"
		response = self.get(url)

		if response is None:
			return None
		else:
			guessable = response.splitlines()

		url = "https://gist.githubusercontent.com/scholtes/94f3c0303ba6a7768b47583aff36654d/raw/wordle-La.txt"
		response = self.get(url)

		if response is None:
			return None
		else:
			solutions = response.splitlines()

		return Words(guessable, solutions)
