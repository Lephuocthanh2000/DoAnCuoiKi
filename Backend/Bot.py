
from .TrainChatBot import TrainedChatBot
import speech_recognition as sr
import smtplib
from email.mime.text import MIMEText
import ctypes
import urllib
import urllib.request
import json
import pathlib
import webbrowser
import geocoder
import datetime
import youtube_search
import wikipedia
import time
import pyttsx3
from threading import Thread
import os

class Bi():
    """
    -----------------------------------------------------------------------------------------
    Lớp Bi:
        
        Thuộc tính gồm có:
            + brain: đối tượng lớp TrainedChatBot
            + talking_speed: tốc độ nói của bot
            + mouth: đối tượng lớp pyttsx3 (chuyển văn bản thành âm thanh)
            + ear: đối tượng lớp Recongnizer (chuyển âm thanh thành văn bản)
        Phương thức gồm có:
            + speak
            + multiprocess_speak
            + listen
            + send_mail
            + change_random_walpaper
            + search_google
            + wheather_forecast
            + play_youtube
            + define
            + get_time
            + get_date
            + react_to
            Gọi __doc__ của từng phương thức để xem chi tiết
    ---------------------------------------------------------------------------------------
    """
    def __init__(self):
        #ChatBot đã được huấn luyện
        self.brain=TrainedChatBot(name='Bi', read_only=True, 
                                  storage_adapter='chatterbot.storage.SQLStorageAdapter',
                                  database_uri='sqlite:///database.sqlite3',
                                  logic_adapters=['chatterbot.logic.MathematicalEvaluation',
                                                  'chatterbot.logic.BestMatch']
                                 )
        self.talking_speed=130
        #module pyttsx3 giúp chuyển văn bản thành âm thanh
        self.mouth = pyttsx3.init()
        voices=self.mouth.getProperty("voices")
        self.mouth.setProperty("voice",voices[1].id)
        self.mouth.setProperty('rate', self.talking_speed)
        #Lớp Regcognizer giúp chuyển âm thanh thành văn bản
        self.ear = sr.Recognizer()

    #-------------------------------------------------------------------------------------------
    def speak(self,text):
        """
        -----------------------------------------------------------------------------------
        Bi.speak(self,text):

        # Params: text
        # Chức năng: Phát ra âm thanh đoạn text
        # Trả về: void
        # exception: bỏ qua
        -----------------------------------------------------------------------------------
        """
        try:
            self.mouth.say(text)
            self.mouth.runAndWait()
        except Exception:
            pass
    #--------------------------------------------------------------------------------------------
    def multiprocess_speak(self,text):
        """
        -----------------------------------------------------------------------------------
        Bi.multiprocess_speak(self,text):

        # Params: text
        # Chức năng: khởi tạo một thread thực hiện method speak(text) 
        # Trả về: text
        -----------------------------------------------------------------------------------
        """
        thread=Thread(target=self.speak,args=(text,))
        thread.start()
        return text

    #--------------------------------------------------------------------------------------------
    def listen(self):
        """
        -----------------------------------------------------------------------------------
        Bi.listen(self):

        # Params: không có
        # Chức năng: chuyển đổi âm thanh từ micro thành text
        # Trả về: text
        # Exception: trả về chuổi rỗng
        -----------------------------------------------------------------------------------
        """
        with sr.Microphone() as source:
            print('listening')
            audio = self.ear.listen(source, phrase_time_limit=3.5)
            try:
                text = self.ear.recognize_google(audio, language="vi-VN")
                return text
            except Exception as e:
                return ''
   
    # Input: địa chỉ mail, tiêu đề, nội dung
    # Chức năng: gửi mail theo những thông số ở trên, nói kết quả thực hiện bằng phương thức speak
    # Output: thông báo kết quả thành công hay thất bại
    def send_email(self,destination,subject,content):
        msg = MIMEText(content)
        msg['Subject'] = subject
        msg['From'] = 'admin@example.com'
        msg['To'] = 'info@example.com'
        self.speak('Bạn chờ chút nhé')
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as mail:
                mail.ehlo()
                mail.starttls()
                mail.login('quang0002@gmail.com', '0917787421q')
                mail.sendmail('quang0002@gmail.com',destination, msg.as_string().encode('utf-8'))
                mail.close()
            return self.multiprocess_speak('Tôi đã gửi đi thành công rồi nhé')
        except Exception as e:
            return self.multiprocess_speak('Hình như có trục trặc gì đó, hãy kiểm tra và làm lại nhé')
    
    #--------------------------------------------------------------------------------------------
    def change_random_walpaper(self):
        """
        -----------------------------------------------------------------------------------
        Bi.change_random_walpaper(self):

        # Params: không có
        # Chức năng: thay đổi hình nền máy tính bằng một ảnh ngẫu nhiên lấy từ unsplash.com và đọc kết quả
        # Trả về: text thông báo kết quả
            + thành công: text='Mình đã đổi xong rồi đấy, bạn coi thử xem'
            + exception: text='Xin lỗi hiện tại mình không thể đổi được ảnh nền giúp bạn, một lát thử lại nhé'
        -----------------------------------------------------------------------------------
        """
        api_key = 'lTRwvyGb1vAmzbDCruvqzCR7hdFpa4HfG-gjNZkDbkc'
        url = 'https://api.unsplash.com/photos/random?client_id=' + api_key 
        self.speak('Ô kê, mất vài giây thôi')
        try:   
            f = urllib.request.urlopen(url)
            json_string = f.read()
            f.close()
            parsed_json = json.loads(json_string)
            photo = parsed_json['urls']['full']
            # Location where we download the image to.
            save_path=os.path.join(pathlib.Path(__file__).parent.absolute(),'Source\img.png')
            urllib.request.urlretrieve(photo, save_path)
            ctypes.windll.user32.SystemParametersInfoW(20,0,save_path,3)
            return self.multiprocess_speak('Mình đã đổi xong rồi đấy, bạn coi thử xem')
        except Exception as e:
            return self.multiprocess_speak('Xin lỗi hiện tại mình không thể đổi được ảnh nền giúp bạn, một lát thử lại nhé')

    
    #--------------------------------------------------------------------------------------------
    def search_google(self,serch_text):
        """
        -----------------------------------------------------------------------------------
        Bi.search_google(self, search_text):

        # Params: search_text là thông tin muốn tìm kiếm
        # Chức năng: tìm search_text trên google và mở trong tab mới trên google chrome
        # Trả về: text thông báo kết quả
            + thành công: text='Có rồi nhé'
            + exception: text='Xin lỗi hiện tại mình không gọi được cho chị gu gồ'
        -----------------------------------------------------------------------------------
        """
        url="https://www.google.com.tr/search?q={}".format(serch_text)
        self.speak('Đợi chút nha')
        try:
            webbrowser.register('chrome',None,webbrowser.BackgroundBrowser("C:\Program Files\Google\Chrome\Application\chrome.exe"))
            webbrowser.get('chrome').open_new_tab(url)
            return self.multiprocess_speak('Có rồi nhé')
        except Exception as e:
            return self.multiprocess_speak('Xin lỗi, hiện tại mình không gọi được cho chị gu gồ')
    
    #--------------------------------------------------------------------------------------------
    def wheather_forecast(self):
        """
        -----------------------------------------------------------------------------------
        Bi.wheather_forecast(self):

        # Params: không có
        # Chức năng: trả về thông tin thời tiết lấy từ openwheathermap.org (thông qua api) và đọc lên
        # Trả về: text thông báo kết quả
            + thành công: thông tin thời tiết lấy được
            + exception: text='Bạn ơi hiện tại mình không thể truy cập vào dữ liệu thời tiết, xin lỗi nhé'
        -----------------------------------------------------------------------------------
        """
        self.speak('Chờ một chút để tôi tìm nhé')
        locate = geocoder.ip('me').latlng
        api_key='dd1374e7b62f69d53f6696a829430e76'
        url='http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}&lang=vi&units=metric'.format(locate[0],locate[1],api_key)
        try:  
            f = urllib.request.urlopen(url)
            json_string = f.read()
            f.close()
            data = json.loads(json_string)
            #set data
            city="Thành phố "+str(geocoder.ip('me').city).replace('City','')
            temp=data['main']['feels_like']
            humid=data['main']['humidity']
            wind=data['wind']['speed']
            vision=data['visibility']
            weather=data['weather'][0]['description']
            sunrise=datetime.datetime.fromtimestamp(data['sys']['sunrise'])
            sunset=datetime.datetime.fromtimestamp(data['sys']['sunset'])
            #respone
            self.speak('đây rồi')
            forecast_script='Thời tiết {}hôm nay có {}, nhiệt độ trung bình là {} độ C, độ ẩm là {}%, sức gió {} km trên giờ,\
                        tầm nhìn xa trên {} mét. Hôm nay mặt trời mọc lúc {} giờ {} phút, lặn lúc {} giờ {} phút. Xin hết'.\
                        format(city,weather,temp,humid,wind,vision,sunrise.hour,sunrise.minute,sunset.hour,sunset.minute)
            return self.multiprocess_speak(forecast_script)
        except Exception as e:
            return self.multiprocess_speak('Bạn ơi hiện tại mình không thể truy cập vào dữ liệu thời tiết, xin lỗi nhé')

    #--------------------------------------------------------------------------------------------
    def play_youtube(self,video_name):
        """
        -----------------------------------------------------------------------------------
        Bi.play_youtube(self, video_name):

        # Params: video_name là tên video muốn mở
        # Chức năng: mở video đầu tiên tìm được trong tab mới bằng google chrome
        # Trả về: text thông báo kết quả
            + thành công: text='Tôi mở rồi đấy. Mời bạn thưởng thức nhá'
            + exception: text='Hình như hết tiền mạng rồi :D'
        -----------------------------------------------------------------------------------
        """
        self.speak('Chờ chút có ngay')
        try:
            video = youtube_search.YoutubeSearch(video_name, max_results=1).to_dict()
            webbrowser.register('chrome',None,webbrowser.BackgroundBrowser("C:\Program Files\Google\Chrome\Application\chrome.exe"))
            webbrowser.get('chrome').open_new_tab('https://www.youtube.com/watch?v='+video[0]['id'])
            return self.multiprocess_speak('Tôi mở rồi đấy. Mời bạn thưởng thức nhá')
        except Exception as e:
            return self.multiprocess_speak("Hình như hết tiền mạng rồi :D")
    
    #--------------------------------------------------------------------------------------------
    def define(self,name):
        """
        -----------------------------------------------------------------------------------
        Bi.define(self,name):

        # Params: name là tên cần định nghĩa
        # Chức năng: trả về thông tin thời tiết lấy từ wikipedia (bằng wikipedia module) và đọc lên
        # Trả về: text thông báo kết quả
            + thành công: thông tin định nghĩa lấy được
            + exception: text='Mình cũng không biết nữa. Bạn hỏi chị gu gồ thử xem'
        -----------------------------------------------------------------------------------
        """
        self.speak('Để mình nhớ xem')
        try:
            wikipedia.set_lang('vi')
            contents = wikipedia.summary(name).split('.')
            return self.multiprocess_speak('Theo mình biết: ' +contents[0])
        except Exception as e:
            return self.multiprocess_speak('Mình cũng không biết nữa. Bạn hỏi chị google thử xem')
    
    #--------------------------------------------------------------------------------------------
    def get_time(self):
        """
        -----------------------------------------------------------------------------------
        Bi.get_time(self,name):

        # Params: không có
        # Chức năng: trả về thời gian hiện tại
        # Trả về:
            + thành công: thời gian hiện tại
            + exception: không bắt
        -----------------------------------------------------------------------------------
        """
        t = time.localtime()
        return time.strftime('%H:%M:%S', t)

    #--------------------------------------------------------------------------------------------
    def get_date(self):
        """
        -----------------------------------------------------------------------------------
        Bi.get_date(self,name):

        # Params: không có
        # Chức năng: trả về ngày hiện tại
        # Trả về:
            + thành công: ngày hiện tại
            + exception: không bắt
        -----------------------------------------------------------------------------------
        """
        t = time.localtime()
        return time.strftime('%d/%m/%Y', t)
    
    #--------------------------------------------------------------------------------------------
    def react_to(self, request):
        """
        -----------------------------------------------------------------------------------
        Bi.react_to(self,request):

        # Params: request là đoạn text 
        # Chức năng: phân tích đoạn text để gọi chức năng thực hiện phù hợp
        # Trả về:
            + thành công: dữ liệu trả về của chức năng đã thực hiên
            + exception: dữ liệu trả về khi xảy ra exception trong chức năng đã thực hiện
        -----------------------------------------------------------------------------------
        """
        request=request.lower()
        if request=='':
            return
        if 'bi ơi' in request:
            return self.multiprocess_speak('Mình đây, bạn cần gì')
        elif 'làm được gì' in request or 'có thể làm gì' in request:
            return self.multiprocess_speak('Tôi có thể trò chuyện, làm toán tiểu học, tìm kiếm, mở video, thay đổi hình nền và trả lời những câu hỏi của bạn')
        elif "tạm biệt bạn" == request or "tạm biệt" == request:
            return self.multiprocess_speak('Bái bai')
        elif "hiện tại" in request or "mấy giờ" in request or 'bây giờ là' in request:
            response='Bây giờ là '+self.get_time()
            self.multiprocess_speak(response)
            return response
        elif 'hôm nay là' in request or 'ngày mấy' in request:
            response='Hôm nay là '+self.get_date()
            self.multiprocess_speak(response)
            return response
        elif 'tìm' in request:
            if request.split(' ').index('tìm')==0:
                return self.search_google(request.replace('tìm',''))
            return self.search_google(request.split(" tìm ",1)[1])
        elif 'mở' in request or 'phát' in request:
            return self.play_youtube(request)
        elif 'gửi mail' in request or 'gởi mail' in request:
            self.speak('Bạn muốn gửi mail cho ai')
            destination=self.listen()
            self.speak('Bạn muốn đặt tiêu đề là gì')
            subject=self.listen()
            self.speak('Nội dung của mail là gì')
            content=self.listen()
            return self.send_email(destination,subject,content)
        elif 'đổi ảnh' in request or 'thay ảnh' in request or 'đổi hình' in request or 'thay hình' in request or 'đổi nền' in request or 'thay nền' in request:
            return self.change_random_walpaper()
        elif 'thời tiết' in request:
            return self.wheather_forecast()
        elif ('là gì' in request or 'là ai' in request) and 'bạn là ai' not in request:
            return self.define(request.replace('là gì','').replace('là ai',''))
        else:
            return self.multiprocess_speak(str(self.brain.get_response(request)))


if __name__=='__main__':
    bot=Bi()
    print(Bi.wheather_forecast.__doc__)