from .apps import PredictorConfig
# from predictor.config import riotConfig
from typing import Dict, Tuple
import asyncio
import json
from catboost import CatBoostClassifier
import pandas as pd


async def getSummonerId(summonerName: str) -> str:
    try:
        print(f'[INFO] Looking up summonerId for: {summonerName}')
        data = await PredictorConfig.panth.getSummonerByName(summonerName)
        # summonerIdQueue.put_nowait(data['id'])
    except Exception as e:
        print(f'[WARNING] getSummonerId ({summonerName}): {e}')
        return '', ''
    else:
        return data['name'], data['id']


async def getSpectatorInfo(summonerId: str, champions: pd.DataFrame) -> Tuple[str, str, dict]:
    try:
        targetTeam = ''
        targetName = ''
        print(f'[INFO] Looking up spectator data for: {summonerId}')
        spectatorData = await PredictorConfig.panth.getCurrentGame(summonerId)
        if spectatorData and spectatorData['gameMode'] == 'ARAM':
            paritipantsList = []
            coroList1 = []
            coroList2 = []
            for i in range(len(spectatorData['participants'])):
                if spectatorData['participants'][i]['summonerId'] == summonerId:
                    targetTeam = 'Blue' if spectatorData['participants'][i]['teamId'] == 100 else 'Red'
                    targetName = spectatorData['participants'][i]['summonerName']
                participant = {'teamId': spectatorData['participants'][i]['teamId'],
                                'summonerName': spectatorData['participants'][i]['summonerName'],
                                'summonerId': spectatorData['participants'][i]['summonerId'],
                                'spell1Id': spectatorData['participants'][i]['spell1Id'],
                                'spell2Id': spectatorData['participants'][i]['spell2Id'],
                                'championId': spectatorData['participants'][i]['championId'],
                                'perk0': spectatorData['participants'][i]['perks']['perkIds'][0],
                                'perk1': spectatorData['participants'][i]['perks']['perkIds'][1],
                                'perk2': spectatorData['participants'][i]['perks']['perkIds'][2],
                                'perk3': spectatorData['participants'][i]['perks']['perkIds'][3],
                                'perk4': spectatorData['participants'][i]['perks']['perkIds'][4],
                                'perk5': spectatorData['participants'][i]['perks']['perkIds'][5],
                                'perk6': spectatorData['participants'][i]['perks']['perkIds'][6],
                                'perk7': spectatorData['participants'][i]['perks']['perkIds'][7],
                                'perk8': spectatorData['participants'][i]['perks']['perkIds'][8]}
                coroList1.append(getChampMastery(participant['summonerId'], participant['championId']))
                coroList2.append(getRankInfo(participant['summonerId']))
                paritipantsList.append(participant)

            champMasteryResults = await asyncio.gather(*coroList1)
            rankResults = await asyncio.gather(*coroList2)

            gameDict = {}
            gameDict['gameId'] = spectatorData['gameId']
            gameDict['avgChampMastery1'] = 0
            gameDict['avgChampMastery2'] = 0
            gameDict['avgRank1'] = 0
            gameDict['avgRank2'] = 0
            count1 = 0
            count2 = 0
            rankMap = {'UNRANKED': 0,
                'IRON IV': 1,
                'IRON III': 2,
                'IRON II': 3,
                'IRON I': 4,
                'BRONZE IV': 5,
                'BRONZE III': 6,
                'BRONZE II': 7,
                'BRONZE I': 8,
                'SILVER IV': 9,
                'SILVER III': 10,
                'SILVER II': 11,
                'SILVER I': 12,
                'GOLD IV': 13,
                'GOLD III': 14,
                'GOLD II': 15,
                'GOLD I': 16,
                'PLATINUM IV': 17,
                'PLATINUM III': 18,
                'PLATINUM II': 19,
                'PLATINUM I': 20,
                'DIAMOND IV': 21,
                'DIAMOND III': 22,
                'DIAMOND II': 23,
                'DIAMOND I': 24,
                'MASTER I': 25,
                'GRANDMASTER I': 26,
                'CHALLENGER I': 27}
            for i in range(len(paritipantsList)):
                paritipantsList[i]['champPts'] = champMasteryResults[i]
                (paritipantsList[i]['rank'], paritipantsList[i]['rankWins'], paritipantsList[i]['rankLosses']) = rankResults[i]
                if i < 5:
                    if rankResults[i][0] != 'UNRANKED':
                        gameDict['avgRank1'] += rankMap[rankResults[i][0]]
                        count1 += 1
                    gameDict['avgChampMastery1'] += champMasteryResults[i]/(len(paritipantsList)/2)
                else:
                    if rankResults[i][0] != 'UNRANKED':
                        gameDict['avgRank2'] += rankMap[rankResults[i][0]]
                        count2 += 1
                    gameDict['avgChampMastery2'] += champMasteryResults[i]/(len(paritipantsList)/2)
                    

            paritipantsList = sorted(paritipantsList, key = lambda i: (i['teamId'], i['championId']))

            for i in range(len(paritipantsList)):
                gameDict[f'summonerName_{i+1}'] = paritipantsList[i]['summonerName']
                gameDict[f'champName_{i+1}'] = champions.loc[paritipantsList[i]['championId'], 'name']
                gameDict[f'champ_{i+1}'] = paritipantsList[i]['championId']
                gameDict[f'champPts_{i+1}'] = paritipantsList[i]['champPts']
                gameDict[f'rank_{i+1}'] = paritipantsList[i]['rank']
                gameDict[f'rankWins_{i+1}'] = paritipantsList[i]['rankWins']
                gameDict[f'rankLosses_{i+1}'] = paritipantsList[i]['rankLosses']
                gameDict[f'rankWinRatio_{i+1}'] = paritipantsList[i]['rankWins'] /  \
                                                    (paritipantsList[i]['rankWins'] + paritipantsList[i]['rankLosses'])
                gameDict[f'spell1Id_{i+1}'] = paritipantsList[i]['spell1Id']
                gameDict[f'spell2Id_{i+1}'] = paritipantsList[i]['spell2Id']
                gameDict[f'perk0_{i+1}'] = paritipantsList[i]['perk0']
                gameDict[f'perk1_{i+1}'] = paritipantsList[i]['perk1']
                gameDict[f'perk2_{i+1}'] = paritipantsList[i]['perk2']
                gameDict[f'perk3_{i+1}'] = paritipantsList[i]['perk3']
                gameDict[f'perk4_{i+1}'] = paritipantsList[i]['perk4']
                gameDict[f'perk5_{i+1}'] = paritipantsList[i]['perk5']
                gameDict[f'champPts_rank_{i+1}'] = paritipantsList[i]['champPts'] * rankMap[paritipantsList[i]['rank']]
                gameDict[f'primaryClass_{i+1}'] = champions.loc[paritipantsList[i]['championId'], 'primaryClass']
                gameDict[f'secondaryClass_{i+1}'] = champions.loc[paritipantsList[i]['championId'], 'secondaryClass']
            
            url = 'https://ddragon.leagueoflegends.com/realms/na.json'
            response = await PredictorConfig.panth.fetch(url, method='GET')
            currentVersion = '.'.join(json.loads(await response.text())['v'].split('.')[:2])
            gameDict['gameVersion'] = currentVersion
            reverseRankMap = dict((v,k) for k, v in rankMap.items())
            if count1:
                gameDict['avgRank1'] = reverseRankMap[gameDict['avgRank1'] // count1]
            else:
                gameDict['avgRank1'] = 'UNRANKED'
            if count2:
                gameDict['avgRank2'] = reverseRankMap[gameDict['avgRank2'] // count2]
            else:
                gameDict['avgRank2'] = 'UNRANKED'
        else:
            gameDict = ''
    except Exception as e:
        print(f'[Warning] getSpectatorInfo ({summonerId}): No ARAM game found. {e}')
        return targetName, targetTeam, ''
    else:
        return targetName, targetTeam, gameDict


async def getChampMastery(summonerId: str, championId: int) -> int:
    try:
        champMasteryData = await PredictorConfig.panth.getChampionMasteriesByChampionId(summonerId, championId)
        if champMasteryData:
            champPts = champMasteryData['championPoints']
        else:
            champPts = 0
            print(f"[Warning] getChampMastery ({summonerId}, {championId}): None found.")
    except Exception:
        champPts = 0
    finally:
        return champPts


async def getRankInfo(summonerId: str) -> (str, int, int):
    try:
        rankData = await PredictorConfig.panth.getLeaguePosition(summonerId)
        rank = ''
        rankWins = -9999999
        rankLosses = -9999999
        if rankData:
            for r in rankData:
                if r['queueType'] == 'RANKED_SOLO_5x5':
                    rank = f"{r['tier']} {r['rank']}"
                    rankWins = r['wins']
                    rankLosses = r['losses']
            if not rank:
                rank = 'UNRANKED'
                rankWins = -9999999
                rankLosses = -9999999
        else:
            # print(f'[INFO] No rank info: {summonerId}')
            rank = 'UNRANKED'
            rankWins = -9999999
            rankLosses = -9999999
    except Exception:
        # print(f'[WARNING] getRankInfo ({summonerId}): {e}')
        rank = 'UNRANKED'
        rankWins = -9999999
        rankLosses = -9999999
    finally:
        return rank, rankWins, rankLosses


async def predictGame(targetName, targetTeam, gameData) -> Dict[str, str]:
    columns = ['gameId', 'summonerName_1', 'summonerName_2', 'summonerName_3', 'summonerName_4', 
        'summonerName_5', 'summonerName_6', 'summonerName_7', 'summonerName_8', 'summonerName_9', 
        'summonerName_10', 'champName_1', 'champName_2', 'champName_3', 'champName_4', 
        'champName_5', 'champName_6', 'champName_7', 'champName_8', 'champName_9', 
        'champName_10', 'champ_1', 'champ_2', 'champ_3', 'champ_4', 'champ_5', 'champ_6', 
        'champ_7', 'champ_8', 'champ_9', 'champ_10', 'rank_1', 'rank_2', 'rank_3', 'rank_4', 
        'rank_5', 'rank_6', 'rank_7', 'rank_8', 'rank_9', 'rank_10', 'rankWins_1', 'rankWins_2', 
        'rankWins_3', 'rankWins_4', 'rankWins_5', 'rankWins_6', 'rankWins_7', 'rankWins_8', 
        'rankWins_9', 'rankWins_10', 'rankLosses_1', 'rankLosses_2', 'rankLosses_3', 
        'rankLosses_4', 'rankLosses_5', 'rankLosses_6', 'rankLosses_7', 'rankLosses_8', 
        'rankLosses_9', 'rankLosses_10', 'champPts_1', 'champPts_2', 'champPts_3', 'champPts_4', 
        'champPts_5', 'champPts_6', 'champPts_7', 'champPts_8', 'champPts_9', 'champPts_10', 
        'spell1Id_1', 'spell1Id_2', 'spell1Id_3', 'spell1Id_4', 'spell1Id_5', 'spell1Id_6', 
        'spell1Id_7', 'spell1Id_8', 'spell1Id_9', 'spell1Id_10', 'spell2Id_1', 'spell2Id_2', 
        'spell2Id_3', 'spell2Id_4', 'spell2Id_5', 'spell2Id_6', 'spell2Id_7', 'spell2Id_8', 
        'spell2Id_9', 'spell2Id_10', 'perk0_1', 'perk0_2', 'perk0_3', 'perk0_4', 'perk0_5', 
        'perk0_6', 'perk0_7', 'perk0_8', 'perk0_9', 'perk0_10', 'perk1_1', 'perk1_2', 'perk1_3', 
        'perk1_4', 'perk1_5', 'perk1_6', 'perk1_7', 'perk1_8', 'perk1_9', 'perk1_10', 'perk2_1', 
        'perk2_2', 'perk2_3', 'perk2_4', 'perk2_5', 'perk2_6', 'perk2_7', 'perk2_8', 'perk2_9', 
        'perk2_10', 'perk3_1', 'perk3_2', 'perk3_3', 'perk3_4', 'perk3_5', 'perk3_6', 'perk3_7', 
        'perk3_8', 'perk3_9', 'perk3_10', 'perk4_1', 'perk4_2', 'perk4_3', 'perk4_4', 'perk4_5', 
        'perk4_6', 'perk4_7', 'perk4_8', 'perk4_9', 'perk4_10', 'perk5_1', 'perk5_2', 'perk5_3', 
        'perk5_4', 'perk5_5', 'perk5_6', 'perk5_7', 'perk5_8', 'perk5_9', 'perk5_10', 
        'gameVersion', 'primaryClass_1', 'secondaryClass_1', 'primaryClass_2', 'secondaryClass_2', 
        'primaryClass_3', 'secondaryClass_3', 'primaryClass_4', 'secondaryClass_4', 
        'primaryClass_5', 'secondaryClass_5', 'primaryClass_6', 'secondaryClass_6', 
        'primaryClass_7', 'secondaryClass_7', 'primaryClass_8', 'secondaryClass_8', 
        'primaryClass_9', 'secondaryClass_9', 'primaryClass_10', 'secondaryClass_10', 
        'rankWinRatio_1', 'rankWinRatio_2', 'rankWinRatio_3', 'rankWinRatio_4', 'rankWinRatio_5', 
        'rankWinRatio_6', 'rankWinRatio_7', 'rankWinRatio_8', 'rankWinRatio_9', 'rankWinRatio_10', 
        'avgRank1', 'avgRank2', 'avgRankWR1', 'avgRankWR2', 'avgChampMastery1', 'avgChampMastery2', 
        'champPts_rank_1', 'champPts_rank_2', 'champPts_rank_3', 'champPts_rank_4', 'champPts_rank_5', 
        'champPts_rank_6', 'champPts_rank_7', 'champPts_rank_8', 'champPts_rank_9', 'champPts_rank_10'] 
    
    X = pd.DataFrame([gameData], columns=columns)
    dropList = ['gameId', 'summonerName_1', 'summonerName_2', 'summonerName_3', 'summonerName_4', 
        'summonerName_5', 'summonerName_6', 'summonerName_7', 'summonerName_8', 'summonerName_9', 
        'summonerName_10', 'champName_1', 'champName_2', 'champName_3', 'champName_4', 
        'champName_5', 'champName_6', 'champName_7', 'champName_8', 'champName_9', 
        'champName_10']

    prob = PredictorConfig.model.predict_proba(X.drop(dropList, axis=1))
    # # print(prob)

    titles = ['summonerName', 'champName', 'rank', 'rankWins', 'rankLosses', 'rankWinRatio', 'champPts', 
                'primaryClass', 'secondaryClass']
    format_title = "{:<16}|{:<14}|{:<13}|{:<8}|{:<10}|{:<12}|{:<8}|{:<12}|{:<10}"
    format_string = "{:<16}|{:<14}|{:<13}|{:>8d}|{:>10d}|{:>12.5f}|{:>8d}|{:<12}|{:<10}"
    print('=' * 115)
    print('[Blue Team - {:0.2f}%] Average Rank: {:<13} | Average Champion Mastery: {:<10.2f} |'
            .format(prob[0,1]*100, X['avgRank1'].values[0], X['avgChampMastery1'].values[0]))
    print('-' * 89)
    print(format_title.format(*titles))
    print('-' * 115)
    for i in range(1, 6):
        print(format_string.format(*[X[f'{c}_{i}'].values[0] for c in titles]))
    print('=' * 115)
    print('[Red Team - {:0.2f}%] Average Rank: {:<13} | Average Champion Mastery: {:<10.2f} |'
            .format(prob[0,0]*100, X['avgRank2'].values[0], X['avgChampMastery2'].values[0]))
    print('-' * 87)
    print(format_title.format(*titles))
    print('-' * 115)
    for i in range(6, 11):
        print(format_string.format(*[X[f'{c}_{i}'].values[0] for c in titles]))
    print('=' * 115)
    if targetTeam == 'Blue':
        print(f"[Blue] {targetName}'s team has {prob[0,1]*100:0.2f}% chance of winning.")
        print(f"[Red] Enemy team has {prob[0,0]*100:0.2f}% chance of winning.")
    else:
        print(f"[Red] {targetName}'s team has {prob[0,0]*100:0.2f}% chance of winning.")
        print(f"[Blue] Enemy team has {prob[0,1]*100:0.2f}% chance of winning.")
    print('~'*50)

    return {'blue': f'{prob[0,1]*100:0.2f}%',
            'red': f'{prob[0,0]*100:0.2f}%'}


async def loadChampions() -> pd.DataFrame:
    versionResponse = await PredictorConfig.panth.fetch(
            'https://ddragon.leagueoflegends.com/api/versions.json', method='GET')
    latestVersion = json.loads(await versionResponse.text())[0]
    championsResponse = await PredictorConfig.panth.fetch(
            f'http://ddragon.leagueoflegends.com/cdn/{latestVersion}/data/en_US/champion.json', method='GET')
    championData = json.loads(await championsResponse.text())
    champions = pd.DataFrame(columns = ['championId', 'name', 'primaryClass', 'secondaryClass'])

    # for k, v in championData['data'].items():
    for v in championData['data'].values():
        champions = champions.append({'championId': int(v['key']),
                            'name': v['name'],
                            'primaryClass': v['tags'][0], 
                            'secondaryClass': v['tags'][1] if len(v['tags']) > 1 else 'None', 
                            }, ignore_index=True)

    champions.set_index('championId', inplace=True)
    # print(champions.head())
    return champions

    