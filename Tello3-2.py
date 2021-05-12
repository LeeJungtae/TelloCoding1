"""
DJI Tello Edu Controller

Tello Edu 드론을 Python3 언어로 제어할 수 있게 해주는 모듈입니다.
Wi-Fi 통신을 위해 Tello Edu 드론에 연결을 해줘야 합니다.

=== 업데이트 기록 ===
2021.05.09 샘플 코드를 개조했음
2021.05.11 객체지향 개념을 도입했음(함수 -> 클래스)
"""


#############
# 전역 모듈 #
#############
import threading    # 스레드 생성을 위한 모듈 
import socket       # UDP 소켓 생성을 위한 모듈
import sys          # 시스템 명령어 사용을 위한 모듈
import time         # 시간 호출을 위한 모듈


############################################################
# Tello : 텔로 에듀 코드를 객체지향적 클래스로 재설계한 것 #
############################################################
class Tello(object):
    ####################
    # 클래스 전역 상수 #
    ####################
    LOCAL_HOST = ""
    LOCAL_PORT = 9000
    LOCAL_ADDRESS = (LOCAL_HOST, LOCAL_PORT)
    TELLO_HOST = "192.168.10.1"
    TELLO_PORT = 8889
    TELLO_ADDRESS = (TELLO_HOST, TELLO_PORT)
    ###############
    # 생성자 함수 #
    ###############
    def __init__(self):
        self.count = 0      # 명령어 입력 횟수
        self.sock = None    # UDP 소켓 변수
        self.recvThread = None  # 스레드 변수
        self.srcFileName = sys.argv[0]      # python 바로 뒤에 오는 첫 번째 매개변수는 소스파일 이름
        try:
            self.codeFileName = sys.argv[1]
        except IndexError:
            self.codeFileName = ""
    ####################################################
    # Tello.recv() : Tello 드론에게 신호를 보내는 함수 #
    ####################################################
    def recv(self):
        while True:
            try:
                data, server = self.sock.recvfrom(1518)
                print("OUT[{}] =>".format(self.count + 1), data.decode(encoding="utf-8"))
                self.count = self.count + 1
            except Exception:
                break
    #####################################################
    # start() : 프로그램의 시작 전에 초기 설정하는 함수 #
    #####################################################
    def start(self):
        """start() : 프로그램의 시작 전에 초기 설정하는 함수"""
        # UDP 소켓 생성
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(self.LOCAL_ADDRESS)
        # recv 함수 스레드 생성
        self.recvThread = threading.Thread(target = self.recv)
        self.recvThread.start()
        # 시작 메시지 출력
        print("###########################################################")
        print("#        Tello Edu Drone Python3 Control Program          #")
        print("# If you want to know about commands, use 'help' keyword. #")
        print("#       Enter 'end' command to quit this program.         #")
        print("#                         Enjoy~!                         #")
        print("###########################################################")
    ########################################
    # loop() : 인터프리터 방식의 반복 함수 #
    ########################################
    def loop(self):
        """loop() : 인터프리터 방식의 반복 함수"""
        # 명령 모드
        if self.codeFileName == "":
            while True:
                try:
                    # 명령어를 입력받는다, 데이터 타입은 str
                    msg = input("IN[{}] ".format(self.count))
                    # 만약 아무 명령어도 입력되지 않았다면
                    if msg == "":
                        # 다시 루프를 돌린다
                        continue
                    # end가 명령어에 포함되어 있다면
                    elif "end" in msg:
                        print("Bye Bye!")
                        self.sock.close()
                        break
                    # 그 외의 명령어는 Tello에게 전송한다
                    msg = msg.encode(encoding = "utf-8")    # UTF-8로 인코딩 변경
                    sent = self.sock.sendto(msg, self.TELLO_ADDRESS)  # 소켓을 통해 메시지를 보낸다
                # Ctrl + C를 눌러 종료했을 때
                except KeyboardInterrupt:
                    # 입력된 키를 보여주면서
                    print("\n<Ctrl + C> Entered\n")
                    # 소켓을 종료시키고
                    self.sock.close()
                    # 루프를 빠져나간다
                    break
        # 파일 입력 모드
        else:
            inputFile = open(self.codeFileName, "r")     # 파일 객체 열기
            lines = inputFile.readlines()   # 명령어들을 리스트로 저장
            print("=== Inputed Command List ===")
            # 각 줄을 읽어온다
            for line in lines:
                line = line.rstrip()
                print("IN[{}] =>".format(self.count), line)
                # end 명령어를 입력하면 프로그램 종료
                if "end" in line:
                    print("Bye Bye!")
                    self.sock.close()
                    break
                # flip 명령어
                elif "flip" in line:
                    commands = line.split(" ")
                    if commands[1] == "1":
                        line = "flip f"
                    elif commands[1] == "2":
                        line = "flip b"
                    elif commands[1] == "3":
                        line = "flip l"
                    elif commands[1] == "4":
                        line = "flip r"
                line2 = line.encode(encoding = "utf-8")   # UTF-8로 인코딩 변경
                sent = self.sock.sendto(line2, self.TELLO_ADDRESS)  # 소켓을 통해 메시지를 보낸다
                if "takeoff" in line:
                    time.sleep(10)
                else:
                    time.sleep(4)
            inputFile.close()   # 파일 객체 닫기


##################################
# main() : Tello3-2.py의 메인 함수 #
##################################
def main():
    """main() : Tello3.py의 메인 함수"""
    tello = Tello()
    tello.start()
    tello.loop()


if __name__ == "__main__":
    main()