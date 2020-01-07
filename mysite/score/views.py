from django.shortcuts import render
from static_data import ddragon
dd = ddragon.ddragon()
import requests, json
 
#League of Legends searching
def score_view(request):
	return render(request, 'score/score_view.html')


def search_result(request):
	if request.method == "GET":
		summoner_name = request.GET.get('search_text')
		
		api_key = 'RGAPI-1806f2b5-9704-4b49-81f7-11394ed4c61d'
		summoner_exist = False
		sum_result = {}
		solo_tier = {}
		store_list = []
		game_list ={}
		game_list2 = []
		history_1 = {}
		history_2 = {}
		history_3 = {}
		
		
		nick_name = str(summoner_name)
		summoner_url = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + str(summoner_name)
		api_id = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + str(summoner_name) + '?api_key=' + api_key #닉네임으로 개인키검색
		r = requests.get(api_id)
		
		params = {'api_key': api_key}
		res = requests.get(summoner_url, params=params)
		
		if res.status_code == requests.codes.ok:                #결과값이 정상적으로 반환되었을때만 실행하도록 설정
			summoner_exist = True
			summoners_result = res.json()                        #response result change to json
			if summoners_result:
				sum_result['name'] = summoners_result['name']
				sum_result['level'] = summoners_result['summonerLevel']
				sum_result['profileIconId'] = summoners_result['profileIconId']
	
								
				tier_url = "https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/" + r.json()['id'] +'?api_key=' + api_key 
				summoner  = requests.get(tier_url)
				player_data = summoner.json()
								
				for solo in player_data:
					if solo['queueType'] == 'RANKED_SOLO_5x5':
						break;

				solo_tier['rank_type'] = 'solo 5:5'
				solo_tier['tier'] = solo['tier']
				solo_tier['rank'] = str(solo['rank'])
				solo_tier['points'] = str(solo['leaguePoints'])
				solo_tier['wins'] = solo['wins']
				solo_tier['losses'] = solo['losses']
			

		
				
		
			match_url = "https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/" + r.json()['accountId'] +'?api_key=' + api_key
			match = requests.get(match_url)
			match_data = match.json()
			
			history = match_data["matches"] # my game history
			first = history[0]  #fisrt of it
			
			gameID_1 = first['gameId']  #the game ID
			match_data = "https://kr.api.riotgames.com/lol/match/v4/matches/" + str(gameID_1) + "?api_key=" + api_key #gameId로 검색
			match_data1 = requests.get(match_data)
			match_data2 = match_data1.json()
			match_data3 = match_data2['participantIdentities']
			participants = match_data2['participants']
			
			for summoner in match_data3:
				if summoner['player']['summonerName'] == nick_name:
					break;
			participantId = summoner['participantId'] #searching if nick_name

			for my_history in participants:
				if my_history['participantId'] == participantId: # get gamedata with participantID
					break;
					
				
					
			championId1 = my_history['championId'] 
			spell1_1 = my_history['spell1Id']
			spell1_2 = my_history['spell2Id']
		
			
			history_1['spell1Id'] = str(dd.getSummoner(spell1_1).image)
			history_1['spell2Id'] = str(dd.getSummoner(spell1_2).image)
			
			stat = my_history['stats']
			result_game = stat['win']
			if result_game == True:   #rue is win, false is lose
				result1 = "Win!"
			else:
				result1 = "Lose"
			
			history_1['result'] = result1

			history_1['kill'] = stat['kills']
			history_1['death'] = stat['deaths']
			history_1['assist'] = stat['assists']
			
			history_1['champion_img'] =str((dd.getChampion(championId1).image))
			
	
	
		
	
	
			second = history[1]
			gameID_2 = second['gameId']  #그 게임의 gameId

			match_data = "https://kr.api.riotgames.com/lol/match/v4/matches/" + str(gameID_2) + "?api_key=" + api_key #gameId로 검색
			match_data1 = requests.get(match_data)
			match_data2 = match_data1.json()
			match_data3 = match_data2['participantIdentities']
			participants = match_data2['participants']
			
			for summoner in match_data3:
				if summoner['player']['summonerName'] == nick_name:
					break;
			participantId = summoner['participantId'] 
			for my_history in participants:
				if my_history['participantId'] == participantId: 
					break;
					
									
			championId2 = my_history['championId'] 
			spell2_1 = my_history['spell1Id']
			spell2_2 = my_history['spell2Id']
			
			history_2['spell1Id'] = str(dd.getSummoner(spell2_1).image)
			history_2['spell2Id'] = str(dd.getSummoner(spell2_2).image)
			
			stat = my_history['stats']
			result_game = stat['win']
			if result_game == True:  
				result2 = "Win!"
			else:
				result2 = "Lose"
			
			history_2['result'] = result2

			history_2['kill'] = stat['kills']
			history_2['death'] = stat['deaths']
			history_2['assist'] = stat['assists']
			
			history_2['champion_img'] =str((dd.getChampion(championId2).image))
			
			
			
									
	
			third = history[2]
			gameID_3 = third['gameId'] 

			match_data = "https://kr.api.riotgames.com/lol/match/v4/matches/" + str(gameID_3) + "?api_key=" + api_key #gameId로 검색
			match_data1 = requests.get(match_data)
			match_data2 = match_data1.json()
			match_data3 = match_data2['participantIdentities']
			participants = match_data2['participants']
			
			for summoner in match_data3:
				if summoner['player']['summonerName'] == nick_name:
					break;
			participantId = summoner['participantId'] 
			for my_history in participants:
				if my_history['participantId'] == participantId:
					break;
					
									
			championId3 = my_history['championId'] 
			spell3_1 = my_history['spell1Id']
			spell3_2 = my_history['spell2Id']
			
			history_3['spell1Id'] = str(dd.getSummoner(spell3_1).image)
			history_3['spell2Id'] = str(dd.getSummoner(spell3_2).image)
			
			stat = my_history['stats']
			result_game = stat['win']
			if result_game == True:  
				result2 = "Win!"
			else:
				result2 = "Lose"
			
			history_3['result'] = result2

			history_3['kill'] = stat['kills']
			history_3['death'] = stat['deaths']
			history_3['assist'] = stat['assists']
			
			history_3['champion_img'] =str((dd.getChampion(championId3).image))
			

			
			nick_name = str(summoner_name)
			
		return render (request, 'score/search_result.html', {'summoner_exist': summoner_exist, 'summoners_result': sum_result, 'solo_tier': solo_tier, 'history_1' : history_1, 'history_2' : history_2, 'history_3' : history_3})
#return to the html template
