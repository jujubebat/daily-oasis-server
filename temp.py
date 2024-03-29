'''
def scheduler():
    #with transaction.atomic():
    print("로직 실행@@@@@@@@@@@@")

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
            quest = User_Activity.objects.select_for_update().create(user_num_id=user_id, activity_num_id=activity_jacard_data_sorted_3.iloc[i]).save()
    return 0


def test(request):
    User_Activity.objects.all().delete()  # 기존 엑티비티 추천목록 삭제
    with transaction.atomic():
        a=scheduler()
        print("테스트 함수에서 실행")
        print(a)
        return render(request, 'test.html',{})
'''

'''
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
'''

class FinishQuest(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request):
        # 퀘스트 완료 처리
        quest_num = request.query_params['quest_num']  #쿼리셋으로 받은 퀘스트 번호
        quest = User_Activity.objects.filter(pk=quest_num)#get에서 filter로 바꿈
        i=1
        # 유저가 보유한 퀘스트이면서 완료되지 않은 퀘스트일 경우만
        if (quest.get().user_num_id == request.user.id and quest.get().questDone == False):
            print("Dfsfdf")
            quest.update(questDone=True)

            now = datetime.datetime.now()
            now_utc = now.replace(tzinfo=timezone.utc)
            now_local = now_utc.astimezone()

            quest.update(doneTime=now_local)

            activity = Activity.objects.get(pk = quest.get().activity_num_id)
            #보상 업데이트(x테스트 해야함)
            newUser = UpdateLevel(request, False, isAlienate(activity))
            newTitle= UpdateTitle(request)
            newCharacterImage = UpdateCharacter(request)

            user_serializer = UserSerializer(newUser)
            title_serializer = TitleSerializer(newTitle, many=True)
            newCharacterImage_serializer = CharacterImageSerializer(newCharacterImage)

            return Response({"UpdateUser": user_serializer.data, "NewTitle": title_serializer.data, "NewCharacterImage": newCharacterImage_serializer.data })
        return Response(status=status.HTTP_400_BAD_REQUEST) #유저가 보유한 퀘스트가 아니거나 이미 완료한 퀘스트면 400리턴


'''
#취향별 엑티비티 리스트 제공
class ActivityListByPreference(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request):
        request_tag = []
        '''
for tag_num in request.query_params['tag']:
    n = tag_num
    a=1
'''

request_tag = [6, 7, 8]
activity_list = []
activity_items = Activity.objects.filter()
for activity_item in activity_items:
    #print(activity_item.num)
    activity_preference_items = Activity_Preference.objects.filter(activity_num_id=activity_item.num)
    activity_tag = []
    for activity_preference_item in activity_preference_items:
        activity_tag.append(activity_preference_item.preference_num_id)
    intersection = set([])
    intersection = set(request_tag).intersection(set(activity_tag))
    inter_list = list(intersection)
    inter_list.sort()
    if (request_tag == inter_list):
        #print('포함합니다.')
        activity_list.append(activity_item.num)

print('끝')

#activity_list=[1,2]
data = Activity.objects.filter(pk__in=activity_list)
serializer = ActivitySerializer(data, many=True)
print(data)
return Response({"ActivityListByPreference" : serializer.data})
'''

'''
class ActivityListByPreference(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):

        request_tag = [6, 7, 8]
        request_len = len(request_tag)
        activity_list = []
        activity_items = Activity.objects.filter()
        activity_nums = activity_items.values_list('num', flat=True)
        for activity_num in activity_nums:
            print(activity_num)
            preference_nums = Activity_Preference.objects.filter(activity_num_id=activity_num)
            items =preference_nums.filter(preference_num_id__in=request_tag).values_list('preference_num_id', flat=True)
            cnt = list(items)
            a=1
            if(request_tag==list(items)):
                print('포함합니다.')
                activity_list.append(activity_num)
'''


'''
#칭호 보상 관련 로직
#완료한 퀘스트 1, 3, 5, 7, 9, 12
def UpdateTitle(request, isReview):
    user_id = request.user.id
    user = User.objects.get(pk=user_id)
    # 완료된 퀘스트수 기반 칭호 부여
    DoneQuest = User_Activity.objects.filter(user_num_id=user_id, questDone=1) #유저가 완료한 퀘스트 목록
    DoneQuestNum = DoneQuest.count()

    title_nums =[]

    if DoneQuestNum == 1:
        newUserQuestTitle = User_Title.objects.create(user_num_id=user_id, title_num_id=1)
    elif DoneQuestNum == 3:
        newUserQuestTitle = User_Title.objects.create(user_num_id=user_id, title_num_id=2)
    elif DoneQuestNum == 5:
        newUserQuestTitle = User_Title.objects.create(user_num_id=user_id, title_num_id=3)
    elif DoneQuestNum == 7:
        newUserQuestTitle =User_Title.objects.create(user_num_id=user_id, title_num_id=4)
    elif DoneQuestNum == 9:
        newUserQuestTitle =User_Title.objects.create(user_num_id=user_id, title_num_id=5)
    else:
        newUserQuestTitle = None

    if  newUserQuestTitle != None:
        title_nums.append(newUserQuestTitle.title_num_id)

    #후기 작성수 기반 칭호 부여
    UsersReview = Review.objects.filter(user_num_id=user_id)
    UsersReviewNum = Review.objects.filter(user_num_id=user_id).count()
    print('UsersReviewNum')
    print(UsersReviewNum)

    if UsersReviewNum == 1:
        newUserReviewTitle = User_Title.objects.create(user_num_id=user_id, title_num_id=6)
    elif UsersReviewNum == 4:
        newUserReviewTitle = User_Title.objects.create(user_num_id=user_id, title_num_id=7)
    elif UsersReviewNum == 6:
        newUserReviewTitle = User_Title.objects.create(user_num_id=user_id, title_num_id=8)
    elif UsersReviewNum == 8:
        newUserReviewTitle = User_Title.objects.create(user_num_id=user_id, title_num_id=9)
    elif UsersReviewNum == 10:
        newUserReviewTitle = User_Title.objects.create(user_num_id=user_id, title_num_id=10)
    else:
        newUserReviewTitle = None

    if  newUserReviewTitle != None:
        title_nums.append(newUserReviewTitle.title_num_id)

    #레벨 기반 칭호 부여
    if user.level == 2:
        newUserlevelTitle = User_Title.objects.create(user_num_id=user_id, title_num_id=11)
    elif user.level == 7:
        newUserlevelTitle = User_Title.objects.create(user_num_id=user_id, title_num_id=12)
    elif user.level == 15:
        newUserlevelTitle = User_Title.objects.create(user_num_id=user_id, title_num_id=13)
    else:
        newUserlevelTitle = None

    if newUserlevelTitle != None:
        title_nums.append(newUserlevelTitle.title_num_id)

    newTitle = Title.objects.filter(pk__in=title_nums)

    #획득한 타이틀이 다수일 경우 쿼리셋 합쳐서 반환 https://wayhome25.github.io/django/2017/11/26/merge-queryset/
    return newTitle


'''