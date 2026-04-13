from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, Footer, Header, Input, Label, ProgressBar, Static

from session import PracticeSession
from ui import PracticePanel, SetupPanel, big_text


class ScorePrep(App):
    TITLE = "Score Prep"
    CSS_PATH = "score_prep.tcss"

    BINDINGS = [
        ("space", "next_measure", "Next Measure"),
        ("r", "reset", "Reset"),
        ("q", "quit", "Quit"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self._session: PracticeSession | None = None

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Vertical(id="main-container"):
            yield Label("Score Prep", id="title")
            yield Label("Random measure practice for recital preparation", id="subtitle")
            yield SetupPanel(id="setup")
            yield PracticePanel(id="practice")
        yield Footer()

    def on_mount(self) -> None:
        self._show_setup()

    # -- Screen transitions --

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
        self.query_one("#measure-display", Static).update(big_text("?"))
        self.query_one("#practice-status", Label).update("Press Space for your first measure")
        self._sync_ui()

    # -- Event handlers --

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

    # -- Actions --

    def _start_session(self) -> None:
        raw = self.query_one("#measure-input", Input).value.strip()
        if not raw or not raw.isdigit() or int(raw) < 1:
            self.query_one("#error-label", Label).update("Please enter a positive integer")
            return

        self._session = PracticeSession(int(raw))
        self._show_practice()

    def action_next_measure(self) -> None:
        if self._session is None or self._session.is_complete:
            return

        measure = self._session.next_measure()

        self.query_one("#measure-display", Static).update(big_text(str(measure)))
        self._sync_ui()

        if self._session.is_complete:
            self.query_one("#practice-status", Label).update("All measures covered! Great work!")
            self.query_one("#next-btn", Button).disabled = True
        else:
            self.query_one("#practice-status", Label).update("Play from this measure now")

    def action_reset(self) -> None:
        self._session = None
        self._show_setup()

    # -- UI sync --

    def _sync_ui(self) -> None:
        """Push current session state to the UI."""
        if self._session is None:
            return

        self.query_one("#counter", Label).update(
            f"{self._session.remaining_count} of {self._session.total} measures remaining"
        )

        bar = self.query_one("#progress-bar", ProgressBar)
        bar.total = self._session.total
        bar.progress = self._session.remaining_count

        if self._session.practiced:
            text = "  ".join(f"m.{m}" for m in self._session.practiced)
        else:
            text = "No measures practiced yet"
        self.query_one("#history-content", Label).update(text)


if __name__ == "__main__":
    ScorePrep().run()
