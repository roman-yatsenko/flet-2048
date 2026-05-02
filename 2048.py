import random

import flet as ft

N = 4
TILE_SIZE = 100
TILE_GAP = 10
PADDING = 20

BOARD_INNER = N * TILE_SIZE + (N + 1) * TILE_GAP
BOARD_OUTER = BOARD_INNER + 2 * TILE_GAP
WINDOW_WIDTH = BOARD_OUTER + 2 * PADDING
WINDOW_HEIGHT = BOARD_OUTER + 2 * PADDING + 185

WIN_VALUE = 2048


class Game2048:
    """Клас стану гри 2048: поле, очки та поточний статус."""

    def __init__(self) -> None:
        """Ініціалізує порожнє поле 4x4 та стартові значення гри."""
        self.reset()

    def reset(self) -> None:
        """Скидає гру: очищає поле, обнуляє очки, стан та додає 2 стартові плитки."""
        self.board: list[list[int]] = [[0] * N for _ in range(N)]
        self._bard_prev: list[list[int]] = [[0] * N for _ in range(N)]
        self.score = 0
        self._score_prev = 0
        self.state = "playing"
        self.add_random_tile()
        self.add_random_tile()

    def add_random_tile(self) -> None:
        """Додає випадкову плитку (2 або 4) у випадкову порожню клітинку поля."""
        empty = [(r, c) for r in range(N) for c in range(N) if self.board[r][c] == 0]

        if empty:
            r, c = random.choice(empty)
            self.board[r][c] = 2 if random.random() < 0.9 else 4


def main(page: ft.Page) -> None:
    """Головна функція, яка налаштовує вікно та інтерфейс гри."""
    page.title = "2048"
    page.window.width = WINDOW_WIDTH
    page.window.height = WINDOW_HEIGHT
    page.window.resizable = False
    page.bgcolor = ft.Colors.BROWN_50
    page.padding = ft.Padding.all(PADDING)

    game = Game2048()

    cell_texts = [
        [
            ft.Text(
                "",
                size=28,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BROWN_500,
                width=TILE_SIZE,
                text_align=ft.TextAlign.CENTER,
            )
            for _ in range(N)
        ]
        for _ in range(N)
    ]
    score_text = ft.Text(
        f"Очки: {game.score}",
        size=20,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.BROWN_500,
    )

    def refresh_ui() -> None:
        """Оновлює значення плиток і текст очок в інтерфейсі."""
        for r in range(N):
            for c in range(N):
                v = game.board[r][c]
                cell_texts[r][c].value = str(v) if v else "."
        score_text.value = f"Очки: {game.score}"
        page.update()

    refresh_ui()

    grid = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(controls=cell_texts[r], spacing=TILE_GAP) for r in range(N)
            ],
            spacing=TILE_GAP,
        ),
        bgcolor=ft.Colors.BROWN_200,
        padding=ft.Padding.all(TILE_GAP),
        border_radius=8,
    )

    def on_restart(e: ft.ControlEvent) -> None:
        """Перезапускає гру та оновлює інтерфейс."""
        game.reset()
        refresh_ui()

    restart_btn = ft.Button(
        content="Нова гра",
        on_click=on_restart,
        style=ft.ButtonStyle(
            bgcolor={"": ft.Colors.BROWN_400}, color={"": ft.Colors.GREY_50}
        ),
    )

    page.add(
        ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text(
                            "2048",
                            size=48,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BROWN_500,
                        ),
                        ft.Column(
                            controls=[score_text, restart_btn],
                            horizontal_alignment=ft.CrossAxisAlignment.END,
                            spacing=4,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                grid,
            ],
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )


ft.run(main)
