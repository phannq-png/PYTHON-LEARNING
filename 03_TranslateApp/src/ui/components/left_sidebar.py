"""Left sidebar component — page navigation list."""

import customtkinter as ctk
from typing import Callable, Optional, List
from src.utils import constants as c
from src.ui.components.tooltip import add_tooltip


class LeftSidebar(ctk.CTkFrame):
    """Left sidebar: displays a scrollable list of page navigation buttons."""

    def __init__(
        self,
        master: ctk.CTk,
        on_page_selected: Optional[Callable[[int], None]] = None,
        on_clear_search: Optional[Callable[[], None]] = None,
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
        self._on_clear_search = on_clear_search
        self._buttons: List[ctk.CTkButton] = []
        self._current_index: int = -1
        self._search_match_indices: List[int] = []
        self._indicators: List[ctk.CTkFrame] = []
        self._review_labels: List[ctk.CTkLabel] = []
        
        self._build_widgets()

    def _build_widgets(self) -> None:
        # Header with Clear Search button
        self.title_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.title_frame.pack(fill="x", pady=(20, 8), padx=10)
        
        self.lbl_title = ctk.CTkLabel(
            self.title_frame,
            text="📄 DANH SÁCH TRANG",
            font=ctk.CTkFont(family=c.FONT_FAMILY[0], size=13, weight="bold"),
            text_color=("gray40", "gray60"),
        )
        self.lbl_title.pack(side="left", padx=5)

        self.btn_clear_search = ctk.CTkButton(
            self.title_frame,
            text="✕",
            width=24,
            height=24,
            corner_radius=12,
            fg_color="transparent",
            text_color="gray50",
            hover_color=("gray80", "gray25"),
            command=self._on_clear_btn_clicked
        )
        self.btn_clear_search.pack(side="right", padx=5)
        self.btn_clear_search.pack_forget() # Hidden by default
        add_tooltip(self.btn_clear_search, "Xóa kết quả tìm kiếm")

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

        # ── Status Legend ───────────────────────────────────────────────────
        self.legend_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.legend_frame.pack(fill="x", side="bottom", padx=15, pady=(5, 15))
        
        # Header with toggle button
        self.legend_header = ctk.CTkFrame(self.legend_frame, fg_color="transparent")
        self.legend_header.pack(fill="x")
        
        self.lbl_legend_title = ctk.CTkLabel(
            self.legend_header, 
            text="CHÚ THÍCH TRẠNG THÁI", 
            font=ctk.CTkFont(size=10, weight="bold"), 
            text_color="gray50"
        )
        self.lbl_legend_title.pack(side="left")
        
        self.btn_toggle_legend = ctk.CTkButton(
            self.legend_header,
            text="🔼", # Up arrow (pointing to header)
            width=20,
            height=20,
            fg_color="transparent",
            text_color="gray50",
            hover_color=("gray80", "gray25"),
            font=ctk.CTkFont(size=10),
            command=self._toggle_legend
        )
        self.btn_toggle_legend.pack(side="right")
        
        self.legend_content_frame = ctk.CTkFrame(self.legend_frame, fg_color="transparent")
        self.legend_content_frame.pack(fill="x", pady=(5, 0))
        
        legend_items = [
            ("gray50", "Chưa dịch"),
            ("#F39C12", "Đã dịch (Chưa check)"),
            ("#107C10", "Đã dịch & OK"),
            ("#E74856", "Đã dịch & Lỗi Check")
        ]
        
        for color, text in legend_items:
            item = ctk.CTkFrame(self.legend_content_frame, fg_color="transparent")
            item.pack(fill="x", pady=1)
            # Dot
            ctk.CTkFrame(item, width=8, height=8, corner_radius=4, fg_color=color).pack(side="left", padx=(0, 8))
            # Label
            ctk.CTkLabel(item, text=text, font=ctk.CTkFont(size=10), text_color="gray60").pack(side="left")

        # Initial placeholder
        self._show_placeholder("(Chưa tải file)")

    def _toggle_legend(self) -> None:
        """Collapse or expand the legend content."""
        if self.legend_content_frame.winfo_viewable():
            self.legend_content_frame.pack_forget()
            self.btn_toggle_legend.configure(text="🔽") # Down arrow to expand
        else:
            self.legend_content_frame.pack(fill="x", pady=(5, 0))
            self.btn_toggle_legend.configure(text="🔼") # Up arrow to collapse

    # ── Public API ───────────────────────────────────────────────────────────

    def populate_pages(self, pages: List[dict], current_page_index: int = 0) -> None:
        """Render the list of page buttons with status indicators and review icons."""
        # Clear existing buttons and placeholder
        for btn in self._buttons:
            if btn.master.winfo_exists():
                btn.master.destroy()
        self._buttons.clear()
        self._indicators.clear()
        self._review_labels.clear()
        
        if hasattr(self, "lbl_placeholder") and self.lbl_placeholder.winfo_exists():
            self.lbl_placeholder.destroy()

        if not pages:
            self._show_placeholder("(Trống)")
            return

        self._current_index = current_page_index

        # Create new buttons
        for i, page in enumerate(pages):
            is_active = (i == current_page_index)
            is_reviewed = page.get("is_reviewed", False)
            
            # Determine status color
            is_translated = page.get("is_translated", False)
            check_status = page.get("check_status", None) # None, 'ok', 'error'
            
            if not is_translated:
                status_color = "gray50"
            else:
                if check_status == "ok":
                    status_color = "#107C10" # Green
                elif check_status == "error":
                    status_color = "#E74856" # Red
                else:
                    status_color = "#F39C12" # Orange (translated but not checked)

            btn_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
            btn_frame.pack(fill="x", pady=2)
            
            # Status indicator dot on the left
            indicator = ctk.CTkFrame(btn_frame, width=10, height=10, corner_radius=5, fg_color=status_color)
            indicator.pack(side="left", padx=(10, 0))
            self._indicators.append(indicator)

            # Review icon (Tick) - Pack this first to the right
            lbl_review = ctk.CTkLabel(
                btn_frame, 
                text="✓" if is_reviewed else "", 
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color="#107C10",
                width=24
            )
            lbl_review.pack(side="right", padx=(0, 5))
            self._review_labels.append(lbl_review)

            btn = ctk.CTkButton(
                btn_frame,
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
            btn.pack(side="left", fill="x", expand=True, padx=(5, 2))
            
            add_tooltip(btn, f"Xem và dịch trang số {i + 1}")
            self._buttons.append(btn)

    def select_page(self, page_index: int) -> None:
        """Programmatically highlight a page button."""
        if 0 <= page_index < len(self._buttons):
            # Reset old button
            if 0 <= self._current_index < len(self._buttons):
                is_search_match = self._current_index in self._search_match_indices
                self._buttons[self._current_index].configure(
                    fg_color="#F1C40F" if is_search_match else "transparent",
                    text_color="black" if is_search_match else ("gray10", "gray90")
                )
            
            # Highlight new button
            self._current_index = page_index
            btn = self._buttons[page_index]
            
            # If not in search mode (or just normal active style)
            btn.configure(
                fg_color=c.COLOR_PRIMARY,
                text_color="white"
            )

    def highlight_search_results(self, match_indices: List[int]) -> None:
        """Highlight specific pages in yellow and show the clear button."""
        self.clear_search_highlights() # Reset first
        
        if not match_indices: return
        
        self.btn_clear_search.pack(side="right", padx=5) # Show clear button
        self._search_match_indices = match_indices
        
        for idx in match_indices:
            if 0 <= idx < len(self._buttons):
                btn = self._buttons[idx]
                btn.configure(
                    fg_color="#F1C40F", # Yellow
                    text_color="black"
                )

    def clear_search_highlights(self) -> None:
        """Reset all button colors to normal and hide clear button."""
        self.btn_clear_search.pack_forget()
        self._search_match_indices = []
        
        for i, btn in enumerate(self._buttons):
            if i == self._current_index:
                btn.configure(fg_color=c.COLOR_PRIMARY, text_color="white")
            else:
                btn.configure(fg_color="transparent", text_color=("gray10", "gray90"))

    def update_page_status(self, page_index: int, is_translated: bool, check_status: Optional[str], is_reviewed: bool = False) -> None:
        """Update the indicator color and review icon for a specific page."""
        if 0 <= page_index < len(self._buttons):
            indicator = self._indicators[page_index]
            lbl_review = self._review_labels[page_index]
            
            if not is_translated:
                status_color = "gray50"
            else:
                if check_status == "ok":
                    status_color = "#107C10"
                elif check_status == "error":
                    status_color = "#E74856"
                else:
                    status_color = "#F39C12"
            
            indicator.configure(fg_color=status_color)
            lbl_review.configure(text="✓" if is_reviewed else "")

    def set_on_page_selected(self, callback: Callable[[int], None]) -> None:
        """Register the callback for page selection events."""
        self._on_page_selected = callback

    # ── Internal ─────────────────────────────────────────────────────────────

    def _on_page_clicked(self, index: int) -> None:
        """Handle button click and notify observer."""
        self.select_page(index)
        if self._on_page_selected:
            self._on_page_selected(index)

    def _on_clear_btn_clicked(self) -> None:
        """Handle clear button click and notify parent."""
        if self._on_clear_search:
            self._on_clear_search()
        else:
            self.clear_search_highlights()

    def _show_placeholder(self, text: str = "(Trống)") -> None:
        """Show the empty state label."""
        self.lbl_placeholder = ctk.CTkLabel(
            self.scroll_frame,
            text=text,
            font=ctk.CTkFont(family=c.FONT_FAMILY[0], size=11),
            text_color=("gray55", "gray50"),
        )
        self.lbl_placeholder.pack(pady=20)
