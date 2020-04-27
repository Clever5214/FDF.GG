from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from static_data import ddragon

import requests, json
dd = ddragon.ddragon() #Third party App

api_key = 'RGAPI-ea965008-59c2-487e-925b-3b21085eae7d' #Type your API KEY here
 
#League of Legends 전적검색
def score_view(request):
	return render(request, 'score/score_view.html')


def search_result(request):
	if request.method == "GET":
		summoner_name = request.GET.get('search_text')
	
		summoner_exist = False
		kal_data = {}  #dictonary of summoner important data
		sum_result = {}
		
		
		summoner_url = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + str(summoner_name)
		api_id = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + str(summoner_name) + '?api_key=' + api_key #닉네임으로 개인키검색
		r = requests.get(api_id)
		
		params = {'api_key': api_key}
		res = requests.get(summoner_url, params=params)
		
		if res.status_code == requests.codes.ok:                #결과값이 정상적으로 반환되었을때만 실행하도록 설정
			summoner_exist = True
			summoners_result = res.json()                        #response 값을 json 형태로 변환시키는 함수
			sum_result['name'] = summoners_result['name']
			sum_result['level'] = summoners_result['summonerLevel']
			
			kal_url = 'https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/' + r.json()['accountId'] +'?queue=450' + '&api_key=' + api_key
			kal_tempt = requests.get(kal_url)
			kal_json = kal_tempt.json()
			sum_result['kal_total'] = kal_json['totalGames']
			
			for i in range(5):  #one loop, one game
				game_id = kal_json['matches'][i]['gameId']
				list = {i:{'game_list' : game_id}}
				kal_data.update(list)
				game_url = "https://kr.api.riotgames.com/lol/match/v4/matches/" + str(kal_data[i]['game_list']) + "?api_key=" + api_key
				game_tempt = requests.get(game_url)
				game_json = game_tempt.json()
				parti_id = game_json['participantIdentities']
				for summoner in parti_id :
					if summoner['player']['accountId'] == r.json()['accountId']:
						break;
						
				kal_data[i]['participantId'] = summoner['participantId']
				participant = game_json['participants']
				for stat in participant :
					if stat['participantId'] == kal_data[i]['participantId']:
						break;
						
				detail = stat['stats']
				kal_data[i]['game_id'] = game_id
				kal_data[i]['champid'] = str(dd.getChampion(stat['championId']).image)
				kal_data[i]['spell_1'] = str(dd.getSummoner(stat['spell1Id']).image)
				kal_data[i]['spell_2'] = str(dd.getSummoner(stat['spell2Id']).image)
				kal_data[i]['champ_lev'] = detail['champLevel']
				kal_data[i]['kill'] = detail['kills']
				kal_data[i]['death'] = detail['deaths']
				kal_data[i]['assist'] = detail['assists']
				kal_data[i]['win'] = detail['win']
				
				
		return render (request, 'score/search_result.html', {'sum_result': sum_result, 'kal_data' : kal_data});


	
	else:
		return render(request, 'score/more.html')

@csrf_exempt #about serurity 
def more(request):
	if request.method == 'POST':
		gameId = request.POST.get('gameid', None)
		game_url = 'https://kr.api.riotgames.com/lol/match/v4/matches/' + gameId + '?api_key=' + api_key
		game_tempt = requests.get(game_url)
		game_json = game_tempt.json()
		participant = game_json['participants']

		more_data = {}  #Dictonary of more_data
		i=0

		for more in participant :
			more_detail = more['stats']
			list = {i:{'id' : more['participantId']}}
			more_data.update(list)
			more_data[i]['nick_name'] = game_json['participantIdentities'][i]['player']['summonerName']
			more_data[i]['champid'] = str(dd.getChampion(more['championId']).image) 
			more_data[i]['spell_1'] = str(dd.getSummoner(more['spell1Id']).image)
			more_data[i]['spell_2'] = str(dd.getSummoner(more['spell2Id']).image)
			more_data[i]['kill'] = more_detail['kills']
			more_data[i]['death'] = more_detail['deaths']
			more_data[i]['assist'] = more_detail['assists']
			more_data[i]['main_rune'] = more_detail['perk0']
			more_data[i]['sub_rune'] = more_detail['perkSubStyle']
			
			for j in range(6):
				tempt_item = 'item' + str(j)
				more_data[i][j] = more_detail[tempt_item]

			i = i + 1
		

		return render(request, 'score/more.html', {'a' : more_data});

	else:
		a = "False!"
		return render(request, 'score/more.html', {'a' : a});
		

