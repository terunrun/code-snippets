"""任意のURLへリクエストを発行する（例としてGoogle Cloud Functionsの関数）"""
# https://note.nkmk.me/python-requests-usage/

import sys
import requests
import google.auth.transport.requests
import google.oauth2.id_token

args = sys.argv
FUNCTION = args[1]
LOCATION = args[2]
PROJECT  = args[3]
REQUEST_NUMBER = args[4]
URL = f'https://{LOCATION}-{PROJECT}.cloudfunctions.net/{FUNCTION}'


def http_request_with_token():
    # # URLに対するトークンを取得
    request = google.auth.transport.requests.Request()
    target_audience = URL
    id_token = google.oauth2.id_token.fetch_id_token(request, target_audience)

    # GETリクエストにパラメーターを追加
    payload = REQUEST_NUMBER if REQUEST_NUMBER else {}
    headers = {'Authorization': f'Bearer {id_token}'}

    # リクエストを発行し結果を得る
    response = requests.get(URL, headers=headers, params=payload)
    response.raise_for_status()

    # responseから様々な情報を取得可能
    print(response.URL)
    print(response.status_code)
    print(response.headers)
    print(response.encoding)
    print(response.text)


if __name__ == "__main__":
    http_request_with_token()
