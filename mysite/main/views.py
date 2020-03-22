from django.shortcuts import render, redirect
from main.models import match

#메인 페이지
def index(request):
	return render(request, 'main/index.html')


#게시글 작성
def new_feed(request):
    if request.method == 'POST': # 폼이 전송되었을 때만 아래 코드를 실행
        new_post = match.objects.create(
            title = request.POST['title'],
            nick_name = request.POST['nick_name'],
            content = request.POST['content'],
			password=request.POST['password'],
        )
        
    return render(request, 'main/post.html')


#게시판 (게시글 확인)
def newsfeed(request):
	articles = match.objects.all()
	
	return render(request, 'main/newsfeed.html', {'articles': articles })


#Delete Post
def remove(request, pk):
	article = match.objects.get(pk=pk)
	
	if request.method == 'POST':
		if request.POST['password'] == article.password:
			article.delete()
			return redirect('/')
	return render(request, 'main/remove.html',  {'feed': article})


	
    #21 새벽/ 지금시도 할려고 했던것  / 닉네임을 받는 모델 하나 더 생성 / 게시글 비밀번호칸 추가(선호 라인같은것도 select형식으로)
	#24 게시글 삭제구현/ 닉네임 받는 history 모델 생성/ 연결은 아직