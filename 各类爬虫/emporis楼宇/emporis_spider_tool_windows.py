import datetime

import wx
from multiprocessing import Process


class MyFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, -1, title="Spider", size=wx.Size(230, 200))
        # 设置头像
        self.SetIcon(wx.Icon(name='image.ico', type=wx.BITMAP_TYPE_ICO))
        panel = wx.Panel(self, -1)
        # 设置开始和停止按钮
        self.button_start = wx.Button(panel, wx.ID_ANY, '开始爬取', pos=(20, 50))
        self.Bind(wx.EVT_BUTTON, self.on_start, self.button_start)
        self.button_stop = wx.Button(panel, wx.ID_ANY, '停止爬取', pos=(100, 50))
        self.Bind(wx.EVT_BUTTON, self.on_stop, self.button_stop)
        self.button_stop.Disable()
        # 关闭提示
        self.Bind(wx.EVT_CLOSE, self.on_shut)

    def begin_spider(self, event):
        self.button_start.Disable()
        self.button_start.SetLabel('正在爬取...')
        self.button_stop.Enable()
        try:
            # 获取IP池
            path = 'ip.txt'  # 存放爬取ip的文档path
            targeturl = 'https://www.emporis.com'  # 验证ip有效性的指定url
            # self.getip(targeturl, path, event)
            # # 开始爬取
            # self.thread_start(event)
            message_box = wx.MessageDialog(None, u"工具爬取完毕！", style=wx.OK)
            choose_result = message_box.ShowModal()
            if choose_result == wx.ID_OK:
                message_box.Destroy()
                event.Skip()
            else:
                message_box.Destroy()
            self.button_start.Enable()
            self.button_start.SetLabel('开始爬取')
            self.button_stop.Disable()
        except Exception as es:
            message_box = wx.MessageDialog(None, u"工具运行异常：%s" % es, u"错误", style=wx.OK | wx.ICON_ERROR)
            choose_result = message_box.ShowModal()
            if choose_result == wx.ID_OK:
                message_box.Destroy()
                event.Skip()
            else:
                message_box.Destroy()
            self.button_start.Enable()
            self.button_start.SetLabel('开始爬取')
            self.button_stop.Disable()

    def on_start_continent(self, event):
        self.pro1 = Process(target=self.begin_spider, args=(event,), daemon=True)
        self.pro1.start()
        self.pro1.join()

    def on_start_country(self, event):
        self.pro2 = Process(target=self.begin_spider, args=(event,), daemon=True)
        self.pro2.start()
        self.pro2.join()

    def on_start_city(self, event):
        self.pro3 = Process(target=self.begin_spider, args=(event,), daemon=True)
        self.pro3.start()
        self.pro3.join()

    def on_stop(self, event):
        message_box = wx.MessageDialog(None, u"确定停止爬取", u"警告", style=wx.YES_NO | wx.ICON_WARNING)
        choose_result = message_box.ShowModal()
        if choose_result == wx.ID_YES:
            try:
                if hasattr(self, 'th1'):
                    stop_thread(self.th1)
                if self.thread_list1:
                    for thread1 in self.thread_list1:
                        stop_thread(thread1)
                    self.thread_list1 = []
                if self.thread_list2:
                    for thread2 in self.thread_list2:
                        stop_thread(thread2)
                    self.thread_list2 = []
            finally:
                self.value = 0
                self.button_start.Enable()
                self.button_start.SetLabel('开始爬取')
                self.button_stop.Disable()
            message_box.Destroy()
            event.Skip()

        else:
            message_box.Destroy()

    def on_shut(self, event):
        message_box = wx.MessageDialog(None, u"确定关闭工具", u"警告", style=wx.YES_NO | wx.ICON_WARNING)
        choose_result = message_box.ShowModal()
        if choose_result == wx.ID_YES:
            message_box.Destroy()
            event.Skip()
        else:
            message_box.Destroy()


class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame()
        frame.Center()
        frame.Show(True)
        return True


if __name__ == '__main__':
    app = MyApp()
    app.MainLoop()
