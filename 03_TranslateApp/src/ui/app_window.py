"""Main application window for the TranslatorApp.

Builds the full UI skeleton:
    - Menu Bar (File / Settings / Help)
    - Top Bar (Upload, Domain, Export)
    - Left Sidebar (page navigation placeholder)
    - Center Panel (JP read-only | VN editable)
    - Right Sidebar (active terms placeholder)
    - Bottom Bar (action buttons + token counter)
"""

import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk

from src.ui.components.bottom_bar import BottomBar
from src.ui.components.center_panel import CenterPanel
from src.ui.components.left_sidebar import LeftSidebar
from src.ui.components.right_sidebar import RightSidebar
from src.ui.components.top_bar import TopBar


class AppWindow(ctk.CTk):
    """Main window of TranslatorApp.

    Minimum size: 1200 × 800 px.
    Default theme: dark mode (set before instantiation via ctk globals).
    """

    _MIN_WIDTH: int = 1200
    _MIN_HEIGHT: int = 800

    def __init__(self) -> None:
        super().__init__()
        self._configure_window()
        self._build_menu_bar()
        self._build_layout()

    # ── Window configuration ────────────────────────────────────────────────

    def _configure_window(self) -> None:
        """Set window title, minimum size, and initial geometry."""
        self.title("TranslatorApp — Dịch tài liệu chuyên ngành Nhật-Việt")
        self.minsize(self._MIN_WIDTH, self._MIN_HEIGHT)
        self.geometry(f"{self._MIN_WIDTH}x{self._MIN_HEIGHT}")

    # ── Menu bar ────────────────────────────────────────────────────────────

    def _build_menu_bar(self) -> None:
        """Build the native tk.Menu bar and attach it to the window.

        CustomTkinter does not provide its own Menu widget, so we use
        the standard tkinter Menu and configure it on the root window.
        """
        menubar = tk.Menu(self)

        # ── File menu ──────────────────────────────────────────────────────
        file_menu = tk.Menu(menubar, tearoff=False)
        file_menu.add_command(label="Mở file…", command=self._menu_file_open)
        file_menu.add_separator()
        file_menu.add_command(label="Thoát", command=self.destroy)
        menubar.add_cascade(label="File", menu=file_menu)

        # ── Settings menu ──────────────────────────────────────────────────
        settings_menu = tk.Menu(menubar, tearoff=False)
        settings_menu.add_command(
            label="Segmentation Settings",
            command=self._open_segmentation_settings,
        )
        settings_menu.add_command(
            label="API Settings",
            command=self._open_api_settings,
        )
        menubar.add_cascade(label="Settings", menu=settings_menu)

        # ── Help menu ──────────────────────────────────────────────────────
        help_menu = tk.Menu(menubar, tearoff=False)
        help_menu.add_command(label="About", command=self._menu_help_about)
        menubar.add_cascade(label="Help", menu=help_menu)

        # Attach to window
        self.config(menu=menubar)

    # ── Main layout ─────────────────────────────────────────────────────────

    def _build_layout(self) -> None:
        """Build and grid all major UI panels.

        Grid structure (rows × columns):
            Row 0 | TopBar      — spans all 3 columns
            Row 1 | Left | Center | Right   — expandable
            Row 2 | BottomBar   — spans all 3 columns
        """
        # Row weights
        self.rowconfigure(0, weight=0)   # TopBar — fixed height
        self.rowconfigure(1, weight=1)   # Main panels — expand
        self.rowconfigure(2, weight=0)   # BottomBar — fixed height

        # Column weights
        self.columnconfigure(0, weight=0)   # LeftSidebar — fixed width
        self.columnconfigure(1, weight=1)   # CenterPanel — expand
        self.columnconfigure(2, weight=0)   # RightSidebar — fixed width

        # ── Top bar ────────────────────────────────────────────────────────
        self.top_bar = TopBar(self)
        self.top_bar.grid(row=0, column=0, columnspan=3, sticky="ew")

        # ── Left sidebar ───────────────────────────────────────────────────
        self.left_sidebar = LeftSidebar(self)
        self.left_sidebar.grid(row=1, column=0, sticky="ns", padx=(4, 0), pady=4)

        # ── Center panel ───────────────────────────────────────────────────
        self.center_panel = CenterPanel(self)
        self.center_panel.grid(row=1, column=1, sticky="nsew", padx=4, pady=4)

        # ── Right sidebar ──────────────────────────────────────────────────
        self.right_sidebar = RightSidebar(self)
        self.right_sidebar.grid(row=1, column=2, sticky="ns", padx=(0, 4), pady=4)

        # ── Bottom bar ─────────────────────────────────────────────────────
        self.bottom_bar = BottomBar(self)
        self.bottom_bar.grid(row=2, column=0, columnspan=3, sticky="ew")

    # ── Menu callbacks ──────────────────────────────────────────────────────

    def _menu_file_open(self) -> None:
        """Placeholder: will be wired to document processor (feature 02)."""
        pass

    def _open_segmentation_settings(self) -> None:
        """Open Segmentation Settings dialog (placeholder until P1-CONF-002)."""
        messagebox.showinfo(
            "Segmentation Settings",
            "Chức năng này sẽ được hoàn thiện ở task P1-CONF-002.",
            parent=self,
        )

    def _open_api_settings(self) -> None:
        """Open API Settings dialog (placeholder until feature 08-api-integration)."""
        messagebox.showinfo(
            "API Settings",
            "Chức năng này sẽ được hoàn thiện ở feature 08-api-integration.",
            parent=self,
        )

    def _menu_help_about(self) -> None:
        """Show application about dialog."""
        messagebox.showinfo(
            "About TranslatorApp",
            "TranslatorApp v0.1\nDịch tài liệu chuyên ngành Nhật → Việt\n\nPhase 1 — UI Skeleton",
            parent=self,
        )
