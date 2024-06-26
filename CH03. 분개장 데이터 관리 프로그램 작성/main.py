# main.py

from journal_ledger import ledger_category, ledger_client

def main():
    while True:
        print("실행하고자 하는 항목을 선택하세요: ")
        print("1: 계정별원장 출력")
        print("2: 거래처원장 출력")
        print("exit: 프로그램 종료")
        input_data = input("실행하고자 하는 항목을 선택 >>> ")

        if input_data == "1":
            journal_name = input("분개장 파일명을 입력하세요(default: 분개장_샘플.xlsx): ")
            if journal_name == "":
                journal_name = "분개장_샘플.xlsx"
            print(f"분개장 파일명: {journal_name}")

            file_name = input("출력할 파일명을 입력하세요(default: 계정별원장_main.xlsx): ")
            if file_name == "":
                file_name = "계정별원장_main.xlsx"
            print(f"출력 파일명: {file_name}")

            ledger_category(journal_name, file_name)
            print(f"{file_name} 파일 생성이 완료되었습니다.\n\n")

        elif input_data == "2":
            journal_name = input("분개장 파일명을 입력하세요(default: 분개장_샘플.xlsx): ")
            if journal_name == "":
                journal_name = "분개장_샘플.xlsx"
            print(f"분개장 파일명: {journal_name}")

            file_name = input("출력할 파일명을 입력하세요(default: 거래처원장_main.xlsx): ")
            if file_name == "":
                file_name = "거래처원장_main.xlsx"
            print(f"출력 파일명: {file_name}")

            ledger_client(journal_name, file_name)
            print(f"{file_name} 파일 생성이 완료되었습니다.\n\n")

        elif input_data == "":
            continue

        elif input_data == "exit":
            print("프로그램 종료")
            return
        
        else:
            print("프로그램 종료")
            return

if __name__ == "__main__":
    main()