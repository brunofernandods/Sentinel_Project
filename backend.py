import base64
import time
from threading import Thread, Event
import cv2
import flet as ft
from ultralytics import YOLO
import mysql.connector
import os
import subprocess
import winsound


class AlarmThread(Thread):
    def run(self):
        try:
            for i in range(5):
                winsound.Beep(2500, 500)
        except RuntimeError as e:
            print(f"Erro ao acionar o alarme: {e}")


def add_red_border(frame, thickness=10):
    try:
        height, width, _ = frame.shape
        red = (0, 0, 255)
        frame[:thickness, :] = red
        frame[-thickness:, :] = red
        frame[:, :thickness] = red
        frame[:, -thickness:] = red
        return frame
    except ValueError as e:
        print(f"Erro ao adicionar borda vermelha ao quadro: {e}")
        return frame


class VideoCaptureWidget(ft.UserControl):
    def __init__(self, video_path, col, width, save_directory, video_duration_limit=60):
        super().__init__()
        self.img = ft.Image(visible=False, border_radius=10)
        self.pr = ft.ProgressRing(
            stroke_width=5,
            visible=True,
            color="lightblue500",
            width=150,
            height=150
        )
        self.tx = ft.Text("Carregando câmera",
                          style=ft.TextThemeStyle.HEADLINE_SMALL,
                          font_family="Consolas",
                          text_align=ft.TextAlign.CENTER)

        self.video_path = video_path
        self.vid_writer = None
        self.modelo = YOLO('yolov8n.pt')
        self.capture_thread = None
        self.col = col
        self.width = width
        self.should_stop = Event()
        self.frames_with_object_count = 0
        self.detecting_objects = False
        self.alarme_thread = None
        self.video_capture = cv2.VideoCapture(video_path, cv2.CAP_DSHOW)
        self.frames_with_object_count = 0
        self.detecting_objects = False
        self.save_directory = save_directory
        self.video_duration_limit = video_duration_limit
        self.last_save_time = time.time()
        self.camera_number = video_path

    def did_mount(self):
        if self.capture_thread is not None and self.capture_thread.is_alive():
            return
        self.should_stop.clear()
        self.capture_thread = Thread(target=self.capture_video)
        self.capture_thread.start()

    def stop_capture_thread(self):
        self.should_stop.set()

    def capture_video(self):
        try:
            batch_size = 1

            while not self.should_stop.is_set():
                time.sleep(0.005)
                frames = []

                for _ in range(batch_size):
                    check, img = self.video_capture.read()
                    if not check:
                        break
                    frames.append(img)

                if frames:
                    self.process_batch(frames)

                    if self.should_stop.is_set():
                        break

            self.video_capture.release()
        except cv2.error as e:
            print(f"Erro durante a captura de vídeo: {e}")

    def process_batch(self, frames):
        try:
            results = self.modelo.track(frames, conf=0.8, stream=True)

            for result in results:
                annotated_frame = result.plot()
                resized_frame = cv2.resize(annotated_frame, (1000, 700))

                if any(conf >= 0.8 for box in result.boxes for conf in box.conf):
                    resized_frame = add_red_border(resized_frame, thickness=10)

                    if not self.detecting_objects:
                        self.detecting_objects = True
                        self.frames_with_object_count = 1
                    else:
                        self.frames_with_object_count += 1

                        if self.frames_with_object_count >= 50:
                            self.emit_signal()
                else:
                    self.frames_with_object_count = 0
                    self.detecting_objects = False

                im_b64 = base64.b64encode(cv2.imencode('.jpeg', resized_frame)[1]).decode("utf-8")

                self.img.src_base64 = im_b64
                self.pr.visible = False
                self.tx.visible = False
                self.img.visible = True
                self.build()
                self.update()
                self.save_preds(resized_frame)

        except cv2.error as e:
            print(f"Erro durante o processamento de quadros: {e}")

    def build(self):
        return ft.ResponsiveRow([
            ft.Column([self.pr, self.tx, self.img], alignment=ft.MainAxisAlignment.CENTER,
                      horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        ])

    def alarme(self):
        try:
            if self.alarme_thread is None or not self.alarme_thread.is_alive():
                self.alarme_thread = AlarmThread()
                self.alarme_thread.start()
        except RuntimeError as e:
            print(f"Erro ao iniciar o alarme: {e}")

    def emit_signal(self):
        try:
            self.alarme()
        except RuntimeError as e:
            print(f"Erro ao emitir sinal para acionar o alarme: {e}")

    def save_preds(self, frame):
        try:
            # Verifica se o tempo decorrido desde a última gravação excede o limite
            if time.time() - self.last_save_time >= self.video_duration_limit or self.vid_writer is None:
                # Define o caminho para salvar o vídeo dentro do diretório da câmera
                current_time = time.strftime("%Y-%m-%d_%H-%M-%S")
                camera_info = fetch_camera_info(self.camera_number)
                establishment_name = camera_info[1]
                camera_directory = os.path.join(self.save_directory,
                                                f"Câmera-{self.camera_number}-{establishment_name}")
                save_path = os.path.join(camera_directory,
                                         f"Câmera-{self.camera_number}-{establishment_name}-{current_time}.mp4")

                # Verifica se o diretório da câmera existe, senão, cria
                os.makedirs(camera_directory, exist_ok=True)

                # Define as configurações do vídeo
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                fps = 30  # Taxa de quadros por segundo
                frame_width, frame_height = frame.shape[1], frame.shape[0]  # Largura e altura do quadro
                # Inicializa o escritor de vídeo
                self.vid_writer = cv2.VideoWriter(save_path, fourcc, fps, (frame_width, frame_height))
                # Atualiza o tempo da última gravação
                self.last_save_time = time.time()
            # Verifica se self.vid_writer não é None antes de chamar write()
            if self.vid_writer is not None:
                # Escreve o quadro no vídeo
                self.vid_writer.write(frame)
        except Exception as e:
            print(f"Erro ao salvar previsões em vídeo: {e}")


def open_recordings_directory(e):
    recordings_directory = r"C:\Users\Bruno\PycharmProjects\SentinelProject\GravaçõesSENTINEL"
    try:
        os.makedirs(recordings_directory)
    except:
        print('sadadas')
    if os.path.exists(recordings_directory):
        subprocess.Popen(f'explorer "{recordings_directory}"')
    else:
        print(f"Diretório de gravações não encontrado: {recordings_directory}")


def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="sentinel"
    )


def find_camera_numbers():
    db_connection = connect_to_database()

    select_query = "SELECT numero FROM cameras"

    db_cursor = db_connection.cursor()
    db_cursor.execute(select_query)

    available_cams = [result[0] for result in db_cursor.fetchall()]

    db_cursor.close()
    db_connection.close()

    return available_cams


def fetch_camera_info(camera_num):
    db_connection = connect_to_database()

    select_query = "SELECT * FROM cameras WHERE numero = %s"

    db_cursor = db_connection.cursor()
    db_cursor.execute(select_query, (camera_num,))

    camera_info = db_cursor.fetchone()

    db_cursor.close()
    db_connection.close()

    return camera_info


def register_camera(numero, nome_estabelecimento, endereco, ambiente, contato):
    db_connection = connect_to_database()

    insert_query = """
        INSERT INTO cameras (numero, localizacao, endereco, comodo, contato)
        VALUES (%s, %s, %s, %s, %s)
        """

    camera_data = (numero, nome_estabelecimento, endereco, ambiente, contato)

    db_cursor = db_connection.cursor()
    db_cursor.execute(insert_query, camera_data)
    db_connection.commit()

    recordings_directory = r"C:\Users\Bruno\PycharmProjects\SentinelProject\GravaçõesSENTINEL"
    camera_directory = os.path.join(recordings_directory, f"Câmera-{numero}-{nome_estabelecimento}")
    os.makedirs(camera_directory, exist_ok=True)

    db_connection.close()


def delete_camera(numero):
    db_connection = connect_to_database()

    delete_query = "DELETE FROM cameras WHERE numero = %s"

    db_cursor = db_connection.cursor()
    db_cursor.execute(delete_query, (numero,))
    db_connection.commit()

    db_cursor.close()
    db_connection.close()
