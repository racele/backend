import argparse
import os

import server


class Args:
	data: str
	host: str
	port: int
	proxy: str | None


def main() -> None:
	args = Args()
	parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

	parser.add_argument("--data", default=":memory:", help="the path for the database file")
	parser.add_argument("--host", default="0.0.0.0", help="the host to run on")
	parser.add_argument("--port", default=3000, help="the port to run on", type=int)
	parser.add_argument("--proxy", help="the proxy for outgoing requests")
	parser.parse_args(namespace=args)

	if args.proxy is not None:
		os.environ["HTTPS_PROXY"] = args.proxy

	app = server.Server(args.data, args.host, args.port)
	app.serve_forever()


if __name__ == "__main__":
	main()
