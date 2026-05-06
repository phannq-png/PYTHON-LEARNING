"""Right sidebar component — active glossary terms panel (placeholder)."""

import customtkinter as ctk


class RightSidebar(ctk.CTkFrame):
    """Right sidebar: displays active glossary terms for the current page.

    In P1-UI-001 this is a placeholder frame.
    Full implementation comes in feature 14-sidebar-glossary.
    """

    def __init__(self, master: ctk.CTk, **kwargs) -> None:
        super().__init__(master, width=220, fg_color=("gray80", "gray17"), **kwargs)
        self.pack_propagate(False)
        self.grid_propagate(False)
        self._build_widgets()

    def _build_widgets(self) -> None:
        """Build placeholder content."""
        lbl_title = ctk.CTkLabel(
            self,
            text="Thuật ngữ (Trang hiện tại)",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=("gray40", "gray60"),
            wraplength=190,
        )
        lbl_title.pack(pady=(16, 8), padx=8)

        # Separator line
        sep = ctk.CTkFrame(self, height=1, fg_color=("gray70", "gray35"))
        sep.pack(fill="x", padx=8, pady=(0, 8))

        lbl_placeholder = ctk.CTkLabel(
            self,
            text="(Chưa có thuật ngữ)",
            font=ctk.CTkFont(size=11),
            text_color=("gray55", "gray50"),
        )
        lbl_placeholder.pack(pady=8, padx=8)
