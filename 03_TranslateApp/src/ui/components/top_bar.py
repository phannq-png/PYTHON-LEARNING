"""Top bar component for the main application window."""

import customtkinter as ctk
from typing import Optional, Callable, List
from src.utils import constants as c
from src.ui.components.tooltip import add_tooltip


class TopBar(ctk.CTkFrame):
    """Top bar containing file upload, domain selector, and export button."""

    def __init__(
        self, 
        master: ctk.CTk, 
        on_upload_callback: Optional[Callable[[], None]] = None,
        on_export_callback: Optional[Callable[[], None]] = None,
        on_detect_callback: Optional[Callable[[], None]] = None,
        on_add_domain_callback: Optional[Callable[[], None]] = None,
        on_search_callback: Optional[Callable[[str], None]] = None,
        on_clear_callback: Optional[Callable[[], None]] = None,
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
        self._on_add_domain_callback = on_add_domain_callback
        self._on_search_callback = on_search_callback
        self._on_clear_callback = on_clear_callback
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
        add_tooltip(self.btn_upload, "Tải file Word (.docx) cần dịch")

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
        self.cmb_domain.pack(side="left", padx=(0, 4), pady=c.PADDING_STD)
        
        # ── Detect button ──────────────────────────────────────────────────
        self.btn_detect = ctk.CTkButton(
            self,
            text="✨",
            width=32,
            corner_radius=c.CORNER_RADIUS,
            fg_color=("gray75", "gray30"),
            hover_color=c.COLOR_AI,
            font=ctk.CTkFont(size=14),
            command=self._on_detect
        )
        self.btn_detect.pack(side="left", padx=(0, 2), pady=c.PADDING_STD)
        add_tooltip(self.btn_detect, "Tự động nhận diện lĩnh vực chuyên ngành bằng AI")

        # ── Add Domain button ──────────────────────────────────────────────
        self.btn_add = ctk.CTkButton(
            self,
            text="+",
            width=32,
            corner_radius=c.CORNER_RADIUS,
            fg_color=("gray75", "gray30"),
            hover_color=c.COLOR_PRIMARY,
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self._on_add
        )
        self.btn_add.pack(side="left", padx=(0, 8), pady=c.PADDING_STD)
        add_tooltip(self.btn_add, "Thêm lĩnh vực chuyên ngành mới")
        
        # ── Search section ──────────────────────────────────────────────────
        self.ent_search = ctk.CTkEntry(
            self,
            placeholder_text="Tìm kiếm nội dung (Nhật/Việt)...",
            width=220,
            corner_radius=c.CORNER_RADIUS,
            font=ctk.CTkFont(family=c.FONT_FAMILY[0], size=c.FONT_SIZE_BODY)
        )
        self.ent_search.pack(side="left", padx=(20, 0), pady=c.PADDING_STD)
        self.ent_search.bind("<Return>", lambda e: self._on_search())
        add_tooltip(self.ent_search, "Nhập từ khóa và nhấn Enter để tìm kiếm toàn bộ tài liệu")

        self.btn_clear = ctk.CTkButton(
            self.ent_search,
            text="✕",
            width=20,
            height=20,
            corner_radius=10,
            fg_color="transparent",
            text_color="gray50",
            hover_color=("gray80", "gray25"),
            font=ctk.CTkFont(size=12),
            command=self._on_clear
        )
        self.btn_clear.place(relx=1.0, rely=0.5, anchor="e", x=-4)
        add_tooltip(self.btn_clear, "Xóa từ khóa và kết quả tìm kiếm")

        self.btn_search = ctk.CTkButton(
            self,
            text="🔍",
            width=36,
            corner_radius=c.CORNER_RADIUS,
            fg_color=c.COLOR_PRIMARY,
            hover_color=c.COLOR_PRIMARY_HOVER,
            font=ctk.CTkFont(size=14),
            command=self._on_search
        )
        self.btn_search.pack(side="left", padx=(4, 8), pady=c.PADDING_STD)


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
        add_tooltip(self.btn_export, "Xuất bản dịch ra file Word (.docx)")

    # ── Actions ─────────────────────────────────────────────────────────────
    def _on_upload(self) -> None:
        """Trigger the upload callback provided by the parent."""
        if self._on_upload_callback:
            self._on_upload_callback()

    def _on_export(self) -> None:
        """Trigger the export callback provided by the parent."""
        if self._on_export_callback:
            self._on_export_callback()

    def _on_detect(self) -> None:
        """Trigger the domain detection callback."""
        if self._on_detect_callback:
            self._on_detect_callback()

    def _on_add(self) -> None:
        """Trigger the manual domain addition callback."""
        if self._on_add_domain_callback:
            self._on_add_domain_callback()

    def _on_search(self) -> None:
        """Trigger the search callback with current entry text."""
        text = self.ent_search.get().strip()
        if self._on_search_callback:
            self._on_search_callback(text)

    def _on_clear(self) -> None:
        """Clear search entry and trigger clear callback."""
        self.ent_search.delete(0, "end")
        if self._on_clear_callback:
            self._on_clear_callback()

    def set_selected_domain(self, domain_name: str) -> None:
        """Programmatically set the selected domain in the combobox."""
        if domain_name in self.cmb_domain.cget("values"):
            self.cmb_domain.set(domain_name)

    def set_search_text(self, text: str) -> None:
        """Update the search entry text."""
        self.ent_search.delete(0, "end")
        self.ent_search.insert(0, text)

    def refresh_domain_list(self, domains: List[str]) -> None:
        """Update the list of available domains in the dropdown."""
        self.cmb_domain.configure(values=domains)
        if self.cmb_domain.get() not in domains:
            self.cmb_domain.set(domains[0] if domains else "common")
