
match_url = "https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/" + r.json()['accountId'] +'?api_key=' + api_key
match = requests.get(match_url)
match_data = match.json()

history = match_data["matches"] # 나의 게임기록
first = history[0]  #기록 중에  첫번째
gameID = first['gameId']  #그 게임의 gameId

match_data = "https://kr.api.riotgames.com/lol/match/v4/matches/" + str(gameID) + "?api_key=" + api_key #gameId로 검색
match_data1 = requests.get(match_data)
match_data2 = match_data1.json()
match_data3 = match_data2['participantIdentities']
participants = match_data2['participants']

for summoner in match_data3:
    if summoner['player']['summonerName'] == nick_name:
        break;
participantId = summoner['participantId'] #닉네임으로 게임 참가번호 검색

for my_history in participants:
    if my_history['participantId'] == participantId: # 참가번호로 그 게임내 데이터 출력
        print(my_history)
        break;


championId = my_history['championId'] # 원하는 JSON값을 변수에 저장
spell1Id = my_history['spell1Id']
spell2Id = my_history['spell2Id']
stats = my_history['stats']
result_game = stats['win']
if result_game == True:   #win값이 True면 win 아니면 loose
    result = "Win!"
else:
    result = "Lose"

kill = stats['kills']
death = stats['deaths']
assist = stats['assists']


champion = (dd.getChampion(championId).name)
champ_img = "C:\\Users\\GIGABYTE\\Desktop\\img\\champ_img\\" + champion + ".gif" #turtle에 챔피언이미지 등록
screen.addshape(champ_img)
t1.left(180)
t1.forward(300)
t1.shape(champ_img)  #turtle의 모양을 champion이미지로 변경
t1.stamp()   #움직이고 찍기

t1.left(90)
t1.forward(600)
t1.write("Result: " + result + " Kill: "+ str(kill) + ", Death: " + str(death) +", Assist: " + str(assist), False, "right", ("",20))

item = ["item1", "item2", "item3", "item4", "item5", "item6"]
k = 1
for i in item:
    t1. forward(80)
    if stats.get (i):
        i = "items" + str(k)
        i = stats['item'+str(k)]
        item_img = "C:\\Users\\GIGABYTE\\Desktop\\img\\item_img\\" + str(i) + ".gif"
        screen.addshape(item_img)
        t1.shape(item_img)
        t1.stamp()    
    else:
        break