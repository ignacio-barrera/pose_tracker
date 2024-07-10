# Esta carpeta contiene los archivos desarrollados con BlazePose.

El archivo final que incluye se basa en el suavizado entre frames se encuentra en **stepDetectionFinal.ipynb**, este archivo marca con verde la pisada y dibuja la estimación de pose del sujeto. El resultado de este código se guarda en la carpeta output:
- output
    - frames (carpeta donde se guarda cada frame procesado)
    - frames_info.json (información si el sujeto pisa o no y con que pie lo hace)
    - output4.mp4 (video resultante)

El archivo **testBlazePose.ipynb** contiene los códigos probados que:

-Convierten los puntos detectados de BlazePose a formato COCO para posterior evaluación

-Cuenta pasos segun umbral dado de frames, incluye direccionalidad del movimiento y si el sujeto esta quieto o no.
El código final funcional de estas pruebas se puede encontrar en **stepDetectionBlazePose**. Este archivo sirve para continuar con el trabajo de identificar movimiento e intersección al punto o marca del suelo 
