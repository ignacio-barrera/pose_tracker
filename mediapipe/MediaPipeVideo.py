import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

video_path = '11_28_22-player9.webm'
cap = cv2.VideoCapture(video_path)

# Obtener las dimensiones del video
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
print("FPS del video original:", fps)  # Imprimir el FPS para verificar

# Crear el objeto VideoWriter
output_path = 'output.mp4'
fourcc = cv2.VideoWriter_fourcc(*'avc1')  # Cambiar el códec a H.264
out = cv2.VideoWriter(output_path, fourcc, 30, (width, height))

## Configurar la instancia de mediapipe
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Recolorar la imagen a RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
      
        # Realizar la detección
        results = pose.process(image)
    
        # Recolorar de vuelta a BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Dibujar los landmarks
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        
        # Opcional: comentar esta línea si no es necesario visualizar durante el procesamiento
        # cv2.imshow("test", image)
        
        # Guardar el frame en el video
        out.write(image)

        # Opcional: ajustar el tiempo de espera a 1 ms para reducir el impacto en la visualización
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
