from django.contrib import admin
from django.urls import path, include
from main.views import index, newsfeed, new_feed, remove
from score.views import score_view, search_result

urlpatterns = [
    path('', index), #메인 페이지
    path('admin/', admin.site.urls), #어드민 페이지
	
    path('newsfeed/', newsfeed), #게시판
	path('post/', new_feed), #듀오 게시판 글 올리기
	path('newsfeed/<pk>/remove/', remove), #게시글 삭제
	
	path('score/', include('score.urls')), #score url 추가
	path('score_view/', score_view),       #검색창 메인 화면
    path('search_result', search_result),  #검색결과를 보여줄 화면
	
]
