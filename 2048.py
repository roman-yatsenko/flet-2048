import flet as ft

N = 4
TILE_SIZE = 100
TILE_GAP = 10
PADDING = 20

BOARD_INNER = N * TILE_SIZE + (N + 1) * TILE_GAP
BOARD_OUTER = BOARD_INNER + 2 * TILE_GAP
WINDOW_WIDTH = BOARD_OUTER + 2 * PADDING
WINDOW_HEIGHT = BOARD_OUTER + 2 * PADDING + 185


def main(page: ft.Page) -> None:
    """Головна функція, яка налаштовує вікно та інтерфейс гри."""
    page.title = "2048"
    page.window.width = WINDOW_WIDTH
    page.window.height = WINDOW_HEIGHT
    page.window.resizable = False
    page.bgcolor = ft.Colors.BROWN_50
    page.padding = ft.Padding.all(PADDING)

    page.add(ft.Text("Привіт, 2048!", size=48, weight=ft.FontWeight.BOLD))


ft.run(main)
