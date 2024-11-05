#TODO: Objetivo 
 # 1. Entender as coordenadas do MediaPipe
 # 2. Converter as coordenadas
 # 3. Distância Euclidiana(1D,2D,3D, n....)
 # 4. Média (calculo do EAR)

import cv2 #pip install opencv-python
#importando mediapipe
import mediapipe as mp #pip install mediapipe
import numpy as np

# capturar a camêra
cap = cv2.VideoCapture(0)

# desenhar os pontos
mp_drawing = mp.solutions.drawing_utils

# coletar solução do Face Mesh
mp_face_mesh = mp.solutions.face_mesh

#FIXME: lista dos pontos do olho esquerdo
p_olho_esq = [385,380,387,373,362,263]
#FIXME: lista dos pontos do olho direito
p_olho_dir = [160,144,158,153,33,133]
p_olhos = p_olho_esq+p_olho_dir

def calculo_ear(face,p_olho_dir,p_olho_esq):
    try:
        face = np.array([[coord.x, coord.y] for coord in face])
        face_esq = face[p_olho_esq,:]
        face_dir = face[p_olho_dir,:]
        ear_esq = (np.linalg.norm(face_esq[0]-face_esq[1])+np.linalg.norm(face_esq[2]-face_esq[3]))/(2*(np.linalg.norm(face_esq[4]-face_esq[5])))
        ear_dir = (np.linalg.norm(face_dir[0]-face_dir[1])+np.linalg.norm(face_dir[2]-face_dir[3]))/(2*(np.linalg.norm(face_dir[4]-face_dir[5])))

    except:
        ear_esq=0.0
        ear_dir=0.0
    media_ear = (ear_esq + ear_dir)/2
    return media_ear

#FIXME:EAR (usando distância euclidiana)







# enquanto a camera estiver aberta
with mp_face_mesh.FaceMesh(min_detection_confidence=0.5,min_tracking_confidence=0.5) as facemesh:
    while cap.isOpened():
        # sucesso é booleana-0 e 1
        sucesso,frame = cap.read()
        if not sucesso:
            print('ignorando o frame vazio da camera')
            continue

            #FIXME: comprimento e largura
        comprimento,largura,_= frame.shape

        # transformando de BGR para RGB
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        # FIXME: processar o frame (OpenCV - MediaPipe) (fixme é quando quer fixar algo, chamar atenção)
        saida_facemesh = facemesh.process(frame)
        # transformando de RGB para BGR
        frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
        # vamos desenhar?
        # 1 - Fizemos a detecção do rosto com facemesh.process(frame)
        # 2 - Agora temos que mostrar essa detecção
        # 3 - Vamos usar o for que é especie de while compacto
        # 4 - Vamos usar multi_face_landmarks :  x,y,z de cada ponto que MediaPipe encontrar no rosto        
        for face_landmarks in saida_facemesh.multi_face_landmarks:
            # desenhando
            # 1 - frame : representa o frame de vídeo
            # 2 - face_landmarks: os landmarks detectados - pontos específicos
            # 3 - FACEMESH_CONTOURS - é uma constante que representa os contornos da face na malha facial.
            # FIXME: face_landmarks - lista de pontos (usado no projeto)
            mp_drawing.draw_landmarks(frame,
                                      face_landmarks,
                                      mp_face_mesh.FACEMESH_CONTOURS,
                                      landmark_drawing_spec=mp_drawing.DrawingSpec(color=(255,102,102),thickness=1,circle_radius=1),
                                      connection_drawing_spec= mp_drawing.DrawingSpec(color=(102,204,0),thickness=1,circle_radius=1)
                                      )    


            #NOTE: Retornando as coordenadas
            # acessando atributo landmark - pontos 
            face = face_landmarks.landmark
            # for    in     enumerate
            for id_coord,coord_xyz in enumerate(face):
                if id_coord in p_olhos:
                    coord_cv = mp_drawing._normalized_to_pixel_coordinates(coord_xyz.x, coord_xyz.y,largura,comprimento)
                    cv2.circle(frame,coord_cv,2,(255,0,0),-1)

            #FIXME: aula_amanha (chamar o calculo EAR )
        cv2.imshow('Camera',frame)

        if cv2.waitKey(10) & 0xFF == ord('c'):
            break
#fecha a captura
cap.release()
cv2.destroyAllWindows()
