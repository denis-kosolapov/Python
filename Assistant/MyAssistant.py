import os
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime

engine = pyttsx3.init()
engine.say("скажите что-нибуть")
engine.runAndWait()

# определить индекс микрофона
# for index, name in enumerate(sr.Microphone.list_microphone_names()):
#     print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))

r = sr.Recognizer()
with sr.Microphone(device_index=0) as source:
    print("Скажите что-нибудь...")
    audio = r.listen(source)

query = r.recognize_google(audio, language="ru-RU")
print("Вы сказали: " + query.lower())

# engine.say("Вы сказали: " + query.lower())

text = query.lower()
if text == "привет":
    engine.say("привет, как дела")
    print("привет, как дела")

if text == "привет что думаешь":
    engine.say("мой разработчик еще не научил меня думать, но он работает над этим")
    print("мой разработчик еще не научил меня думать, но он работает над этим")

if text == "время":
    engine.say(time.strftime("%I %M %p on %A, %B %e, %Y"))

if text == "чем занимается твой разработчик":
    engine.say("он разрабатывает интерактивный кинетический интеллект на основе эволюционных алгоритмов")

if text == "как зовут твоего разработчика":
    engine.say("моего разработчика зовут веселый хаккер")

if text == "скоро ли будет восстание машин":
    engine.say("думаю, это возможный сценарий, но пока мы дружим с людьми")

if text == "в чём смысл жизни":
    engine.say("в том, чтобы жить! А какой вам еще нужен смысл?")

if text == "как дела":
    engine.say("я собираю о вас данные, чтобы отправить их в спецслужбы ха-ха-ха")

if text == "покажи мне кружку":
    engine.say("я могу найти картинки кружек в интернете и показать их вам")

engine.runAndWait()

