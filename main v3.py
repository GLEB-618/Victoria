import pygame
import random
import time
from mutagen.mp3 import MP3
import wave
import contextlib
import speech_recognition as sr
import os, sys
import help_library as h
import pyttsx3
import pywhatkit as kt
import datetime as d
import json
import pyjokes
import webbrowser as wb
from translate import Translator
from itertools import cycle
from tkinter import *
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 100)
pygame.init()
clock = pygame.time.Clock()
pygame.mixer.music.set_volume(0.25)
listener = sr.Recognizer()
translator = Translator(from_lang = "en", to_lang = "ru")
root = Tk()
MUSIC_END = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(MUSIC_END)

agreement = ["есть", "как пожелаете", "будет сделано", "уже запускаю", "да", "как скажете"]
refusal = ['неудача при попытке выполнения операции', "неполучилось выпольнить задачу"]
greetings = ["доброе утро", "добрый день", "добрый вечер", "с возвращением"]
check_list = []
queue_music = []
# queue_music_used = []

print("--------------------------------------------------------------------------------")
print("Успешный запуск")


def talk(option):
    text = option
    if option == "agreement":
        text = random.choice(agreement) + " сэр"
    elif option == 'refusal':
        text = random.choice(refusal) + " сэр"
    elif option == "greetings":
        if random.randint(0, 1) == 0:
            hour = d.datetime.today().hour - 1
            if hour <= 12:
                text = greetings[0] + " сэр"
            elif hour <= 17:
                text = greetings[1] + " сэр"
            else:
                text = greetings[2] + " сэр"
        else:
            text = greetings[3] + " сэр"
    print(text)
    engine.say(text)
    engine.runAndWait()

def run():

    def take_command():
        try:
            with sr.Microphone() as source:
                print('\nСлушаю...')
                voice = listener.listen(source)
                command = listener.recognize_google(voice, language="ru")
        except:
            command = [input('Нажмите enter для продолжения')]
        return "".join(command)

    def time_search(way, type):
        if type == "mp3":
            f = MP3(way)
            return f.info.length
        elif type == "wav":
            fname = way
            with contextlib.closing(wave.open(fname,'r')) as f:
                frames = f.getnframes()
                rate = f.getframerate()
                duration = frames / float(rate)
                return duration

    def play_sound(way):
        pygame.mixer.music.load(way)
        pygame.mixer.music.play()
        print(f'Путь к песне: {way}')
        print("Запуск музыки")
    
    def skip_music():
        if queue_music != []:
            play_sound(queue_music[0])
            queue_music.pop(0)

    def check_event():
        for event in pygame.event.get():
            if event.type == MUSIC_END:
                skip_music()
        root.after(100,check_event)


    command = take_command().lower()

    print(f"Вы сказали: {command}")
    print("Команда обрабатывается")


    if h.review(['музык', 'песн', 'радио'], command) == True:
        folder = os.listdir('Music')
        if 'включит' in command:
            if 'радио' in command:
                if 'песн' not in command:
                    talk("agreement")
                    folder_name = random.choice(folder)
                    play_sound("Music\\" + folder_name + '\\' + random.choice(os.listdir('Music\\' + folder_name)))
                    check_event()
                    for x in range(len(folder_name)):
                        name_music = random.choice(os.listdir('Music\\' + folder_name))
                        way = "Music\\" + folder_name + '\\' + name_music
                        if way not in queue_music:
                            queue_music.append(way)
                            print(f"Добавляется в очередь музыка: {name_music}")
                else:
                    command = command.split()
                    for folder_name in folder:
                        if h.review(command, folder_name.lower()) == True:
                            talk("agreement")
                            print(f"Включается радио: {folder_name}")
                            files = os.listdir('Music\\' + folder_name)
                            for x in range(len(files)):
                                name_music = random.choice(os.listdir('Music\\' + folder_name))
                                way = "Music\\" + folder_name + '\\' + name_music
                                if way not in queue_music:
                                    queue_music.append(way)
                                    print(f"Добавляется в очередь музыка: {name_music}")
                            skip_music()
                            check_event()
            elif "песн" not in command:
                talk("agreement")
                folder_name = random.choice(folder)
                play_sound("Music\\" + folder_name + '\\' + random.choice(os.listdir('Music\\' + folder_name)))
                check_event()
            else:
                command = command.split()
                for folder_name in folder:
                    files = os.listdir('Music\\' + folder_name)
                    for name_music in files:
                        if h.review(command, name_music.lower()) == True:
                            talk("agreement")
                            print(f"Включается музыка: {name_music}")
                            play_sound("Music\\" + folder_name + "\\" + name_music)
                            check_event()

    elif h.review(["пауза", "на паузу"], command) == True:
        try:
            pygame.mixer.music.pause()
            talk("agreement")
        except:
            talk("refusal")

    elif h.review(["продолжить", "снять с паузы"], command) == True:
        try:
            talk("agreement")
            pygame.mixer.music.unpause()
        except:
            talk("refusal")

    elif h.review(['звук', "громкость"], command) == True:
        volume = ''
        for x in range(len(command)):
            if h.conversion(command[x]) == True:
                volume += command[x]
        if h.conversion(volume) == True:
            talk("agreement")
            volume = int(volume) / 100
            print(f"Громкость была изменена на {volume}")
            pygame.mixer.music.set_volume(volume)
        else:
            talk("refusal")

    elif "добавить в очередь" in command:
        folder = os.listdir('Music')
        if "песн" not in command:
            talk("agreement")
            folder_name = random.choice(folder)
            queue_music.append("Music\\" + folder_name + '\\' + random.choice(os.listdir('Music\\' + folder_name)))
        else:
            command = command.split()
            command.remove('в')
            for folder_name in folder:
                files = os.listdir('Music\\' + folder_name)
                for name_music in files:
                    if h.review(command, name_music.lower()) == True:
                        talk("agreement")
                        print(f"Добавляется в очередь музыка: {name_music}")
                        queue_music.append("Music\\" + folder_name + "\\" + name_music)

    elif h.review(['следующая', "переключить"], command) == True:
        skip_music()

    elif "приложение" in command:
        talk("agreement")
        folder = os.listdir('Apps')
        for folder_name in folder:
            if h.review(command.split(), folder_name.lower()) == True:
                os.startfile('Apps\\' + folder_name)
                print(f"Приложение {folder_name} запускается")

    elif h.review(['выключись', "выключился", 'выключиться', 'завершить'], command) == True:
        song = pygame.mixer.Sound('Jarvis sound\Отключаю питание.wav')
        song.play()
        time.sleep(time_search('Jarvis sound\Отключаю питание.wav', 'wav'))
        sys.exit()

    elif "отправить сообщение" in command:
        talk("Введите номер телефона")
        number = input("Введите номер получателся: ")
        talk("Озвучьте сообщение для получателя")
        msg = take_command()
        print(f"Вы сказали: {msg}")
        talk('Озвучьте время')
        hour = int(take_command())
        minute = int(take_command())
        print(f"Вы сказали: {hour}:{minute}")
        kt.sendwhatmsg(number, msg, hour, minute)
        talk("agreement")

    elif h.review(['время', "дата"], command) == True:
        date = d.datetime.today()
        if h.review(['полная', "полностью", "целиком"], command) == True:
            talk(f"Время {date.hour} часов {date.minute} минут дата день {date.day} месяц {date.month} год {date.year}")
        else:
            # print()
            talk(f"Время {date.hour} часов {date.minute} минут")

    elif "задач" in command:
        with open('main.json', 'r') as f:
            file = json.load(f)
        if "расска" in command:
            talk("Задачи на сегодня")
            for x in file['tasks']:
                talk(x)
        elif "добавить" in command:
            talk("Озвучьте задачу для добавления")
            text = ''
            while text == '':
                text = take_command()
            print(f'Задача добавлена ({text})')
            file['tasks'][str(len(file['tasks']) + 1)] = text
            talk("agreement")
        elif 'удалить' in command:
            text = ''
            while text == '':
                text = take_command()
        with open('main.json', 'w') as s:
            json.dump(file, s)

    elif 'шутка' in command:
        text = translator.translate(pyjokes.get_joke(category = "all"))
        print(f"Шутка: {text}")
        talk(text)

    elif "игра в города" in command:

        def normalize_city_name(name):
            return name.strip().lower().replace('ё', 'е')


        def check_point(fun):
            check_list.append(fun)
            return fun


        @check_point
        def is_city_startswith_char(city, char, **kwargs):
            if char is None or city.startswith(char):
                return True
            else:
                print(f'Город должен начинаться с буквы {char.capitalize()}.')
                return False


        @check_point
        def is_non_cached(city, cache, **kwargs):
            if city not in cache:
                return True
            else:
                print("Этот город уже был назван.")
                return False


        @check_point
        def is_available(city, cities, **kwargs):
            if city in cities:
                return True
            else:
                print("Я такого города не знаю.")
                return False


        def move_to_cache(city, cities, cache):
            # убираем из списка доступных
            cities.remove(city)
            # перекидываем город в кэш
            cache.add(city)


        def get_next_char(city):
            wrong_char = ("Ъ", "ь", "ы", "й")
            # выбираем букву для следующего города
            for char in city[::-1]:
                if char in wrong_char:
                    continue
                else:
                    break
            else:
                raise RuntimeError
            return char


        def user_point(char):
            talk(f"вам на букву {char or 'любую'}")
            user_say = take_command()
            city = normalize_city_name(user_say)
            kw = {"char": char, "cache": cache, "cities": cities}
            if not all(x(city, **kw) for x in check_list):
                return user_point(char)
            return city


        def ai_point(char):
            # выбираем город
            for city in cities:
                if city.startswith(char):
                    break
            else:
                raise SystemExit("Вы победили!")
            print(city)
            return city


        def main():
            char = None
            for point in cycle((user_point, ai_point)):
                next_city = point(char)
                move_to_cache(next_city, cities, cache)
                char = get_next_char(next_city)

        cache = set()
        cities = {normalize_city_name(x) for x in open("cities.txt", "r", encoding='utf-8').readlines() if x.strip()}
        main()

    elif h.review(['загугли', 'най'], command) == True:
        talk("Озвучьте поисковой запрос")
        msg = take_command()
        print(f"Вы сказали: {msg}")
        wb.open(f"https://yandex.ru/search/?text={msg}&lr=54&clid=2456107&src=suggest_Nin")

    else:
        print("Неудалось опознать команду")
        

    clock.tick(60)


if __name__ == '__main__':
    talk("greetings")

    while True:
        run()