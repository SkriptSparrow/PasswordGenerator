import random
import string
import flet as ft
import pyperclip
import webbrowser


# Function to close the dialog
def close_dialog_min(page, dialog):
    dialog.open = False
    page.update()


# Function to show an error dialog
def show_error_dialog(page, message):
    dialog = ft.AlertDialog(
        title=ft.Text("Error!", text_align=ft.TextAlign.CENTER),
        shape=ft.RoundedRectangleBorder(radius=8),
        content=ft.Text(message, text_align=ft.TextAlign.CENTER),
        actions=[
            ft.Container(
                content=ft.TextButton("OK", on_click=lambda e: close_dialog_min(page, dialog)),
                alignment=ft.alignment.center
            )
        ]
    )
    page.overlay.append(dialog)
    dialog.open = True
    page.update()


# function - generate password
def generate_password(page, length=12, use_letters=True,
                      use_digits=True, use_symbols=True):
    """
    Generates a random password of a specified length,
    taking into account the user's settings.
    Args:
        page: The page object
        length (int): Length of the password. Default is 12.
        use_letters (bool): Include letters in the password.
        use_digits (bool): Include digits in the password.
        use_symbols (bool): Include special symbols in the password.
    Returns:
        str: A random password.
    """
    characters = ''
    if use_letters:
        characters += string.ascii_letters
    if use_digits:
        characters += string.digits
    if use_symbols:
        symbols = ['+', '-', '=', '_']
        characters += ''.join(symbols)

    if not characters:
        show_error_dialog(page, "Select at least one character category")
        return ""

    password = ''.join(random.choice(characters) for _ in range(length))
    return password


password_visible = False


def main(page: ft.Page):
    # Set up the main page
    page.window.center()
    page.title = "Password generator"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window.width = 445
    page.window.height = 773
    page.window.resizable = False
    page.window.title_bar_hidden = True
    page.window.frameless = False

    # Set the theme
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary='#00bcd4',
            primary_container='#01a6bb'
        ),
    )

    # function - close dialog function
    def close_dialog(dialog):
        dialog.open = False  # Закрываем диалог
        page.update()

    # Function to open contact information dialog
    def open_nfo_window(e):
        def open_link(url):
            webbrowser.open(url)

        dialog = ft.AlertDialog(
            title=ft.Text("My contacts:", text_align=ft.TextAlign.CENTER),
            shape=ft.RoundedRectangleBorder(radius=8),
            content=ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.icons.EMAIL,
                        tooltip="Email",
                        on_click=lambda e: open_link("mailto:alexgicheva@gmail.com")
                    ),
                    ft.IconButton(
                        icon=ft.icons.SEND,
                        tooltip="Telegram",
                        on_click=lambda e: open_link("https://t.me/Alex_Gicheva")
                    ),
                    ft.IconButton(
                        icon=ft.icons.CODE,  # Замена иконки GitHub
                        tooltip="GitHub",
                        on_click=lambda e: open_link("https://github.com/SkriptSparrow")
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20
            ),
            actions=[
                ft.TextButton("OK", on_click=lambda e: close_dialog(dialog))
            ]
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    # function - minimize the window
    def minimize_window(e):
        page.window.minimized = True
        page.update()

    # function - close the window
    def close_window(e):
        page.window.close()

    # function - button "generate"
    def on_generate_password_click(e):
        try:
            length = int(length_selector.value)
        except ValueError:
            length = 12

        use_letters = letters_switch.value
        use_digits = digits_switch.value
        use_symbols = symbols_switch.value

        password_input.value = generate_password(
            page,
            length,
            use_letters,
            use_digits,
            use_symbols
        )
        page.update()

    # function - password visibility
    def on_toggle_visibility_click(e):
        password_input.password = not password_input.password
        e.control.icon = ft.icons.VISIBILITY if not password_input.password else ft.icons.VISIBILITY_OFF
        page.update()

    # function - copy to clipboard
    def on_copy_password_click(e):
        if password_input.value:
            pyperclip.copy(password_input.value)
            snack_bar = ft.SnackBar(
                ft.Text("Copied to clipboard!"),
                bgcolor=ft.colors.BLACK,
                duration=1000
            )
            page.overlay.append(snack_bar)
            snack_bar.open = True
            page.update()
        else:
            pyperclip.copy(password_input.value)
            snack_bar = ft.SnackBar(ft.Text("Nothing to copy!"),
                                    bgcolor=ft.colors.BLACK,
                                    duration=1000)
            page.overlay.append(snack_bar)
            snack_bar.open = True
            page.update()

    # margins
    margin_top = ft.Container(height=100, width=400)
    margin_img_txt = ft.Container(height=65, width=400)
    margin_middle = ft.Container(height=25, width=400)
    margin_botton = ft.Container(height=5, width=400)

    # Custom buttons for close, maximize, and minimize
    close_button = ft.IconButton(ft.icons.CLOSE, on_click=close_window)
    maximize_button = ft.IconButton(ft.icons.MENU, on_click=open_nfo_window)
    minimize_button = ft.IconButton(ft.icons.REMOVE, on_click=minimize_window)

    # Draggable area for moving the window
    drag_area = ft.WindowDragArea(
        ft.Container(height=50, width=1000),
        expand=True,
        maximizable=False
    )

    # Custom title bar
    title_bar = ft.Row(
        controls=[
            maximize_button,
            drag_area,
            minimize_button,
            close_button
        ],
        alignment=ft.MainAxisAlignment.END,
        vertical_alignment=ft.CrossAxisAlignment.START
    )

    # Adding custom font and image for the password generator.
    page.fonts = {"Rubik": "../fonts/rubik/Rubik-Medium.ttf"}
    image = ft.Image(src="C:\\Users\\Asus\\PycharmProjects\\PasswordGenerator\\img&icons\\password_image.png",
                     width=150,
                     height=150)

    # main title
    title = ft.Text(
        value="PASSWORD GENERATOR",
        font_family="Rubik",
        size=26,
        weight=ft.FontWeight.BOLD,
        color=ft.colors.BLACK,
        text_align=ft.TextAlign.CENTER
    )

    # Column layout containing the image and title
    header_column = ft.Column(
        controls=[image, margin_img_txt, title],
        alignment = ft.MainAxisAlignment.START,
        horizontal_alignment = ft.CrossAxisAlignment.CENTER,
        width=400,
        spacing=0
    )

    # switchers
    letters_switch = ft.Switch(value=True, thumb_icon=ft.icons.TITLE_ROUNDED)
    digits_switch = ft.Switch(value=True, thumb_icon=ft.icons.EXPOSURE_ZERO)
    symbols_switch = ft.Switch(value=True, thumb_icon=ft.icons.ALTERNATE_EMAIL)

    # password length selector
    length_selector = ft.Dropdown(
        label="Password length:",
        options=[
            ft.dropdown.Option("6"),
            ft.dropdown.Option("8"),
            ft.dropdown.Option("10"),
            ft.dropdown.Option("12"),
            ft.dropdown.Option("20")
        ],
        width=350,
        value="12"
    )

    # generated password
    password_input = ft.TextField(
        label="Generated password:",
        width=350,
        height=55,
        read_only=True,
        password=True,
        suffix=ft.IconButton(
            icon=ft.icons.VISIBILITY_OFF,
            on_click=on_toggle_visibility_click
        )
    )

    # button "Generate"
    generate_button = ft.ElevatedButton(
        text="GENERATE",
        color=ft.colors.WHITE,
        bgcolor='#00bcd4',
        on_click=on_generate_password_click,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
    )

    # button "Copy"
    copy_button = ft.ElevatedButton(
        content=ft.Icon(ft.icons.CONTENT_COPY),
        on_click=on_copy_password_click,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
    )

    # footer
    footer = ft.Text(
        "DEVELOPED BY CODEBIRD",
        color=ft.colors.GREY_500,
        width=350,
        text_align=ft.TextAlign.CENTER
    )

    # container - switchers
    switch_row = ft.Row(
        controls=[
            ft.Row([letters_switch]),
            ft.Row([digits_switch]),
            ft.Row([symbols_switch])
        ],
        alignment=ft.MainAxisAlignment.SPACE_AROUND,
        spacing=0
    )

    # container - buttons
    button_row = ft.Row(
        controls=[generate_button, copy_button],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=160)

    # container - all
    container = ft.Column(
        controls=[title_bar, margin_top, header_column, margin_middle,
                  switch_row, length_selector, password_input,
                  button_row, margin_botton, footer],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10
    )

    page.add(container)
    page.update()


ft.app(target=main)
