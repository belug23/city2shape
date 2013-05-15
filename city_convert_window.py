#!/usr/bin/python
# -*- coding: utf-8 -*-

# rename.py

import wx
import os

from city_converter import CityConverter

class CityToShape(wx.Frame):

    def __init__(self, parent, title):
        super(CityToShape, self).__init__(parent, title=title,
            size=(325, 205))
            
        self.InitUI()
        self.Centre()
        self.Show()     

    def InitUI(self):

        panel = wx.Panel(self)
        sizer = wx.GridBagSizer(6, 4)

        #File opener
        textFile = wx.StaticText(panel, label="City file")
        sizer.Add(textFile, pos=(0, 0), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=5)

        self.tcFile = wx.TextCtrl(panel)
        sizer.Add(self.tcFile, pos=(1, 0), span=(1, 4),
            flag=wx.EXPAND|wx.LEFT, border=5)


        buttonOpen = wx.Button(panel, label="Open", size=(90, 28))
        sizer.Add(buttonOpen, pos=(1, 4), flag=wx.RIGHT, border=5)
        buttonOpen.Bind(wx.EVT_BUTTON, self.OnOpen)

        #position
        textPosition = wx.StaticText(panel, label="Position (x,y)")
        sizer.Add(textPosition, pos=(2, 0), flag=wx.LEFT|wx.BOTTOM, border=5)

        self.tcX = wx.TextCtrl(panel)
        sizer.Add(self.tcX, pos=(3, 0), span=(1, 3),
            flag=wx.LEFT, border=5)
        self.tcX.ChangeValue('0')


        self.tcY = wx.TextCtrl(panel)
        sizer.Add(self.tcY, pos=(3, 3), span=(1, 3),
            flag=wx.RIGHT, border=5)
        self.tcY.ChangeValue('0')


        buttonConvert = wx.Button(panel, label="Convert", size=(90, 28))
        buttonClose = wx.Button(panel, label="Close", size=(90, 28))
        sizer.Add(buttonConvert, pos=(5, 3))
        sizer.Add(buttonClose, pos=(5, 4), flag=wx.RIGHT|wx.BOTTOM, border=5)

        buttonConvert.Bind(wx.EVT_BUTTON, self.OnConvert)
        buttonClose.Bind(wx.EVT_BUTTON, self.OnClose)

        panel.SetSizerAndFit(sizer)

    def OnOpen(self, event):
        self.dirname = ''
        dlg = wx.FileDialog(self, "Choose a City file", self.dirname,"", "City map file|*.sgs", wx.OPEN)
        if dlg.ShowModal()==wx.ID_OK:
            self.filename=dlg.GetFilename()
            self.dirname=dlg.GetDirectory()
            filepath = "%s%s%s" % (self.dirname, os.sep, self.filename)
            self.tcFile.ChangeValue(filepath)
        dlg.Destroy()
    
    def OnConvert(self, event):
        if self.tcFile.IsEmpty() or self.tcX.IsEmpty() or self.tcY.IsEmpty():
            dial = wx.MessageDialog(None, 'Error please fill all fields', 'Error',
                wx.OK | wx.ICON_ERROR)
            dial.ShowModal()
            return

        try:
            posX = float(self.tcX.GetValue())
            posY = float(self.tcY.GetValue())
        except Exception:
            dial = wx.MessageDialog(None, 'Error the positions must be numbers', 'Error',
                wx.OK | wx.ICON_ERROR)
            dial.ShowModal()

        city_converter = CityConverter(self.dirname, self.filename, {'x':posX, 'y': posY})
        if city_converter.convert():
            self.tcFile.ChangeValue('')
            self.tcX.SetValue('0')
            self.tcY.SetValue('0')
            dial = wx.MessageDialog(None, 'Convertion successful', 'Success',
                wx.OK)
            dial.ShowModal()

        else:
            dial = wx.MessageDialog(None, 'There was an error while parsing the file', 'Error',
                wx.OK | wx.ICON_ERROR)
            dial.ShowModal()

    def OnClose(self, event):

        self.Destroy()



if __name__ == '__main__':
  
    app = wx.App()
    CityToShape(None, title='City to Shape')
    app.MainLoop()