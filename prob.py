import pandas as pd
import sys
from time import time
from random import seed, sample

class Prob:
    def __init__(self):
        self.filename = 'qbank.xlsx'
        self.filename2 = 'exdata.xlsx'
        self.name = ""
        self.count = 0
        self.str = ['전과목', '소프트웨어 설계', '소프트웨어 개발', '데이터베이스 구축', '프로그래밍 언어 활용', '정보시스템 구축관리', '종료']
        self.list = ['번호', '문제', '보기1', '보기2', '보기3', '보기4', '정답', '선택률1', '선택률2', '선택률3', '선택률4', '자료']

    def prob_Extraction(self, name, subject):   # name -> str ; subject -> int
        # global input
        # subject 0 이면 전과목 1~5면 선택과목 else 종료
        self.name = name
        self.filename2 = name + '.xlsx'
        # self.name = input("name : ")                # 이름 입력
        seed(Prob.rand_Seed(self))                  # 랜덤 시드값
        #_________________________________________________________________________________________
        # print("__________문제은행___________")
        # for i in range(len(self.str)):
        #     print("(",i,")",". ",self.str[i], sep="")   # 문제은행 UI 형식
        #_________________________________________________________________________________________
        # input = int(input("input : "))              # 과목 입력
        df = pd.read_excel(self.filename, engine='openpyxl')    # 엑셀 파일 읽어 오기
        if subject       >= len(self.str) or subject < 0 or subject == len(self.str)-1: # 올바르지 않은 입력
            print("Exit")
            sys.exit()                              # 종료
        elif self.str[subject] == '전과목':           # subject이 전과목
            case = df[self.list]                    # case 데이터프레임(전과목)
            print(self.str[subject], "문제 저장")
        else :
            df1 = df[df['과목'] == self.str[subject]]       #소프트웨어 설계
            case = df1[self.list]                   # case 데이터프레임(선택과목)
            del df1
            print(self.str[subject], "문제 저장")
        #_________________________________________________________________________
        # case = case.sample(n = 20,random_state = subject + int(time()), replace=True) # UNIX시간
        # sample 함수를 구현
        randlist = []   # 무작위 문제 리스트
        if self.str[subject] == '전과목': # 전과목이면 case 인덱스를 0~499까지 지정
            case.index = list(range(0, 500))
            randlist = sample(range(0, 500), 20)    # 랜덤 인덱스 값 리스트에 저장(중복X)
        else:
            case.index = list(range(0, 100))        # 선택 과목이면 case 인덱스를 0~99까지 지정
            randlist = sample(range(0, 100), 20)    # 랜덤 인덱스 값 리스트에 저장(중복X)
        # 선택과목일 경우 번호로 지정, randint(1,100) 난수로 문제지정
        # 전과목일 경우 인덱스 값으로 지정 randint(0, 499) 난수로 문제지정
        #_____________________________________________________________________________
        case = case.loc[randlist]   # randlist를 인덱스로 20문제 case 데이터프레임 저장
        numlist = list(range(self.count + 1, self.count + 21))
        self.count += 20    # 문제가 20개 저장됨
        case['번호'] = numlist  # 번호 재지정(1~20) 이후는 20씩 더한 값으로 진행
        #------------------------------------------------------------------------
        for i in randlist:  # i 는 무작위로 저장한 문제의 인덱스
            if bool(case.loc[i].isnull().sum()) != True:    # 한 행에 NaN이 1개도 없으면
                case.at[i ,'문제'] = case['문제'][i] + '#' + case['자료'][i]
        # case 자료가 nan이 아니면 문제#자료 형식으로 문제에 저장
        case.drop(['자료'], axis=1, inplace=True) # 자료 열 삭제
        #-----------------------------------------------------------------------
        case.to_excel(self.filename2, index=False)  # 엑셀 저장
        del case, subject, randlist, numlist          # 변수 날리기
        # Prob.add_Prob(self)                         # 추가 문제 메소드
    
    def add_Prob(self, subject):
        seed(Prob.rand_Seed(self))                  # 시간 변화에 따라 시드값 재지정
        #_________________________________________________________________________
        # print("________추가문제(",str(self.count),")________", sep = "")
        # for i in range(len(self.str)):
        #     print("(",i,")",". ",self.str[i], sep="")
        # global input
        # input = int(input("input : "))
        #________________________________________________________________________
        df = pd.read_excel(self.filename, engine='openpyxl')
        if subject >= len(self.str) or subject < 0 or subject == len(self.str)-1:
            print("name :", self.name, "\ncount", str(self.count))
            print("Direction :", self.filename2)
            sys.exit()
        elif self.str[subject] == '전과목':
            case = df[self.list]
            print(self.str[subject], "문제 저장")
        else :
            df1 = df[df['과목'] == self.str[subject]]       # 과목별 데이터프레임
            case = df1[self.list]
            del df1
            print(self.str[subject], "문제 저장")
        #____________________________________________________________________________
        randlist = []
        if self.str[subject] == '전과목': # 전과목이면 case 인덱스를 0~499까지 지정
            case.index = list(range(0, 500))
            randlist = sample(range(0, 500), 20)    # 랜덤 인덱스 값 리스트에 저장
        else:
            case.index = list(range(0, 100))
            randlist = sample(range(0, 100), 20)
        # 선택과목일 경우 번호로 지정, randint(1,100) 난수로 문제지정
        # 전과목일 경우 인덱스 값으로 지정 randint(0, 499) 난수로 문제지정
        #_______________________________________________________________________________
        case = case.loc[randlist] 
        numlist = list(range(self.count + 1, self.count + 21))
        self.count += 20
        case['번호'] = numlist  # 무작위로 지정된 번호 재지정(1~20)
        #------------------------------------------------------------------------
        for i in randlist:
            if bool(case.loc[i].isnull().sum()) != True:
                case.at[i ,'문제'] = case['문제'][i] + '#' + case['자료'][i]
        case.drop(['자료'], axis=1, inplace=True) # 자료 열 삭제
        #------------------------------------------------------------------------
        dt = pd.read_excel(self.filename2, engine='openpyxl')   # 이어서 붙이려고 가져오는 거
        case = pd.concat([dt, case]) # 합치기
        case.to_excel(self.filename2, index=False) # 저장
        del case, subject, randlist, numlist          # 변수 날리기
        # Prob.add_Prob(self)                         # 다시 추가 문제 메소드

    def rand_Seed(self):        # 시드값(str)을 위한 숫자->한글 변환
        t = int(time())         # int로 변환
        list = []
        nums ='일이삼사오육칠팔구공'
        while t > 0:
            n, r = divmod(t, 10)        # n -> 10으로 나눈 몫 / r -> 10으로 나눈 나머지
            t = n                       
            list.append(nums[r-1])      # 리스트에 한글 형식으로 추가
        list.reverse()
        if ord('가') <= ord(self.name[0]) <= ord('힣'): # 첫글자가 한국어라면 시간을 한국어로 변환
            result = ''.join(s for s in list)           # 리스트를 문자열 변환
        else :                                          # 숫자나 영어면 시간을 문자열 변환
            result = str(t)

        return self.name + result