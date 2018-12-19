# from pykeyboard import *
# from pymouse import *
# import time
# class TapRecord(PyKeyboardEvent):
#     def __init__(self):
#         PyKeyboardEvent.__init__(self)
#
#     def tap(self, keycode, character, press):
#         print(time.time(), keycode, character, press)
#
# class Clickonacci(PyMouseEvent):
#     def __init__(self):
#
#         PyMouseEvent.__init__(self)
#
#     def click(self, x, y, button, press):
#
#         print(time.time(), button, press)
#
# c = Clickonacci()
# t = TapRecord()
# # t.run()
# c.run()


# k = PyKeyboard()

# k.type_string('杀毒防御')  # 我靠不能输入中文啊。。。
# k.press_key('H')  # 模拟键盘按H键
# k.release_key('H')  # 模拟键盘松开H键
# k.tap_key('H')  # 模拟点击H键
#
# k.tap_key('H', n=2, interval=5)  # 模拟点击H键，2次，每次间隔5秒
# k.tap_key(k.function_keys[5])  # 点击功能键F5

#组合键模拟
#例如同时按alt+tab键盘
# k.press_key(k.alt_key)  # 按住alt键
# k.tap_key(k.tab_key)  # 点击tab键
# k.release_key(k.alt_key)  # 松开alt键

# #
# from win32gui import *
#
# titles = list()
#
# #
# def foo(hwnd, mouse):
#     # 去掉下面这句就所有都输出了，但是我不需要那么多
#     if IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd):
#         titles.append(GetWindowText(hwnd))
#
#
# EnumWindows(foo, 0)
# lt = [t for t in titles if t]
# lt.sort()
# for t in lt:
#     print(t)
#
#
# import win32gui
# import win32con
# import win32api
#
#
# name = r'C:\Program Files (x86)\Notepad++\notepad++.exe'
#
# handle = win32gui.FindWindow(None,name)
#
# print(handle)


import pyautogui
screenWidth, screenHeight = pyautogui.size()
pyautogui.moveTo(screenWidth / 2, screenHeight / 2)



pyautogui.typewrite('Hello world!', interval=0.25)
# pyautogui.alert('这个消息弹窗是文字+OK按钮')
#
# pyautogui.confirm('这个消息弹窗是文字+OK+Cancel按钮')
#
# pyautogui.prompt('这个消息弹窗是让用户输入字符串，单击OK')
#
# import pyautogui
# print('Press Ctrl-C to quit')
# try:
#     while True:
#         x, y = pyautogui.position()
#         positionStr = 'X: {} Y: {}'.format(*[str(x).rjust(4) for x in [x, y]])
#         print(positionStr, end='')
#         print('\b' * len(positionStr), end='', flush=True)
# except KeyboardInterrupt:
#     print('\n')