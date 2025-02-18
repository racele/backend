import argparse
import os

import server


def main() -> None:
	parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument("--port", default=3000, help="the port to run on", type=int)
	parser.add_argument("--proxy", help="the proxy for outgoing requests")

	args = parser.parse_args()
	port: int = args.port
	proxy: str | None = args.proxy

	if proxy is not None:
		os.environ["HTTPS_PROXY"] = proxy

	app = server.Server(port)
	app.serve_forever()


if __name__ == "__main__":
	main()
