"""Right sidebar component — active glossary terms panel."""

import re
from typing import Callable, Dict, List, Optional, Tuple

import customtkinter as ctk
from src.utils import constants as c
from src.ui.components.tooltip import add_tooltip


class TermItem(ctk.CTkFrame):
    """A single clickable term item in the sidebar."""

    def __init__(
        self, 
        master: any, 
        jp_term: str, 
        vn_term: str, 
        count: int, 
        on_click: Callable[[str, str, 'TermItem'], None],
        status: str = "ok",
        **kwargs
    ):
        super().__init__(
            master, 
            fg_color="transparent", 
            cursor="hand2", 
            corner_radius=c.CORNER_RADIUS,
            **kwargs
        )
        self.jp_term = jp_term
        self.vn_term = vn_term
        self.on_click = on_click
        self._is_selected = False

        self.grid_columnconfigure(1, weight=1)

        # Icon/Checkmark
        icon = "✓" if status == "ok" else "×"
        icon_color = c.COLOR_SUCCESS if status == "ok" else c.COLOR_DANGER
        
        ctk.CTkLabel(
            self, 
            text=icon, 
            text_color=icon_color, 
            font=ctk.CTkFont(family=c.FONT_FAMILY[0], size=14, weight="bold")
        ).grid(row=0, column=0, padx=(c.PADDING_STD, 5))

        # JP -> VN Label
        text = f"{jp_term} → {vn_term}"
        self.lbl_term = ctk.CTkLabel(
            self, 
            text=text, 
            anchor="w", 
            font=ctk.CTkFont(family=c.FONT_FAMILY[0], size=c.FONT_SIZE_BODY),
            wraplength=170,
            justify="left"
        )
        self.lbl_term.grid(row=0, column=1, sticky="w", pady=c.PADDING_STD)

        # Count Badge
        self.lbl_count = ctk.CTkLabel(
            self, 
            text=f"{count}", 
            font=ctk.CTkFont(family=c.FONT_FAMILY[0], size=c.FONT_SIZE_SMALL, weight="bold"),
            text_color="white",
            fg_color=c.COLOR_PRIMARY,
            corner_radius=8,
            width=24,
            height=20
        )
        self.lbl_count.grid(row=0, column=2, padx=(5, c.PADDING_STD))

        # Bind events
        for widget in (self, self.lbl_term, self.lbl_count):
            widget.bind("<Button-1>", self._handle_click)
            widget.bind("<Enter>", self._on_enter)
            widget.bind("<Leave>", self._on_leave)

    def _on_enter(self, event=None):
        if not self._is_selected:
            self.configure(fg_color=("gray80", "gray25"))

    def _on_leave(self, event=None):
        if not self._is_selected:
            self.configure(fg_color="transparent")

    def set_selected(self, is_selected: bool):
        """Update visual state for selection."""
        self._is_selected = is_selected
        if is_selected:
            self.configure(fg_color=("#D4AC0D", "#9A7D0A")) # Darker yellow/gold
        else:
            self.configure(fg_color="transparent")

    def _handle_click(self, event=None):
        self.on_click(self.jp_term, self.vn_term, self)


class RightSidebar(ctk.CTkFrame):
    """Right sidebar: displays active glossary terms."""

    def __init__(
        self, 
        master: ctk.CTk, 
        on_term_click: Optional[Callable[[str, str], None]] = None,
        **kwargs
    ) -> None:
        super().__init__(
            master, 
            width=240, 
            fg_color=("gray90", "gray15"), 
            corner_radius=0, 
            **kwargs
        )
        self.on_term_click = on_term_click
        self._selected_item: Optional[TermItem] = None
        self.pack_propagate(False)
        self._build_widgets()

    def _build_widgets(self) -> None:
        """Build the sidebar header and scrollable area."""
        # ── Header ─────────────────────────────────────────────────────────
        lbl_header = ctk.CTkLabel(
            self,
            text="📑 THUẬT NGỮ ACTIVE",
            font=ctk.CTkFont(family=c.FONT_FAMILY[0], size=c.FONT_SIZE_HEADER, weight="bold"),
        )
        lbl_header.pack(pady=(20, 8), padx=c.PADDING_STD, fill="x")

        # Separator line
        sep = ctk.CTkFrame(self, height=1, fg_color=("gray70", "gray25"))
        sep.pack(fill="x", padx=16, pady=(0, 10))

        # ── Scrollable list ────────────────────────────────────────────────
        self.scroll_frame = ctk.CTkScrollableFrame(
            self, 
            fg_color="transparent",
            corner_radius=0,
            label_text=None
        )
        self.scroll_frame.pack(expand=True, fill="both", padx=4, pady=(0, 8))

        # Placeholder
        self._show_placeholder()

    def update_terms(self, jp_text: str, glossary: Dict[str, str], mismatches: List[Dict] = None) -> None:
        """Scan text for glossary terms and refresh the list.
        
        Args:
            jp_text: The Japanese source text to scan.
            glossary: Merged glossary dictionary (JP -> VN).
            mismatches: Optional list of mismatches from ConsistencyChecker.
        """
        # Clear existing items
        for child in self.scroll_frame.winfo_children():
            child.destroy()

        if not jp_text or not glossary:
            self._show_placeholder()
            return

        # Find active terms
        active_terms = [] # List of (jp, vn, count)
        for jp, vn in glossary.items():
            # Use regex for accurate counting
            matches = list(re.finditer(re.escape(jp), jp_text))
            if matches:
                active_terms.append((jp, vn, len(matches)))

        if not active_terms:
            self._show_placeholder()
            return

        # Sort by count (descending)
        active_terms.sort(key=lambda x: x[2], reverse=True)

        # Extract error terms for quick lookup
        error_terms = {m["jp_term"] for m in mismatches} if mismatches else set()

        # Render items
        for jp, vn, count in active_terms:
            status = "error" if jp in error_terms else "ok"
            item = TermItem(
                self.scroll_frame,
                jp_term=jp,
                vn_term=vn,
                count=count,
                status=status,
                on_click=self._on_item_clicked
            )
            item.pack(fill="x", pady=1)
            add_tooltip(item, f"Highlight '{jp}' trong văn bản")

    def _on_item_clicked(self, jp_term: str, vn_term: str, item: TermItem):
        """Internal handler for term click with toggle logic."""
        if self._selected_item == item:
            # Deselect if clicking the same item
            self.clear_selection()
            if self.on_term_click:
                self.on_term_click("", "") # Signal clear
        else:
            # Select new item
            self.clear_selection()
            self._selected_item = item
            item.set_selected(True)
            if self.on_term_click:
                self.on_term_click(jp_term, vn_term)

    def clear_selection(self):
        """Deselect any currently selected term item."""
        if self._selected_item:
            self._selected_item.set_selected(False)
            self._selected_item = None

    def _show_placeholder(self) -> None:
        self.lbl_placeholder = ctk.CTkLabel(
            self.scroll_frame,
            text="(Không có thuật ngữ nào)",
            font=ctk.CTkFont(size=11),
            text_color=("gray55", "gray50"),
        )
        self.lbl_placeholder.pack(pady=20)
