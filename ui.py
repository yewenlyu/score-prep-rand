import pyfiglet
from textual.app import ComposeResult
from textual.containers import Center, Horizontal, Vertical
from textual.widgets import Button, Input, Label, ProgressBar, Static


def big_text(text: str) -> str:
    return pyfiglet.figlet_format(text, font="big").rstrip("\n")


class SetupPanel(Vertical):
    def compose(self) -> ComposeResult:
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


class PracticePanel(Vertical):
    def compose(self) -> ComposeResult:
        with Center():
            with Static(id="measure-card"):
                yield Static(big_text("?"), id="measure-display")
        yield Label("Press Space for your first measure", id="practice-status")
        yield Label("", id="counter")
        yield ProgressBar(total=100, show_eta=False, id="progress-bar")
        with Horizontal(id="btn-row"):
            yield Button("Next [Space]", id="next-btn", variant="primary")
            yield Button("Reset [R]", id="reset-btn", variant="default")
        yield Label("Practiced Measures", id="history-title")
        with Vertical(id="history-box"):
            yield Label("No measures practiced yet", id="history-content")
