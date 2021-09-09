from PyQt5 import QtCore, QtGui, QtWidgets
# from PyQt5.QtGui import

PADDING = QtCore.QMargins(10,10,110,20)
BACK_PADDING = QtCore.QMargins(0,0,100,10)
FONT=QtGui.QFont('Arial',10)
USER_TEXT=QtGui.QColor('white')
USER_BACK=QtGui.QColor('#217eff')
BOT_TEXT=QtGui.QColor('black')
BOT_BACK=QtGui.QColor('#c8d0e3')

class MessageDelegate(QtWidgets.QStyledItemDelegate): 
    """
    -----------------------------------------------------------------------------------
    Lớp MessageDelegate:
    
        - Kế thừa từ lớp QStyledItemDelegate, tham khảo tại: https://doc.qt.io/qt-5/qstyleditemdelegate.html 
        - QStyledItemDelegate là lớp trừu tượng được thư viện pyqt5 cung cấp dùng để hiển thị đối tượng trong model dữ liệu
          Cần implement lại cụ thể để phủ hợp với mục đích sử dụng
    -----------------------------------------------------------------------------------
    """

    def paint(self, painter, option, index):
        sender_name, Text=index.model().data(index, QtCore.Qt.DisplayRole)
        painter.setFont(QtGui.QFont(FONT))
        painter.setPen(QtCore.Qt.NoPen)
        if sender_name=='user':
            option.displayAlignment = QtCore.Qt.AlignRight
        if sender_name=='user':
            painter.setBrush(USER_BACK)
        elif sender_name=='bot':
            painter.setBrush(BOT_BACK)
        textrect=option.rect.marginsRemoved(PADDING)
        backrect=option.rect.marginsRemoved(BACK_PADDING)
        painter.drawRect(backrect)
        if sender_name=='user':
            painter.setPen(USER_TEXT)
        elif sender_name=='bot':
            painter.setPen(BOT_TEXT)
        painter.drawText(textrect,QtCore.Qt.TextWordWrap,Text,)
    def sizeHint(self, option, index):
        _, text = index.model().data(index, QtCore.Qt.DisplayRole)
        metrics = QtGui.QFontMetrics(FONT)
        rect = option.rect
        rect = metrics.boundingRect(rect, QtCore.Qt.TextWordWrap, text)
        rect = rect.marginsAdded(PADDING)
        return rect.size()


##################################################################

class MessageModel(QtCore.QAbstractListModel):
    """
    -----------------------------------------------------------------------------------
    Lớp MessageDelegate:
    
        - Kế thừa từ lớp QAbstractListModel, tham khảo tại: https://doc.qt.io/qt-5/qabstractlistmodel.html
        - QAbstractListModel là lớp trừu tượng được thư viện pyqt5 cung cấp dùng để lưu và xử lí dữ liệu của View
          Cần implement lại cụ thể để phủ hợp với mục đích sử dụng
    -----------------------------------------------------------------------------------
    """

    def __init__(self, *args, **kwargs):
        super(MessageModel, self).__init__(*args, **kwargs)
        self.Messages=[]
    def data(self, index, role):
        if (role == QtCore.Qt.DisplayRole):
            return self.Messages[index.row()]
    def rowCount(self, index):
        return len(self.Messages)
    def addMessage(self, sender_name, message):
        if message:
            self.Messages.append((sender_name, message))
        self.layoutChanged.emit()
    def count(self):
        return len(self.Messages)
 