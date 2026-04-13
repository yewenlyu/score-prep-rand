import random

import pyfiglet
from textual.app import App, ComposeResult
from textual.containers import Center, Horizontal, Vertical
from textual.widgets import Button, Footer, Header, Input, Label, ProgressBar, Static
from textual.reactive import reactive


class ScorePrep(App):
    TITLE = "Score Prep"

    CSS = """
    Screen {
        background: $surface;
        align: center top;
    }

    #main-container {
        width: 64;
        height: auto;
        margin: 1 0;
        align: center top;
    }

    #title {
        text-align: center;
        text-style: bold;
        color: $text;
        margin-bottom: 1;
    }

    #subtitle {
        text-align: center;
        color: $text-muted;
        margin-bottom: 1;
    }

    /* Setup screen */
    #setup {
        height: auto;
        padding: 1 2;
    }

    #setup-label {
        text-align: center;
        margin-bottom: 1;
    }

    #measure-input {
        width: 20;
        margin: 0 0 1 0;
    }

    #start-btn {
        width: 20;
    }

    #error-label {
        text-align: center;
        color: $error;
        margin-top: 1;
    }

    /* Practice screen */
    #practice {
        height: auto;
        padding: 1 2;
    }

    #measure-card {
        background: $panel;
        border: tall $primary;
        height: 16;
        width: 100%;
        margin-bottom: 1;
        align: center middle;
        content-align: center middle;
    }

    #measure-display {
        text-style: bold;
        color: green;
        width: auto;
        height: auto;
    }

    #practice-status {
        text-align: center;
        color: $text-muted;
        margin-bottom: 1;
    }

    #counter {
        text-align: center;
        text-style: bold;
        margin-bottom: 1;
    }

    #progress-bar {
        margin: 0 4 1 4;
    }

    #btn-row {
        height: 3;
        align: center middle;
        margin-bottom: 1;
    }

    #next-btn {
        margin-right: 2;
    }

    #reset-btn {
        margin-left: 2;
    }

    #history-title {
        text-align: center;
        text-style: bold;
        color: $text-muted;
        margin-bottom: 1;
    }

    #history-box {
        background: $panel;
        height: 6;
        padding: 1 2;
        overflow-y: auto;
    }

    #history-content {
        width: 100%;
    }
    """

    BINDINGS = [
        ("space", "next_measure", "Next Measure"),
        ("r", "reset", "Reset"),
        ("q", "quit", "Quit"),
    ]

    remaining_measures: reactive[list[int]] = reactive(list, init=False)
    total_measures: reactive[int] = reactive(0, init=False)
    practiced_measures: reactive[list[int]] = reactive(list, init=False)
    in_session: reactive[bool] = reactive(False, init=False)

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Vertical(id="main-container"):
            yield Label("Score Prep", id="title")
            yield Label("Random measure practice for recital preparation", id="subtitle")

            with Vertical(id="setup"):
                yield Label("Total measures in your piece:", id="setup-label")
                with Center():
                    yield Input(
                        placeholder="e.g. 64",
                        id="measure-input",
                        type="integer",
                        max_length=6,
                    )
                with Center():
                    yield Button("Start Practice", id="start-btn", variant="primary")
                yield Label("", id="error-label")

            with Vertical(id="practice"):
                with Center():
                    with Static(id="measure-card"):
                        yield Static(self._big_text("?"), id="measure-display")
                yield Label("Press Space for your first measure", id="practice-status")
                yield Label("", id="counter")
                yield ProgressBar(total=100, show_eta=False, id="progress-bar")
                with Horizontal(id="btn-row"):
                    yield Button("Next [Space]", id="next-btn", variant="primary")
                    yield Button("Reset [R]", id="reset-btn", variant="default")
                yield Label("Practiced Measures", id="history-title")
                with Vertical(id="history-box"):
                    yield Label("No measures practiced yet", id="history-content")
        yield Footer()

    def on_mount(self) -> None:
        self.remaining_measures = []
        self.total_measures = 0
        self.practiced_measures = []
        self.in_session = False
        self._show_setup()

    def _show_setup(self) -> None:
        self.query_one("#setup").display = True
        self.query_one("#practice").display = False
        self.query_one("#measure-input", Input).value = ""
        self.query_one("#error-label", Label).update("")
        self.query_one("#measure-input", Input).focus()

    def _show_practice(self) -> None:
        self.query_one("#setup").display = False
        self.query_one("#practice").display = True
        self.query_one("#next-btn", Button).disabled = False

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id == "measure-input":
            self._start_session()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "start-btn":
            self._start_session()
        elif event.button.id == "next-btn":
            self.action_next_measure()
        elif event.button.id == "reset-btn":
            self.action_reset()

    def _start_session(self) -> None:
        raw = self.query_one("#measure-input", Input).value.strip()
        if not raw or not raw.isdigit() or int(raw) < 1:
            self.query_one("#error-label", Label).update("Please enter a positive integer")
            return

        self.total_measures = int(raw)
        self.remaining_measures = list(range(1, self.total_measures + 1))
        random.shuffle(self.remaining_measures)
        self.practiced_measures = []
        self.in_session = True

        self._show_practice()
        self.query_one("#measure-display", Static).update(self._big_text("?"))
        self.query_one("#practice-status", Label).update("Press Space for your first measure")
        self._update_progress()
        self._update_history()

    def action_next_measure(self) -> None:
        if not self.in_session or not self.remaining_measures:
            return

        measure = self.remaining_measures.pop()
        self.practiced_measures.append(measure)

        self.query_one("#measure-display", Static).update(self._big_text(str(measure)))
        self._update_progress()
        self._update_history()

        if not self.remaining_measures:
            self.query_one("#practice-status", Label).update("All measures covered! Great work!")
            self.query_one("#next-btn", Button).disabled = True
        else:
            self.query_one("#practice-status", Label).update("Play from this measure now")

    def _update_progress(self) -> None:
        remaining = len(self.remaining_measures)
        self.query_one("#counter", Label).update(
            f"{remaining} of {self.total_measures} measures remaining"
        )

        bar = self.query_one("#progress-bar", ProgressBar)
        bar.total = self.total_measures
        bar.progress = remaining

    def _update_history(self) -> None:
        if self.practiced_measures:
            text = "  ".join(f"m.{m}" for m in self.practiced_measures)
        else:
            text = "No measures practiced yet"
        self.query_one("#history-content", Label).update(text)

    @staticmethod
    def _big_text(text: str) -> str:
        return pyfiglet.figlet_format(text, font="big").rstrip("\n")

    def action_reset(self) -> None:
        self.remaining_measures = []
        self.total_measures = 0
        self.practiced_measures = []
        self.in_session = False
        self._show_setup()


if __name__ == "__main__":
    ScorePrep().run()
