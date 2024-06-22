import cv2
import os

def create_video_from_frames(input_folder, output_video, fps):
    # Obtener la lista de archivos en la carpeta de entrada
    files = [f for f in os.listdir(input_folder) if f.endswith('.jpg')]
    files.sort()  # Ordenar los archivos para que se unan en el orden correcto
    
    # Leer la primera imagen para obtener el tamaño del video
    first_frame = cv2.imread(os.path.join(input_folder, files[0]))
    height, width, layers = first_frame.shape
    
    # Crear el objeto VideoWriter
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec para el archivo de salida
    video = cv2.VideoWriter(output_video, fourcc, fps, (width, height))
    
    # Leer y escribir cada frame en el video
    for file in files:
        frame = cv2.imread(os.path.join(input_folder, file))
        video.write(frame)
    
    # Liberar el objeto VideoWriter
    video.release()
    print(f'Video creado con éxito: {output_video}')

# Parámetros
input_folder = './output_images'  # Cambia esto a la ruta de tu carpeta de frames
output_video = 'fabian_video_2.mp4'   # Cambia esto a la ruta donde quieres guardar el video
fps = 30  # Frames por segundo

# Llamar a la función para crear el video
create_video_from_frames(input_folder, output_video, fps)
