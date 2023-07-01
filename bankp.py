import prob
import PySimpleGUI as sg
import pandas as pd
import matplotlib.pyplot as plotter

class AddFrame:
    def __init__(self):
         # AddFrame 레이아웃 설정
        layout = [[sg.Text('정보처리기사 문제 은행')],
                  [sg.Combo(['전과목', '소프트웨어 설계', '소프트웨어 개발', '데이터베이스 구축',
                             '프로그래밍 언어 활용', '정보시스템 구축 관리'],
                            default_value='과목 선택', key='-sub-', size=(50))],
                  [sg.Button('문제 추출', size=(10)), sg.Button("종료", size=(8))]]  
        self.addWin = sg.Window('정보처리기사 문제은행', layout, margins=(300, 200))     # 윈도우 변수 설정


    def Run_addF(self, loop_num, pracmaker):
        while True:
            event, values = self.addWin.read()
            # '종료' 버튼 또는 우측 상단 x 버튼 누르면 프로그램 종료
            if event == '종료' or event == sg.WINDOW_CLOSED:
                self.addWin.close()
                break

            # 과목 선택에 따라 넘기는 인덱스 번호 달라짐
            if values['-sub-'] == '전과목':
                subject = 0
            elif values['-sub-'] == '소프트웨어 설계':
                subject = 1
            elif values['-sub-'] == '소프트웨어 개발':
                subject = 2
            elif values['-sub-'] == '데이터베이스 구축':
                subject = 3
            elif values['-sub-'] == '프로그래밍 언어 활용':
                subject = 4
            elif values['-sub-'] == '정보시스템 구축 관리':
                subject = 5


            # 문제 추출 시작
            if event == '문제 추출':
                pracmaker.add_Prob(subject)

                self.mainF = MainFrame()
                self.addWin.close()
                self.mainF.loop_Win(values['-sub-'], loop_num, pracmaker)


class EndFrame():
    def __init__(self):
          # EndFrame 레이아웃 설정
        layout = [[sg.Button('문제 더 풀기'), sg.Button('종료')]]

        self.EndWin = sg.Window('정보처리기사 문제은행', layout, margins=(300, 200))  # 윈도우 변수 설정

    def Run_EndF(self, loop_num, pracmaker):
        while True:
            event, values = self.EndWin.read()
            # '문제 더 풀기' 버튼 눌렀을 때
            if event == '문제 더 풀기':
                self.EndWin.close()
                addF = AddFrame()
                loop_num += 1
                addF.Run_addF(loop_num, pracmaker)
                break

            # '종료' 버튼 또는 우측 상단 x 버튼 누르면 프로그램 종료
            elif event == '종료' or sg.WINDOW_CLOSED:
                self.EndWin.close()
                break


class MainFrame():
    def Win_layout(self, subject, num, proc, a_list):
        # MainFrame 레이아웃 설정
        layout = [[sg.Text(num), sg.VSeparator(), sg.Text(subject)],
                  [sg.Text(proc, size=(70, None))],
                  [sg.Button('1'), sg.Text(a_list[0])],
                  [sg.Button('2'), sg.Text(a_list[1])],
                  [sg.Button('3'), sg.Text(a_list[2])],
                  [sg.Button('4'), sg.Text(a_list[3])],
                  [sg.Button('정답'), sg.Button('정답률'), sg.Button('다음 문제')]]

        self.MainWin = sg.Window('정보처리기사 문제은행', layout, margins=(300, 200))  # 윈도우 변수 설정

    def Run_mainF(self, df, num, c_ans, ch_per):
        while True:
            event, values = self.MainWin.read()
            # 다음 문제 넘어가기
            if event == sg.WINDOW_CLOSED or event == '다음 문제':
                self.MainWin.close()
                break

            # 정답, 오답 팝업 출력
            if c_ans == '1':
                if event == '1':
                    sg.popup("정답")
                elif event == '2' or event == '3' or event == '4':
                    sg.popup("오답")
            elif c_ans == '2':
                if event == '2':
                    sg.popup("정답")
                elif event == '1' or event == '3' or event == '4':
                    sg.popup("오답")
            elif c_ans == '3':
                if event == '3':
                    sg.popup("정답")
                elif event == '2' or event == '1' or event == '4':
                    sg.popup("오답")
            elif c_ans == '4':
                if event == '4':
                    sg.popup("정답")
                elif event == '2' or event == '3' or event == '1':
                    sg.popup("오답")

            # 정답 버튼 누르기
            if event == '정답':
                sg.popup(c_ans + '번', title='정답')

            # 정답률 나타내기
            if event == '정답률':
                pieLabel = '1', '2', '3', '4'
                populationShare = ch_per

                figureObject, axesObject = plotter.subplots()

                axesObject.pie(populationShare,
                               labels=pieLabel,
                               autopct="%.1f",
                               startangle=90)

                plotter.show()

    def loop_Win(self, subject, loop_num, pracmaker):

        path = pracmaker.name + '.xlsx'
        df = pd.read_excel(path)
        # 엑셀 파일의 하단 20문제 출력
        for i in range(0 + (loop_num * 20), 20 + (loop_num * 20)):
            num = i + 1
            proc = df['문제'][i]
            proc = proc.replace('#', '\n')
            proc = proc.replace('\\n', '\n')
            proc = proc.replace('],', '],\n')
            c_ans = str(df['정답'][i])
            a_list = [(df['보기1'][i]), (df['보기2'][i]), (df['보기3'][i]), (df['보기4'][i])]
            ch_per = [(df['선택률1'][i]), (df['선택률2'][i]), (df['선택률3'][i]), (df['선택률4'][i])]

            self.Win_layout(subject, num, proc, a_list)  # MainFrame 레이아웃 만듦
            self.Run_mainF(df, num, c_ans, ch_per)  # MainFrame 윈도우 실행

        EndF = EndFrame()
        EndF.Run_EndF(loop_num, pracmaker)  # 20문제 다 출력하면 EndFrame 실행


class StartFrame():
    def __init__(self):
        # StartFrame 레이아웃 설정
        layout = [[sg.Text('정보처리기사 문제 은행')],
                  [sg.Input('이름 입력 (공백X, 한/영, 8글자 이내)', size=(50), key='-name-')],
                  [sg.Combo(['전과목', '소프트웨어 설계', '소프트웨어 개발', '데이터베이스 구축',
                             '프로그래밍 언어 활용', '정보시스템 구축 관리'],
                            default_value='과목 선택', key='-sub-', size=(50))],
                  [sg.Button('문제 추출', size=(10)), sg.Button("종료", size=(8))]] 

        self.window1 = sg.Window("정보처리기사 문제은행", layout, margins=(300, 200))  # 윈도우 변수 설정

    def Run_StartF(self):
        while True:
            event, values = self.window1.read()
            # 과목 선택에 따라 넘기는 인덱스 번호 달라짐

            # '종료' 버튼 또는 우측 상단 x 버튼 누르면 프로그램 종료            
            if event == '종료' or event == sg.WINDOW_CLOSED:
                self.window1.close()
                break
            elif values['-sub-'] == '전과목':
                subject = 0
            elif values['-sub-'] == '소프트웨어 설계':
                subject = 1
            elif values['-sub-'] == '소프트웨어 개발':
                subject = 2
            elif values['-sub-'] == '데이터베이스 구축':
                subject = 3
            elif values['-sub-'] == '프로그래밍 언어 활용':
                subject = 4
            elif values['-sub-'] == '정보시스템 구축 관리':
                subject = 5

            if event == '문제 추출':
                # 공백, 특수문자, 8글자 초과 할 경우 프로그램 진행 X
                if values['-name-'].isalpha() == False or len(values['-name-']) > 9:
                    sg.popup("공백X, 한/영, 8글자 이내로만 입력이 가능합니다.")

                # 문제 추출 시작
                elif event == '문제 추출':
                    self.pracmaker = prob.Prob()
                    self.pracmaker.prob_Extraction(values['-name-'], subject)
                    self.window1.close()
                    self.mainF = MainFrame()
                    loop_num = 0
                    self.mainF.loop_Win(values['-sub-'], loop_num, self.pracmaker)  # MainFrame 실행


program = StartFrame()
program.Run_StartF()