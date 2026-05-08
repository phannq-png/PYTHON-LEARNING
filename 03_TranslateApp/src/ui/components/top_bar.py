"""Top bar component for the main application window."""

import customtkinter as ctk
from typing import Optional, Callable, List
from src.utils import constants as c


class TopBar(ctk.CTkFrame):
    """Top bar containing file upload, domain selector, and export button."""

    def __init__(
        self, 
        master: ctk.CTk, 
        on_upload_callback: Optional[Callable[[], None]] = None,
        on_export_callback: Optional[Callable[[], None]] = None,
        **kwargs
    ) -> None:
        super().__init__(
            master, 
            height=54, 
            fg_color=("gray90", "gray15"), 
            corner_radius=0,
            **kwargs
        )
        self.pack_propagate(False)
        self._on_upload_callback = on_upload_callback
        self._on_export_callback = on_export_callback
        self._build_widgets()

    def _build_widgets(self) -> None:
        """Build and layout all widgets in the top bar."""
        # ── Upload File button ──────────────────────────────────────────────
        self.btn_upload = ctk.CTkButton(
            self,
            text="📂 Upload File",
            width=140,
            corner_radius=c.CORNER_RADIUS,
            fg_color=c.COLOR_PRIMARY,
            hover_color=c.COLOR_PRIMARY_HOVER,
            font=ctk.CTkFont(family=c.FONT_FAMILY[0], size=c.FONT_SIZE_BODY),
            command=self._on_upload,
        )
        self.btn_upload.pack(side="left", padx=(16, 8), pady=c.PADDING_STD)

        # ── Domain label + dropdown ─────────────────────────────────────────
        lbl_domain = ctk.CTkLabel(
            self, 
            text="Lĩnh vực:",
            font=ctk.CTkFont(family=c.FONT_FAMILY[0], size=c.FONT_SIZE_BODY)
        )
        lbl_domain.pack(side="left", padx=(12, 4), pady=c.PADDING_STD)

        self.cmb_domain = ctk.CTkComboBox(
            self,
            values=["common"],
            width=180,
            state="readonly",
            corner_radius=c.CORNER_RADIUS,
            border_width=c.BORDER_WIDTH,
            font=ctk.CTkFont(family=c.FONT_FAMILY[0], size=c.FONT_SIZE_BODY)
        )
        self.cmb_domain.set("common")
        self.cmb_domain.pack(side="left", padx=(0, 8), pady=c.PADDING_STD)

        # ── Export button (right-aligned) ───────────────────────────────────
        self.btn_export = ctk.CTkButton(
            self,
            text="📤 Export DOCX",
            width=130,
            corner_radius=c.CORNER_RADIUS,
            fg_color=c.COLOR_SUCCESS,
            font=ctk.CTkFont(family=c.FONT_FAMILY[0], size=c.FONT_SIZE_BODY),
            command=self._on_export,
        )
        self.btn_export.pack(side="right", padx=(8, 16), pady=c.PADDING_STD)

    # ── Actions ─────────────────────────────────────────────────────────────
    def _on_upload(self) -> None:
        """Trigger the upload callback provided by the parent."""
        if self._on_upload_callback:
            self._on_upload_callback()

    def _on_export(self) -> None:
        """Trigger the export callback provided by the parent."""
        if self._on_export_callback:
            self._on_export_callback()

    def set_selected_domain(self, domain_name: str) -> None:
        """Programmatically set the selected domain in the combobox."""
        if domain_name in self.cmb_domain.cget("values"):
            self.cmb_domain.set(domain_name)

    def refresh_domain_list(self, domains: List[str]) -> None:
        """Update the list of available domains in the dropdown."""
        self.cmb_domain.configure(values=domains)
        if self.cmb_domain.get() not in domains:
            self.cmb_domain.set(domains[0] if domains else "common")
