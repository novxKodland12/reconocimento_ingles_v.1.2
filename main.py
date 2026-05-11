import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr
from colorama import Fore, init
import io
import random

init(autoreset=True)

sample_rate = 44100  
duration = 2.5
VIDAS = 3

banner = """
╔══════════════════════════════════╗
║   🦜  JUEGO TRADUCTOR VOZ  🦜   ║
║   Learn English by Speaking!     ║
╚══════════════════════════════════╝
"""
words = {
"facil": [
    {"es": "Perro",   "en": "dog"},
    {"es": "Gato",    "en": "cat"},
    {"es": "Sol",     "en": "sun"},
    {"es": "Luna",    "en": "moon"},
    {"es": "Agua",    "en": "water"},
    {"es": "Casa",    "en": "house"},
    {"es": "Pan",     "en": "bread"},
    {"es": "Leche",   "en": "milk"},
    {"es": "Mesa",    "en": "table"},
    {"es": "Silla",   "en": "chair"},
    {"es": "Árbol",   "en": "tree"},
    {"es": "Flor",    "en": "flower"},
    {"es": "Pez",     "en": "fish"},
    {"es": "Pájaro",  "en": "bird"},
    {"es": "Carro",   "en": "car"},
    {"es": "Puerta",  "en": "door"},
    {"es": "Mano",    "en": "hand"},
    {"es": "Ojo",     "en": "eye"},
    {"es": "Fuego",   "en": "fire"},
    {"es": "Tierra",  "en": "earth"},
],
"medio": [
    {"es": "Amigo",    "en": "friend"},
    {"es": "Libro",    "en": "book"},
    {"es": "Ciudad",   "en": "city"},
    {"es": "Comer",    "en": "eat"},
    {"es": "Correr",   "en": "run"},
    {"es": "Escuela",  "en": "school"},
    {"es": "Familia",  "en": "family"},
    {"es": "Trabajo",  "en": "work"},
    {"es": "Dinero",   "en": "money"},
    {"es": "Tiempo",   "en": "time"},
    {"es": "Ventana",  "en": "window"},
    {"es": "Cocina",   "en": "kitchen"},
    {"es": "Camino",   "en": "road"},
    {"es": "Música",   "en": "music"},
    {"es": "Playa",    "en": "beach"},
    {"es": "Noche",    "en": "night"},
    {"es": "Lluvia",   "en": "rain"},
    {"es": "Montaña",  "en": "mountain"},
    {"es": "Mercado",  "en": "market"},
    {"es": "Jardín",   "en": "garden"},
],
"dificil": [
    {"es": "Biblioteca",   "en": "library"},
    {"es": "Computadora",  "en": "computer"},
    {"es": "Estudiante",   "en": "student"},
    {"es": "Universo",     "en": "universe"},
    {"es": "Aventura",     "en": "adventure"},
    {"es": "Conocimiento", "en": "knowledge"},
    {"es": "Electricidad", "en": "electricity"},
    {"es": "Democracia",   "en": "democracy"},
    {"es": "Fotografía",   "en": "photography"},
    {"es": "Imaginación",  "en": "imagination"},
    {"es": "Responsable",  "en": "responsible"},
    {"es": "Entretenimiento", "en": "entertainment"},
    {"es": "Arquitectura", "en": "architecture"},
    {"es": "Comunicación", "en": "communication"},
    {"es": "Independencia","en": "independence"},
    {"es": "Temperatura",  "en": "temperature"},
    {"es": "Experimento",  "en": "experiment"},
    {"es": "Pronunciación","en": "pronunciation"},
    {"es": "Celebración",  "en": "celebration"},
    {"es": "Transformación","en": "transformation"},
],
"experto": [
    {"es": "Ambigüedad",      "en": "ambiguity"},
    {"es": "Perspectiva",     "en": "perspective"},
    {"es": "Consecuencia",    "en": "consequence"},
    {"es": "Sostenibilidad",  "en": "sustainability"},
    {"es": "Predominante",    "en": "predominant"},
    {"es": "Controversia",    "en": "controversy"},
    {"es": "Simultáneamente", "en": "simultaneously"},
    {"es": "Infraestructura", "en": "infrastructure"},
    {"es": "Vulnerabilidad",  "en": "vulnerability"},
    {"es": "Circunstancia",   "en": "circumstance"},
    {"es": "Desigualdad",     "en": "inequality"},
    {"es": "Manifestación",   "en": "manifestation"},
    {"es": "Reconocimiento",  "en": "recognition"},
    {"es": "Establecimiento", "en": "establishment"},
    {"es": "Aproximadamente", "en": "approximately"},
    {"es": "Investigación",   "en": "investigation"},
    {"es": "Implementación",  "en": "implementation"},
    {"es": "Extraordinario",  "en": "extraordinary"},
    {"es": "Confidencialidad","en": "confidentiality"},
    {"es": "Responsabilidad", "en": "responsibility"},
],
"nativo": [
    {"es": "Efímero",              "en": "ephemeral"},
    {"es": "Perspicaz",            "en": "insightful"},
    {"es": "Condescendiente",      "en": "condescending"},
    {"es": "Introspección",        "en": "introspection"},
    {"es": "Serendipia",           "en": "serendipity"},
    {"es": "Omnipresente",         "en": "omnipresent"},
    {"es": "Pragmático",           "en": "pragmatic"},
    {"es": "Yuxtaposición",        "en": "juxtaposition"},
    {"es": "Idiosincrasia",        "en": "idiosyncrasy"},
    {"es": "Paradigma",            "en": "paradigm"},
    {"es": "Ambivalente",          "en": "ambivalent"},
    {"es": "Discrepancia",         "en": "discrepancy"},
    {"es": "Connotación",          "en": "connotation"},
    {"es": "Meticuloso",           "en": "meticulous"},
    {"es": "Obsoleto",             "en": "obsolete"},
    {"es": "Eufemismo",            "en": "euphemism"},
    {"es": "Trascendental",        "en": "transcendental"},
    {"es": "Inequívoco",           "en": "unequivocal"},
    {"es": "Consternación",        "en": "consternation"},
    {"es": "Magnanimidad",         "en": "magnanimity"},
]
}

def grabar():
    print(Fore.CYAN + "🎙️ Habla ahora...")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype="int16")
    sd.wait()
    buffer = io.BytesIO()
    wav.write(buffer, sample_rate, recording)
    buffer.seek(0)
    return buffer

def reconocer(buffer):
    recognizer = sr.Recognizer()
    with sr.AudioFile(buffer) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio, language="en").lower()
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        print(Fore.RED + f"⚠️ Error del servicio: {e}")
        return None

def verificar(dicho, esperado):
    if dicho == esperado.lower():
        print(Fore.GREEN + "✅ ¡Correcto!")
        return True
    else:
        print(Fore.RED + f"❌ Dijiste: '{dicho}' — Era: '{esperado}'")
        return False
    
def jugar():
    print(Fore.YELLOW + banner)

    print(Fore.WHITE + "🎯 Ingrese el numero del nivel de dificultad:")
    print("  1. 😊 Fácil")
    print("  2. 😐 Medio")
    print("  3. 😈 Difícil")
    print("  4. 🎓 Experto")
    print("  5. 🦅 Nativo")
    opcion = input(Fore.WHITE + "\nIngresa el numero de tu elección: ")

    niveles = {"1": "facil", "2": "medio", "3": "dificil", "4": "experto", "5": "nativo"}
    nivel = niveles.get(opcion, "facil")
    cantidad = {"1": 5, "2": 8, "3": 10, "4": 12, "5": 15}
    lista = random.sample(words[nivel], cantidad.get(opcion, 5))

    puntos = 0
    vidas = VIDAS
    streak = 0

    for i, palabra in enumerate(lista, 1):
        print(Fore.CYAN + f"\n{'='*40}")
        print(Fore.WHITE + f"❓ Pregunta {i}/{len(lista)}")
        print(Fore.YELLOW + f"🇪🇸 ¿Cómo se dice en inglés: '{palabra['es']}'?")
        corazones = "❤️ " * vidas + "🖤 " * (VIDAS - vidas)
        print(Fore.RED + f"Vidas: {corazones}")
        if streak >= 2:
            print(Fore.YELLOW + f"🔥 Racha: {streak}")

        buffer = grabar()
        dicho = reconocer(buffer)

        if dicho:
            if verificar(dicho, palabra["en"]):
                puntos += 1
                streak += 1
            else:
                vidas -= 1
                streak = 0
        else:
            print(Fore.YELLOW + "😵 No se entendió, siguiente pregunta...")
            streak = 0

        if vidas == 0:
            print(Fore.RED + "\n💀 ¡Sin vidas! Fin del juego.")
            break

    print(Fore.CYAN + f"\n{'='*40}")
    print(Fore.YELLOW + f"🏆 Resultado: {puntos}/{len(lista)} correctas")
    if puntos == len(lista):
        print(Fore.GREEN + "🌟 ¡Perfecto! ¡Eres un genio!")
    elif puntos >= len(lista) // 2:
        print(Fore.YELLOW + "👍 ¡Buen trabajo! Sigue practicando.")
    else:
        print(Fore.RED + "💪 ¡No te rindas! Inténtalo de nuevo.")

    again = input(Fore.WHITE + "\n🔄 ¿Jugar de nuevo? (s/n): ")
    if again.lower() == "s":
        jugar()
    else:
        print(Fore.CYAN + "\n👋 ¡Hasta luego! Keep learning! 🦜")

jugar()