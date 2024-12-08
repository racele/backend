import importlib
import os

import database
import endpoint


def collect(database: database.Database) -> list[endpoint.Endpoint]:
	endpoints: list[endpoint.Endpoint] = []

	for file in os.listdir("src/endpoints"):
		if file.endswith(".py"):
			name = file.removesuffix(".py")
			module = importlib.import_module(f"endpoints.{name}")

			for value in vars(module).values():
				if isinstance(value, type) and issubclass(value, endpoint.Endpoint):
					endpoints.append(value(database))

	return endpoints
