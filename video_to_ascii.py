import imageio
import numpy as np
import time
import sys
import os

class AsciiVideo:
    def __init__(self, video_path, ascii_chars_file):
        # leer el archivo de caracteres ascii
        with open(ascii_chars_file) as f:
            self.ascii_chars = [c for c in list(f.read()) if c != '\n']

        self.video_path = video_path

    def generate_frames(self):
        # Cargar video con imageio
        vid = imageio.get_reader(self.video_path)

        # Obtener FPS del video
        self.fps = vid.get_meta_data()["fps"]

        # Inicializar arreglo de frames
        self.ascii_frames = []

        self.num_frames = len(vid)

        i = 0

        # Procesar cada frame del video
        for frame in vid:
            ascii_frame  = self._convert_frame_to_ascii(frame, i)

            # Agregar el frame convertido en ASCII a la lista
            self.ascii_frames.append(ascii_frame)
            i += 1
        return self.ascii_frames

    def play_frames(self):
        # Leer y mostrar cada frame en un bucle infinito
        while True:
            for ascii_frame in self.ascii_frames:
                # Sobreescribir lo que haya en la consola
                print(ascii_frame, end="\r")
                time.sleep(1/self.fps) # agregar un retraso para la animación

    def _convert_frame_to_ascii(self, frame, currentFrameIndex):
        # Reducir la resolución del frame
        # frame = frame[::8, ::4]
        frame = frame[::8, ::4]

        # Convertir el frame a escala de grises
        frame = np.dot(frame[...,:3], [0.2989, 0.5870, 0.1140])

        # Escalar los valores del frame al rango de valores de los caracteres ASCII
        frame = (frame / 255) * (len(self.ascii_chars) - 1)

        # Convertir los valores del frame a caracteres ASCII
        ascii_frame = ""

        i = 0
        frameLines = len(frame)
        for row in frame:
            ascii_row = "".join([self.ascii_chars[int(round(x))] for x in row])
            ascii_frame += ascii_row + "\n"

            # Imprime el porcentaje de procesamiento
            status = self._get_status_bar(frameLines, currentFrameIndex, self.num_frames, i)
            print(status, end="\r")
            i += 1

        return ascii_frame

    def _get_status_bar(self, num_lines, current_frame_idx, total_frames, current_line):
        progress_percent = int(current_line * num_lines / 100)
        status_bar = "[" + "#" * progress_percent + "-" * (num_lines - progress_percent) + "]"
        status = f"{status_bar} {current_frame_idx + 1}/{total_frames} frames procesados"
        return status

if __name__ == "__main__":
    video_path = input("Nombre del video (default video.mp4): ") or "video.mp4"
    ascii_path = "ascii.txt"
    video = AsciiVideo(video_path, ascii_path)
    video.generate_frames()
    video.play_frames()