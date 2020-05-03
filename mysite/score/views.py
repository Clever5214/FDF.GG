from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from static_data import ddragon
import requests, json
dd = ddragon.ddragon() #Third party App
api_key = 'RGAPI-c89a8014-b033-4e9c-be43-f9c2579dc98a' #Type your API KEY here

rune_dic = { 8100 : "https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/7200_Domination.png", 
8112 : "https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/Domination/Electrocute/Electrocute.png",
8124 : "https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/Domination/Predator/Predator.png", 
8128: "https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/Domination/DarkHarvest/DarkHarvest.png",
9923: "https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/Domination/HailOfBlades/HailOfBlades.png", 
8300: "https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/7203_Whimsy.png",
8351: "https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/Inspiration/GlacialAugment/GlacialAugment.png",
8360: "https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/Inspiration/UnsealedSpellbook/UnsealedSpellbook.png",
8358: "https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/Inspiration/MasterKey/MasterKey.png",
8000: "https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/7201_Precision.png",
8005: "https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/Precision/PressTheAttack/PressTheAttack.png",
8008: "https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/Precision/LethalTempo/LethalTempoTemp.png",
8021: "https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/Precision/FleetFootwork/FleetFootwork.png",
8010: "https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/Precision/Conqueror/Conqueror.png",
8400: "https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/7204_Resolve.png",
8437: "https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/Resolve/GraspOfTheUndying/GraspOfTheUndying.png",
8439: "https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/Resolve/VeteranAftershock/VeteranAftershock.png",
8465: "https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/Resolve/Guardian/Guardian.png",
8200: "https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/7202_Sorcery.png",
8214: "https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/Sorcery/SummonAery/SummonAery.png",
8229: "https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/Sorcery/ArcaneComet/ArcaneComet.png",
8230: "https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/Sorcery/PhaseRush/PhaseRush.png"}
 
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
				kal_data[i]['game_id'] = game_id #{% static 'images/fdf.ico' %}
				kal_data[i]['main_rune'] = rune_dic[detail['perk0']]
				kal_data[i]['sub_rune'] = rune_dic[detail['perkSubStyle']]
				kal_data[i]['champid'] = str(dd.getChampion(stat['championId']).image)
				kal_data[i]['spell_1'] = str(dd.getSummoner(stat['spell1Id']).image)
				kal_data[i]['spell_2'] = str(dd.getSummoner(stat['spell2Id']).image)
				kal_data[i]['kill'] = detail['kills']
				kal_data[i]['death'] = detail['deaths']
				kal_data[i]['assist'] = detail['assists']
				kal_data[i]['kda'] = round((kal_data[i]['kill'] + kal_data[i]['assist']) / kal_data[i]['death'] , 2)
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

		red_data = {}  #Dictonary of more_data
		blue_data = {}
		i=0

		for more in participant[0:5] :
			more_detail = more['stats']
			list = {i:{'id' : more['participantId']}}
			red_data.update(list)
			red_data[i]['nick_name'] = game_json['participantIdentities'][i]['player']['summonerName']
			red_data[i]['champ_lev'] = more_detail['champLevel']
			red_data[i]['champid'] = str(dd.getChampion(more['championId']).image) 
			red_data[i]['spell_1'] = str(dd.getSummoner(more['spell1Id']).image)
			red_data[i]['spell_2'] = str(dd.getSummoner(more['spell2Id']).image)
			red_data[i]['kill'] = more_detail['kills']
			red_data[i]['death'] = more_detail['deaths']
			red_data[i]['assist'] = more_detail['assists']
			red_data[i]['kda'] = round((red_data[i]['kill'] + red_data[i]['assist']) / red_data[i]['death'] , 2)
			red_data[i]['main_rune'] = rune_dic[more_detail['perk0']]
			red_data[i]['sub_rune'] = rune_dic[more_detail['perkSubStyle']]
			#http://ddragon.leagueoflegends.com/cdn/10.9.1/img/item/1001.png
			
			for j in range(6):
				tempt_item = 'item' + str(j)
				red_data[i][j] = "http://ddragon.leagueoflegends.com/cdn/10.9.1/img/item/"+ str(more_detail[tempt_item]) + ".png"

			i = i + 1


		for more in participant[5:] :
			more_detail = more['stats']
			list = {i:{'id' : more['participantId']}}
			blue_data.update(list)
			blue_data[i]['nick_name'] = game_json['participantIdentities'][i]['player']['summonerName']
			blue_data[i]['champ_lev'] = more_detail['champLevel']
			blue_data[i]['champid'] = str(dd.getChampion(more['championId']).image) 
			blue_data[i]['spell_1'] = str(dd.getSummoner(more['spell1Id']).image)
			blue_data[i]['spell_2'] = str(dd.getSummoner(more['spell2Id']).image)
			blue_data[i]['kill'] = more_detail['kills']
			blue_data[i]['death'] = more_detail['deaths']
			blue_data[i]['assist'] = more_detail['assists']
			blue_data[i]['kda'] = round((blue_data[i]['kill'] + blue_data[i]['assist']) / blue_data[i]['death'] , 2)
			blue_data[i]['main_rune'] = rune_dic[more_detail['perk0']]
			blue_data[i]['sub_rune'] = rune_dic[more_detail['perkSubStyle']]
			#http://ddragon.leagueoflegends.com/cdn/10.9.1/img/item/1001.png
			
			for j in range(6):
				tempt_item = 'item' + str(j)
				blue_data[i][j] = "http://ddragon.leagueoflegends.com/cdn/10.9.1/img/item/"+ str(more_detail[tempt_item]) + ".png"

			i = i + 1
		

		return render(request, 'score/more.html', {'red' : red_data, 'blue' : blue_data});

		
		

	else:
		a = "False!"
		return render(request, 'score/more.html', {'a' : a});
		

