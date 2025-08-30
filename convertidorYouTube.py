import yt_dlp
import os
import subprocess

RUTA_DESCARGA = r"C:\Users\paul_\Desktop\Programacion\Proyectos Python"
FFMPEG_PATH = r"C:\ffmpeg\bin\ffmpeg.exe"

def descargar_mp4(url):
    """Descargar en MP4 con menú de calidades"""
    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
        info = ydl.extract_info(url, download=False)
        titulo = info.get("title", "video_descargado").replace(":", "").replace("|", "").replace("?", "")
        
        # Obtener resoluciones disponibles
        formatos_video = []
        for fmt in info['formats']:
            if fmt.get("vcodec") != "none" and fmt.get("height"):
                formatos_video.append({
                    "format_id": fmt["format_id"],
                    "height": fmt["height"],
                    "fps": fmt.get("fps", 30),
                    "ext": fmt.get("ext"),
                })

        # Filtrar por resoluciones únicas
        resoluciones = {}
        for f in formatos_video:
            h = f["height"]
            if h not in resoluciones:
                resoluciones[h] = f
        formatos_ordenados = sorted(resoluciones.values(), key=lambda x: x["height"], reverse=True)

        # Mostrar opciones
        print("\n=== 📺 Calidades disponibles (MP4) ===")
        for i, f in enumerate(formatos_ordenados, 1):
            print(f"{i}. {f['height']}p - {f['fps']} fps ({f['ext']})")

        # Elegir
        while True:
            try:
                eleccion = int(input(f"\n👉 Elige una opción (1-{len(formatos_ordenados)}): ")) - 1
                if 0 <= eleccion < len(formatos_ordenados):
                    formato = formatos_ordenados[eleccion]
                    break
                else:
                    print("Número fuera de rango.")
            except ValueError:
                print("Por favor ingresa un número válido.")

        # Archivos temporales
        video_temp = os.path.join(RUTA_DESCARGA, "video_temp.webm")
        audio_temp = os.path.join(RUTA_DESCARGA, "audio_temp.m4a")
        salida_final = os.path.join(RUTA_DESCARGA, f"{titulo}.mp4")

        # Descargar video
        ydl_video_opts = {
            "format": formato["format_id"],
            "outtmpl": video_temp,
        }
        print("\n⬇️ Descargando video...")
        with yt_dlp.YoutubeDL(ydl_video_opts) as ydl:
            ydl.download([url])

        # Descargar audio
        ydl_audio_opts = {
            "format": "bestaudio",
            "outtmpl": audio_temp,
        }
        print("⬇️ Descargando audio...")
        with yt_dlp.YoutubeDL(ydl_audio_opts) as ydl:
            ydl.download([url])

        # Combinar con FFmpeg
        print("🔗 Uniendo video + audio...")
        comando = [
            FFMPEG_PATH,
            "-i", video_temp,
            "-i", audio_temp,
            "-c:v", "copy",
            "-c:a", "aac",
            "-y", salida_final
        ]
        subprocess.run(comando, check=True)

        # Borrar temporales
        if os.path.exists(video_temp): os.remove(video_temp)
        if os.path.exists(audio_temp): os.remove(audio_temp)

        print(f"\n✅ ¡Listo! El video con audio está en:\n{salida_final}")


def descargar_mp3(url):
    """Descargar solo audio en MP3"""
    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
        info = ydl.extract_info(url, download=False)
        titulo = info.get("title", "audio_descargado").replace(":", "").replace("|", "").replace("?", "")
        salida_final = os.path.join(RUTA_DESCARGA, f"{titulo}.mp3")

    # Elegir calidad
    print("\n=== 🎵 Calidades disponibles (MP3) ===")
    print("1. 128 kbps")
    print("2. 192 kbps")
    print("3. 320 kbps")
    while True:
        eleccion = input("\n Elige una opción (1-3): ").strip()
        if eleccion == "1": calidad = "128"; break
        elif eleccion == "2": calidad = "192"; break
        elif eleccion == "3": calidad = "320"; break
        else: print("Número inválido.")

    print(f"\n⬇️ Descargando audio en MP3 ({calidad} kbps)...")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": salida_final,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": calidad,
        }],
        "ffmpeg_location": FFMPEG_PATH,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    print(f"\n ¡Listo! El MP3 está en:\n{salida_final}")


if __name__ == "__main__":
    print("=== Descargador YouTube ===")
    url = input("Ingresa el enlace del video: ").strip()

    print("\n1. Descargar como MP4 (video + audio)")
    print("2. Descargar como MP3 (solo audio)")

    opcion = input("\n Elige una opción (1-2): ").strip()

    if opcion == "1":
        descargar_mp4(url)
    elif opcion == "2":
        descargar_mp3(url)
    else:
        print(" Opción inválida.")
