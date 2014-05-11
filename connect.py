#!/usr/bin/env python3
import api

print("Visit the following URL:")
print(api.get_auth_url())

redir_code = input("Enter the code you are redirected to (from the URL): ")
access_token = api.get_access_token(redir_code)

print("Access token:")
print(access_token)
