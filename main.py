from backend import *


def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.ALWAYS

    def close(e):
        page.window_close()

    def restart_app(e):
        page.clean()
        page.add(main_layout)
        page.update()
        print("Aplicação reiniciada")



    def show_info(cam_info):
        numero, nome_estabelecimento, endereco, ambiente, contato = cam_info

        formatted_info = (
            f"Número: {numero}\n"
            f"Nome do Estabelecimento: {nome_estabelecimento}\n"
            f"Endereço: {endereco}\n"
            f"Ambiente: {ambiente}\n"
            f"Contato: {contato}\n"
        )

        info = ft.BottomSheet(
            ft.Container(
                ft.Column(
                    [
                        ft.Text("Informações da Câmera"),
                        ft.Text(formatted_info)
                    ], tight=True,
                ),
                padding=20,
            ),
            open=True,
        )
        page.overlay.append(info)
        page.update()


    def toggle_icon_button(e):
        e.control.selected = not e.control.selected
        page.theme_mode = (
            ft.ThemeMode.DARK
            if page.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        e.control.update()
        page.update()

    def new_cam(e):
        numero_camera = numero_camera_controller.value
        nome_estabelecimento = nome_estabelecimento_controller.value
        endereco = endereco_controller.value
        ambiente = ambiente_controller.value
        contato = contato_controller.value
        register_camera(numero_camera, nome_estabelecimento, endereco, ambiente, contato)
        info_cam = fetch_camera_info(numero_camera)
        number_cam = int(info_cam[0])
        camera_local = info_cam[1]
        avaliable_cams = find_camera_numbers()
        if len(avaliable_cams) > 1:
            colunas = {"sm": 2, "md": 6, "xl": 6}
        else:
            colunas = {"sm": 2, "md": 11, "xl": 11}
        save_directory = r"C:\Users\Bruno\PycharmProjects\SentinelProject\GravaçõesSENTINEL"
        video_content.append(
            ft.Card(
                ft.Column(
                    [
                        VideoCaptureWidget(
                            video_path=int(numero_camera), col={"sm": 2, "md": 6, "xl": 6},
                            width=2000, save_directory=save_directory),
                        ft.ResponsiveRow([
                            ft.IconButton(icon='ARROW_UPWARD', icon_color='lightblue500',
                                          on_click=lambda
                                          e, camera=number_cam, save_dir=save_directory: show_one(camera, save_dir),
                                          col={"sm": 1, "md": 1, "xl": 1}),
                            ft.PopupMenuButton(
                                items=[ft.PopupMenuItem(icon='INFO_OUTLINED', text="Informações",
                                                        on_click=lambda e, cam_info=info_cam: show_info(cam_info))],
                                tooltip="Informações", col={"sm": 1, "md": 1, "xl": 1}
                            ), ft.Text(f'Câmera {number_cam}:{camera_local}',
                                       style=ft.TextThemeStyle.HEADLINE_SMALL, font_family="Consolas",
                                       text_align=ft.TextAlign.START, col={"sm": 8, "md": 8, "xl": 8})
                        ], col={"sm": 1, "md": 1, "xl": 1}, alignment=ft.MainAxisAlignment.CENTER)],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                col=colunas, data=int(number_cam)))
        cams = find_camera_numbers()
        if len(cams) > 1:
            video_content[0].col = {"sm": 2, "md": 6, "xl": 6}
        page.update()

    # Função para exibir a folha de baixo (bottom sheet) de cadastro de câmera
    def show_bs(e):
        bs.open = True
        bs.update()

    # Definindo os controladores de texto para o cadastro de câmera
    numero_camera_controller = ft.TextField(label="Número da Câmera")
    nome_estabelecimento_controller = ft.TextField(label="Estabelecimento")
    endereco_controller = ft.TextField(label="Endereço")
    ambiente_controller = ft.TextField(label="Ambiente")
    contato_controller = ft.TextField(label="Contato")

    # Folha de baixo (bottom sheet) para o cadastro de câmera
    bs = ft.BottomSheet(
        ft.Container(
            ft.Column(
                [
                    numero_camera_controller,
                    nome_estabelecimento_controller,
                    endereco_controller,
                    ambiente_controller,
                    contato_controller,
                    ft.ElevatedButton(text='Cadastrar', icon='SEND', icon_color='green600',
                                      on_click=new_cam)
                ],
                scroll=ft.ScrollMode.ALWAYS,
            ),
            padding=10,
        ),
        open=False,
    )

    page.overlay.append(bs)

    # Função para excluir uma câmera
    def delete_cam_click(e):
        numero_camera = delete_camera_controller.value
        delete_camera(numero_camera)
        for indexx, cardd in enumerate(video_content):
            if cardd.data == int(numero_camera):
                video_content.pop(indexx)
        available_cams = find_camera_numbers()
        if len(available_cams) == 1:
            video_content[0].col = {"sm": 2, "md": 12, "xl": 12}
        page.update()

    # Função para exibir a folha de baixo (bottom sheet) de exclusão de câmera
    def show_delete_option(e):
        delete_bs.open = True
        delete_bs.update()

    # Função para exibir uma câmera individualmente
    def show_one(selected_camera, save_directory):
        page.clean()
        available_cams = find_camera_numbers()
        selected_camera_info = fetch_camera_info(selected_camera)
        camera_number, establishment_name = selected_camera_info[0], selected_camera_info[1]

        selected_webcam = VideoCaptureWidget(
            video_path=selected_camera,
            col={"sm": 2, "md": 11, "xl": 11},
            width=2000, save_directory=save_directory
        )

        def move_to_previous():
            new_index = (camera_index - 1) % len(available_cams)
            show_one(available_cams[new_index], save_directory)

        def move_to_next():
            new_index = (camera_index + 1) % len(available_cams)
            show_one(available_cams[new_index], save_directory)

        def close_one(e):
            page.clean()
            page.add(main_layout)
            page.update()

        camera_index = available_cams.index(selected_camera)

        camera_info_text = ft.ResponsiveRow([
            ft.Text('', col={"sm": 2, "md": 2, "xl": 2}),
            ft.IconButton(icon='ARROW_BACK', on_click=lambda e: move_to_previous(),
                          icon_color='lightblue500', col={"sm": 1, "md": 1, "xl": 1}),
            ft.PopupMenuButton(
                items=[ft.PopupMenuItem(icon='INFO_OUTLINED', text="Informações",
                                        on_click=lambda e, cam_info=selected_camera_info: show_info(cam_info))],
                tooltip="Informações", col={"sm": 1, "md": 1, "xl": 1}
            ),
            ft.IconButton(icon='ARROW_FORWARD', on_click=lambda e: move_to_next(),
                          icon_color='lightblue500', col={"sm": 1, "md": 1, "xl": 1}),
            ft.IconButton(icon='CLOSE_ROUNDED', on_click=close_one, icon_color='pink600',
                          col={"sm": 1, "md": 1, "xl": 1}),
            ft.Text(f'Câmera {camera_number}:{establishment_name}',
                    style=ft.TextThemeStyle.HEADLINE_SMALL, font_family="Consolas",
                    text_align=ft.TextAlign.START, col={"sm": 6, "md": 6, "xl": 6})
        ], col={"sm": 12, "md": 12, "xl": 12})

        selected_card = ft.Card(
            ft.Column([selected_webcam, camera_info_text], horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                      alignment=ft.MainAxisAlignment.CENTER),
            col={"sm": 2, "md": 11, "xl": 11}, data=selected_camera)

        selected_column = ft.Column([dark_mode, settings, records, reset_app, close_window],
                                    col={"sm": 1, "md": 1, "xl": 1}, alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        selected_layout = ft.ResponsiveRow([selected_column, selected_card],
                                           vertical_alignment=ft.CrossAxisAlignment.CENTER)

        page.add(selected_layout)
        page.update()

    delete_camera_controller = ft.TextField(label="Digite o código da câmera que deseja excluir")

    delete_bs = ft.BottomSheet(
        ft.Container(
            ft.Column(
                [
                    ft.Text("Deletar Câmera!"),
                    delete_camera_controller,
                    ft.ElevatedButton(text='Deletar', icon='DELETE_FOREVER_ROUNDED', icon_color='pink600',
                                      on_click=delete_cam_click)
                ], tight=True, scroll=ft.ScrollMode.ALWAYS,
            ),
            padding=10,
        ),
        open=False,
    )

    page.overlay.append(delete_bs)

    close_window = ft.IconButton(
        icon='EXIT_TO_APP',
        on_click=close,
        tooltip='Sair'
    )

    settings = ft.PopupMenuButton(
        items=[
            ft.PopupMenuItem(icon='ADD_A_PHOTO_ROUNDED', text="Cadastrar Câmera", on_click=show_bs),
            ft.PopupMenuItem(icon='DELETE_FOREVER_ROUNDED', text="Deletar Câmera", on_click=show_delete_option),
        ], tooltip="Configurações"
    )

    records = ft.IconButton(
        icon='CAMERA_OUTDOOR_ROUNDED',
        on_click=open_recordings_directory,
        tooltip='Gravações'
    )

    dark_mode = ft.IconButton(
        icon=ft.icons.DARK_MODE,
        selected_icon=ft.icons.LIGHT_MODE,
        on_click=toggle_icon_button,
        col={"sm": 1, "md": 1, "xl": 1},
        selected=False,
        tooltip='Tema'
    )

    reset_app = ft.IconButton(
        icon='CAMERASWITCH_ROUNDED',
        on_click=restart_app,
        tooltip='Resetar Câmeras',
    )

    available_cams = find_camera_numbers()
    video_content = []

    for index, video in enumerate(available_cams):
        camera_info = fetch_camera_info(video)
        camera_number = camera_info[0]
        establishment_name = camera_info[1]
        if len(available_cams) < 2:
            save_directory = r"C:\Users\Bruno\PycharmProjects\SentinelProject\GravaçõesSENTINEL"
            webcam = VideoCaptureWidget(video_path=int(video),
                                        col={"sm": 2, "md": 11, "xl": 11}, width=2000, save_directory=save_directory)
        else:
            save_directory = r"C:\Users\Bruno\PycharmProjects\SentinelProject\GravaçõesSENTINEL"
            webcam = VideoCaptureWidget(video_path=int(video),
                                        col={"sm": 2, "md": 6, "xl": 6}, width=2000, save_directory=save_directory)
        camera_info_text = ft.ResponsiveRow([
            ft.Text('', col={"sm": 2, "md": 2, "xl": 2}),
            ft.IconButton(icon='ARROW_UPWARD',
                          icon_color='lightblue500',
                          on_click=lambda e, camera=camera_number, save_dir=save_directory: show_one(camera, save_dir),
                          col={"sm": 1, "md": 1, "xl": 1}),
            ft.PopupMenuButton(
                items=[ft.PopupMenuItem(icon='INFO_OUTLINED', text="Informações",
                                        on_click=lambda e, cam_info=camera_info: show_info(cam_info))],
                tooltip="Informações", col={"sm": 1, "md": 1, "xl": 1}
            ), ft.Text(f'Câmera {camera_number}:{establishment_name}',
                       style=ft.TextThemeStyle.HEADLINE_SMALL, font_family="Consolas",
                       text_align=ft.TextAlign.START, col={"sm": 8, "md": 8, "xl": 8})
        ], col={"sm": 1, "md": 1, "xl": 1}, alignment=ft.MainAxisAlignment.CENTER)
        if len(available_cams) < 2:
            card = (ft.Card(ft.Column([webcam, camera_info_text],
                                      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                      alignment=ft.MainAxisAlignment.CENTER),
                            col={"sm": 2, "md": 12, "xl": 12}, data=int(camera_number)))
        else:
            card = (ft.Card(ft.Column([webcam, camera_info_text],
                                      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                      alignment=ft.MainAxisAlignment.CENTER),
                            col={"sm": 2, "md": 6, "xl": 6}, data=int(camera_number)))
        video_content.append(card)

    # Layout da coluna esquerda com botões e configurações
    left_column = ft.Column([dark_mode, settings, records, reset_app, close_window],
                            col={"sm": 1, "md": 1, "xl": 1}, alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    # Layout principal com cards de visualização das câmeras
    main_card = ft.Card(content=ft.ResponsiveRow(video_content, alignment=ft.MainAxisAlignment.CENTER,
                                                 vertical_alignment=ft.CrossAxisAlignment.CENTER),
                        col={"sm": 2, "md": 11, "xl": 11}, )

    main_layout = ft.ResponsiveRow([left_column, main_card], alignment=ft.MainAxisAlignment.CENTER,
                                   vertical_alignment=ft.CrossAxisAlignment.CENTER)

    page.add(main_layout)


ft.app(target=main)