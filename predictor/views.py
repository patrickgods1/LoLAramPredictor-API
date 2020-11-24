from django.http import HttpResponse, JsonResponse
from .predictor import getSummonerId, getSpectatorInfo, loadChampions, predictGame
import asyncio


# async def overview(request):
#     res = 'URL: http://example.com/api/v1/?summoner={summoner-name}'
#     return HttpResponse(res)


async def predictorView(request, summoner):
    if request.method == 'GET':
        # searchName = request.GET.get('summoner')
        (summonerName, summonerId), champions = await asyncio.gather(getSummonerId(summoner),  loadChampions())
        if summonerId:
            targetName, targetTeam, spectatorData = await getSpectatorInfo(summonerId, champions)
        else:
            targetName = ''
            targetTeam = ''
            spectatorData = f"Cannot find summoner name '{summoner}'"
        if targetName:
            prediction = await predictGame(targetName, targetTeam, spectatorData)
        else:
            prediction = ''    
        response = {'summonerName': targetName if targetName else summonerName,
                    # 'summonerId': summonerId if summonerId else 'Not found',
                    'targetTeam': targetTeam if targetTeam else '',
                    'spectatorData': spectatorData if spectatorData else 'No ARAM game found',
                    'prediction': prediction
                    }
        return JsonResponse(response)

