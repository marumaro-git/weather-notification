from weather_forecast import WeatherForecast

import os
import requests


def lambda_handler(event, context):
    api_key = get_parameter()
    instance = WeatherForecast(api_key)
    instance.main()


def get_parameter():
    parameteStoreName = os.getenv("parameterStoreName")
    # デフォルトポートは2773
    end_point = "http://localhost:2773"
    path = "/systemsmanager/parameters/get/?name={}&withDecryption=true".format(
        parameteStoreName
    )
    url = end_point + path

    # GETリクエストに必要なトークン
    headers = {"X-Aws-Parameters-Secrets-Token": os.environ["AWS_SESSION_TOKEN"]}
    res = requests.get(url, headers=headers)
    return res.json()["Parameter"]["Value"]
