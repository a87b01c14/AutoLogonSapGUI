import subprocess
import time
import pyautogui
from threading import Thread
import sys
import os
import json
import wx
import wx.lib.agw.aquabutton

ctrl = 'ctrl'
if sys.platform == "darwin":
    ctrl = 'command'
    # from AppKit import NSWorkspace, NSWindowList, NSWindow
    from Quartz import (
        CGWindowListCopyWindowInfo,
        kCGWindowListOptionOnScreenOnly,
        kCGNullWindowID
    )
elif sys.platform == "win32":
    import win32gui

config = json.load(open("conf.json"))


def is_application_active(launch):
    if sys.platform == "darwin":
        # curr_app = NSWorkspace.sharedWorkspace().frontmostApplication()
        # curr_pid = NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationProcessIdentifier']
        # curr_app_name = curr_app.localizedName()
        windows = CGWindowListCopyWindowInfo(kCGWindowListOptionOnScreenOnly, kCGNullWindowID)
        for window in windows:
            # pid = window['kCGWindowOwnerPID']
            # windowNumber = window['kCGWindowNumber']
            owner = window['kCGWindowOwnerName']
            geometry = window['kCGWindowBounds']
            # windowTitle = window.get('kCGWindowName', u'Unknown')
            if owner == config.get('ApplicationName', 'SAPGUI'):
                # 第一次启动的时候，需要等待窗口全屏，加载完毕
                if launch:
                    return geometry['X'] == 0
                else:
                    return True
            # print("%s - %s (PID: %d, WID: %d): %s" % (ownerName, windowTitle, pid, windowNumber, geometry))

    elif sys.platform == "win32":
        windows = pyautogui.getWindowsWithTitle(config.get('ApplicationName', 'SAP Logon'))
        if len(windows) > 0:
            if launch:
                return windows[0].left == 0
            else:
                windows[0].activate()
                return True


# 线程函数
def open_gui():
    if sys.platform == "darwin":
        subprocess.call(
            ["/usr/bin/open", "-W", "-n", "-a",
             config.get("ApplicationPath", "/Applications/SAP Clients/SAPGUI/SAPGUI.app")],
            timeout=10)
    elif sys.platform == "win32":
        os.system(config.get("ApplicationPath",
                             r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\SAP Front End\SAP Logon"))


def active_window():
    app_name = config.get('ApplicationName', 'SAPGUI')
    cmd = 'osascript -e \'activate application "{0}"\''.format(app_name)
    subprocess.call(cmd, shell=True)
    i = 0
    while i < 100:
        title = subprocess.check_output(['osascript', 'GetNameAndTitleOfActiveWindow.scpt'])
        if title.decode().strip() == config.get('WindowName', "SAP GUI for Java"):
            break
        else:
            pyautogui.hotkey([ctrl, '`'])
        i += 1


def login_gui(index):
    item = config.get("items")[index]
    if is_application_active(False):
        if sys.platform == "darwin":
            active_window()
        elif sys.platform == "win32":
            app_name = config.get('ApplicationName', 'SAP Logon')
            hwnd = win32gui.FindWindow(None, app_name)
            if hwnd:
                win32gui.SetForegroundWindow(hwnd)
    else:
        # 创建线程对象
        t = Thread(target=open_gui)
        # 启动线程
        t.start()
        for _ in range(10):
            time.sleep(1)
            if is_application_active(True):
                break

    pyautogui.press(['up'] * 50)
    if item.get("index", 0) > 1:
        pyautogui.press(['down'] * (item.get("index") - 1))
    pyautogui.press(['enter'], interval=2)
    pyautogui.press(['up'] * 3)
    pyautogui.hotkey(ctrl, 'a', interval=0.25)
    pyautogui.typewrite(item.get("client"))
    pyautogui.hotkey('tab', interval=0.25)
    pyautogui.typewrite(item.get("user"))
    pyautogui.hotkey('tab', interval=0.25)
    pyautogui.typewrite(item.get("password"), interval=0.01)
    pyautogui.press(['enter'])


class MyApp(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(800, 500))

        panel = wx.Panel(self)
        panel.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBack)

        # panel.SetBackgroundColour(wx.Colour(200, 200, 200))
        vbox = wx.BoxSizer(wx.VERTICAL)

        scroller = wx.ScrolledWindow(panel, -1)
        child_panel = wx.Panel(scroller)
        child_vbox = wx.BoxSizer(wx.VERTICAL)
        # 加载位图
        self.bg_bmp = wx.Bitmap("background.jpeg")
        bmp = wx.Image("sap.bmp", wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        font = wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        width = 300
        height = 80
        border = 5
        for i, item in enumerate(config.get("items")):
            sub_panel = wx.Panel(child_panel)
            sub_hbox = wx.BoxSizer(wx.HORIZONTAL)
            button = wx.lib.agw.aquabutton.AquaButton(sub_panel, label=item.get("title", None), id=i,
                                                      size=(width, height))

            button.SetFont(font)
            # button.SetSize(100, 50)
            sub_hbox.AddSpacer(250)
            sub_hbox.Add(button, 0, flag=wx.ALL | wx.EXPAND, border=border)
            sub_hbox.AddSpacer(250)
            button.Bind(event=wx.EVT_BUTTON, handler=self.on_button_click, source=button)
            child_vbox.Add(sub_panel, 0, flag=wx.ALL | wx.CENTER)
            sub_panel.SetSizerAndFit(sub_hbox)
            sub_hbox.Fit(child_panel)
        child_panel.SetSizerAndFit(child_vbox)
        child_vbox.Fit(panel)
        scroller.SetScrollbars(0, 1, 0, (height + border * 2) * len(config.get("items")))  # 是否横向|竖向滚动条，小于该长度时出现滚动条

        scroller.SetScrollRate(0, 20)  # 滚动速度
        vbox.Add(scroller, 1, flag=wx.ALL | wx.EXPAND, border=border)
        panel.SetSizer(vbox)

    def OnEraseBack(self, event):
        dc = event.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        dc.DrawBitmap(self.bg_bmp, 0, 0)

    def on_button_click(self, event):
        login_gui(event.Id)


if __name__ == '__main__':
    app = wx.App(redirect=False)
    MyApp(None, -1, "SAPGUI AUTO LOGON").Show(True)
    app.MainLoop()
