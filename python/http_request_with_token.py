"""任意のURLへリクエストを発行する（例としてGoogle Cloud Functionsの関数）"""
# https://note.nkmk.me/python-requests-usage/

import requests
import sys
import google.auth.transport.requests
import google.oauth2.id_token

args = sys.argv
function = args[1]
location = args[2]
project  = args[3]
request_parameter = args[4]
url = f'https://{location}-{project}.cloudfunctions.net/{function}'


def http_request_with_token():
    # # URLに対するトークンを取得
    request = google.auth.transport.requests.Request()
    target_audience = url
    id_token = google.oauth2.id_token.fetch_id_token(request, target_audience)

    # GETリクエストにパラメーターを追加
    payload = request_parameter if request_parameter else {}
    headers = {'Authorization': f'Bearer {id_token}'}

    # リクエストを発行し結果を得る
    response = requests.get(url, headers=headers, params=payload)
    response.raise_for_status()

    # responseから様々な情報を取得可能
    print(response.url)
    print(response.status_code)
    print(response.headers)
    print(response.encoding)
    print(response.text)


if __name__ == "__main__":
    http_request_with_token()
