import http
import random
import typing

import database
import endpoint
import response


class GetDaily(endpoint.Endpoint):
	auth = False
	method = http.HTTPMethod.GET
	path = "/words/daily"
	query = []

	@staticmethod
	@typing.override
	def run(context: database.Context) -> response.Response:
		daily = context.database.dailies.get()

		if daily is None:
			words = context.gateway.words()

			if words is None:
				return response.error("could not fetch words", http.HTTPStatus.BAD_GATEWAY)

			while daily is None:
				solution = random.choice(words.solutions)
				daily = context.database.dailies.set(solution)

		return response.success(vars(daily))


class GetWords(endpoint.Endpoint):
	auth = False
	method = http.HTTPMethod.GET
	path = "/words"
	query = []

	@staticmethod
	@typing.override
	def run(context: database.Context) -> response.Response:
		words = context.gateway.words()

		if words is None:
			return response.error("could not fetch words", http.HTTPStatus.BAD_GATEWAY)

		return response.success(vars(words))
