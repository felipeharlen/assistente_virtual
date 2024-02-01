import speech_recognition as sr
import pyttsx3
from datetime import datetime
import wikipedia
import webbrowser
import winshell

wikipedia.set_lang('pt')

class AssistenteVirtual:
    def __init__(self):
        # Inicializar o módulo de fala
        self.engine = pyttsx3.init()
        # Configurar reconhecimento de fala
        self.recognizer = sr.Recognizer()

    def obter_audio(self):
        with sr.Microphone() as source:
            self.recognizer.pause_threshold = 1
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = self.recognizer.listen(source)
            try:
                said = self.recognizer.recognize_google(audio, language='pt-BR')
                print(said)
                return said.lower()
            except sr.UnknownValueError:
                self.falar('Desculpe, não entendi.')
                return ""
            except sr.RequestError:
                self.falar('Desculpe, o serviço não está disponível.')
                return ""

    def falar(self, texto):
        self.engine.say(texto)
        self.engine.runAndWait()

    def pesquisar_youtube(self):
        self.falar('O que você deseja pesquisar?')
        palavra_chave = self.obter_audio()
        if palavra_chave:
            yt = f'https://youtube.com/results?search_query={palavra_chave}'
            webbrowser.get().open(yt)
            self.falar(f'Aqui está o que eu encontrei para {palavra_chave} no YouTube.')

    def pesquisar_wikipedia(self):
        self.falar('O que você deseja pesquisar?')
        consulta = self.obter_audio()
        if consulta:
            resultado = wikipedia.summary(consulta, sentences=3)
            self.falar('De acordo com a Wikipedia, ')
            print(resultado)
            self.falar(resultado)

    def esvaziar_lixeira(self):
        winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=True)
        self.falar('Lixeira esvaziada.')

    def mostrar_horario(self):
        str_time = 'São ' + datetime.today().strftime('%H:%M')
        print(str_time + 'h.')
        self.falar(str_time)

    def pesquisar_musica(self):
        self.falar('Qual música você gostaria de ouvir?')
        musica = self.obter_audio()
        if musica:
            yt_music = f'https://music.youtube.com/search?q={musica}'
            webbrowser.get().open(yt_music)
            self.falar(f'Exibindo os principais resultados para {musica} no YouTube Music.')

    def sair(self):
        self.falar('Até a próxima')

if __name__ == "__main__":
    assistente = AssistenteVirtual()
    continuar = True

    while continuar:
        print('Estou ouvindo...')
        texto = assistente.obter_audio()
        if texto:
            if 'youtube' in texto:
                assistente.pesquisar_youtube()
            elif 'pesquisar' in texto:
                assistente.pesquisar_wikipedia()
            elif 'esvaziar lixeira' in texto:
                assistente.esvaziar_lixeira()
            elif 'que horas' in texto:
                assistente.mostrar_horario()
            elif 'música' in texto:
                assistente.pesquisar_musica()
            elif 'sair' in texto:
                assistente.sair()
                continuar = False