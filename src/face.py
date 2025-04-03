import face_recognition
import cv2
import os
import numpy as np
from datetime import datetime

def load_known_faces(faces_dir):
    """Carrega todas as imagens de referência do diretório especificado"""
    known_face_encodings = []
    known_face_names = []
    
    # Listar todos os arquivos no diretório
    for filename in os.listdir(faces_dir):
        # Verificar se é uma imagem
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            # Extrair o nome da pessoa do nome do arquivo (sem extensão)
            name = os.path.splitext(filename)[0].replace("_", " ")
            
            # Caminho completo para a imagem
            image_path = os.path.join(faces_dir, filename)
            
            # Carregar a imagem
            print(f"Carregando imagem de: {name}")
            image = face_recognition.load_image_file(image_path)
            
            # Detectar faces na imagem
            face_locations = face_recognition.face_locations(image, model="hog")  # Use "cnn" para maior precisão, se tiver GPU
            
            if len(face_locations) > 0:
                # Usar a primeira face encontrada
                encoding = face_recognition.face_encodings(image, face_locations)[0]
                known_face_encodings.append(encoding)
                known_face_names.append(name)
                print(f"Face de {name} adicionada com sucesso!")
            else:
                print(f"Nenhuma face detectada na imagem de {name}!")
    
    return known_face_encodings, known_face_names

def log_attendance(name):
    """Registra a presença da pessoa em um arquivo CSV"""
    now = datetime.now()
    date_string = now.strftime("%Y-%m-%d")
    time_string = now.strftime("%H:%M:%S")
    
    # Criar diretório de logs se não existir
    log_dir = "../logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Nome do arquivo baseado na data atual
    log_file = os.path.join(log_dir, f"attendance_{date_string}.csv")
    
    # Verificar se o arquivo existe, se não, criar com cabeçalho
    if not os.path.exists(log_file):
        with open(log_file, 'w') as f:
            f.write("Nome,Data,Hora\n")
    
    # Registrar presença (evitar duplicatas na mesma sessão)
    if name not in attendance_log:
        with open(log_file, 'a') as f:
            f.write(f"{name},{date_string},{time_string}\n")
        attendance_log.add(name)
        return True
    return False

# Diretório onde estão as imagens das pessoas conhecidas
faces_dir = "../img/known_faces"

# Verificar se o diretório existe
if not os.path.exists(faces_dir):
    os.makedirs(faces_dir)
    print(f"Diretório {faces_dir} criado. Adicione imagens de faces conhecidas nele.")
    print("Cada imagem deve conter apenas uma face e ser nomeada como NOME_SOBRENOME.jpg")
    exit()

# Carregar todas as faces conhecidas
known_face_encodings, known_face_names = load_known_faces(faces_dir)

if len(known_face_encodings) == 0:
    print("Nenhuma face conhecida foi carregada. Adicione imagens ao diretório.")
    exit()

print(f"Total de {len(known_face_names)} pessoas carregadas: {', '.join(known_face_names)}")

# Captura de vídeo e reconhecimento
cap = cv2.VideoCapture(0)

# Configurações para melhorar a performance
process_this_frame = True

# Conjunto para rastrear pessoas que já tiveram presença registrada
attendance_log = set()

# Configurações de visualização
show_fps = True
last_time = datetime.now()
fps = 0
frame_count = 0

# Contador para estabilizar o reconhecimento
face_recognition_counter = {}

while True:
    ret, frame = cap.read()
    if not ret:
        print("Falha ao capturar imagem da câmera")
        break
    
    # Calcular FPS
    if show_fps:
        frame_count += 1
        current_time = datetime.now()
        time_diff = (current_time - last_time).total_seconds()
        
        if time_diff >= 1.0:
            fps = frame_count / time_diff
            frame_count = 0
            last_time = current_time
    
    # Processar apenas um a cada dois frames para economizar processamento
    if process_this_frame:
        # Redimensionar o frame para melhorar a performance
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        # Converter de BGR (OpenCV) para RGB (face_recognition)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Detectar faces no vídeo
        face_locations = face_recognition.face_locations(rgb_small_frame)
        
        # Só processar encodings se encontrou faces
        face_names = []
        if face_locations:
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            for i, face_encoding in enumerate(face_encodings):
                # Comparar com rostos conhecidos
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.6)
                name = "Desconhecido"
                
                # Usar distância facial para encontrar a melhor correspondência
                if len(known_face_encodings) > 0:
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    
                    # Se a melhor correspondência for boa o suficiente
                    if matches[best_match_index] and face_distances[best_match_index] < 0.6:
                        name = known_face_names[best_match_index]
                        
                        # Incrementar contador para estabilização
                        face_key = f"{i}_{name}"
                        if face_key in face_recognition_counter:
                            face_recognition_counter[face_key] += 1
                        else:
                            # Inicializar contador para todas as possíveis identidades
                            for known_name in known_face_names:
                                face_recognition_counter[f"{i}_{known_name}"] = 0
                            face_recognition_counter[face_key] = 1
                            
                        # Se a mesma pessoa foi reconhecida por 3 frames consecutivos
                        if face_recognition_counter[face_key] >= 3:
                            # Registrar presença quando uma pessoa é reconhecida
                            if name != "Desconhecido" and log_attendance(name):
                                print(f"Presença registrada: {name} às {datetime.now().strftime('%H:%M:%S')}")
                
                face_names.append(name)
        
        # Limpar contadores de faces que não estão mais presentes
        current_face_keys = set()
        for i, name in enumerate(face_names):
            if name != "Desconhecido":
                current_face_keys.add(f"{i}_{name}")
        
        # Remover contadores de faces ausentes
        keys_to_remove = []
        for key in face_recognition_counter:
            if key.split('_')[0] not in [str(i) for i in range(len(face_names))]:
                keys_to_remove.append(key)
        
        for key in keys_to_remove:
            del face_recognition_counter[key]
    
    process_this_frame = not process_this_frame
    
    # Exibir os resultados
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Redimensionar as coordenadas da face para o tamanho original
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Desenhar a caixa de correspondência
        color = (0, 255, 0) if name != "Desconhecido" else (0, 0, 255)  # Verde para conhecido, vermelho para desconhecido
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        
        # Desenhar uma caixa para o nome
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
        cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

    # Mostrar FPS
    if show_fps:
        cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    # Mostrar contador de pessoas reconhecidas
    recognized_count = len([n for n in face_names if n != "Desconhecido"])
    total_count = len(face_names)
    cv2.putText(frame, f"Pessoas: {recognized_count}/{total_count}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    # Mostrar o resultado
    cv2.imshow('Reconhecimento Facial', frame)

    # Sair com a tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
