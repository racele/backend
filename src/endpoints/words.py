import http
import random

import database
import endpoint
import response


class GetDaily(endpoint.Endpoint):
	auth = False
	method = http.HTTPMethod.GET
	path = "/words/daily"
	query = ["language"]

	@staticmethod
	def run(context: database.Context) -> response.Response:
		language = context.data["language"]
		daily = context.database.dailies.get(language)

		if daily is None:
			words = context.gateway.words(language)

			if words is None:
				return response.error("could not load word list", http.HTTPStatus.BAD_GATEWAY)

			while daily is None:
				solution = random.choice(words.solutions)
				daily = context.database.dailies.set(language, solution)

		return response.success(daily)


class GetWords(endpoint.Endpoint):
	auth = False
	method = http.HTTPMethod.GET
	path = "/words"
	query = ["language"]

	@staticmethod
	def run(context: database.Context) -> response.Response:
		language = context.data["language"]
		words = context.gateway.words(language)

		if words is None:
			return response.error("could not load word list", http.HTTPStatus.BAD_GATEWAY)

		return response.success(words)
