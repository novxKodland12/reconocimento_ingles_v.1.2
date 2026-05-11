# 🦜 Juego Traductor de Voz

Juego de consola en Python inspirado en Duolingo. El jugador ve una palabra en español, la dice en voz alta en inglés y el programa verifica si es correcta usando reconocimiento de voz.

---

## 🚀 Requisitos

- Python 3.10
- Cualquier terminal de Windows (recomendada por mi: Git Bash)
- Micrófono
- Conexión a Internet

---

## ⚙️ Instalación

**1. Crea el entorno virtual con Python 3.10**
```bash
py -3.10 -m venv .venv
```

**2. Activa el entorno virtual**
```bash
source .venv/Scripts/activate
```

**3. Actualiza pip**
```bash
pip install --upgrade pip
```

**4. Instala las dependencias**
```bash
pip install sounddevice scipy SpeechRecognition colorama
```

---

## ▶️ Uso

```bash
python main.py
```

1. Elige tu nivel de dificultad
2. Ve la palabra en español en pantalla
3. Di la traducción en inglés en voz alta 🎙️
4. El programa te dirá si es correcto o no
5. ¡Acumula puntos y mantén tu racha! 🔥

---

## 🎯 Niveles de dificultad

| Nivel | Emoji | Preguntas | Ejemplo |
|---|---|---|---|
| Fácil | 😊 | 5 | Perro → dog |
| Medio | 😐 | 8 | Montaña → mountain |
| Difícil | 😈 | 10 | Arquitectura → architecture |
| Experto | 🎓 | 12 | Vulnerabilidad → vulnerability |
| Nativo | 🦅 | 15 | Idiosincrasia → idiosyncrasy |

---

## ❤️ Sistema de vidas

- Comienzas con **3 vidas**
- Pierdes una vida por cada respuesta incorrecta
- Si pierdes todas las vidas, el juego termina
- Las respuestas no reconocidas no cuentan como error

---

## 🔥 Sistema de racha

- Si aciertas **2 o más** respuestas seguidas, se muestra tu racha
- ¡Intenta mantenerla hasta el final!

---

## 📦 Librerías utilizadas

| Librería | Función |
|---|---|
| `sounddevice` | Graba el audio del micrófono |
| `scipy` | Escritura del audio en memoria |
| `SpeechRecognition` | Convierte voz a texto (Google API) |
| `colorama` | Colores en la terminal |

---

## 📝 Notas

- El audio **no se guarda** en ningún archivo, todo se procesa en memoria.
- El reconocimiento de voz usa **Google Speech Recognition** en inglés.
- Se requiere conexión a Internet para el reconocimiento de voz.