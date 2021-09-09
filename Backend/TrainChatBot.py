from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import os
class TrainedChatBot(ChatBot):
    """
    -----------------------------------------------------------------------------------
    Lớp TrainedChatBot:
    
        Kế thừa từ lớp ChatBot trong module chatterbot, tham khảo tại: https://chatterbot.readthedocs.io/en/stable/chatterbot.html
        Là ChatBot đã được train theo corpus tiếng việt đã chuẩn bị
    -----------------------------------------------------------------------------------
    """

    def __init__(self, *args, **kwargs):
        super(TrainedChatBot, self).__init__(*args, **kwargs)
        list_trainer = ChatterBotCorpusTrainer(self)
        for corpus in os.listdir('./BackEnd/Source/Corpus'):
            try:
                list_trainer.train('./BackEnd/Source/Corpus/'+corpus)
            except Exception:
                print('Không thể truy cập {}, corpus này sẽ bị bỏ qua'.format(corpus))

if __name__=="__main__":
    print(TrainedChatBot.__doc__)


