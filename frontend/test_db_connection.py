"""FastAPI connectivity smoke test.

The frontend intentionally has no PostgreSQL credentials or driver anymore.
Run the backend first, then execute this file from the frontend directory.
"""

import requests


def main() -> None:
    response = requests.get("http://127.0.0.1:8000/", timeout=10)
    response.raise_for_status()
    print("FastAPI reachable:", response.json())


if __name__ == "__main__":
    main()
