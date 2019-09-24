from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
import pandas
from .serializers import UserSerializer, UserSerializerWithToken, ActivitySerializer
from .models import Activity, User_Preference, Preference, Activity_Preference, User_Activity, Title, User
from django.db import transaction
from django.db.models import F

class CurrentQuest(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request):
        items = User_Activity.objects.filter(user_num_id=request.user.id)
        list=[]
        for item in items:
            list.append(item.activity_num)
        data=Activity.objects.filter(pk__in=[list[0].num, list[1].num, list[2].num])
        serializer = ActivitySerializer(data, many=True)
        return Response({"CurrentQuest":serializer.data})


#데이터베이스로부터 데이터를 가져오고, 선언해둔 시리얼라이저를 통해 데이터를 직렬화해준다.
class ActivityList(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request):
        data = Activity.objects.all()
        serializer = ActivitySerializer(data, many=True)
        return Response({"ActivityList":serializer.data})

class DoneQuest(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request):
        data = User_Activity.objects.filter(user_num_id=request.user.id, done=1)
        serializer = ActivitySerializer(data, many=True)
        return Response({"DoneQuest":serializer.data})

class FinishQuest(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request):
        data = User_Activity.objects.filter(user_num_id=request.user.id, done=1)
        serializer = ActivitySerializer(data, many=True)
        return Response({"DoneQuest":serializer.data})


@api_view(['GET'])
def current_user(request):
    """
    Determine the current user by their token, and return their data
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

class UserList(APIView):
    """
    Create a new user. It's called 'UserList' because normally we'd have a get
    method here too, for retrieving a list of all User objects.
    """
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def scheduler():
    with transaction.atomic():
        print("로직 실행@@@@@@@@@@@@")
        User_Activity.objects.filter(done=0).delete()  #이전에 추천된 완료되지 않은 퀘스트 목록 삭제

        # 모든 유저에 대하여 모든 엑티비티의 자코드 유사도를 구하고 그중 상위 10개중에 3개를 추출하여 user_activity(quest)테이블에 넣어야한다.
        activity_jacard_shema = {'activity_num': [], 'Jacard_similarity': []}
        activity_jacard_data = pandas.DataFrame(activity_jacard_shema)  # activity, jacard 유사도 데이터 프레임 테이블

        user_items = User.objects.all()
        for user_item in user_items: #모든 user 튜플을 가져와서 하나씩 꺼낸다.
            i = 0
            user_id = user_item.id
            User_Preference_items = User_Preference.objects.filter(user_num_id=user_id)  #각 user들이 가지고 있는 preference 목록
            user_tags = []  #자카드 유사도를 구하기 위해 딕셔너리 형태로 preference를 정리해 놓음, 유저의 preference 목록임(preference의 name에 띄어쓰기가 있으면 안된다.)
            #ex) ['분위기있는' '야외의' '실내의' '신나는']
            for User_Preference_item in User_Preference_items:
                tag = Preference.objects.get(pk=User_Preference_item.preference_num_id)#user_preference 튜플의(item) preference 키를 이용하여 prefernce 튜플을 추출한후 preference의 이름을 tag에 저장
                user_tags.append(tag.name)  # 유저가 보유한 태그 딕셔너리에 preferene를 추가
            activity_items = Activity.objects.all()  # 모든 엑티비티를 가져와서
            for activity_item in activity_items:  # 하나씩 엑티비티의 태그와 유저의 태그에 대해 자카드 유사도를 계산한다.
                activity_tags = []
                items = Activity_Preference.objects.filter(activity_num_id=activity_item.num)  # 엑티비티가 가지고 있는 선호도 목록
                for item in items:
                    tag = Preference.objects.get(pk=item.preference_num_id)
                    activity_tags.append(tag.name)  # 엑티비티가 보유한 태그 딕셔너리
                union = set(user_tags).union(set(activity_tags))  # 합집합
                intersection = set(user_tags).intersection(set(activity_tags))  # 교집합합
                try:#태그가 없을 경우 len이 0이 되어 ZeroDivision 오류나서 예외처리해줌
                    Jacard_similarity = len(intersection) / len(union)  # 유저태그와 엑티비티태그의 자카드 유사도
                except(ZeroDivisionError):
                    Jacard_similarity=0
                # 엑티비티, 자카드 유사도
                activity_jacard_data.loc[i] = [activity_item.num, Jacard_similarity]  # 엑티비티 번호, 자카드 유사도 insert
                i += 1
            # print("자카드 유사도")
            # print(activity_jacard_data)
            activity_jacard_data_sorted = activity_jacard_data.sort_values(by=['Jacard_similarity'],ascending=False)  # 유저태그와 엑티비티태그에 대한 자카드유사도 계산후 오름차순정렬
            activity_jacard_data_sorted_10 = activity_jacard_data_sorted.head(10)  # 자카드 유사도순 상위 10개의 데이터프레임 추출
            activity_jacard_data_sorted_3 = activity_jacard_data_sorted_10.sample(n=3)  # 자카드 유사도순 상위 10개의 데이터프레임중 랜덤으로 3개의 데이터프레임 추출
            activity_jacard_data_sorted_3 = activity_jacard_data_sorted_3.reset_index(drop=True)  # 인덱스 0부터 시작하도록 초기화
            activity_jacard_data_sorted_3 = activity_jacard_data_sorted_3['activity_num']  # 엑티비티 속성만 추출
            print(user_id)
            print("번 유저에 대한 추천 데이터 3개")
            print(activity_jacard_data_sorted_3)
            print("포문 시작")
            for i in range(3):
                print("User_activity 인스턴스 생성")
                quest = User_Activity.objects.create(user_num_id=user_id, activity_num_id=activity_jacard_data_sorted_3.iloc[i]).save()
    return 0

def test(request):
    a=scheduler()
    print("테스트 함수에서 실행")
    print(a)
    return render(request, 'test.html',{})

#메모
#위치기반 추천기능 추가
#Tmap 지오코딩

#만들어야할 api 목록
#진행중인 퀘스트 목록
#완료 퀘스트 목록
#전체 엑티비티 퀘스트 목록
#퀘스트 완료 -> 레벨, 칭호 로직 반영
#댓글 기능 -> 레벨, 칭호, 로직 반영




# def scheduler():
#     #with transaction.atomic():
#     print("로직 실행@@@@@@@@@@@@")
#
#     # 모든 유저에 대하여 모든 엑티비티의 자코드 유사도를 구하고 그중 상위 10개중에 3개를 추출하여 user_activity(quest)테이블에 넣어야한다.
#     activity_jacard_shema = {'activity_num': [], 'Jacard_similarity': []}
#     activity_jacard_data = pandas.DataFrame(activity_jacard_shema)  # activity, jacard 유사도 데이터 프레임 테이블
#
#     user_items = User.objects.all()
#     for user_item in user_items: #모든 user 튜플을 가져와서 하나씩 꺼낸다.
#         i = 0
#         user_id = user_item.id
#         User_Preference_items = User_Preference.objects.filter(user_num_id=user_id)  #각 user들이 가지고 있는 preference 목록
#         user_tags = []  #자카드 유사도를 구하기 위해 딕셔너리 형태로 preference를 정리해 놓음, 유저의 preference 목록임(preference의 name에 띄어쓰기가 있으면 안된다.)
#         #ex) ['분위기있는' '야외의' '실내의' '신나는']
#         for User_Preference_item in User_Preference_items:
#             tag = Preference.objects.get(pk=User_Preference_item.preference_num_id)#user_preference 튜플의(item) preference 키를 이용하여 prefernce 튜플을 추출한후 preference의 이름을 tag에 저장
#             user_tags.append(tag.name)  # 유저가 보유한 태그 딕셔너리에 preferene를 추가
#         activity_items = Activity.objects.all()  # 모든 엑티비티를 가져와서
#         for activity_item in activity_items:  # 하나씩 엑티비티의 태그와 유저의 태그에 대해 자카드 유사도를 계산한다.
#             activity_tags = []
#             items = Activity_Preference.objects.filter(activity_num_id=activity_item.num)  # 엑티비티가 가지고 있는 선호도 목록
#             for item in items:
#                 tag = Preference.objects.get(pk=item.preference_num_id)
#                 activity_tags.append(tag.name)  # 엑티비티가 보유한 태그 딕셔너리
#             union = set(user_tags).union(set(activity_tags))  # 합집합
#             intersection = set(user_tags).intersection(set(activity_tags))  # 교집합합
#             try:#태그가 없을 경우 len이 0이 되어 ZeroDivision 오류나서 예외처리해줌
#                 Jacard_similarity = len(intersection) / len(union)  # 유저태그와 엑티비티태그의 자카드 유사도
#             except(ZeroDivisionError):
#                 Jacard_similarity=0
#             # 엑티비티, 자카드 유사도
#             activity_jacard_data.loc[i] = [activity_item.num, Jacard_similarity]  # 엑티비티 번호, 자카드 유사도 insert
#             i += 1
#         # print("자카드 유사도")
#         # print(activity_jacard_data)
#         activity_jacard_data_sorted = activity_jacard_data.sort_values(by=['Jacard_similarity'],ascending=False)  # 유저태그와 엑티비티태그에 대한 자카드유사도 계산후 오름차순정렬
#         activity_jacard_data_sorted_10 = activity_jacard_data_sorted.head(10)  # 자카드 유사도순 상위 10개의 데이터프레임 추출
#         activity_jacard_data_sorted_3 = activity_jacard_data_sorted_10.sample(n=3)  # 자카드 유사도순 상위 10개의 데이터프레임중 랜덤으로 3개의 데이터프레임 추출
#         activity_jacard_data_sorted_3 = activity_jacard_data_sorted_3.reset_index(drop=True)  # 인덱스 0부터 시작하도록 초기화
#         activity_jacard_data_sorted_3 = activity_jacard_data_sorted_3['activity_num']  # 엑티비티 속성만 추출
#         print(user_id)
#         print("번 유저에 대한 추천 데이터 3개")
#         print(activity_jacard_data_sorted_3)
#         print("포문 시작")
#         for i in range(3):
#             print("User_activity 인스턴스 생성")
#             quest = User_Activity.objects.select_for_update().create(user_num_id=user_id, activity_num_id=activity_jacard_data_sorted_3.iloc[i]).save()
#     return 0
#
#
# def test(request):
#     User_Activity.objects.all().delete()  # 기존 엑티비티 추천목록 삭제
#     with transaction.atomic():
#         a=scheduler()
#         print("테스트 함수에서 실행")
#         print(a)
#         return render(request, 'test.html',{})