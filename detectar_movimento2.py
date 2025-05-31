import cv2
import numpy as np
from datetime import datetime, timedelta

# Variáveis globais
drawing = False
points = []
roi_mask = None

def draw_roi(event, x, y, flags, param):
    global drawing, points, roi_mask
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        points = [(x, y)]
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            points.append((x, y))
            temp_img = param['frame'].copy()
            if len(points) > 1:
                cv2.polylines(temp_img, [np.array(points)], False, (0, 255, 0), 2)
            cv2.imshow("Selecione a área do seu carro", temp_img)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        if len(points) > 2:
            temp_img = param['frame'].copy()
            cv2.polylines(temp_img, [np.array(points)], True, (0, 255, 0), 2)
            cv2.imshow("Selecione a área do seu carro", temp_img)
            mask = np.zeros_like(temp_img[:, :, 0])
            cv2.fillPoly(mask, [np.array(points)], 255)
            roi_mask = mask

def get_roi_from_user(video_path):
    global roi_mask, points
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    if not ret:
        print("Erro ao ler o vídeo")
        return None
    
    frame = cv2.resize(frame, (1280, 720))
    
    cv2.namedWindow("Selecione a área do seu carro")
    cv2.setMouseCallback("Selecione a área do seu carro", draw_roi, {'frame': frame})
    
    instructions = [
        "INSTRUÇÕES:",
        "1. Clique e arraste para desenhar ao redor do seu carro",
        "2. Solte o botão para finalizar",
        "3. Pressione 'S' para confirmar",
        "4. Pressione 'Q' para cancelar"
    ]
    
    for i, text in enumerate(instructions):
        cv2.putText(frame, text, (10, 30 + i*30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    cv2.imshow("Selecione a área do seu carro", frame)
    
    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s') and roi_mask is not None:
            break
        elif key == ord('q'):
            roi_mask = None
            break
    
    cv2.destroyAllWindows()
    cap.release()
    
    if roi_mask is not None:
        return {
            'mask': roi_mask,
            'points': points,
            'original_size': (frame.shape[1], frame.shape[0])
        }
    return None

def detect_movement(prev_frame, current_frame, roi_data):
    if roi_data is None:
        return False
    
    try:
        scale_x = current_frame.shape[1] / roi_data['original_size'][0]
        scale_y = current_frame.shape[0] / roi_data['original_size'][1]
        
        # Redimensiona os pontos e cria nova máscara
        scaled_points = [(int(x * scale_x), int(y * scale_y)) for x, y in roi_data['points']]
        mask = np.zeros((current_frame.shape[0], current_frame.shape[1]), dtype=np.uint8)
        cv2.fillPoly(mask, [np.array(scaled_points)], 255)
        
        prev_roi = cv2.bitwise_and(prev_frame, prev_frame, mask=mask)
        curr_roi = cv2.bitwise_and(current_frame, current_frame, mask=mask)
        
        prev_gray = cv2.cvtColor(prev_roi, cv2.COLOR_BGR2GRAY)
        curr_gray = cv2.cvtColor(curr_roi, cv2.COLOR_BGR2GRAY)
        
        frame_diff = cv2.absdiff(prev_gray, curr_gray)
        _, thresh = cv2.threshold(frame_diff, 25, 255, cv2.THRESH_BINARY)
        
        kernel = np.ones((5, 5), np.uint8)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        
        movement_ratio = np.sum(thresh) / np.sum(mask > 0)
        return movement_ratio > 0.001
        
    except Exception as e:
        print(f"Erro ao detectar movimento: {str(e)}")
        return False

def analyze_video(video_path, roi_data):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Erro ao abrir o vídeo")
        return []
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    movement_events = []
    current_event_start = None
    prev_frame = None
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            if prev_frame is None:
                prev_frame = frame.copy()
                continue
            
            frame_count = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
            
            if frame_count % int(fps * 5) == 0:
                movement = detect_movement(prev_frame, frame, roi_data)
                current_time = frame_count / fps
                
                if movement:
                    if current_event_start is None:
                        current_event_start = current_time
                        print(f"Movimento detectado em {timedelta(seconds=current_time)}")
                else:
                    if current_event_start is not None:
                        movement_events.append((current_event_start, current_time))
                        current_event_start = None
            
            prev_frame = frame.copy()
            
    except Exception as e:
        print(f"Erro durante a análise: {str(e)}")
    
    finally:
        cap.release()
        if current_event_start is not None:
            movement_events.append((current_event_start, cap.get(cv2.CAP_PROP_POS_FRAMES) / fps))
    
    return movement_events

if __name__ == "__main__":
    video_path = "estacionamento.mp4"
    
    print("Selecione a área do seu carro no vídeo...")
    roi_data = get_roi_from_user(video_path)
    if not roi_data:
        print("Seleção cancelada ou inválida")
        exit()
    
    print("\nAnalisando o vídeo... Isso pode levar várias horas")
    print("Pressione Ctrl+C para parar a execução e salvar os resultados parciais\n")
    
    try:
        events = analyze_video(video_path, roi_data)
        
        with open("movimentos_detectados.txt", "w") as f:
            f.write("Horários com movimento detectado:\n")
            for start, end in events:
                f.write(f"{timedelta(seconds=start)} - {timedelta(seconds=end)}\n")
        
        print("\nAnálise concluída. Resultados salvos em 'movimentos_detectados.txt'")
    
    except KeyboardInterrupt:
        print("\nAnálise interrompida pelo usuário. Salvando resultados parciais...")
        with open("movimentos_parciais.txt", "w") as f:
            f.write("Resultados parciais:\n")
            for start, end in events:
                f.write(f"{timedelta(seconds=start)} - {timedelta(seconds=end)}\n")
        print("Resultados parciais salvos em 'movimentos_parciais.txt'")