"""Center panel component — JP (read-only) / VN (editable) split view."""

import tkinter as tk
import customtkinter as ctk
from typing import Callable, Optional
from src.utils import constants as c


class CenterPanel(ctk.CTkFrame):
    """Center panel split horizontally into JP (read-only) and VN (editable)."""

    def __init__(
        self,
        master: ctk.CTk,
        on_vn_changed: Optional[Callable[[str], None]] = None,
        on_add_glossary: Optional[Callable[[str], None]] = None,
        on_search_local: Optional[Callable[[str], None]] = None,
        **kwargs,
    ) -> None:
        super().__init__(master, fg_color="transparent", **kwargs)
        self._on_vn_changed = on_vn_changed
        self._on_add_glossary = on_add_glossary
        self._on_search_local = on_search_local
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

        vn_header = ctk.CTkFrame(self.vn_card, fg_color="transparent")
        vn_header.grid(row=0, column=0, sticky="ew", padx=12, pady=4)
        vn_header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            vn_header, 
            text="🇻🇳  BẢN DỊCH TIẾNG VIỆT", 
            font=ctk.CTkFont(family=c.FONT_FAMILY[0], size=c.FONT_SIZE_SMALL, weight="bold"),
            text_color=c.COLOR_SUCCESS
        ).grid(row=0, column=0, sticky="w")

        self.chk_review = ctk.CTkCheckBox(
            vn_header, 
            text="Đã Review", 
            font=ctk.CTkFont(family=c.FONT_FAMILY[0], size=c.FONT_SIZE_SMALL),
            checkbox_width=18, 
            checkbox_height=18,
            corner_radius=4,
            command=self._on_text_changed # Use same callback or new one? I'll add a new one if needed, but AppWindow can check both.
        )
        self.chk_review.grid(row=0, column=1, sticky="e")

        self.txt_vietnamese = ctk.CTkTextbox(
            self.vn_card,
            font=ctk.CTkFont(family=c.FONT_FAMILY[0], size=13),
            fg_color="transparent",
            wrap="word",
            padx=12,
            pady=8
        )
        self.txt_vietnamese.grid(row=1, column=0, sticky="nsew", padx=2, pady=(0, 2))

        # Bind events
        self.txt_vietnamese.bind("<KeyRelease>", self._on_text_changed)
        self.txt_japanese.bind("<Button-3>", self._show_context_menu)
        self.txt_vietnamese.bind("<Button-3>", self._show_context_menu)
        
        # Context Menu
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="✨ Thêm vào thuật ngữ", command=self._add_selection_to_glossary)
        self.context_menu.add_command(label="🔍 Tìm kiếm", command=self._search_selection)

    # ── Event handler ────────────────────────────────────────────────────────

    def _on_text_changed(self, event=None) -> None:
        """Called every time the user releases a key in the VN textbox."""
        if self._on_vn_changed is not None:
            self._on_vn_changed(self.get_vietnamese_text())

    def _show_context_menu(self, event):
        """Show context menu if text is selected in the textbox."""
        self._last_context_widget = event.widget
        try:
            # For CTK Textbox, we need to access the underlying tkinter widget's selection
            selected_text = self._last_context_widget.selection_get()
            if selected_text:
                # If clicking VN box, hide glossary command as it's for JP source
                if self._last_context_widget == self.txt_vietnamese:
                    self.context_menu.entryconfigure("✨ Thêm vào thuật ngữ", state="disabled")
                else:
                    self.context_menu.entryconfigure("✨ Thêm vào thuật ngữ", state="normal")
                    
                self.context_menu.post(event.x_root, event.y_root)
        except tk.TclError:
            # No selection
            pass

    def _add_selection_to_glossary(self):
        """Invoke the callback to add selected text to glossary."""
        try:
            if not hasattr(self, "_last_context_widget"): return
            selected_text = self._last_context_widget.selection_get()
            if selected_text and self._on_add_glossary:
                self._on_add_glossary(selected_text.strip())
        except tk.TclError:
            pass

    def _search_selection(self):
        """Invoke search callback for global search."""
        try:
            if not hasattr(self, "_last_context_widget"): return
            selected_text = self._last_context_widget.selection_get()
            if not selected_text: return
            
            selected_text = selected_text.strip()
            if self._on_search_local:
                self._on_search_local(selected_text)
        except tk.TclError:
            pass


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

    def get_japanese_text(self) -> str:
        """Return the current contents of the Japanese textbox."""
        return self.txt_japanese.get("1.0", "end-1c")

    def set_reviewed(self, is_reviewed: bool) -> None:
        """Set the checked state of the review checkbox."""
        if is_reviewed:
            self.chk_review.select()
        else:
            self.chk_review.deselect()

    def is_reviewed(self) -> bool:
        """Return whether the review checkbox is checked."""
        return self.chk_review.get() == 1

    def set_on_vn_changed(self, callback: Callable[[str], None]) -> None:
        """Register or replace the VN-text-changed callback after construction."""
        self._on_vn_changed = callback

    def highlight_terms(self, jp_term: str, vn_term: Optional[str] = None) -> None:
        """Highlight occurrences in both JP (read-only) and VN (editable) textboxes."""
        self.clear_highlights()
        
        # Highlight JP
        if jp_term:
            self._highlight_in_widget(self.txt_japanese, jp_term, "#0078D4") # Primary blue

        # Highlight VN
        if vn_term:
            self._highlight_in_widget(self.txt_vietnamese, vn_term, "#107C10") # Success green

    def highlight_search_text(self, text: str) -> None:
        """Highlight occurrences of text in both boxes with yellow search color."""
        if not text: return
        self._highlight_in_widget(self.txt_japanese, text, "#FFFF00", tag_name="search", text_color="black")
        self._highlight_in_widget(self.txt_vietnamese, text, "#FFFF00", tag_name="search", text_color="black")

    def highlight_term_selection(self, jp: str, vn: str) -> None:
        """Highlight a specific JP and VN term pair (Orange-Yellow)."""
        self.clear_term_selection_highlight()
        if jp:
            self._highlight_in_widget(self.txt_japanese, jp, "#F39C12", tag_name="term_select", text_color="black")
        if vn:
            self._highlight_in_widget(self.txt_vietnamese, vn, "#F39C12", tag_name="term_select", text_color="black")

    def clear_term_selection_highlight(self) -> None:
        """Remove only the term selection highlight."""
        self.txt_japanese.tag_remove("term_select", "1.0", "end")
        self.txt_vietnamese.tag_remove("term_select", "1.0", "end")

    def clear_search_highlights(self) -> None:
        """Remove search-specific highlights from both boxes."""
        self.txt_japanese.tag_remove("search", "1.0", "end")
        self.txt_vietnamese.tag_remove("search", "1.0", "end")

    def _highlight_in_widget(self, widget: ctk.CTkTextbox, term: str, color: str, tag_name: str = "highlight", text_color: str = "white") -> None:
        """Internal helper to highlight text in a specific textbox."""
        if not term: return
        
        widget.tag_config(tag_name, background=color, foreground=text_color)
        widget.tag_raise("sel")
        
        start_pos = "1.0"
        first_match = None
        
        while True:
            start_pos = widget.search(term, start_pos, stopindex="end", nocase=True)
            if not start_pos:
                break
            
            if first_match is None:
                first_match = start_pos
                
            end_pos = f"{start_pos}+{len(term)}c"
            widget.tag_add(tag_name, start_pos, end_pos)
            start_pos = end_pos

        if first_match:
            widget.see(first_match)

    def clear_highlights(self) -> None:
        """Remove all highlight tags from both textboxes."""
        self.txt_japanese.tag_remove("highlight", "1.0", "end")
        self.txt_japanese.tag_remove("search", "1.0", "end")
        self.txt_vietnamese.tag_remove("highlight", "1.0", "end")
        self.txt_vietnamese.tag_remove("search", "1.0", "end")
