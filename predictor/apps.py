from django.apps import AppConfig
from catboost import CatBoostClassifier
# from predictor.config import riotConfig
from pantheon import pantheon
import ssl
import os


class PredictorConfig(AppConfig):
    name = 'predictor'
    filename = 'OptimizeBrierMaxCat01716961192'
    server = 'NA1'
    model = CatBoostClassifier()
    model.load_model(name + '/' + filename)
    ssl.match_hostname = lambda cert, hostname: True
    # panth = pantheon.Pantheon(server, riotConfig['api_key'], errorHandling=True, debug=False)
    panth = pantheon.Pantheon(server, os.environ['RIOT_API_KEY'], errorHandling=True, debug=False)
