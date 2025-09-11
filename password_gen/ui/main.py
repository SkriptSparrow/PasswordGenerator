import importlib.resources as res
import webbrowser

import flet as ft
import pyperclip

from password_gen.generator.generator import generate_password
from password_gen.generator.strength import check_strength


def main(page: ft.Page):
    # Window setup
    page.window.center()
    page.title = "Password generator"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window.width = 445
    page.window.height = 773
    page.window.resizable = False
    page.window.title_bar_hidden = True
    page.window.frameless = False
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(primary="#00bcd4", primary_container="#01a6bb")
    )

    # Dialog helpers
    def close_dialog(dialog):
        dialog.open = False
        page.update()

    def open_nfo_window(e):
        def open_link(url):
            webbrowser.open(url)

        dialog = ft.AlertDialog(
            title=ft.Text("My contacts:", text_align=ft.TextAlign.CENTER),
            shape=ft.RoundedRectangleBorder(radius=8),
            content=ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.Icons.EMAIL,
                        tooltip="Email",
                        on_click=lambda e: open_link("mailto:alexgicheva@gmail.com"),
                    ),
                    ft.IconButton(
                        icon=ft.Icons.SEND,
                        tooltip="Telegram",
                        on_click=lambda e: open_link("https://t.me/Alex_Gicheva"),
                    ),
                    ft.IconButton(
                        icon=ft.Icons.CODE,
                        tooltip="GitHub",
                        on_click=lambda e: open_link(
                            "https://github.com/SkriptSparrow"
                        ),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            ),
            actions=[ft.TextButton("OK", on_click=lambda e: close_dialog(dialog))],
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    # Window controls
    def minimize_window(e):
        page.window.minimized = True
        page.update()

    def close_window(e):
        page.window.close()

    # Button actions
    def on_generate_password_click(e):
        try:
            length = int(length_selector.value)
        except ValueError:
            length = 12

        try:
            password_input.value = generate_password(
                length, letters_switch.value, digits_switch.value, symbols_switch.value
            )
            strength_label.value = f"Strength: {check_strength(password_input.value)}"
        except ValueError as err:
            password_input.value = ""
            strength_label.value = str(err)

        strength = check_strength(password_input.value)
        strength_color.visible = True

        if strength == "weak":
            strength_color.bgcolor = ft.Colors.RED
            strength_label.value = "Strength: Weak"
            strength_label.color = ft.Colors.RED
            strength_container.border = ft.border.all(1, ft.Colors.RED)
        elif strength == "fair":
            strength_color.bgcolor = ft.Colors.ORANGE
            strength_label.value = "Strength: Fair"
            strength_label.color = ft.Colors.ORANGE
            strength_container.border = ft.border.all(1, ft.Colors.ORANGE)
        else:  # strong
            strength_color.bgcolor = ft.Colors.GREEN
            strength_label.value = "Strength: Strong"
            strength_label.color = ft.Colors.GREEN
            strength_container.border = ft.border.all(1, ft.Colors.GREEN)

        page.update()

    def on_toggle_visibility_click(e):
        password_input.password = not password_input.password
        e.control.icon = (
            ft.Icons.VISIBILITY
            if not password_input.password
            else ft.Icons.VISIBILITY_OFF
        )
        page.update()

    def on_copy_password_click(e):
        if password_input.value:
            pyperclip.copy(password_input.value)
            snack_bar = ft.SnackBar(
                ft.Text("Copied to clipboard!"), bgcolor=ft.Colors.BLACK, duration=1000
            )
        else:
            snack_bar = ft.SnackBar(
                ft.Text("Nothing to copy!"), bgcolor=ft.Colors.BLACK, duration=1000
            )
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()

    # Layout parts
    margin_top = ft.Container(height=100, width=400)
    margin_img_txt = ft.Container(height=65, width=400)
    margin_middle = ft.Container(height=25, width=400)
    margin_botton = ft.Container(height=5, width=400)

    close_button = ft.IconButton(ft.Icons.CLOSE, on_click=close_window)
    maximize_button = ft.IconButton(ft.Icons.MENU, on_click=open_nfo_window)
    minimize_button = ft.IconButton(ft.Icons.REMOVE, on_click=minimize_window)

    drag_area = ft.WindowDragArea(
        ft.Container(height=50, width=1000), expand=True, maximizable=False
    )

    title_bar = ft.Row(
        controls=[maximize_button, drag_area, minimize_button, close_button],
        alignment=ft.MainAxisAlignment.END,
        vertical_alignment=ft.CrossAxisAlignment.START,
    )

    font_path = res.files("password_gen").joinpath(
        "assets/fonts/rubik/Rubik-Medium.ttf"
    )
    page.fonts = {"Rubik": str(font_path)}
    img_path = res.files("password_gen").joinpath("assets/images/logo.png")
    image = ft.Image(src=str(img_path), width=150, height=150)

    title = ft.Text(
        value="PASSWORD GENERATOR",
        font_family="Rubik",
        size=26,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.BLACK,
        text_align=ft.TextAlign.CENTER,
    )

    header_column = ft.Column(
        controls=[image, margin_img_txt, title],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        width=400,
        spacing=0,
    )

    letters_switch = ft.Switch(value=True, thumb_icon=ft.Icons.TITLE_ROUNDED)
    digits_switch = ft.Switch(value=True, thumb_icon=ft.Icons.EXPOSURE_ZERO)
    symbols_switch = ft.Switch(value=True, thumb_icon=ft.Icons.ALTERNATE_EMAIL)

    length_selector = ft.Dropdown(
        label="Password length:",
        options=[ft.dropdown.Option(str(n)) for n in [6, 8, 10, 12, 20]],
        width=350,
        value="12",
    )

    password_input = ft.TextField(
        label="Generated password:",
        width=350,
        height=55,
        read_only=True,
        password=True,
        suffix=ft.IconButton(
            icon=ft.Icons.VISIBILITY_OFF, on_click=on_toggle_visibility_click
        ),
    )

    generate_button = ft.ElevatedButton(
        text="GENERATE",
        color=ft.Colors.WHITE,
        bgcolor="#00bcd4",
        on_click=on_generate_password_click,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
    )

    copy_button = ft.ElevatedButton(
        content=ft.Icon(ft.Icons.CONTENT_COPY),
        on_click=on_copy_password_click,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
    )

    footer = ft.Text(
        "DEVELOPED BY CODEBIRD",
        color=ft.Colors.GREY_500,
        width=350,
        text_align=ft.TextAlign.CENTER,
    )

    switch_row = ft.Row(
        controls=[
            ft.Row([letters_switch]),
            ft.Row([digits_switch]),
            ft.Row([symbols_switch]),
        ],
        alignment=ft.MainAxisAlignment.SPACE_AROUND,
        spacing=0,
    )

    # индикатор силы
    strength_color = ft.Container(
        width=12,
        height=12,
        border_radius=6,
        bgcolor=None,  # пусто, пока пароль не сгенерирован
        visible=False,  # кружок скрыт
    )

    strength_label = ft.Text(
        "Strength", color=ft.Colors.BLACK, text_align=ft.TextAlign.CENTER
    )

    strength_row = ft.Row(
        controls=[strength_color, strength_label],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=8,
    )

    strength_container = ft.Container(
        content=strength_row,
        padding=5,
        border_radius=8,
        border=ft.border.all(1, ft.Colors.BLACK),  # по умолчанию weak
        width=190,
        alignment=ft.alignment.center,
    )

    button_row = ft.Row(
        controls=[generate_button, strength_container, copy_button],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10,
    )

    container = ft.Column(
        controls=[
            title_bar,
            margin_top,
            header_column,
            margin_middle,
            switch_row,
            length_selector,
            password_input,
            button_row,
            margin_botton,
            footer,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
    )

    page.add(container)
    page.update()


if __name__ == "__main__":
    import multiprocessing as mp

    mp.freeze_support()
    ft.app(target=main)
