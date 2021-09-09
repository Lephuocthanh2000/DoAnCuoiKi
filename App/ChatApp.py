import threading
from PyQt5 import QtCore, QtGui, QtWidgets
from Interface.CustomedElementWidgets import RecordButton, SendButton, MessageEditor, MessageView
import sys
from Backend.Bot import Bi
from threading import Thread,  Timer
import time
class ChatApp(object):
    """
    Là lớp ứng dụng chatbot kiêm trợ lí ảo
    Bao gồm các chức năng:
        + show(): khởi chạy và hiển thị giao diện ứng dụng
        + close(): đóng ứng dụng
    """
    def __init__(self):
        self.__app = QtWidgets.QApplication(sys.argv)
        #ChatBot
        self.__bot=Bi()
        #Main Window
        self.__UI = QtWidgets.QMainWindow()
        self.__UI.setObjectName("ChatBot")
        self.__UI.resize(431, 518)
        self.__UI.setMaximumSize(QtCore.QSize(431, 518))
        self.__UI.setStyleSheet("QMainWindow{\n"
                                   "background:rgb(255, 255, 255);\n"
                                   "}")
        self.__centralwidget = QtWidgets.QWidget(self.__UI)
        self.__centralwidget.setObjectName("centralwidget")
        QtCore.QMetaObject.connectSlotsByName(self.__UI)
        self.__UI.setCentralWidget(self.__centralwidget)
        #Record button
        self.__recordButton = RecordButton(self.__centralwidget)
        self.__recordButton.pressed.connect(self.__send_user_message_from_micro)
        #Send button
        self.__sendButton = SendButton(self.__centralwidget)
        self.__sendButton.pressed.connect(self.__send_user_message_from_keyboard)
        #Message Editor
        self.__editMessage = MessageEditor(self.__centralwidget)
        self.__editMessage.returnPressed.connect(self.__send_user_message_from_keyboard)
        #Message View
        self.__MessageView = MessageView(self.__centralwidget)
        #Wlecome
        self.__sendBotMessage(self.__bot.multiprocess_speak('Xin chào, mình có thể giúp gì cho bạn'))

    
    #-----------------------------------------Method-------------------------------------------------#


    #Hiển thị app
    def show(self):
        self.__UI.show()
        self.__app.exec_()


    #Đóng app
    def close(self):
        self.__app.closeAllWindows()
    
        
    #Gửi tin nhắn nhập từ bán phím và gọi xử lí
    def __send_user_message_from_keyboard(self):
        request=self.__editMessage.text()
        self.__editMessage.setText('')
        self.__editMessage.setPlaceholderText('Chờ bi xử lí chút nhé')
        #self.editMessage.setDisabled(True)
        self.__MessageView.MessageList.addMessage('user',request )
        QtWidgets.QApplication.processEvents()
        self.__bot_processing(request)
        #thread=Thread(target=self.bot_processing,args=(self.editMessage.text(),))
        #thread.setDaemon(True)
        #thread.start()
        self.__editMessage.setPlaceholderText('')
        self.__MessageView.scrollToBottom()
        if 'tạm biệt bạn' == request.lower() or 'tạm biệt' == request.lower():
            self.close()
    

    #Thay đổi icon nút record báo là bot đang nghe
    def __on_listening(self):
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Interface/Icon/hear.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.__recordButton.setIcon(icon)


    #Thay dổi icon nút record báo là bot đã nghe xong
    def __has_listened(self):
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Interface/Icon/recordVoice.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.__recordButton.setIcon(icon)
    

    #Gửi tin nhắn dạng được từ micro và gọi xử lí
    def __send_user_message_from_micro(self):
        self.__editMessage.setDisabled(True)
        self.__editMessage.setPlaceholderText('Bi đang nghe bạn nói đấy')
        self.__on_listening()
        QtWidgets.QApplication.processEvents()
        request=self.__bot.listen()
        self.__has_listened()
        QtWidgets.QApplication.processEvents()
        self.__editMessage.setPlaceholderText('Chờ Bi xử lí chút nhé')
        self.__editMessage.setDisabled(False)
        self.__MessageView.MessageList.addMessage('user',request)
        QtWidgets.QApplication.processEvents()
        self.__bot_processing(request)
        self.__editMessage.setPlaceholderText('')
        #thread=Thread(target=self.bot_processing,args=(temp,))
        #thread.setDaemon(True)
        #thread.start()
        #########
        self.__MessageView.scrollToBottom()
        if 'tạm biệt bạn' == request.lower() or 'tạm biệt' == request.lower():
            self.close()


    #Gửi tin nhắn từ bot 
    def __sendBotMessage(self, message=''):
        self.__MessageView.MessageList.addMessage('bot', message)
        # self.MessageView.MessageList.addMessage('bot', MessageModel(QtGui.qt))
    

    #Gọi xử lí phía bot
    def __bot_processing(self,request):   
        try:
            self.__sendBotMessage(self.__bot.react_to(request))
        except Exception:
            self.__sendBotMessage(self.__bot.multiprocess_speak('Mình không hiểu bạn muốn gì'))


if __name__=='__main__':
    ui = ChatApp()
    ui.show()