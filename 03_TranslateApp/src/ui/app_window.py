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
import threading
import traceback
from tkinter import messagebox, filedialog
from typing import Optional, List, Dict, Any

import customtkinter as ctk

from src.data.config_manager import ConfigManager
from src.data.session_manager import SessionManager
from src.data.glossary_repo import GlossaryRepository
from src.core.doc_processor import DocumentProcessor
from src.core.segmenter import TextSegmenter
from src.core.checker import ConsistencyChecker
from src.core.docx_exporter import DocxExporter
from src.core.token_tracker import TokenTracker
from src.services.gemini_client import GeminiClient
from src.utils.logger import setup_logger, get_logger
from src.utils import constants as c

from src.ui.components.bottom_bar import BottomBar
from src.ui.components.center_panel import CenterPanel
from src.ui.components.check_result_window import CheckResultWindow
from src.ui.components.export_window import ExportWindow
from src.ui.components.domain_detector import DomainSuggestionWindow
from src.ui.components.progress_window import ProgressWindow
from src.ui.segmentation_settings import SegmentationSettingsDialog
from src.ui.components.left_sidebar import LeftSidebar
from src.ui.components.right_sidebar import RightSidebar
from src.ui.components.top_bar import TopBar
from src.ui.term_manager import GlossaryManagerWindow


class AppWindow(ctk.CTk):
    """Main window of TranslatorApp.

    Orchestrates the flow between UI components and core logic modules.
    """

    _MIN_WIDTH: int = 1200
    _MIN_HEIGHT: int = 800

    def __init__(self) -> None:
        super().__init__()
        
        # ── Global Styling ─────────────────────────────────────────────────
        ctk.set_appearance_mode(c.THEME_MODE)
        ctk.set_default_color_theme("blue") # We'll use blue but customize colors
        
        # ── Logging ────────────────────────────────────────────────────────
        setup_logger()
        self.logger = get_logger("UI")
        
        # ── Logic Components ───────────────────────────────────────────────
        self.config_manager = ConfigManager()
        self.doc_processor = DocumentProcessor()
        self.segmenter = TextSegmenter()
        self.session_manager = SessionManager()
        self.checker = ConsistencyChecker()
        self.exporter = DocxExporter()
        self.token_tracker = TokenTracker()
        
        # ── State ──────────────────────────────────────────────────────────
        self.current_session: Optional[Dict[str, Any]] = None
        self.format_metadata: List[Dict[str, Any]] = []
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

        # ── Tools menu ─────────────────────────────────────────────────────
        tools_menu = tk.Menu(menubar, tearoff=False)
        tools_menu.add_command(
            label="Quản lý thuật ngữ",
            command=self._open_glossary_manager,
        )
        menubar.add_cascade(label="Tools", menu=tools_menu)

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
        self.top_bar = TopBar(
            self, 
            on_upload_callback=self._handle_file_upload,
            on_export_callback=self._open_export_dialog
        )
        self.top_bar.grid(row=0, column=0, columnspan=3, sticky="ew")

        # ── Left sidebar ───────────────────────────────────────────────────
        self.left_sidebar = LeftSidebar(self, on_page_selected=self._on_page_selected)
        self.left_sidebar.grid(row=1, column=0, sticky="ns", padx=(4, 0), pady=4)

        # ── Center panel ───────────────────────────────────────────────────
        self.center_panel = CenterPanel(self)
        self.center_panel.grid(row=1, column=1, sticky="nsew", padx=4, pady=4)

        # ── Right sidebar ──────────────────────────────────────────────────
        self.right_sidebar = RightSidebar(self, on_term_click=self.center_panel.highlight_japanese_term)
        self.right_sidebar.grid(row=1, column=2, sticky="ns", padx=(0, 4), pady=4)

        # ── Bottom bar ─────────────────────────────────────────────────────
        self.bottom_bar = BottomBar(
            self, 
            on_check_page_callback=self._handle_consistency_check,
            on_translate_callback=self._handle_translate
        )
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

        progress = ProgressWindow(self, title="Đang nạp tài liệu...")
        
        def run_load():
            try:
                # 1. Extract text
                self.after(0, lambda: progress.set_progress(0.2, "Đang đọc file DOCX..."))
                texts, metadata = self.doc_processor.extract_docx(file_path)
                self.format_metadata = metadata
                
                # 2. Segment & Paginate
                self.after(0, lambda: progress.set_progress(0.5, "Đang phân đoạn văn bản..."))
                seg_config = self.config_manager.get_segmentation_config()
                self.segmenter.split_on_enter = seg_config.get("split_on_enter", True)
                self.segmenter.split_on_soft_return = seg_config.get("split_on_soft_return", False)
                self.segmenter.custom_markers = seg_config.get("custom_markers", [])
                
                segments = self.segmenter.segment(texts)
                pages_segments = self.segmenter.paginate(segments)
                pages_text = ["\n".join(p) for p in pages_segments]
                
                # 3. Create Session
                self.after(0, lambda: progress.set_progress(0.8, "Đang khởi tạo phiên làm việc..."))
                domain = self.top_bar.cmb_domain.get()
                self.current_session = self.session_manager.create_session(
                    docx_path=file_path, 
                    segments=pages_text,
                    domain=domain
                )
                self.current_page_idx = 0
                
                # 4. Success callback
                def on_done():
                    progress.complete()
                    self.title(f"TranslatorApp — {tk.os.path.basename(file_path)}")
                    self.left_sidebar.populate_pages(len(pages_text), self.current_page_idx)
                    self._update_center_panel()
                    messagebox.showinfo("Thành công", f"Đã tải {len(pages_text)} trang văn bản.")
                    
                    # AI Domain Detection
                    sample_text = "\n".join(texts)[:5000]
                    threading.Thread(target=self._run_domain_detection, args=(sample_text,), daemon=True).start()

                self.after(0, on_done)
                
            except Exception as e:
                self.after(0, lambda: [progress.complete(), messagebox.showerror("Lỗi", f"Không thể xử lý file: {e}")])

        threading.Thread(target=run_load, daemon=True).start()

    def _on_page_selected(self, index: int) -> None:
        """Callback from LeftSidebar when a page is clicked."""
        if not self.current_session:
            return
            
        # 1. Save current page content to session memory
        current_vn = self.center_panel.get_vietnamese_text()
        self.current_session["pages"][self.current_page_idx]["vn"] = current_vn
        
        # 2. Switch page
        self.current_page_idx = index
        self.token_tracker.reset_page_counter()
        self._update_center_panel()
        self.bottom_bar.update_tokens(self.token_tracker.get_formatted_status())

    def _update_center_panel(self) -> None:
        """Refresh CenterPanel with data from current session page."""
        if not self.current_session:
            return
            
        page_data = self.current_session["pages"][self.current_page_idx]
        self.center_panel.set_japanese_text(page_data["jp"])
        self.center_panel.set_vietnamese_text(page_data["vn"])
        
        # Refresh Active Glossary Sidebar
        self.right_sidebar.update_terms(page_data["jp"], self._get_merged_glossary())
        
        # Update token display (page count is reset when selecting, so show 0 unless already tracked)
        self.bottom_bar.update_tokens(self.token_tracker.get_formatted_status())

    # ── Actions ────────────────────────────────────────────────────────────

    def _handle_translate(self) -> None:
        """Trigger AI translation for the current page."""
        if not self.current_session:
            return

        jp_text = self.center_panel.get_japanese_text()
        if not jp_text.strip():
            return

        # Show progress on bottom bar
        self.bottom_bar.show_progress("Đang dịch trang hiện tại...")
        
        def run_api():
            try:
                client = self._get_ai_client()
                glossary = self._get_merged_glossary()
                
                # Mock steps for progress visibility if it's too fast
                self.after(0, lambda: self.bottom_bar.set_progress(0.3, "Đang gửi prompt..."))
                
                translated_text, tokens = client.translate(jp_text, glossary)
                
                self.after(0, lambda: self.bottom_bar.set_progress(0.8, "Đang nhận kết quả..."))
                
                # Switch to main thread
                self.after(0, self._on_translation_complete, translated_text, tokens)
            except Exception as e:
                self.after(0, lambda: [
                    self.bottom_bar.hide_progress(),
                    messagebox.showerror("Lỗi API", f"Dịch thất bại: {e}")
                ])

        threading.Thread(target=run_api, daemon=True).start()

    def _on_translation_complete(self, text: str, tokens: int) -> None:
        """Handle translation result on the main thread."""
        self.bottom_bar.hide_progress()
        
        # Update UI text
        self.center_panel.set_vietnamese_text(text)
        
        # Update Session Data
        self.current_session["pages"][self.current_page_idx]["vn"] = text
        
        # Update Token Tracker
        self.token_tracker.add_usage(tokens)
        self.bottom_bar.update_tokens(self.token_tracker.get_formatted_status())
        self.show_toast("Dịch thành công!")

    # ── Error & Notification ───────────────────────────────────────────────

    def show_error(self, title: str, message: str, details: Optional[str] = None) -> None:
        """Show a user-friendly error dialog with optional technical details."""
        # 1. Log the error
        logger = get_logger("UI")
        log_msg = f"{title}: {message}"
        if details:
            log_msg += f"\nDetails: {details}"
        logger.error(log_msg)

        # 2. Show UI Dialog
        # Standard messagebox for now
        msg = f"{message}"
        if details:
            if messagebox.askyesno(title, f"{message}\n\nBạn có muốn xem chi tiết lỗi kỹ thuật không?", parent=self):
                # Show details in a new window (simple version)
                detail_win = ctk.CTkToplevel(self)
                detail_win.title("Chi tiết lỗi")
                detail_win.geometry("600x400")
                txt = ctk.CTkTextbox(detail_win)
                txt.pack(expand=True, fill="both", padx=10, pady=10)
                txt.insert("1.0", details)
                txt.configure(state="disabled")
        else:
            messagebox.showerror(title, message, parent=self)

    def show_toast(self, message: str, duration: int = 3000) -> None:
        """Show a temporary status message in the Bottom Bar."""
        # We reuse the status label in BottomBar for this
        self.bottom_bar.lbl_status.configure(text=message, text_color="#107C10")
        self.bottom_bar.progress_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.bottom_bar.progress_bar.pack_forget() # Hide bar, keep label
        
        def hide():
            self.bottom_bar.progress_frame.place_forget()
            self.bottom_bar.progress_bar.pack(side="top", fill="x") # Restore for next use
            self.bottom_bar.lbl_status.configure(text_color="#0078D4")
            
        self.after(duration, hide)

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

    def _open_glossary_manager(self) -> None:
        """Open the Glossary Manager window."""
        self.glossary_window = GlossaryManagerWindow(
            self,
            ai_client=self._get_ai_client(),
            on_change_callback=self._on_glossary_changed
        )

    def _get_ai_client(self) -> GeminiClient:
        """Initialize and return an AI client based on current configuration."""
        # For now, we only support Gemini in implementation
        api_config = self.config_manager.get_api_config()
        # Note: In a real scenario, we would decrypt the key here
        # For P3-BULK-001, we assume the key is available or will be handled by ConfigManager
        gemini_key = api_config.get("translation_api", {}).get("api_key", "")
        model = api_config.get("translation_api", {}).get("model", "gemini-1.5-pro")
        
        return GeminiClient(api_key=gemini_key, model_name=model)

    def _run_domain_detection(self, sample_text: str) -> None:
        """Call AI to detect domain in background."""
        try:
            # For detection, we can use a faster model if available
            client = self._get_ai_client()
            suggested = client.detect_domain(sample_text)
            
            # Switch back to main thread to update UI
            self.after(0, self._process_domain_result, suggested)
        except Exception as e:
            print(f"Domain detection failed: {e}")

    def _process_domain_result(self, suggested: str) -> None:
        """Analyze detection result and update UI or suggest new domain."""
        # 1. Get existing domains
        repo = GlossaryRepository("common")
        existing = repo.get_all_domains() # We assume this method exists or will be added
        
        # 2. Check for match
        suggested_lower = suggested.lower().strip()
        matched = None
        for d in existing:
            if d.lower() == suggested_lower:
                matched = d
                break
        
        if matched:
            # Auto select
            self.top_bar.set_selected_domain(matched)
            # Update session
            if self.current_session:
                self.current_session["domain"] = matched
        else:
            # Suggest new domain
            DomainSuggestionWindow(
                self,
                suggested_name=suggested,
                on_confirm=self._handle_create_domain
            )

    def _handle_create_domain(self, domain_name: str) -> None:
        """Create a new domain repository and select it."""
        try:
            # Create new repo (this creates the JSON file)
            new_repo = GlossaryRepository(domain_name)
            new_repo.save_glossary({"terms": {}, "domain": domain_name})
            
            # Update TopBar list
            all_domains = new_repo.get_all_domains()
            self.top_bar.refresh_domain_list(all_domains)
            self.top_bar.set_selected_domain(domain_name)
            
            if self.current_session:
                self.current_session["domain"] = domain_name
                
            messagebox.showinfo("Thành công", f"Đã tạo lĩnh vực mới: {domain_name}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tạo lĩnh vực mới: {e}")

    def _on_glossary_changed(self) -> None:
        """Callback when glossary data is modified."""
        if self.current_session:
            jp_text = self.center_panel.get_japanese_text()
            self.right_sidebar.update_terms(jp_text, self._get_merged_glossary())

    def _get_merged_glossary(self) -> Dict[str, str]:
        """Load and merge common and current domain glossaries."""
        # Load Common
        common_repo = GlossaryRepository("common")
        merged = common_repo.get_terms().copy()
        
        # Load Current Domain (if not common)
        current_domain = self.top_bar.cmb_domain.get()
        if current_domain != "common":
            domain_repo = GlossaryRepository(current_domain)
            merged.update(domain_repo.get_terms())
            
        return merged

    def _handle_consistency_check(self) -> None:
        """Run consistency check on the current page."""
        if not self.current_session:
            return

        # 1. Get current text
        jp_text = self.center_panel.get_japanese_text()
        vn_text = self.center_panel.get_vietnamese_text()

        # 2. Prepare merged glossary
        merged_glossary = self._get_merged_glossary()

        # 3. Run check
        mismatches = self.checker.check(jp_text, vn_text, merged_glossary)

        # 4. Display result
        CheckResultWindow(self, mismatches, self.current_page_idx + 1)

    def _open_export_dialog(self) -> None:
        """Open the Export Options dialog."""
        if not self.current_session:
            messagebox.showwarning("Cảnh báo", "Vui lòng mở tài liệu trước khi export.")
            return

        default_name = tk.os.path.basename(self.current_session["docx_path"])
        ExportWindow(
            self,
            default_filename=default_name,
            on_export=self._handle_export
        )

    def _handle_export(self, options: Dict[str, bool], output_path: str) -> None:
        """Execute the actual DOCX export using DocxExporter."""
        try:
            # Sync current page text before export
            self.current_session["pages"][self.current_page_idx]["vn"] = self.center_panel.get_vietnamese_text()
            
            self.exporter.export(
                original_path=self.current_session["docx_path"],
                output_path=output_path,
                pages_data=self.current_session["pages"],
                format_metadata=self.format_metadata,
                only_translated=options["only_translated"],
                bilingual=options["bilingual"]
            )
            messagebox.showinfo("Thành công", f"Đã export tài liệu thành công tại:\n{output_path}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Export thất bại: {str(e)}")
