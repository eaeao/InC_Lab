from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from inc.evaluation.models import EvaluationQuestion


class ErrorAnalysisResult(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(EvaluationQuestion)
    code = models.TextField(default="")
    type = models.TextField(default="")
    msg = models.TextField(default="")
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "1. 제출된 오류분석(ErrorAnalysisResult)"

    def __str__(self):
        return '[%d] %s:%s > %s' % (self.id, self.user, self.question, self.type)

errorsanalysis_errors = [
    {'unit':"기본",'type':"SystemExit",'msg':'오류 구분: 기본\n시스템 종료 - 시스템이 종료되었습니다. 확인해 보세요.\n%s'},
    {'unit':"기본",'type':"KeyboardInterrupt",'msg':'오류 구분: 기본\n인터럽트 - 인터럽트가 발생되었습니다.\n%s'},
    {'unit':"기본",'type':"GeneratorExit",'msg':'오류 구분: 기본\nGenerator 종료 - generator 또는 coroutine가 닫혔습니다.\n%s'},
    {'unit':"구문오류",'type':"SyntaxError",'msg':'오류 구분: 구문\n문법 및 단어 오류 - 오타가 있는지 누락된 문자가 있는지 확인하세요.\n%s'},
    {'unit':"구문오류",'type':"IndentationError",'msg':'오류 구분: 구문\n들여쓰기 오류 - 들여쓰기가 잘못되었습니다.\n%s'},
    {'unit':"구문오류",'type':"TabError",'msg':'오류 구분: 구문\n탭 오류 - 들여쓰기된 코드들의 간격이 일정하지 않습니다.\n%s'},
    {'unit':"문법오류",'type':"AssertionError",'msg':'오류 구분: 문법\n진술 오류 - assert 문 실패입니다.\n%s'},
    {'unit':"문법오류",'type':"AttributeError",'msg':'오류 구분: 문법\n속성 오류 - 속성 참조나 할당에 실패하였습니다.\n%s'},
    {'unit':"문법오류",'type':"ImportError",'msg':'오류 구분: 문법\n가져오기 오류 - 가져올 수 있는 이름을 찾을 수 없습니다.\n%s'},
    {'unit':"문법오류",'type':"LookupError",'msg':'오류 구분: 문법\n색인 오류 - 키 또는 인덱스 매핑이 잘못되었습니다.\n%s'},
    {'unit':"문법오류",'type':"IndexError",'msg':'오류 구분: 문법\n인덱스 오류 - 인덱스 범위를 벗어났거나 값이 없습니다.\n%s'},
    {'unit':"문법오류",'type':"KeyError",'msg':'오류 구분: 문법\n키 오류 - 딕셔너리(사전)에 매핑키가 존재하지 않습니다.\n%s'},
    {'unit':"문법오류",'type':"NameError",'msg':'오류 구분: 문법\n이름 오류 - 로컬 또는 전역 이름을 찾을 수 없습니다. 이름을 선언해 주세요.\n%s'},
    {'unit':"문법오류",'type':"UnboundLocalError",'msg':'오류 구분: 문법\n로컨 연결 오류 - 로컬 변수가 있지만, 값과 변수가 연결되지 않았습니다. 연결해 주세요. %s'},
    {'unit':"문법오류",'type':"TypeError",'msg':'오류 구분: 문법\n타입 오류 - 명령어의 기능이 부적절하게 선언되었습니다. 해당 명령어의 유형에 맞게 수정해 주세요.\n%s'},
    {'unit':"문법오류",'type':"ValueError",'msg':'오류 구분: 문법\n값 오류 - 기능은 올바르지만, 부적절한 값이 입력되었습니다. 값을 수정해 주세요.\n%s'},
    {'unit':"문법오류",'type':"UnicodeError",'msg':'오류 구분: 문법\n유니코드 오류 - 유니코드와 관련하여 인코딩이나 디코딩에 오류가 발생하였습니다.\n%s'},
    {'unit':"문법오류",'type':"UnicodeDecodeError",'msg':'오류 구분: 문법\n디코드 오류 - 유니코드에서 디코딩 중에 오류가 발생하였습니다.\n%s'},
    {'unit':"문법오류",'type':"UnicodeEncodeError",'msg':'오류 구분: 문법\n인코드 오류 - 유니코드로 인코딩 중에 오류가 발생하였습니다.\n%s'},
    {'unit':"문법오류",'type':"UnicodeTranslateError",'msg':'오류 구분: 문법\n번역 오류 - 변역하는 동안 오류가 발생하였습니다.\n%s'},
    {'unit':"논리오류",'type':"ArithmeticError",'msg':'오류 구분: 논리\n연산 오류 - 다양한 연산 과정 중 오류가 발생하였습니다. 연산자를 확인해 주세요.\n%s'},
    {'unit':"논리오류",'type':"FloatingPointError",'msg':'오류 구분: 논리\n부동소수점 오류 - 부동 소수점 연산 실패. 부동소수점을 확인해 주세요.\n%s'},
    {'unit':"논리오류",'type':"OverflowError",'msg':'오류 구분: 논리\n범위초과 오류 - 보여질 결과의 크기가 너무 커서 표현할 수가 없습니다. 한계를 정해주세요.\n%s'},
    {'unit':"논리오류",'type':"ZeroDivisionError",'msg':'오류 구분: 논리\n0 나누기 오류 - 0으로는 나눌 수가 없습니다. 해당 부분을 수정해 주세요.\n%s'},
    {'unit':"논리오류",'type':"EOFError",'msg':'오류 구분: 논리\nEOF 오류 - 데이터를 모두 읽지 않고 중간의 문장을 건너뛰어 끝문장을 처리하였습니다. 중간의 문장을 처리해 갈 수 있도록 수정하세요.\n%s'},
    {'unit':"논리오류",'type':"ReferenceError",'msg':'오류 구분: 논리\n참조 오류 - 참조에 대한 예외가 발생하였습니다. 예외 상황을 제거해 주세요.\n%s'},
    {'unit':"논리오류",'type':"RuntimeError",'msg':'오류 구분: 논리\n실행시간 오류 - 연관된 값에 대해서 잘못된 부분이 있습니다. 확인해 보세요.\n%s'},
    {'unit':"논리오류",'type':"NotImplementedError",'msg':'오류 구분: 논리\n비실행 오류 - 메소드를 오버라이드하는 파생 클래스가 필요합니다.\n%s'},
    {'unit':"논리오류",'type':"RecursionError",'msg':'오류 구분: 논리\n반복 오류 - 사용하신 재귀함수의 최대 재귀 횟수를 오버하였습니다. 한계를 설정해 주세요.\n%s'},
    {'unit':"기타오류",'type':"StopIteration",'msg':'오류 구분: 기타\n반복 정지 - __next의 __() 반복자에 의해 생성되는 항목이 더 이상 없습니다.\n%s'},
    {'unit':"기타오류",'type':"StopAsyncIteration",'msg':'오류 구분: 기타\n비동기화 - __anext__()의 방법으로 비동기 반복자를 오브젝트화하면 반복을 중지.\n%s'},
    {'unit':"기타오류",'type':"BufferError",'msg':'오류 구분: 기타\n버퍼 오류 - 버퍼 관련 작업을 수행할 수 없습니다.\n%s'},
    {'unit':"기타오류",'type':"MemoryError",'msg':'오류 구분: 기타\n메모리 오류 - 메모리가 부족합니다.\n%s'},
    {'unit':"기타오류",'type':"SystemError",'msg':'오류 구분: 기타\n시스템 오류 - 인터프리터 내부에서 오류가 발생하였습니다.\n%s'},
    {'unit':"기타오류",'type':"OSError",'msg':'오류 구분: 기타\nOS 오류 - 시스템 기능적 오류입니다.\n%s'},
    {'unit':"기타오류",'type':"BlockingIOError",'msg':'오류 구분: 기타\nBlockingIOError - Raised when an operation would block on an object (e.g. socket) set for non-blocking operation.\n%s'},
    {'unit':"기타오류",'type':"ChildProcessError",'msg':'오류 구분: 기타\nChildProcessError - Raised when an operation on a child process failed.\n%s'},
    {'unit':"기타오류",'type':"ConnectionError",'msg':'오류 구분: 기타\nConnectionError - A base class for connection-related issues.\n%s'},
    {'unit':"기타오류",'type':"BrokenPipeError",'msg':'오류 구분: 기타\nBrokenPipeError - Raised when trying to write on a pipe while the other end has been closed, or trying to write on a socket which has been shutdown for writing.\n%s'},
    {'unit':"기타오류",'type':"ConnectionAbortedError",'msg':'오류 구분: 기타\nConnectionAbortedError - Raised when a connection attempt is aborted by the peer.\n%s'},
    {'unit':"기타오류",'type':"ConnectionRefusedError",'msg':'오류 구분: 기타\nConnectionRefusedError - Raised when a connection attempt is refused by the peer.\n%s'},
    {'unit':"기타오류",'type':"ConnectionResetError",'msg':'오류 구분: 기타\nConnectionResetError - Raised when a connection is reset by the peer.\n%s'},
    {'unit':"기타오류",'type':"FileExistsError",'msg':'오류 구분: 기타\nFileExistsError - Raised when trying to create a file or directory which already exists.\n%s'},
    {'unit':"기타오류",'type':"FileNotFoundError",'msg':'오류 구분: 기타\nFileNotFoundError - Raised when a file or directory is requested but doesn’t exist.\n%s'},
    {'unit':"기타오류",'type':"InterruptedError",'msg':'오류 구분: 기타\nInterruptedError - Raised when a system call is interrupted by an incoming signal.\n%s'},
    {'unit':"기타오류",'type':"IsADirectoryError",'msg':'오류 구분: 기타\nIsADirectoryError - Raised when a file operation (such as os.remove()) is requested on a directory.\n%s'},
    {'unit':"기타오류",'type':"NotADirectoryError",'msg':'오류 구분: 기타\nNotADirectoryError - Raised when a directory operation (such as os.listdir()) is requested on something which is not a directory.\n%s'},
    {'unit':"기타오류",'type':"PermissionError",'msg':'오류 구분: 기타\nPermissionError - Raised when trying to run an operation without the adequate access rights.\n%s'},
    {'unit':"기타오류",'type':"ProcessLookupError",'msg':'오류 구분: 기타\nProcessLookupError - Raised when a given process doesn’t exist.\n%s'},
    {'unit':"기타오류",'type':"TimeoutError",'msg':'오류 구분: 기타\nTimeoutError - Raised when a system function timed out at the system level.\n%s'},
    {'unit':"오류없음",'type':"Success",'msg':'오류없음'}
]