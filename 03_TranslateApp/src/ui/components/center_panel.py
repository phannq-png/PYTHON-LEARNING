"""Center panel component — JP (read-only) / VN (editable) split view."""

import customtkinter as ctk
from typing import Callable, Optional
from src.utils import constants as c


class CenterPanel(ctk.CTkFrame):
    """Center panel split horizontally into JP (read-only) and VN (editable)."""

    def __init__(
        self,
        master: ctk.CTk,
        on_vn_changed: Optional[Callable[[str], None]] = None,
        **kwargs,
    ) -> None:
        super().__init__(master, fg_color="transparent", **kwargs)
        self._on_vn_changed = on_vn_changed
        self._build_widgets()

    def _build_widgets(self) -> None:
        """Build the card-style text panels with headers."""
        self.columnconfigure(0, weight=1)
        self.rowconfigure((0, 1), weight=1)

        # ── Japanese Panel (Card) ──────────────────────────────────────────
        self.jp_card = ctk.CTkFrame(self, corner_radius=c.CORNER_RADIUS, border_width=c.BORDER_WIDTH)
        self.jp_card.grid(row=0, column=0, sticky="nsew", pady=(0, 4))
        self.jp_card.grid_columnconfigure(0, weight=1)
        self.jp_card.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            self.jp_card, 
            text="🇯🇵  NGUỒN TIẾNG NHẬT", 
            font=ctk.CTkFont(family=c.FONT_FAMILY[0], size=c.FONT_SIZE_SMALL, weight="bold"),
            text_color=c.COLOR_PRIMARY
        ).grid(row=0, column=0, sticky="w", padx=12, pady=4)

        self.txt_japanese = ctk.CTkTextbox(
            self.jp_card,
            font=ctk.CTkFont(family=c.FONT_FAMILY[2], size=13),
            fg_color="transparent",
            wrap="word",
            state="disabled",
            padx=12,
            pady=8
        )
        self.txt_japanese.grid(row=1, column=0, sticky="nsew", padx=2, pady=(0, 2))

        # ── Vietnamese Panel (Card) ────────────────────────────────────────
        self.vn_card = ctk.CTkFrame(self, corner_radius=c.CORNER_RADIUS, border_width=c.BORDER_WIDTH)
        self.vn_card.grid(row=1, column=0, sticky="nsew", pady=(4, 0))
        self.vn_card.grid_columnconfigure(0, weight=1)
        self.vn_card.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            self.vn_card, 
            text="🇻🇳  BẢN DỊCH TIẾNG VIỆT", 
            font=ctk.CTkFont(family=c.FONT_FAMILY[0], size=c.FONT_SIZE_SMALL, weight="bold"),
            text_color=c.COLOR_SUCCESS
        ).grid(row=0, column=0, sticky="w", padx=12, pady=4)

        self.txt_vietnamese = ctk.CTkTextbox(
            self.vn_card,
            font=ctk.CTkFont(family=c.FONT_FAMILY[0], size=13),
            fg_color="transparent",
            wrap="word",
            padx=12,
            pady=8
        )
        self.txt_vietnamese.grid(row=1, column=0, sticky="nsew", padx=2, pady=(0, 2))

        # Bind event
        self.txt_vietnamese.bind("<KeyRelease>", self._on_text_changed)

    # ── Event handler ────────────────────────────────────────────────────────

    def _on_text_changed(self, event=None) -> None:
        """Called every time the user releases a key in the VN textbox."""
        if self._on_vn_changed is not None:
            self._on_vn_changed(self.get_vietnamese_text())

    # ── Public API ───────────────────────────────────────────────────────────

    def set_japanese_text(self, text: str) -> None:
        """Replace the contents of the Japanese (read-only) textbox."""
        self.txt_japanese.configure(state="normal")
        self.txt_japanese.delete("1.0", "end")
        self.txt_japanese.insert("1.0", text)
        self.txt_japanese.configure(state="disabled")

    def set_vietnamese_text(self, text: str) -> None:
        """Replace the contents of the Vietnamese (editable) textbox."""
        self.txt_vietnamese.delete("1.0", "end")
        self.txt_vietnamese.insert("1.0", text)

    def get_vietnamese_text(self) -> str:
        """Return the current contents of the Vietnamese textbox (trailing newline stripped)."""
        return self.txt_vietnamese.get("1.0", "end-1c")

    def set_on_vn_changed(self, callback: Callable[[str], None]) -> None:
        """Register or replace the VN-text-changed callback after construction."""
        self._on_vn_changed = callback

    def highlight_japanese_term(self, term: str) -> None:
        """Highlight all occurrences of a term in the Japanese textbox and scroll to the first one."""
        self.clear_highlights()
        if not term:
            return

        # Configure highlight tag (Light blue)
        self.txt_japanese.tag_config("highlight", background="#0078D4", foreground="white")

        start_pos = "1.0"
        first_match = None
        
        while True:
            start_pos = self.txt_japanese.search(term, start_pos, stopindex="end")
            if not start_pos:
                break
            
            if first_match is None:
                first_match = start_pos
                
            end_pos = f"{start_pos}+{len(term)}c"
            self.txt_japanese.tag_add("highlight", start_pos, end_pos)
            start_pos = end_pos

        if first_match:
            self.txt_japanese.see(first_match)

    def clear_highlights(self) -> None:
        """Remove all highlight tags from the Japanese textbox."""
        self.txt_japanese.tag_remove("highlight", "1.0", "end")
