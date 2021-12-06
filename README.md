# LoLAramPredictor-API

LoLAramPredictor-API is an API that serves League of Legends' ARAM game mode win prediction for each team based on a trained machine learning model. 

## Getting Started
These instructions will help you get started with using the API.

### API Usage

```
https://lol-aram-predictor.herokuapp.com/api/v1/summoner_name
```
Replace 'summoner_name' in the URL with the player's summoner name you would like to look up and make a prediction of their current game.

### Sample Output
#### Summoner not actively in a game JSON response
```json
{
  "summonerName": "Example123",
  "targetTeam": "",
  "spectatorData": "No ARAM game found",
  "prediction": ""
}
```
#### Summoner does not exist JSON response
```json
{
  "summonerName": "Example123",
  "targetTeam": "",
  "spectatorData": "Cannot find summoner name 'Example123'",
  "prediction": ""
}
```
#### Active Summoner's prediction JSON response
```json
{
  "summonerName": "BluePlayer2",
  "targetTeam": "Blue",
  "spectatorData": {
    "gameId": 4128746655,
    "avgChampMastery1": 13368.199999999999,
    "avgChampMastery2": 67745.8,
    "avgRank1": "SILVER I",
    "avgRank2": "PLATINUM IV",
    "summonerName_1": "BluePlayer1",
    "champName_1": "Twitch",
    "champ_1": 29,
    "champPts_1": 4192,
    "rank_1": "GOLD IV",
    "rankWins_1": 545,
    "rankLosses_1": 523,
    "rankWinRatio_1": 0.5102996254681648,
    "spell1Id_1": 14,
    "spell2Id_1": 4,
    "perk0_1": 8005,
    "perk1_1": 8009,
    "perk2_1": 9104,
    "perk3_1": 8014,
    "perk4_1": 8143,
    "perk5_1": 8105,
    "champPts_rank_1": 54496,
    "primaryClass_1": "Marksman",
    "secondaryClass_1": "Assassin",
    "summonerName_2": "BluePlayer2",
    "champName_2": "Shaco",
    "champ_2": 35,
    "champPts_2": 5690,
    "rank_2": "GOLD III",
    "rankWins_2": 124,
    "rankLosses_2": 109,
    "rankWinRatio_2": 0.5321888412017167,
    "spell1Id_2": 4,
    "spell2Id_2": 14,
    "perk0_2": 8229,
    "perk1_2": 8226,
    "perk2_2": 8210,
    "perk3_2": 8236,
    "perk4_2": 8138,
    "perk5_2": 8105,
    "champPts_rank_2": 79660,
    "primaryClass_2": "Assassin",
    "secondaryClass_2": "None",
    "summonerName_3": "BluePlayer3",
    "champName_3": "Corki",
    "champ_3": 42,
    "champPts_3": 3992,
    "rank_3": "UNRANKED",
    "rankWins_3": -9999999,
    "rankLosses_3": -9999999,
    "rankWinRatio_3": 0.5,
    "spell1Id_3": 21,
    "spell2Id_3": 4,
    "perk0_3": 8128,
    "perk1_3": 8126,
    "perk2_3": 8138,
    "perk3_3": 8106,
    "perk4_3": 8226,
    "perk5_3": 8236,
    "champPts_rank_3": 0,
    "primaryClass_3": "Marksman",
    "secondaryClass_3": "None",
    "summonerName_4": "BluePlayer4",
    "champName_4": "Mordekaiser",
    "champ_4": 82,
    "champPts_4": 818,
    "rank_4": "GOLD IV",
    "rankWins_4": 451,
    "rankLosses_4": 455,
    "rankWinRatio_4": 0.4977924944812362,
    "spell1Id_4": 32,
    "spell2Id_4": 4,
    "perk0_4": 8010,
    "perk1_4": 9111,
    "perk2_4": 9105,
    "perk3_4": 8299,
    "perk4_4": 8473,
    "perk5_4": 8453,
    "champPts_rank_4": 10634,
    "primaryClass_4": "Fighter",
    "secondaryClass_4": "None",
    "summonerName_5": "BluePlayer5",
    "champName_5": "Xayah",
    "champ_5": 498,
    "champPts_5": 52149,
    "rank_5": "SILVER II",
    "rankWins_5": 160,
    "rankLosses_5": 129,
    "rankWinRatio_5": 0.5536332179930796,
    "spell1Id_5": 4,
    "spell2Id_5": 7,
    "perk0_5": 8008,
    "perk1_5": 8009,
    "perk2_5": 9103,
    "perk3_5": 8014,
    "perk4_5": 8139,
    "perk5_5": 8135,
    "champPts_rank_5": 573639,
    "primaryClass_5": "Marksman",
    "secondaryClass_5": "None",
    "summonerName_6": "RedPlayer1",
    "champName_6": "Tryndamere",
    "champ_6": 23,
    "champPts_6": 7082,
    "rank_6": "UNRANKED",
    "rankWins_6": -9999999,
    "rankLosses_6": -9999999,
    "rankWinRatio_6": 0.5,
    "spell1Id_6": 32,
    "spell2Id_6": 4,
    "perk0_6": 8008,
    "perk1_6": 9111,
    "perk2_6": 9104,
    "perk3_6": 8014,
    "perk4_6": 8139,
    "perk5_6": 8135,
    "champPts_rank_6": 0,
    "primaryClass_6": "Fighter",
    "secondaryClass_6": "Assassin",
    "summonerName_7": "RedPlayer2",
    "champName_7": "Zilean",
    "champ_7": 26,
    "champPts_7": 105308,
    "rank_7": "UNRANKED",
    "rankWins_7": -9999999,
    "rankLosses_7": -9999999,
    "rankWinRatio_7": 0.5,
    "spell1Id_7": 4,
    "spell2Id_7": 13,
    "perk0_7": 8229,
    "perk1_7": 8226,
    "perk2_7": 8210,
    "perk3_7": 8236,
    "perk4_7": 8138,
    "perk5_7": 8105,
    "champPts_rank_7": 0,
    "primaryClass_7": "Support",
    "secondaryClass_7": "Mage",
    "summonerName_8": "RedPlayer3",
    "champName_8": "Renekton",
    "champ_8": 58,
    "champPts_8": 67756,
    "rank_8": "PLATINUM IV",
    "rankWins_8": 104,
    "rankLosses_8": 113,
    "rankWinRatio_8": 0.4792626728110599,
    "spell1Id_8": 4,
    "spell2Id_8": 32,
    "perk0_8": 8010,
    "perk1_8": 9111,
    "perk2_8": 9103,
    "perk3_8": 8014,
    "perk4_8": 8143,
    "perk5_8": 8135,
    "champPts_rank_8": 1151852,
    "primaryClass_8": "Fighter",
    "secondaryClass_8": "Tank",
    "summonerName_9": "RedPlayer4",
    "champName_9": "Kennen",
    "champ_9": 85,
    "champPts_9": 66228,
    "rank_9": "UNRANKED",
    "rankWins_9": -9999999,
    "rankLosses_9": -9999999,
    "rankWinRatio_9": 0.5,
    "spell1Id_9": 4,
    "spell2Id_9": 32,
    "perk0_9": 8112,
    "perk1_9": 8139,
    "perk2_9": 8138,
    "perk3_9": 8135,
    "perk4_9": 9111,
    "perk5_9": 8014,
    "champPts_rank_9": 0,
    "primaryClass_9": "Mage",
    "secondaryClass_9": "Marksman",
    "summonerName_10": "RedPlayer5",
    "champName_10": "Aphelios",
    "champ_10": 523,
    "champPts_10": 92355,
    "rank_10": "UNRANKED",
    "rankWins_10": -9999999,
    "rankLosses_10": -9999999,
    "rankWinRatio_10": 0.5,
    "spell1Id_10": 4,
    "spell2Id_10": 7,
    "perk0_10": 8008,
    "perk1_10": 9111,
    "perk2_10": 9104,
    "perk3_10": 8014,
    "perk4_10": 8138,
    "perk5_10": 8135,
    "champPts_rank_10": 0,
    "primaryClass_10": "Marksman",
    "secondaryClass_10": "None",
    "gameVersion": "11.23"
  },
  "prediction": {
    "blue": "30.52%",
    "red": "69.48%"
  }
}
```

## Development
These instructions will get you a copy of the project up and running on your local machine for development.

### Built With
* [Python 3.6](https://docs.python.org/3/) - The scripting language used.
* [Pandas](https://pandas.pydata.org/) - Data manipulation tool used.
* [Django](https://www.djangoproject.com/) - The web framework used to route and serve the API.
* [Pantheon](https://github.com/Canisback/pantheon) - Asyncronous Python wrapper to interface with the Riot API.
* [CatBoost](https://catboost.ai/en/docs/) - Gradient boosting algorithm and framework used to model the data and make predictions.
* [Uvicorn](https://www.uvicorn.org/) - ASGI server implementation used (when deployed to ASGI host services).
* [Gunicorn](https://gunicorn.org/) - WSGI server implementation used (when deployed to WSGI host services).

### Setup
Run the following command to installer all the required Python modules:
```
pip install -r requirements.txt
```

### Starting the web server
To start ASGI server:
```
uvicorn LoLAramPredictor.asgi:application
```

Or to start WSGI servier with Uvicorn worker:
```
gunicorn LoLAramPredictor.asgi:application -b 0.0.0.0:$PORT -w 1 -k uvicorn.workers.UvicornWorker
```

## Authors
* **Patrick Yu** - *Initial work* - [patrickgods1](https://github.com/patrickgods1)