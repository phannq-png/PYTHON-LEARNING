"""Left sidebar component — page navigation list."""

import customtkinter as ctk
from typing import Callable, Optional, List


class LeftSidebar(ctk.CTkFrame):
    """Left sidebar: displays a scrollable list of page navigation buttons.

    Args:
        master: Parent widget.
        on_page_selected: Callback function called with page index when a button is clicked.
    """

    def __init__(
        self,
        master: ctk.CTk,
        on_page_selected: Optional[Callable[[int], None]] = None,
        **kwargs
    ) -> None:
        super().__init__(master, width=180, fg_color=("gray80", "gray17"), **kwargs)
        self.pack_propagate(False)
        self.grid_propagate(False)
        
        self._on_page_selected = on_page_selected
        self._buttons: List[ctk.CTkButton] = []
        self._current_index: int = -1
        
        self._build_widgets()

    def _build_widgets(self) -> None:
        """Build the sidebar structure with title and scrollable container."""
        self.lbl_title = ctk.CTkLabel(
            self,
            text="Danh sách trang",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=("gray40", "gray60"),
        )
        self.lbl_title.pack(pady=(16, 8), padx=8)

        # Separator line
        sep = ctk.CTkFrame(self, height=1, fg_color=("gray70", "gray35"))
        sep.pack(fill="x", padx=12, pady=(0, 8))

        # Scrollable container for buttons
        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            label_text="",
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=4, pady=4)

        # Initial placeholder
        self.lbl_placeholder = ctk.CTkLabel(
            self.scroll_frame,
            text="(Chưa tải file)",
            font=ctk.CTkFont(size=11),
            text_color=("gray55", "gray50"),
        )
        self.lbl_placeholder.pack(pady=20)

    # ── Public API ───────────────────────────────────────────────────────────

    def populate_pages(self, total_pages: int, current_page_index: int = 0) -> None:
        """Render the list of page buttons.
        
        Args:
            total_pages: Number of pages to display.
            current_page_index: The index of the page to highlight initially.
        """
        # Clear existing buttons and placeholder
        for btn in self._buttons:
            btn.destroy()
        self._buttons.clear()
        
        if hasattr(self, "lbl_placeholder") and self.lbl_placeholder.winfo_exists():
            self.lbl_placeholder.destroy()

        if total_pages == 0:
            self._show_placeholder()
            return

        self._current_index = current_page_index

        # Create new buttons
        for i in range(total_pages):
            is_active = (i == current_page_index)
            
            btn = ctk.CTkButton(
                self.scroll_frame,
                text=f"Trang {i + 1}",
                font=ctk.CTkFont(size=11),
                height=32,
                anchor="w",
                fg_color=("#3B8ED0", "#1F6AA5") if is_active else "transparent",
                text_color=("gray10", "gray90") if not is_active else "white",
                hover_color=("#DBDBDB", "#2B2B2B") if not is_active else None,
                command=lambda p=i: self._on_page_clicked(p)
            )
            btn.pack(fill="x", padx=4, pady=2)
            self._buttons.append(btn)

    def select_page(self, page_index: int) -> None:
        """Programmatically highlight a page button without triggering the callback."""
        if 0 <= page_index < len(self._buttons):
            # Reset old button
            if 0 <= self._current_index < len(self._buttons):
                self._buttons[self._current_index].configure(
                    fg_color="transparent",
                    text_color=("gray10", "gray90")
                )
            
            # Highlight new button
            self._current_index = page_index
            self._buttons[page_index].configure(
                fg_color=("#3B8ED0", "#1F6AA5"),
                text_color="white"
            )

    def set_on_page_selected(self, callback: Callable[[int], None]) -> None:
        """Register the callback for page selection events."""
        self._on_page_selected = callback

    # ── Internal ─────────────────────────────────────────────────────────────

    def _on_page_clicked(self, index: int) -> None:
        """Handle button click and notify observer."""
        self.select_page(index)
        if self._on_page_selected:
            self._on_page_selected(index)

    def _show_placeholder(self) -> None:
        """Show the empty state label."""
        self.lbl_placeholder = ctk.CTkLabel(
            self.scroll_frame,
            text="(Trống)",
            font=ctk.CTkFont(size=11),
            text_color=("gray55", "gray50"),
        )
        self.lbl_placeholder.pack(pady=20)
