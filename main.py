import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr
from colorama import Fore, init
import io
import random

init(autoreset=True)

# ─────────────────────────────────────────
# CONSTANTES — Cambia estos valores fácilmente
# ─────────────────────────────────────────
SAMPLE_RATE = 44100
DURATION    = 2.5
VIDAS       = 3

BANNER = """
╔══════════════════════════════════╗
║   🦜  JUEGO TRADUCTOR VOZ  🦜   ║
║   Learn English by Speaking!     ║
╚══════════════════════════════════╝
"""

NIVELES = {
    "1": ("facil",   5,  "😊 Fácil"),
    "2": ("medio",   8,  "😐 Medio"),
    "3": ("dificil", 10, "😈 Difícil"),
    "4": ("experto", 12, "🎓 Experto"),
    "5": ("nativo",  15, "🦅 Nativo"),
}

WORDS = {
    "facil": [
        {"es": "Perro",  "en": "dog"},   {"es": "Gato",   "en": "cat"},
        {"es": "Sol",    "en": "sun"},   {"es": "Luna",   "en": "moon"},
        {"es": "Agua",   "en": "water"}, {"es": "Casa",   "en": "house"},
        {"es": "Pan",    "en": "bread"}, {"es": "Leche",  "en": "milk"},
        {"es": "Mesa",   "en": "table"}, {"es": "Silla",  "en": "chair"},
        {"es": "Árbol",  "en": "tree"},  {"es": "Flor",   "en": "flower"},
        {"es": "Pez",    "en": "fish"},  {"es": "Pájaro", "en": "bird"},
        {"es": "Carro",  "en": "car"},   {"es": "Puerta", "en": "door"},
        {"es": "Mano",   "en": "hand"},  {"es": "Ojo",    "en": "eye"},
        {"es": "Fuego",  "en": "fire"},  {"es": "Tierra", "en": "earth"},
    ],
    "medio": [
        {"es": "Amigo",   "en": "friend"},   {"es": "Libro",   "en": "book"},
        {"es": "Ciudad",  "en": "city"},     {"es": "Comer",   "en": "eat"},
        {"es": "Correr",  "en": "run"},      {"es": "Escuela", "en": "school"},
        {"es": "Familia", "en": "family"},   {"es": "Trabajo", "en": "work"},
        {"es": "Dinero",  "en": "money"},    {"es": "Tiempo",  "en": "time"},
        {"es": "Ventana", "en": "window"},   {"es": "Cocina",  "en": "kitchen"},
        {"es": "Camino",  "en": "road"},     {"es": "Música",  "en": "music"},
        {"es": "Playa",   "en": "beach"},    {"es": "Noche",   "en": "night"},
        {"es": "Lluvia",  "en": "rain"},     {"es": "Montaña", "en": "mountain"},
        {"es": "Mercado", "en": "market"},   {"es": "Jardín",  "en": "garden"},
    ],
    "dificil": [
        {"es": "Biblioteca",      "en": "library"},     {"es": "Computadora",  "en": "computer"},
        {"es": "Estudiante",      "en": "student"},     {"es": "Universo",     "en": "universe"},
        {"es": "Aventura",        "en": "adventure"},   {"es": "Conocimiento", "en": "knowledge"},
        {"es": "Electricidad",    "en": "electricity"}, {"es": "Democracia",   "en": "democracy"},
        {"es": "Fotografía",      "en": "photography"}, {"es": "Imaginación",  "en": "imagination"},
        {"es": "Responsable",     "en": "responsible"}, {"es": "Entretenimiento", "en": "entertainment"},
        {"es": "Arquitectura",    "en": "architecture"},{"es": "Comunicación", "en": "communication"},
        {"es": "Independencia",   "en": "independence"},{"es": "Temperatura",  "en": "temperature"},
        {"es": "Experimento",     "en": "experiment"},  {"es": "Pronunciación","en": "pronunciation"},
        {"es": "Celebración",     "en": "celebration"}, {"es": "Transformación","en": "transformation"},
    ],
    "experto": [
        {"es": "Ambigüedad",      "en": "ambiguity"},      {"es": "Perspectiva",     "en": "perspective"},
        {"es": "Consecuencia",    "en": "consequence"},    {"es": "Sostenibilidad",  "en": "sustainability"},
        {"es": "Predominante",    "en": "predominant"},    {"es": "Controversia",    "en": "controversy"},
        {"es": "Simultáneamente", "en": "simultaneously"}, {"es": "Infraestructura", "en": "infrastructure"},
        {"es": "Vulnerabilidad",  "en": "vulnerability"},  {"es": "Circunstancia",   "en": "circumstance"},
        {"es": "Desigualdad",     "en": "inequality"},     {"es": "Manifestación",   "en": "manifestation"},
        {"es": "Reconocimiento",  "en": "recognition"},    {"es": "Establecimiento", "en": "establishment"},
        {"es": "Aproximadamente", "en": "approximately"},  {"es": "Investigación",   "en": "investigation"},
        {"es": "Implementación",  "en": "implementation"}, {"es": "Extraordinario",  "en": "extraordinary"},
        {"es": "Confidencialidad","en": "confidentiality"},{"es": "Responsabilidad", "en": "responsibility"},
    ],
    "nativo": [
        {"es": "Efímero",         "en": "ephemeral"},    {"es": "Perspicaz",      "en": "insightful"},
        {"es": "Condescendiente", "en": "condescending"},{"es": "Introspección",  "en": "introspection"},
        {"es": "Serendipia",      "en": "serendipity"},  {"es": "Omnipresente",   "en": "omnipresent"},
        {"es": "Pragmático",      "en": "pragmatic"},    {"es": "Yuxtaposición",  "en": "juxtaposition"},
        {"es": "Idiosincrasia",   "en": "idiosyncrasy"}, {"es": "Paradigma",      "en": "paradigm"},
        {"es": "Ambivalente",     "en": "ambivalent"},   {"es": "Discrepancia",   "en": "discrepancy"},
        {"es": "Connotación",     "en": "connotation"},  {"es": "Meticuloso",     "en": "meticulous"},
        {"es": "Obsoleto",        "en": "obsolete"},     {"es": "Eufemismo",      "en": "euphemism"},
        {"es": "Trascendental",   "en": "transcendental"},{"es": "Inequívoco",    "en": "unequivocal"},
        {"es": "Consternación",   "en": "consternation"},{"es": "Magnanimidad",   "en": "magnanimity"},
    ],
}

def grabar():
    """Graba DURATION segundos desde el micrófono y retorna un buffer WAV."""
    print(Fore.CYAN + "🎙️  Habla ahora...")
    recording = sd.rec(
        int(DURATION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="int16"
    )
    sd.wait()  # Espera a que termine la grabación

    buffer = io.BytesIO()
    wav.write(buffer, SAMPLE_RATE, recording)
    buffer.seek(0)  # Vuelve al inicio del buffer para que se pueda leer después
    return buffer

def reconocer(buffer):
    """Convierte el audio en texto usando Google Speech Recognition."""
    recognizer = sr.Recognizer()
    with sr.AudioFile(buffer) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio, language="en").lower()
    except sr.UnknownValueError:
        return None  # No se entendió nada
    except sr.RequestError as e:
        print(Fore.RED + f"⚠️  Error del servicio: {e}")
        return None

def verificar(dicho, esperado):
    """Compara lo que dijo el usuario con la respuesta correcta."""
    if dicho == esperado.lower():
        print(Fore.GREEN + "✅ ¡Correcto!")
        return True
    print(Fore.RED + f"❌ Dijiste: '{dicho}' — Era: '{esperado}'")
    return False

def seleccionar_nivel():
    """Muestra el menú de niveles y retorna (clave_nivel, cantidad_preguntas)."""
    print(Fore.WHITE + "🎯 Selecciona el nivel de dificultad:")
    for opcion, (_, _, etiqueta) in NIVELES.items():
        print(f"  {opcion}. {etiqueta}")

    while True:
        opcion = input(Fore.WHITE + "\nIngresa el número de tu elección: ").strip()
        if opcion in NIVELES:
            clave, cantidad, etiqueta = NIVELES[opcion]
            print(Fore.CYAN + f"\n🚀 Nivel seleccionado: {etiqueta}\n")
            return clave, cantidad
        # Si la opción no es válida, vuelve a preguntar
        print(Fore.RED + "⚠️  Opción inválida. Elige un número del 1 al 5.")

def mostrar_pregunta(numero, total, palabra, vidas, streak):
    """Imprime el encabezado de cada pregunta con vidas y racha."""
    print(Fore.CYAN + f"\n{'='*40}")
    print(Fore.WHITE + f"❓ Pregunta {numero}/{total}")
    print(Fore.YELLOW + f"🇪🇸 ¿Cómo se dice en inglés: '{palabra['es']}'?")

    corazones = "❤️ " * vidas + "🖤 " * (VIDAS - vidas)
    print(Fore.RED + f"Vidas: {corazones}")

    if streak >= 2:
        print(Fore.YELLOW + f"🔥 Racha: {streak}")

def mostrar_resumen(puntos, total):
    """Imprime el resultado al terminar la partida."""
    print(Fore.CYAN + f"\n{'='*40}")
    print(Fore.YELLOW + f"🏆 Resultado: {puntos}/{total} correctas")

    if puntos == total:
        print(Fore.GREEN + "🌟 ¡Perfecto! ¡Eres un genio!")
    elif puntos >= total // 2:
        print(Fore.YELLOW + "👍 ¡Buen trabajo! Sigue practicando.")
    else:
        print(Fore.RED + "💪 ¡No te rindas! Inténtalo de nuevo.")

def jugar():
    """Controla el flujo principal del juego. Usa un while en vez de recursión."""
    print(Fore.YELLOW + BANNER)

    # El while permite jugar varias veces sin riesgo de stack overflow
    while True:
        clave, cantidad = seleccionar_nivel()
        lista   = random.sample(WORDS[clave], cantidad)
        puntos  = 0
        vidas   = VIDAS
        streak  = 0

        for i, palabra in enumerate(lista, 1):
            mostrar_pregunta(i, len(lista), palabra, vidas, streak)

            buffer = grabar()
            dicho  = reconocer(buffer)

            if dicho:
                if verificar(dicho, palabra["en"]):
                    puntos += 1
                    streak += 1
                else:
                    vidas  -= 1
                    streak  = 0
            else:
                print(Fore.YELLOW + "😵 No se entendió, siguiente pregunta...")
                streak = 0

            if vidas == 0:
                print(Fore.RED + "\n💀 ¡Sin vidas! Fin del juego.")
                break

        mostrar_resumen(puntos, len(lista))

        again = input(Fore.WHITE + "\n🔄 ¿Jugar de nuevo? (s/n): ").strip().lower()
        if again != "s":
            print(Fore.CYAN + "\n👋 ¡Hasta luego! Keep learning! 🦜")
            break  # Sale del while limpiamente

if __name__ == "__main__":
    # Solo corre el juego si ejecutas este archivo directamente.
    # Si otro archivo hace "import juego_traductor", no se ejecuta solo.
    jugar()