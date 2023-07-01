import prob

filename = 'qbank.xlsx'                                   # 읽어올 엑셀 파일 지정
filename2 = "endxl.xlsx"                                    # 추출한 엑셀파일 저장 위치 #  "C:\\Users\\LIL\\Desktop\\vscode\\endxl.xlsx" 
pe = prob.Prob(filename, filename2)                   # prob클래스에서 입력 엑셀, 출력 엑셀 경로 지정
pe.prob_Extraction()                                        # 20문제 랜덤 추출(시드값은 UNIX time)x