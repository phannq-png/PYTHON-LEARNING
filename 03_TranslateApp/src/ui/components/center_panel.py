"""Center panel component — JP (read-only) / VN (editable) split view."""

import customtkinter as ctk
from typing import Callable, Optional


class CenterPanel(ctk.CTkFrame):
    """Center panel split horizontally into Japanese (top) and Vietnamese (bottom) text areas.

    - Top half: read-only Japanese source text.
    - Bottom half: editable Vietnamese translation text.

    Args:
        master: Parent widget.
        on_vn_changed: Optional callback invoked with the current Vietnamese text
                       every time the user releases a key in the VN textbox.
    """

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
        """Build the split text panel with labels and text areas."""
        # Allow both rows to expand equally
        self.rowconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)

        # ── Japanese panel (top) ────────────────────────────────────────────
        lbl_jp = ctk.CTkLabel(
            self,
            text="🇯🇵  Tiếng Nhật (Gốc)",
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w",
        )
        lbl_jp.grid(row=0, column=0, sticky="ew", padx=8, pady=(8, 2))

        self.txt_japanese = ctk.CTkTextbox(
            self,
            font=ctk.CTkFont(family="Yu Gothic", size=11),
            wrap="word",
            state="disabled",           # read-only
            fg_color=("gray90", "gray15"),
        )
        self.txt_japanese.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 4))
        self.rowconfigure(1, weight=3)

        # ── Horizontal divider ──────────────────────────────────────────────
        divider = ctk.CTkFrame(self, height=3, fg_color=("gray60", "gray35"))
        divider.grid(row=2, column=0, sticky="ew", padx=8, pady=2)
        self.rowconfigure(2, weight=0)

        # ── Vietnamese panel (bottom) ───────────────────────────────────────
        lbl_vn = ctk.CTkLabel(
            self,
            text="🇻🇳  Tiếng Việt (Bản dịch)",
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w",
        )
        lbl_vn.grid(row=3, column=0, sticky="ew", padx=8, pady=(4, 2))

        self.txt_vietnamese = ctk.CTkTextbox(
            self,
            font=ctk.CTkFont(size=11),
            wrap="word",
            fg_color=("gray95", "gray18"),
        )
        self.txt_vietnamese.grid(row=4, column=0, sticky="nsew", padx=8, pady=(0, 8))
        self.rowconfigure(3, weight=0)
        self.rowconfigure(4, weight=3)

        # Bind key-release event on VN textbox to fire the change callback
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
