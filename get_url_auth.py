import urllib.parse

import requests


# # birinchi link generatsiya qilinadi
#
#


def get_github_code(client_id, redirect_uri):
    url = f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}"
    response = requests.get(url)
    return response.url


print(
    get_github_code(
        "Ov23lifn4y25nfQAnUvu", "http://127.0.0.1:8000/auth/github/callback/"
    )
)


#
#
# # Example usage
# client_id = "your_github_client_id"
# redirect_uri = "your_redirect_uri"
# authorization_url = get_github_code(client_id, redirect_uri)
# print(authorization_url)
#
# # ikkinchi linkdan code olinadi
#
#
# def get_github_token(client_id, client_secret, code):
#     url = "https://github.com/login/oauth/access_token"
#     headers = {"Accept": "application/json"}
#     data = {
#         "client_id": client_id,
#         "client_secret": client_secret,
#         "code": code
#     }
#     response = requests.post(url, headers=headers, data=data)
#     response.raise_for_status()
#     return response.json().get("access_token")
#
#
# # Example usage
# client_id = "your_github_client_id"
# client_secret = "your_github_client_secret"
# code = "code_received_from_github"
# token = get_github_token(client_id, client_secret, code)
# print(token)
#
# # uchinchi linkdan token olinadi
# import requests
#
#
# def get_github_user_info(token):
#     url = "https://api.github.com/user"
#     headers = {"Authorization": f"token {token}"}
#     response = requests.get(url, headers=headers)
#     response.raise_for_status()
#     return response.json()


def get_google_code(client_id, redirect_uri, scopes):
    # Join scopes with a space and URL encode them
    scope = urllib.parse.quote(" ".join(scopes))
    url = (
        f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={client_id}&"
        f"redirect_uri={redirect_uri}&"
        f"response_type=code&"
        f"scope={scope}"
    )
    return url


# Example usage
client_id = "367993672441-sg99c5dmc7padjbirvok3esbi8j8j0cj.apps.googleusercontent.com"
redirect_uri = "http://127.0.0.1:8000/auth/google/callback/"
scopes = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "openid",
]
authorization_url = get_google_code(client_id, redirect_uri, scopes)
print(authorization_url)
