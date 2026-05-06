"""Center panel component — JP (read-only) / VN (editable) split view."""

import customtkinter as ctk


class CenterPanel(ctk.CTkFrame):
    """Center panel split horizontally into Japanese (top) and Vietnamese (bottom) text areas.

    - Top half: read-only Japanese source text.
    - Bottom half: editable Vietnamese translation text.

    Full translation logic is wired in feature 07-translation-ui.
    """

    def __init__(self, master: ctk.CTk, **kwargs) -> None:
        super().__init__(master, fg_color="transparent", **kwargs)
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
