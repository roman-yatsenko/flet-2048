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

    def add_random_tile(self) -> None:
        """Додає випадкову плитку (2 або 4) у випадкову порожню клітинку поля."""
        empty = [(r, c) for r in range(N) for c in range(N) if self.board[r][c] == 0]

        if empty:
            r, c = random.choice(empty)
            self.board[r][c] = 2 if random.random() < 0.9 else 4

    def move_left(self) -> bool:
        """Виконує хід вліво для всіх рядків поля.

        Перед обробкою зберігає попередній стан для `undo()`. Для кожного
        рядка застосовує стискання/злиття, додає набрані очки та визначає,
        чи змінилося поле. Повертає `True`, якщо хоча б один рядок змінився.
        """
        self._save()
        changed = False
        for r in range(N):
            new_row, gained = self._process_row(self.board[r][:])
            self.score += gained
            if new_row != self.board[r]:
                changed = True
            self.board[r] = new_row
        return changed

    def move_right(self) -> bool:
        """Виконує хід вправо для всіх рядків поля.

        Перед обробкою зберігає попередній стан для `undo()`. Для кожного
        рядка виконує обробку в реверсі (еквівалент ходу вліво), повертає
        результат у вихідний порядок, додає набрані очки та визначає,
        чи змінилося поле. Повертає `True`, якщо хоча б один рядок змінився.
        """
        self._save()
        changed = False
        for r in range(N):
            new_row, gained = self._process_row(self.board[r][::-1])
            new_row = new_row[::-1]
            self.score += gained
            if new_row != self.board[r]:
                changed = True
            self.board[r] = new_row
        return changed

    def move_up(self) -> bool:
        """Виконує хід вгору для всіх стовпців поля.

        Перед обробкою зберігає попередній стан для `undo()`. Для кожного
        стовпця застосовує стискання/злиття, додає набрані очки та визначає,
        чи змінилося поле. Повертає `True`, якщо хоча б один стовпець змінився.
        """
        self._save()
        changed = False
        for c in range(N):
            col = [self.board[r][c] for r in range(N)]
            new_col, gained = self._process_row(col)
            self.score += gained
            if new_col != col:
                changed = True
            for r in range(N):
                self.board[r][c] = new_col[r]
        return changed

    def move_down(self) -> bool:
        """Виконує хід вниз для всіх стовпців поля.

        Перед обробкою зберігає попередній стан для `undo()`. Для кожного
        стовпця виконує обробку у зворотному порядку (еквівалент ходу вгору),
        повертає результат у вихідний порядок, додає набрані очки та визначає,
        чи змінилося поле. Повертає `True`, якщо хоча б один стовпець змінився.
        """
        self._save()
        changed = False
        for c in range(N):
            col = [self.board[r][c] for r in range(N)]
            new_col, gained = self._process_row(col[::-1])
            new_col = new_col[::-1]
            self.score += gained
            if new_col != col:
                changed = True
            for r in range(N):
                self.board[r][c] = new_col[r]
        return changed

    def reset(self) -> None:
        """Скидає гру: очищає поле, обнуляє очки, стан та додає 2 стартові плитки."""
        self.board: list[list[int]] = [[0] * N for _ in range(N)]
        self._board_prev: list[list[int]] = [[0] * N for _ in range(N)]
        self.score = 0
        self._score_prev = 0
        self.state = "playing"
        self.add_random_tile()
        self.add_random_tile()

    def undo(self) -> None:
        """Відкочує гру до попереднього стану поля та очок."""
        self.board = [row[:] for row in self._board_prev]
        self.score = self._score_prev
        self.state = "playing"

    @staticmethod
    def _compress(row: list[int]) -> list[int]:
        """Стискає рядок вліво: прибирає нулі та доповнює рядок нулями до довжини N."""
        result = [x for x in row if x != 0]
        result += [0] * (N - len(result))
        return result

    def _merge(self, row: list[int]) -> tuple[list[int], int]:
        """Об'єднує сусідні однакові значення в рядку та рахує отримані очки.

        Прохід виконується зліва направо. Якщо дві сусідні плитки рівні та
        не були об'єднані на попередньому кроці, ліва плитка подвоюється,
        права зануляється. Повертає змінений рядок і кількість очок,
        набраних саме під час цього злиття.
        """
        gained = 0
        merged = False
        for i in range(N - 1):
            if row[i] != 0 and row[i] == row[i + 1] and not merged:
                row[i] *= 2
                gained += row[i]
                row[i + 1] = 0
                merged = True
                if row[i] >= WIN_VALUE:
                    self.state = "won"
            else:
                merged = False
        return row, gained

    def _process_row(self, row: list[int]) -> tuple[list[int], int]:
        """Обробляє один рядок для ходу вліво: стискання, злиття, повторне стискання.

        Повертає оновлений рядок та кількість очок, набраних під час злиття.
        """
        row = self._compress(row)
        row, gained = self._merge(row)
        row = self._compress(row)
        return row, gained

    def _save(self) -> None:
        """Зберігає попередній стан поля та очок для можливого відкату ходу."""
        self._board_prev = [row[:] for row in self.board]
        self._score_prev = self.score


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
    status_text = ft.Text(
        "Натискайте кнопки",
        size=13,
        color=ft.Colors.BROWN_500,
        text_align=ft.TextAlign.CENTER,
    )

    def refresh_ui(msg: str = "") -> None:
        """Оновлює значення плиток і текст очок в інтерфейсі."""
        for r in range(N):
            for c in range(N):
                v = game.board[r][c]
                cell_texts[r][c].value = str(v) if v else "."
        score_text.value = f"Очки: {game.score}"
        if game.state == "won":
            status_text.value = "YOU WON!"
        elif game.state == "lost":
            status_text.value = "GAME OVER"
        else:
            status_text.value = msg or "Натискайте кнопки"
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

    btn_style = ft.ButtonStyle(
        bgcolor={"": ft.Colors.BROWN_400}, color={"": ft.Colors.GREY_50}
    )

    def on_move(direction: str):
        """Обробник ходу."""
        fns = {
            "left": game.move_left,
            "right": game.move_right,
            "up": game.move_up,
            "down": game.move_down,
        }

        def handler(e: ft.ControlEvent) -> None:
            if game.state == "lost":
                return
            if fns[direction]():
                game.add_random_tile()
                # game.check_lost()
                refresh_ui()

        return handler

    def on_undo(e: ft.ControlEvent) -> None:
        """Обробник повернення ходу"""
        if game.state != "lost":
            game.undo()
            refresh_ui()

    def on_restart(e: ft.ControlEvent) -> None:
        """Перезапускає гру та оновлює інтерфейс."""
        game.reset()
        refresh_ui()

    move_btns = ft.Row(
        controls=[
            ft.Button(content="◀️", on_click=on_move("left"), style=btn_style),
            ft.Button(content="▲", on_click=on_move("up"), style=btn_style),
            ft.Button(content="▼", on_click=on_move("down"), style=btn_style),
            ft.Button(content="▶️", on_click=on_move("right"), style=btn_style),
            ft.Button(content="⬅️", on_click=on_undo, style=btn_style),
            ft.Button(content="🔁", on_click=on_restart, style=btn_style),
        ]
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
                        score_text,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                grid,
                move_btns,
                status_text,
            ],
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )


ft.run(main)
