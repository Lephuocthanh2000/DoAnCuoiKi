if __name__=='__main__':
    try:
        from App import ChatApp
        ui = ChatApp()
        ui.show()
    except Exception:
        print('Đã xảy ra lỗi')