from PyQt5 import QtCore, QtGui, QtWidgets
from .MessageBubble import MessageDelegate, MessageModel

class RecordButton(QtWidgets.QPushButton):
    """
    -----------------------------------------------------------------------------------
    Lớp RecordButton :
    
        Kế thừ từ lớp QPushButton, tham khảo tại: https://doc.qt.io/qt-5/qpushbutton.html
        Được cấu hình lại để đại diện cho chức năng thu âm
    -----------------------------------------------------------------------------------
    """
    def __init__(self, *args, **kwargs):
        super(RecordButton, self).__init__(*args, **kwargs)
        self.setGeometry(QtCore.QRect(10, 460, 41, 41))
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.setMouseTracking(True)
        self.setToolTipDuration(1500)
        self.setStyleSheet("QPushButton{\n"
                                        "background: none;\n"
                                        "border:none;\n"
                                        "border-radius:20%\n"
                                        "}\n"
                                        "QPushButton:hover{\n"
                                        "background:rgb(166, 200, 255)\n"
                                        "}")
        self.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Interface/Icon/recordVoice.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setIcon(icon)
        self.setIconSize(QtCore.QSize(40, 40))
        self.setObjectName("recordButton")

###################################################################
###################################################################

class SendButton(QtWidgets.QPushButton):
    """
    -----------------------------------------------------------------------------------
    Lớp SendButton :
    
        Kế thừ từ lớp QPushButton, tham khảo tại: https://doc.qt.io/qt-5/qpushbutton.html
        Được cấu hình lại để đại diện cho chức năng gửi đi tin nhắn
    -----------------------------------------------------------------------------------
    """

    def __init__(self, *args, **kwargs):
        super(SendButton, self).__init__(*args, **kwargs)
        self.setGeometry(QtCore.QRect(380, 460, 41, 41))
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.setMouseTracking(True)
        self.setToolTipDuration(1500)
        self.setStyleSheet("QPushButton{\n"
                                      "background: none;\n"
                                      "border:none;\n"
                                      "border-radius:20%\n"
                                      "}\n"
                                      "QPushButton:Hover{\n"
                                      "background: rgb(160, 196, 255);\n"
                                      "}")
        self.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Interface/Icon/send.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setIcon(icon)
        self.setIconSize(QtCore.QSize(55, 53))
        self.setObjectName("sendButton")

######################################################################
######################################################################

class MessageEditor(QtWidgets.QLineEdit):
    """
    -----------------------------------------------------------------------------------
    Lớp SendButton :
    
        Kế thừ từ lớp QLineEdit, tham khảo tại: https://doc.qt.io/qt-5/qlineedit.html
        Được cấu hình lại để đại diện cho khung nhập tin nhắn
    -----------------------------------------------------------------------------------
    """

    def __init__(self, *args, **kwargs):
        super(MessageEditor, self).__init__(*args, **kwargs)
        self.setGeometry(QtCore.QRect(60, 460, 311, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.setFont(font)
        self.setStyleSheet("QLineEdit{\n"
                                   "border: none;\n"
                                   "border-radius: 20px;\n"
                                   "corlor: rgb(209, 209, 209);\n"
                                   "background: rgb(208, 208, 208);\n"
                                   "padding-top:7%;\n"
                                   "padding-left:10px;\n"
                                   "font-size:10pt;\n"
                                   "padding-right:15px;\n"
                                   "padding-bottom:6%\n"
                                   "}")
        self.setLocale(QtCore.QLocale(QtCore.QLocale.Vietnamese, QtCore.QLocale.Vietnam))
        self.setPlaceholderText("Type here !")
        self.setObjectName("chatBox") 

##########################################################################
##########################################################################

class MessageView(QtWidgets.QListView):
    """
    -----------------------------------------------------------------------------------
    Lớp MessageView :
    
        Kế thừ từ lớp QListView, tham khảo tại: https://doc.qt.io/qt-5/qlistview.html
        Được cấu hình lại để làm khung hiển thị các tin nhắn của cuộc trò chuyện 
    -----------------------------------------------------------------------------------
    """

    def __init__(self, *args, **kwargs):
        super(MessageView, self).__init__(*args, *kwargs)
        self.setGeometry(QtCore.QRect(10, 10, 410, 430))
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.setAutoFillBackground(True)
        self.setStyleSheet("QListView{\n"
                                      "border:none;\n"
                                      "background:white;\n"
                                      "}")
        self.setObjectName("MessageView")
        self.setItemDelegate(MessageDelegate())
        self.MessageList = MessageModel()
        self.setModel(self.MessageList)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

if __name__=='__main__':
    print(RecordButton.__doc__)