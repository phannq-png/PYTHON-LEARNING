"""Bottom bar component — action buttons and token counter (placeholder)."""

import customtkinter as ctk


class BottomBar(ctk.CTkFrame):
    """Bottom bar containing translation action buttons and token counter.

    Buttons are placeholders in P1-UI-001.
    Logic will be wired in feature 07-translation-ui.
    """

    def __init__(self, master: ctk.CTk, **kwargs) -> None:
        super().__init__(master, height=52, fg_color=("gray85", "gray20"), **kwargs)
        self.pack_propagate(False)
        self._build_widgets()

    def _build_widgets(self) -> None:
        """Build action buttons and token counter label."""
        # ── Action buttons (left side) ──────────────────────────────────────
        btn_configs = [
            ("⚡ Translate",    "blue",  self._on_translate),
            ("📋 Get Prompt",   None,    self._on_get_prompt),
            ("✅ Check Page",   None,    self._on_check_page),
            ("💾 Save",         "green", self._on_save),
        ]

        for label, color, cmd in btn_configs:
            kwargs: dict = {"text": label, "width": 130, "command": cmd}
            if color == "blue":
                kwargs["fg_color"] = ("#1A73E8", "#1558B0")
                kwargs["hover_color"] = ("#155DC0", "#0F4490")
            elif color == "green":
                kwargs["fg_color"] = ("#2E7D32", "#1B5E20")
                kwargs["hover_color"] = ("#1B5E20", "#104010")
            else:
                kwargs["fg_color"] = ("gray70", "gray30")
                kwargs["hover_color"] = ("gray60", "gray40")

            btn = ctk.CTkButton(self, **kwargs)
            btn.pack(side="left", padx=(8, 4), pady=10)

        # ── Token counter (right side) ──────────────────────────────────────
        self.lbl_tokens = ctk.CTkLabel(
            self,
            text="Tokens: — (Trang) | — (Tổng)",
            font=ctk.CTkFont(size=11),
            text_color=("gray40", "gray60"),
        )
        self.lbl_tokens.pack(side="right", padx=(8, 16), pady=10)

    # ── Placeholder callbacks ───────────────────────────────────────────────
    def _on_translate(self) -> None:
        """Placeholder: will be wired to translation engine."""
        pass

    def _on_get_prompt(self) -> None:
        """Placeholder: will be wired to prompt builder."""
        pass

    def _on_check_page(self) -> None:
        """Placeholder: will be wired to consistency checker."""
        pass

    def _on_save(self) -> None:
        """Placeholder: will be wired to session manager."""
        pass
