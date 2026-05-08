"""Left sidebar component — page navigation list."""

import customtkinter as ctk
from typing import Callable, Optional, List
from src.utils import constants as c


class LeftSidebar(ctk.CTkFrame):
    """Left sidebar: displays a scrollable list of page navigation buttons."""

    def __init__(
        self,
        master: ctk.CTk,
        on_page_selected: Optional[Callable[[int], None]] = None,
        **kwargs
    ) -> None:
        super().__init__(
            master, 
            width=200, 
            fg_color=("gray90", "gray15"), 
            corner_radius=0, 
            **kwargs
        )
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
            text="📄 DANH SÁCH TRANG",
            font=ctk.CTkFont(family=c.FONT_FAMILY[0], size=c.FONT_SIZE_BODY, weight="bold"),
            text_color=("gray40", "gray60"),
        )
        self.lbl_title.pack(pady=(20, 8), padx=c.PADDING_LARGE)

        # Separator line
        sep = ctk.CTkFrame(self, height=1, fg_color=("gray70", "gray25"))
        sep.pack(fill="x", padx=16, pady=(0, 10))

        # Scrollable container for buttons
        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            corner_radius=0,
            label_text="",
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=4, pady=4)

        # Initial placeholder
        self._show_placeholder("(Chưa tải file)")

    # ── Public API ───────────────────────────────────────────────────────────

    def populate_pages(self, total_pages: int, current_page_index: int = 0) -> None:
        """Render the list of page buttons."""
        # Clear existing buttons and placeholder
        for btn in self._buttons:
            btn.destroy()
        self._buttons.clear()
        
        if hasattr(self, "lbl_placeholder") and self.lbl_placeholder.winfo_exists():
            self.lbl_placeholder.destroy()

        if total_pages == 0:
            self._show_placeholder("(Trống)")
            return

        self._current_index = current_page_index

        # Create new buttons
        for i in range(total_pages):
            is_active = (i == current_page_index)
            
            btn = ctk.CTkButton(
                self.scroll_frame,
                text=f"Trang {i + 1}",
                font=ctk.CTkFont(family=c.FONT_FAMILY[0], size=c.FONT_SIZE_BODY),
                height=34,
                anchor="w",
                corner_radius=c.CORNER_RADIUS,
                fg_color=c.COLOR_PRIMARY if is_active else "transparent",
                text_color="white" if is_active else ("gray10", "gray90"),
                hover_color=("gray80", "gray25"),
                command=lambda p=i: self._on_page_clicked(p)
            )
            btn.pack(fill="x", padx=c.PADDING_STD, pady=2)
            self._buttons.append(btn)

    def select_page(self, page_index: int) -> None:
        """Programmatically highlight a page button."""
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
                fg_color=c.COLOR_PRIMARY,
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
