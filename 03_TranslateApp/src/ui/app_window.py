"""Main application window for the TranslatorApp.

Builds the full UI skeleton:
    - Menu Bar (File / Settings / Help)
    - Top Bar (Upload, Domain, Export)
    - Left Sidebar (page navigation placeholder)
    - Center Panel (JP read-only | VN editable)
    - Right Sidebar (active terms placeholder)
    - Bottom Bar (action buttons + token counter)
"""

import tkinter as tk
from tkinter import messagebox, filedialog
from typing import Optional, List, Dict, Any

import customtkinter as ctk

from src.data.config_manager import ConfigManager
from src.data.session_manager import SessionManager
from src.core.doc_processor import DocumentProcessor
from src.core.segmenter import TextSegmenter

from src.ui.components.bottom_bar import BottomBar
from src.ui.components.center_panel import CenterPanel
from src.ui.segmentation_settings import SegmentationSettingsDialog
from src.ui.components.left_sidebar import LeftSidebar
from src.ui.components.right_sidebar import RightSidebar
from src.ui.components.top_bar import TopBar


class AppWindow(ctk.CTk):
    """Main window of TranslatorApp.

    Orchestrates the flow between UI components and core logic modules.
    """

    _MIN_WIDTH: int = 1200
    _MIN_HEIGHT: int = 800

    def __init__(self) -> None:
        super().__init__()
        
        # ── Logic Components ───────────────────────────────────────────────
        self.config_manager = ConfigManager()
        self.doc_processor = DocumentProcessor()
        self.segmenter = TextSegmenter()
        self.session_manager = SessionManager()
        
        # ── State ──────────────────────────────────────────────────────────
        self.current_session: Optional[Dict[str, Any]] = None
        self.current_page_idx: int = 0
        self.seg_dialog = None
        
        # ── UI Setup ───────────────────────────────────────────────────────
        self._configure_window()
        self._build_menu_bar()
        self._build_layout()

    # ── Window configuration ────────────────────────────────────────────────

    def _configure_window(self) -> None:
        """Set window title, minimum size, and initial geometry."""
        self.title("TranslatorApp — Dịch tài liệu chuyên ngành Nhật-Việt")
        self.minsize(self._MIN_WIDTH, self._MIN_HEIGHT)
        self.geometry(f"{self._MIN_WIDTH}x{self._MIN_HEIGHT}")

    # ── Menu bar ────────────────────────────────────────────────────────────

    def _build_menu_bar(self) -> None:
        """Build the native tk.Menu bar."""
        menubar = tk.Menu(self)

        # ── File menu ──────────────────────────────────────────────────────
        file_menu = tk.Menu(menubar, tearoff=False)
        file_menu.add_command(label="Mở file…", command=self._handle_file_upload)
        file_menu.add_separator()
        file_menu.add_command(label="Thoát", command=self.destroy)
        menubar.add_cascade(label="File", menu=file_menu)

        # ── Settings menu ──────────────────────────────────────────────────
        settings_menu = tk.Menu(menubar, tearoff=False)
        settings_menu.add_command(
            label="Segmentation Settings",
            command=self._open_segmentation_settings,
        )
        settings_menu.add_command(
            label="API Settings",
            command=self._open_api_settings,
        )
        menubar.add_cascade(label="Settings", menu=settings_menu)

        # ── Help menu ──────────────────────────────────────────────────────
        help_menu = tk.Menu(menubar, tearoff=False)
        help_menu.add_command(label="About", command=self._menu_help_about)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.config(menu=menubar)

    # ── Main layout ─────────────────────────────────────────────────────────

    def _build_layout(self) -> None:
        """Build and grid all major UI panels."""
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=0)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0)

        # ── Top bar ────────────────────────────────────────────────────────
        self.top_bar = TopBar(self, on_upload_callback=self._handle_file_upload)
        self.top_bar.grid(row=0, column=0, columnspan=3, sticky="ew")

        # ── Left sidebar ───────────────────────────────────────────────────
        self.left_sidebar = LeftSidebar(self, on_page_selected=self._on_page_selected)
        self.left_sidebar.grid(row=1, column=0, sticky="ns", padx=(4, 0), pady=4)

        # ── Center panel ───────────────────────────────────────────────────
        self.center_panel = CenterPanel(self)
        self.center_panel.grid(row=1, column=1, sticky="nsew", padx=4, pady=4)

        # ── Right sidebar ──────────────────────────────────────────────────
        self.right_sidebar = RightSidebar(self)
        self.right_sidebar.grid(row=1, column=2, sticky="ns", padx=(0, 4), pady=4)

        # ── Bottom bar ─────────────────────────────────────────────────────
        self.bottom_bar = BottomBar(self)
        self.bottom_bar.grid(row=2, column=0, columnspan=3, sticky="ew")

    # ── Business Logic ──────────────────────────────────────────────────────

    def _handle_file_upload(self) -> None:
        """Process file selection, extraction, segmentation, and session creation."""
        file_path = filedialog.askopenfilename(
            title="Chọn tài liệu tiếng Nhật",
            filetypes=[("Word documents", "*.docx")]
        )
        
        if not file_path:
            return

        try:
            # 1. Extract text
            texts, _ = self.doc_processor.extract_docx(file_path)
            
            # 2. Segment & Paginate
            # Update segmenter from config before processing
            seg_config = self.config_manager.get_segmentation_config()
            self.segmenter.split_on_enter = seg_config.get("split_on_enter", True)
            self.segmenter.split_on_soft_return = seg_config.get("split_on_soft_return", False)
            self.segmenter.custom_markers = seg_config.get("custom_markers", [])
            
            segments = self.segmenter.segment(texts)
            pages_segments = self.segmenter.paginate(segments)
            pages_text = ["\n".join(p) for p in pages_segments]
            
            # 3. Create Session
            domain = self.top_bar.cmb_domain.get()
            self.current_session = self.session_manager.create_session(
                docx_path=file_path, 
                segments=pages_text,
                domain=domain
            )
            self.current_page_idx = 0
            
            # 4. Update UI
            self.title(f"TranslatorApp — {tk.os.path.basename(file_path)}")
            self.left_sidebar.populate_pages(len(pages_text), self.current_page_idx)
            self._update_center_panel()
            
            messagebox.showinfo("Thành công", f"Đã tải {len(pages_text)} trang văn bản.")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xử lý file: {str(e)}")

    def _on_page_selected(self, index: int) -> None:
        """Callback from LeftSidebar when a page is clicked."""
        if not self.current_session:
            return
            
        # 1. Save current page content to session memory
        current_vn = self.center_panel.get_vietnamese_text()
        self.current_session["pages"][self.current_page_idx]["vn"] = current_vn
        
        # 2. Switch page
        self.current_page_idx = index
        self._update_center_panel()

    def _update_center_panel(self) -> None:
        """Refresh CenterPanel with data from current session page."""
        if not self.current_session:
            return
            
        page_data = self.current_session["pages"][self.current_page_idx]
        self.center_panel.set_japanese_text(page_data["jp"])
        self.center_panel.set_vietnamese_text(page_data["vn"])

    # ── Dialogs ─────────────────────────────────────────────────────────────

    def _open_segmentation_settings(self) -> None:
        """Open Segmentation Settings dialog."""
        if self.seg_dialog is None or not self.seg_dialog.winfo_exists():
            self.seg_dialog = SegmentationSettingsDialog(self, self.config_manager)
        else:
            self.seg_dialog.focus()

    def _open_api_settings(self) -> None:
        """Open API Settings dialog (placeholder until feature 08-api-integration)."""
        messagebox.showinfo(
            "API Settings",
            "Chức năng này sẽ được hoàn thiện ở feature 08-api-integration.",
            parent=self,
        )

    def _menu_help_about(self) -> None:
        """Show application about dialog."""
        messagebox.showinfo(
            "About TranslatorApp",
            "TranslatorApp v0.1\nDịch tài liệu chuyên ngành Nhật → Việt\n\nPhase 1 — UI Skeleton",
            parent=self,
        )
