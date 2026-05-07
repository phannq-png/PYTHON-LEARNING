"""Top bar component for the main application window."""

import customtkinter as ctk
from typing import Optional, Callable


class TopBar(ctk.CTkFrame):
    """Top bar containing file upload, domain selector, and export button."""

    def __init__(
        self, 
        master: ctk.CTk, 
        on_upload_callback: Optional[Callable[[], None]] = None,
        **kwargs
    ) -> None:
        super().__init__(master, height=48, fg_color=("gray85", "gray20"), **kwargs)
        self.pack_propagate(False)
        self._on_upload_callback = on_upload_callback
        self._build_widgets()

    def _build_widgets(self) -> None:
        """Build and layout all widgets in the top bar."""
        # ── Upload File button ──────────────────────────────────────────────
        self.btn_upload = ctk.CTkButton(
            self,
            text="📂 Upload File",
            width=140,
            command=self._on_upload,
        )
        self.btn_upload.pack(side="left", padx=(12, 8), pady=8)

        # ── Domain label + dropdown ─────────────────────────────────────────
        lbl_domain = ctk.CTkLabel(self, text="Lĩnh vực:")
        lbl_domain.pack(side="left", padx=(4, 2), pady=8)

        self.cmb_domain = ctk.CTkComboBox(
            self,
            values=["common"],
            width=180,
            state="readonly",
        )
        self.cmb_domain.set("common")
        self.cmb_domain.pack(side="left", padx=(0, 8), pady=8)

        # ── Export button (right-aligned) ───────────────────────────────────
        self.btn_export = ctk.CTkButton(
            self,
            text="📤 Export",
            width=120,
            fg_color=("gray70", "gray30"),
            hover_color=("gray60", "gray40"),
            command=self._on_export,
        )
        self.btn_export.pack(side="right", padx=(8, 12), pady=8)

    # ── Placeholder callbacks ───────────────────────────────────────────────
    def _on_upload(self) -> None:
        """Trigger the upload callback provided by the parent."""
        if self._on_upload_callback:
            self._on_upload_callback()

    def _on_export(self) -> None:
        """Placeholder: will be wired to export logic."""
        pass
