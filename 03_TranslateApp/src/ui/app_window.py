"""Main application window for the TranslatorApp (v1.1)."""

import tkinter as tk
import os
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
from src.services.openai_client import OpenAIClient
from src.services.base_client import BaseAIClient
from src.utils.logger import setup_logger, get_logger
from src.utils import constants as c

from src.ui.components.bottom_bar import BottomBar
from src.ui.components.spinner import LoadingSpinner
from src.ui.components.center_panel import CenterPanel
from src.ui.components.check_result_window import CheckResultWindow
from src.ui.components.export_window import ExportWindow
from src.ui.components.domain_detector import DomainSuggestionWindow
from src.ui.components.progress_window import ProgressWindow
from src.ui.api_settings import ApiSettingsDialog
from src.ui.segmentation_settings import SegmentationSettingsDialog
from src.ui.components.left_sidebar import LeftSidebar
from src.ui.components.right_sidebar import RightSidebar
from src.ui.components.top_bar import TopBar
from src.ui.components.help_window import UserGuideWindow
from src.ui.components.about_window import AboutWindow
from src.ui.term_manager import GlossaryManagerWindow


class AppWindow(ctk.CTk):
    """Orchestrator for the TranslatorApp."""

    _MIN_WIDTH: int = 1200
    _MIN_HEIGHT: int = 800

    def __init__(self) -> None:
        super().__init__()
        
        # ── Global Styling ─────────────────────────────────────────────────
        ctk.set_appearance_mode(c.THEME_MODE)
        ctk.set_default_color_theme("blue")
        
        # ── Logging ────────────────────────────────────────────────────────
        setup_logger()
        self.logger = get_logger("UI")
        
        # ── Logic Components ───────────────────────────────────────────────
        self.config_manager = ConfigManager()
        
        # Apply preferences (Appearance mode)
        prefs = self.config_manager.load_preferences()
        ctk.set_appearance_mode(prefs.get("appearance_mode", "dark"))
        
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
        self.current_mismatches: List[Dict[str, Any]] = []
        self.seg_dialog = None
        self._auto_save_timer_id = None
        self.current_search_text: Optional[str] = None
        
        # ── UI Setup ───────────────────────────────────────────────────────
        self._configure_window()
        self._build_menu_bar()
        self._build_layout()
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        
        # ── Key Bindings ───────────────────────────────────────────────────
        self.bind("<Escape>", lambda e: self._handle_esc_key())

        
        # ── Startup ────────────────────────────────────────────────────────
        self._refresh_all_domains()
        self.after(100, self._perform_startup_api_check)
        self._start_auto_save_timer()
        self.state("zoomed") # Ensure maximized on start

    def _perform_startup_api_check(self):
        """Automatically validate all API keys on startup and re-enable working ones."""
        config = self.config_manager.load_api_config()
        keys = config.get("keys", [])
        if not keys:
            messagebox.showwarning("Thiếu cấu hình", "Chưa có API Key nào được cấu hình. Vui lòng vào Tools -> API Settings.")
            self.after(500, self._open_api_settings)
            return

        self.spinner.start("Đang kiểm tra toàn bộ API Keys...")
        
        def run_all_tests():
            active_count = 0
            for i, k_data in enumerate(keys):
                name = k_data.get("name", k_data["provider"].upper())
                self.after(0, lambda n=name, idx=i+1: self.spinner.set_text(f"Đang kiểm tra API {idx}/{len(keys)}: {n}..."))
                
                success = False
                try:
                    client = self._create_client_from_data(k_data)
                    if client:
                        success = client.test_connection()
                except: success = False
                
                if success:
                    active_count += 1
                    self.config_manager.update_api_key_status(k_data["id"], "active", is_enabled=True)
                else:
                    self.config_manager.update_api_key_status(k_data["id"], "inactive")

            def on_done():
                self.spinner.stop()
                if active_count == 0:
                    messagebox.showerror("Lỗi Kết nối", "Không có API Key nào hoạt động. Vui lòng kiểm tra lại cấu hình.")
                    self._open_api_settings()
                else:
                    messagebox.showinfo("Kết quả kiểm tra API", f"Hoàn tất kiểm tra!\n\nSố lượng: {active_count}/{len(keys)} API Keys đang hoạt động tốt và đã sẵn sàng.")
                    # After API check is done and user closed the dialog, check for resume session
                    self._check_for_resume_session()
            
            self.after(0, on_done)

        threading.Thread(target=run_all_tests, daemon=True).start()

    def _on_close(self):
        """Handle application close event with save confirmation."""
        if self.current_session:
            ans = messagebox.askyesnocancel(
                "Xác nhận thoát", 
                "Bạn có muốn lưu lại tiến độ phiên làm việc hiện tại trước khi thoát không?"
            )
            if ans is True: # Yes
                self._handle_save()
                self.destroy()
            elif ans is False: # No
                self.destroy()
            # If None (Cancel), do nothing
        else:
            if messagebox.askokcancel("Thoát", "Bạn có chắc chắn muốn thoát ứng dụng?"):
                self.destroy()

    def _configure_window(self) -> None:
        self.title("TranslatorApp v1.2.0 — Dịch tài liệu chuyên ngành Nhật-Việt")
        self.minsize(self._MIN_WIDTH, self._MIN_HEIGHT)

    def _build_menu_bar(self) -> None:
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=False)
        file_menu.add_command(label="Mở file DOCX…", command=self._handle_file_upload)
        file_menu.add_command(label="Lịch sử phiên dịch…", command=self._open_session_history)
        file_menu.add_separator()
        file_menu.add_command(label="Thoát", command=self.destroy)
        menubar.add_cascade(label="File", menu=file_menu)

        settings_menu = tk.Menu(menubar, tearoff=False)
        settings_menu.add_command(label="Segmentation Settings", command=self._open_segmentation_settings)
        settings_menu.add_command(label="API Settings", command=self._open_api_settings)
        settings_menu.add_command(label="Preferences", command=self._open_preferences)
        settings_menu.add_separator()
        settings_menu.add_command(label="Export All Settings…", command=self._export_all_settings)
        settings_menu.add_command(label="Import All Settings…", command=self._import_all_settings)
        menubar.add_cascade(label="Settings", menu=settings_menu)

        tools_menu = tk.Menu(menubar, tearoff=False)
        tools_menu.add_command(label="Quản lý thuật ngữ", command=self._open_glossary_manager)
        tools_menu.add_command(label="Quản lý lĩnh vực", command=self._open_domain_manager)
        menubar.add_cascade(label="Tools", menu=tools_menu)

        help_menu = tk.Menu(menubar, tearoff=False)
        help_menu.add_command(label="Hướng dẫn sử dụng", command=self._open_user_guide)
        help_menu.add_command(label="About", command=self._menu_help_about)
        menubar.add_cascade(label="Help", menu=help_menu)
        self.config(menu=menubar)

    def _build_layout(self) -> None:
        self.rowconfigure(1, weight=1)
        self.columnconfigure(1, weight=1)

        self.top_bar = TopBar(self, 
                             on_upload_callback=self._handle_file_upload,
                             on_export_callback=self._open_export_dialog,
                             on_detect_callback=self._handle_manual_domain_detection,
                             on_add_domain_callback=self._handle_add_domain_manual,
                             on_search_callback=self._handle_search_all,
                             on_clear_callback=self._handle_clear_search)
        self.top_bar.grid(row=0, column=0, columnspan=3, sticky="ew")

        self.left_sidebar = LeftSidebar(self, 
                                        on_page_selected=self._on_page_selected,
                                        on_clear_search=self._handle_clear_search)
        self.left_sidebar.grid(row=1, column=0, sticky="ns", padx=(4, 0), pady=4)

        self.center_panel = CenterPanel(self, 
                                        on_vn_changed=self._on_vn_changed,
                                        on_add_glossary=self._handle_add_glossary_from_selection,
                                        on_search_local=self._handle_local_search)
        self.center_panel.grid(row=1, column=1, sticky="nsew", padx=4, pady=4)

        self.right_sidebar = RightSidebar(self, on_term_click=self._handle_term_selection)
        self.right_sidebar.grid(row=1, column=2, sticky="nsew", padx=4, pady=4)

        self.bottom_bar = BottomBar(
            self, 
            on_check_page_callback=self._handle_consistency_check,
            on_check_all_callback=self._handle_check_all,
            on_translate_callback=self._handle_translate,
            on_translate_all_callback=self._handle_translate_all,
            on_get_prompt_callback=self._handle_get_prompt,
            on_save_callback=lambda: self._handle_save(show_msg=True)
        )
        self.bottom_bar.grid(row=2, column=0, columnspan=3, sticky="ew")

        # ── Global Spinner Overlay ────────────────────────────────────────
        self.spinner = LoadingSpinner(self)

    # ── Logic ──────────────────────────────────────────────────────────────

    def _handle_file_upload(self) -> None:
        """Process file selection with session-close confirmation."""
        # Check for active session first (Spec 4.9.4)
        if self.current_session:
            msg = "Bạn có một phiên làm việc đang mở. Bạn có muốn LƯU tiến độ hiện tại trước khi mở file mới không?"
            choice = messagebox.askyesnocancel("Xác nhận thay đổi", msg, parent=self)
            
            if choice is True: # Yes, save first
                self._handle_save()
            elif choice is None: # Cancel operation
                return
            # If False (No), proceed to open without saving

        file_path = filedialog.askopenfilename(title="Chọn tài liệu", filetypes=[("Word documents", "*.docx")])
        if not file_path: return
        progress = ProgressWindow(self, title="Đang nạp tài liệu...")
        
        def run_load():
            try:
                self.after(0, lambda: progress.set_progress(0.2, "Đang đọc file..."))
                texts, metadata = self.doc_processor.extract_docx(file_path)
                self.format_metadata = metadata
                
                self.after(0, lambda: progress.set_progress(0.5, "Đang phân đoạn..."))
                cfg = self.config_manager.get_segmentation_config()
                self.segmenter.split_on_enter = cfg.get("split_on_enter", True)
                self.segmenter.split_on_soft_return = cfg.get("split_on_soft_return", False)
                self.segmenter.custom_markers = cfg.get("custom_markers", [])
                self.segmenter.max_chars_per_page = cfg.get("max_chars", 1000)
                
                segs = self.segmenter.segment(texts)
                pages = self.segmenter.paginate(segs)
                pages_text = ["\n".join(p) for p in pages]
                
                self.after(0, lambda: progress.set_progress(0.8, "Khởi tạo session..."))
                dom = self.top_bar.cmb_domain.get()
                self.current_session = self.session_manager.create_session(docx_path=file_path, segments=pages_text, domain=dom)
                self.current_page_idx = 0
                
                def on_done():
                    progress.complete()
                    self.title(f"TranslatorApp — {os.path.basename(file_path)}")
                    self.left_sidebar.populate_pages(self.current_session["pages"], 0)
                    self._update_center_panel(self.current_page_idx)
                    # AI Detect: Skip first page if possible as it's often a title/ToC
                    detection_text = "\n".join(pages_text[1:]) if len(pages_text) > 1 else pages_text[0]
                    threading.Thread(target=self._run_domain_detection, args=(detection_text[:5000],), daemon=True).start()

                self.after(0, on_done)
            except Exception as e:
                err_msg = str(e)
                self.after(0, lambda msg=err_msg: [progress.complete(), self.show_error("Lỗi nạp file", msg)])

        threading.Thread(target=run_load, daemon=True).start()

    def _on_vn_changed(self, text: str):
        """Callback from CenterPanel when VN text changes."""
        if self.current_session:
            page = self.current_session["pages"][self.current_page_idx]
            page["vn"] = text
            if text.strip():
                page["is_translated"] = True
            # Update sidebar indicator
            self.left_sidebar.update_page_status(self.current_page_idx, page["is_translated"], page.get("check_status"), page.get("is_reviewed", False))

    def _on_page_selected(self, index: int) -> None:
        if not self.current_session: return
        vn_text = self.center_panel.get_vietnamese_text()
        page = self.current_session["pages"][self.current_page_idx]
        page["vn"] = vn_text
        if vn_text.strip():
            page["is_translated"] = True
        
        # Save state
        page["is_reviewed"] = self.center_panel.is_reviewed()
        self.left_sidebar.update_page_status(self.current_page_idx, page["is_translated"], page["check_status"], page["is_reviewed"])
        
        self.current_page_idx = index
        page = self.current_session["pages"][index]
        self.current_mismatches = page.get("mismatches", []) # Load from session
        self.token_tracker.reset_page_counter()
        self._update_center_panel(self.current_page_idx)

    def _update_center_panel(self, page_index: int) -> None:
        """Load page content and apply highlights."""
        # Clear term selection when switching pages
        self.right_sidebar.clear_selection()
        self.center_panel.clear_term_selection_highlight()
        
        if not self.current_session: return
        page = self.current_session["pages"][page_index]
        self.center_panel.set_japanese_text(page["jp"])
        self.center_panel.set_vietnamese_text(page["vn"])
        self.center_panel.set_reviewed(page.get("is_reviewed", False))
        
        # Re-apply search highlight if active
        if self.current_search_text:
            self.center_panel.highlight_search_text(self.current_search_text)
            
        self.right_sidebar.update_terms(page["jp"], self._get_merged_glossary(), mismatches=self.current_mismatches)
        self.bottom_bar.update_tokens(self.token_tracker.get_formatted_status())

    def _handle_translate(self) -> None:
        if not self.current_session: return
        jp = self.center_panel.get_japanese_text()
        if not jp.strip(): return
        self.spinner.start("Đang dịch văn bản...")
        domain = self.top_bar.cmb_domain.get()
        
        def run():
            try:
                # Use failover logic
                translated, tokens = self._translate_with_failover(jp, self._get_merged_glossary(), domain=domain)
                self.after(0, lambda: self._on_translation_complete(translated, tokens))
            except Exception as e:
                self.after(0, lambda err=e: [self.spinner.stop(), self.show_error("Lỗi Dịch", f"Tất cả API Key đều thất bại hoặc không có Key nào khả dụng.\nChi tiết: {str(err)}")])
        
        threading.Thread(target=run, daemon=True).start()

    def _handle_translate_all(self) -> None:
        """Translate all pages that are not yet translated, rotating through enabled API keys."""
        if not self.current_session: return
        
        pages_to_translate = [i for i, p in enumerate(self.current_session["pages"]) if not p.get("is_translated", False)]
        if not pages_to_translate:
            messagebox.showinfo("Thông báo", "Tất cả các trang đã được dịch.")
            return

        domain = self.top_bar.cmb_domain.get()
        confirm_msg = (
            f"⚠️ CẢNH BÁO CHI PHÍ & CHẤT LƯỢNG\n\n"
            f"Việc dịch toàn bộ ({len(pages_to_translate)} trang) sẽ tiêu tốn một lượng Token đáng kể.\n\n"
            f"Để có kết quả tốt nhất và tránh lãng phí, hãy đảm bảo bạn đã nhập đầy đủ thuật ngữ cho lĩnh vực '{domain}'.\n\n"
            f"Bạn có chắc chắn muốn bắt đầu dịch toàn bộ không?"
        )
        if not messagebox.askyesno("Xác nhận dịch toàn bộ", confirm_msg):
            return

        self.spinner.start(f"Đang dịch toàn bộ (0/{len(pages_to_translate)})...")
        domain = self.top_bar.cmb_domain.get()
        glossary = self._get_merged_glossary()

        def run_all():
            count = 0
            total = len(pages_to_translate)
            
            # Fetch all enabled keys for rotation
            config = self.config_manager.load_api_config()
            available_keys = [k for k in config.get("keys", []) if k.get("is_enabled", True)]
            if not available_keys:
                active_id = config.get("active_id")
                available_keys = [k for k in config.get("keys", []) if k["id"] == active_id]
            
            if not available_keys:
                self.after(0, lambda: [self.spinner.stop(), self.show_error("Lỗi", "Không có API Key nào khả dụng.")])
                return

            import random
            random.shuffle(available_keys) # Random starting order
            
            failed_count = 0
            for i, page_idx in enumerate(pages_to_translate):
                page = self.current_session["pages"][page_idx]
                jp_text = page["jp"]
                
                # Success flag for this page
                page_success = False
                
                # Try each key in the pool if one fails
                # Start with the one in rotation
                start_key_idx = i % len(available_keys)
                
                for attempt in range(len(available_keys)):
                    k_data = available_keys[(start_key_idx + attempt) % len(available_keys)]
                    try:
                        client = self._create_client_from_data(k_data)
                        if not client: continue
                        
                        translated, tokens = client.translate(jp_text, glossary=glossary, domain=domain)
                        
                        def update_page_data(idx=page_idx, txt=translated, tks=tokens):
                            p = self.current_session["pages"][idx]
                            p["vn"] = txt
                            p["is_translated"] = True
                            p["check_status"] = None
                            p["tokens"] = tks
                            self.token_tracker.add_usage(tks)
                            self.left_sidebar.update_page_status(idx, True, None, p.get("is_reviewed", False))
                            if idx == self.current_page_idx:
                                self._update_center_panel(self.current_page_idx)
                        
                        self.after(0, update_page_data)
                        count += 1
                        page_success = True
                        self.after(0, lambda c=count: self.spinner.set_text(f"Đang dịch toàn bộ ({c}/{total})..."))
                        break # Success! Go to next page
                        
                    except Exception as e:
                        self.logger.warning(f"Key {k_data.get('name')} failed for page {page_idx+1}: {e}")
                        # Automatically disable the broken key
                        self.config_manager.update_api_key_status(k_data["id"], "inactive", is_enabled=False)
                        # Remove from local rotation to avoid retrying in this batch
                        if k_data in available_keys:
                            available_keys.remove(k_data)
                        continue
                
                if not page_success:
                    failed_count += 1
                    self.logger.error(f"All keys failed for page {page_idx+1}")
                    # If even the last key failed, it's likely a persistent issue (quota, connection)
                    # We continue to the next page but keep track.
            
            def finalize():
                self.spinner.stop()
                self._handle_save()
                if failed_count == 0:
                    self.show_toast(f"Đã hoàn thành dịch toàn bộ {count} trang!")
                else:
                    msg = f"Dịch toàn bộ hoàn tất với lỗi.\n- Thành công: {count}\n- Thất bại: {failed_count}\n\nVui lòng kiểm tra lại các API Key hoặc kết nối mạng."
                    messagebox.showwarning("Hoàn tất có lỗi", msg)

            self.after(0, finalize)

        threading.Thread(target=run_all, daemon=True).start()

    def _translate_with_failover(self, text: str, glossary: Dict[str, str], domain: str):
        """Translate with random key selection and automatic failover."""
        return self._call_ai_with_failover("translate", text, glossary, domain=domain)

    def _create_client_from_data(self, k_data: Dict[str, Any]) -> Optional[BaseAIClient]:
        provider = k_data.get("provider")
        key = k_data.get("key")
        model = k_data.get("model")
        if not key: return None
        
        if provider == "openai":
            return OpenAIClient(api_key=key, model_name=model)
        else:
            return GeminiClient(api_key=key, model_name=model)

    def _on_translation_complete(self, text, tokens):
        self.spinner.stop()
        self.center_panel.set_vietnamese_text(text)
        page = self.current_session["pages"][self.current_page_idx]
        page["vn"] = text
        page["is_translated"] = True
        page["check_status"] = None # Reset check status since text changed
        self.current_mismatches = [] # Reset on translation
        
        self.left_sidebar.update_page_status(self.current_page_idx, True, None, page.get("is_reviewed", False))
        
        self.token_tracker.add_usage(tokens)
        self.bottom_bar.update_tokens(self.token_tracker.get_formatted_status())
        self.show_toast("Dịch thành công!")

    # ── Functional Handlers ────────────────────────────────────────────────

    def _handle_save(self, show_msg=False) -> None:
        if not self.current_session: return
        try:
            self.current_session["pages"][self.current_page_idx]["vn"] = self.center_panel.get_vietnamese_text()
            self.current_session["current_page"] = self.current_page_idx
            self.session_manager.save_session(self.current_session)
            self.show_toast("Đã lưu tiến độ!")
            if show_msg:
                messagebox.showinfo("Thành công", "Đã lưu tiến độ phiên làm việc!", parent=self)
        except Exception as e: self.show_error("Lỗi Lưu", str(e))

    def _handle_get_prompt(self) -> None:
        if not self.current_session: return
        jp = self.center_panel.get_japanese_text()
        domain = self.top_bar.cmb_domain.get()
        glos = self._get_merged_glossary()
        
        # Filter relevant terms
        relevant_glos = {k: v for k, v in glos.items() if k in jp}
        
        prompt = (
            "Bạn là một dịch giả chuyên nghiệp. Hãy dịch danh sách các đoạn văn Markdown sau từ tiếng Nhật SANG TIẾNG VIỆT.\n"
            f"Văn bản thuộc lĩnh vực: {domain}.\n\n"
            "QUY TẮC BẮT BUỘC (STRICT RULES):\n"
            "1. NGÔN NGỮ ĐẦU RA: BẮT BUỘC trả về kết quả bằng TIẾNG VIỆT. Tuyệt đối không trả về tiếng Anh hay ngôn ngữ khác.\n"
            "2. TUÂN THỦ THUẬT NGỮ: Bạn PHẢI sử dụng đúng các cặp thuật ngữ dưới đây:\n"
        )
        
        if relevant_glos:
            for k, v in relevant_glos.items():
                prompt += f"- {k} -> {v}\n"
        else:
            prompt += "(Không có thuật ngữ cụ thể)\n"
            
        prompt += (
            "\n3. GIỮ NGUYÊN ĐỊNH DẠNG: Tuyệt đối giữ nguyên Markdown (**, *, _, #) và các ký hiệu đặc biệt như 【 】, 「 」, 『 』. KHÔNG ĐƯỢC thay thế 【 】 bằng [ ].\n"
            "4. GIỮ CẤU TRÚC DÒNG: Nếu trong một đoạn văn có xuống dòng, hãy giữ nguyên vị trí xuống dòng đó.\n"
            "5. KHÔNG GIẢI THÍCH: Chỉ trả về bản dịch tiếng Việt.\n"
            "6. TƯƠNG ĐỒNG SỐ CÂU: Số lượng câu trong bản dịch tiếng Việt phải BẰNG CHÍNH XÁC số lượng câu trong văn bản tiếng Nhật gốc. Tuyệt đối không tự ý gộp hoặc tách câu.\n\n"
            "Văn bản gốc:\n"
            f"[1] {jp}"
        )
        
        self.clipboard_clear()
        self.clipboard_append(prompt)
        messagebox.showinfo("Prompt", "Đã copy prompt chuẩn hóa vào clipboard.")

    def _check_for_resume_session(self) -> None:
        sessions = self.session_manager.list_sessions()
        if not sessions: return
        latest = sessions[0]
        if messagebox.askyesno("Tiếp tục?", f"Tiếp tục phiên làm việc cũ cho '{os.path.basename(latest['source_file'])}'?"):
            self._load_session_by_id(latest["id"])

    def _open_session_history(self) -> None:
        """Open the history window to choose a session to load."""
        from src.ui.session_history import SessionHistoryWindow
        SessionHistoryWindow(self, self.session_manager, on_session_selected=self._load_session_by_id)

    def _load_session_by_id(self, session_id: str) -> None:
        """Load a session from disk and update UI."""
        try:
            data = self.session_manager.load_session(session_id)
            self.current_session = data
            self.current_page_idx = data.get("current_page", 0)
            self.left_sidebar.populate_pages(data["pages"], self.current_page_idx)
            
            # Refresh list to ensure data["domain"] exists in dropdown values
            self._refresh_all_domains()
            self.top_bar.set_selected_domain(data["domain"])
            
            self._update_center_panel(self.current_page_idx)
            self.title(f"TranslatorApp — {os.path.basename(data['source_file'])}")
            self.show_toast("Đã khôi phục phiên!")
        except Exception as e: 
            self.show_error("Lỗi Tải", str(e))

    def _start_auto_save_timer(self):
        self._auto_save_session()

    def _auto_save_session(self):
        if self.current_session:
            try: self._handle_save()
            except: pass
        self._auto_save_timer_id = self.after(300000, self._auto_save_session) # Every 5 mins

    def _refresh_all_domains(self):
        """Refresh the domain list in TopBar from disk."""
        repo = GlossaryRepository("common")
        all_domains = repo.get_all_domains()
        self.top_bar.refresh_domain_list(all_domains)

    # ── Helper Utils ───────────────────────────────────────────────────────

    def _get_ai_client(self) -> Optional[BaseAIClient]:
        """Deprecated: Use _translate_with_failover or _create_client_from_data instead.
        Kept for compatibility with other components temporarily.
        """
        cfg = self.config_manager.load_api_config()
        keys = cfg.get("keys", [])
        active_id = cfg.get("active_id")
        active_key_data = next((k for k in keys if k["id"] == active_id), None)
        if not active_key_data and keys:
            active_key_data = keys[0]
        return self._create_client_from_data(active_key_data) if active_key_data else None

    def _get_merged_glossary(self) -> Dict[str, str]:
        common = GlossaryRepository("common").get_terms().copy()
        curr = self.top_bar.cmb_domain.get()
        if curr != "common": common.update(GlossaryRepository(curr).get_terms())
        return common

    def _run_domain_detection(self, text, manual=False):
        if not text or not text.strip():
            self.logger.warning("Skip domain detection: Input text is empty.")
            return

        if not manual:
            self.after(0, lambda: self.spinner.start("Đang tự động nhận diện lĩnh vực..."))

        try:
            # Fetch existing domains
            repo = GlossaryRepository("common")
            existing = repo.get_all_domains()
            
            self.logger.info(f"Starting domain detection (manual={manual}) for text length: {len(text)}")
            
            # Use failover for detection
            suggested = self._call_ai_with_failover("detect_domain", text, existing_domains=existing)
            self.after(0, lambda: self._process_domain_result(suggested, manual=manual))
        except Exception as e: 
            self.logger.error(f"Domain detection failed: {e}")
            self.after(0, self.spinner.stop)
            if manual:
                self.after(0, lambda err=e: self.show_error("Lỗi", f"Không thể kết nối AI để nhận diện lĩnh vực.\nChi tiết: {str(err)}"))
            else:
                self.after(0, lambda: self.show_toast("⚠️ Lỗi AI. Hãy chọn lĩnh vực thủ công ở thanh trên cùng."))

    def _call_ai_with_failover(self, method_name: str, *args, **kwargs):
        """Generic wrapper to call any AI client method with failover."""
        import random
        config = self.config_manager.load_api_config()
        available_keys = [k for k in config.get("keys", []) if k.get("is_enabled", True)]
        if not available_keys:
            # If no keys are enabled, fallback to the default starred key if it exists
            active_id = config.get("active_id")
            available_keys = [k for k in config.get("keys", []) if k["id"] == active_id]
            
        random.shuffle(available_keys)
        
        last_err = "No API keys"
        for k_data in available_keys:
            try:
                client = self._create_client_from_data(k_data)
                if not client: continue
                
                method = getattr(client, method_name)
                return method(*args, **kwargs)
            except Exception as e:
                last_err = str(e)
                self.logger.warning(f"AI Method {method_name} failed for {k_data.get('name')}: {e}")
                # Automatically disable the broken key
                self.config_manager.update_api_key_status(k_data["id"], "inactive", is_enabled=False)
                continue
        raise Exception(last_err)

    def _process_domain_result(self, suggested, manual=False):
        # Stop spinner first so the UI is unblocked immediately
        self.after(0, self.spinner.stop)
        
        self.logger.info(f"AI suggested domain: '{suggested}' (manual={manual})")
        if not suggested or suggested.lower() in ["common", "chung", "không rõ", "tổng quát"]:
            self.show_toast("AI không rõ lĩnh vực. Hãy chọn thủ công ở thanh trên cùng.")
            return

        repo = GlossaryRepository("common")
        existing = repo.get_all_domains()
        matched = next((d for d in existing if d.lower() == suggested.lower().strip()), None)
        
        if matched:
            DomainSuggestionWindow(self, suggested_name=matched, is_existing=True, on_confirm=self._handle_apply_existing_domain)
        else:
            DomainSuggestionWindow(self, suggested_name=suggested, is_existing=False, on_confirm=self._handle_create_domain)

    def _handle_apply_existing_domain(self, name):
        """Apply an existing domain to the session and UI."""
        self.top_bar.set_selected_domain(name)
        if self.current_session:
            self.current_session["domain"] = name
            self._handle_save()
        self.show_toast(f"✨ Đã áp dụng lĩnh vực: {name}")

    def _handle_create_domain(self, name):
        try:
            repo = GlossaryRepository(name)
            repo.save_glossary({"terms": {}, "domain": name})
            # Refresh list across all repositories by getting all domains from common dir
            all_domains = repo.get_all_domains()
            self.top_bar.refresh_domain_list(all_domains)
            self.top_bar.set_selected_domain(name)
            if self.current_session: self.current_session["domain"] = name
        except Exception as e: self.show_error("Lỗi", str(e))

    def _handle_add_domain_manual(self):
        dialog = ctk.CTkInputDialog(text="Nhập tên lĩnh vực mới:", title="Thêm Lĩnh vực")
        # Position dialog relative to main window if possible (default is center screen)
        name = dialog.get_input()
        if not name or not name.strip(): return
        
        name = name.strip()
        repo = GlossaryRepository("common")
        existing = repo.get_all_domains()
        
        matched = next((d for d in existing if d.lower() == name.lower()), None)
        if matched:
            messagebox.showinfo("Thông báo", f"Lĩnh vực '{matched}' đã tồn tại.")
            self.top_bar.set_selected_domain(matched)
            if self.current_session: 
                self.current_session["domain"] = matched
                self._handle_save()
        else:
            self._handle_create_domain(name)
            self.show_toast(f"Đã tạo lĩnh vực: {name}")
            if self.current_session:
                self._handle_save()

    def _handle_add_glossary_from_selection(self, jp_text: str):
        """Show dialog to get translation and select domain."""
        from src.ui.term_manager import QuickAddGlossaryDialog
        
        # Get all available domains
        domains = GlossaryRepository("common").get_all_domains()
        current_domain = self.top_bar.cmb_domain.get()
        
        dialog = QuickAddGlossaryDialog(self, jp_text, domains, current_domain)
        self.wait_window(dialog)
        
        if dialog.result:
            res = dialog.result
            repo = GlossaryRepository(res["domain"])
            repo.add_term(res["jp"], res["vn"])
            self._on_glossary_changed()
            self.show_toast(f"Đã thêm vào [{res['domain']}]: {res['jp']} -> {res['vn']}")

    def _handle_manual_domain_detection(self):
        text = self.center_panel.get_japanese_text()
        if not text.strip():
            self.show_error("Thông báo", "Vui lòng mở file hoặc chọn trang có nội dung tiếng Nhật.")
            return
        
        self.spinner.start("Đang nhận diện lĩnh vực...")
        threading.Thread(target=self._run_domain_detection, args=(text[:5000], True), daemon=True).start()

    def _handle_consistency_check(self):
        if not self.current_session: return
        res = self.checker.check(self.center_panel.get_japanese_text(), self.center_panel.get_vietnamese_text(), self._get_merged_glossary())
        
        # Update status based on check results
        page = self.current_session["pages"][self.current_page_idx]
        page["check_status"] = "error" if res else "ok"
        page["mismatches"] = res # Save to session
        self.current_mismatches = res
        self.left_sidebar.update_page_status(self.current_page_idx, page["is_translated"], page["check_status"], page.get("is_reviewed", False))
        self._update_center_panel(self.current_page_idx) # Refresh sidebar icons
        
        CheckResultWindow(self, res, self.current_page_idx + 1)

    def _handle_check_all(self) -> None:
        """Run consistency check for all translated pages."""
        if not self.current_session: return
        
        pages_to_check = [i for i, p in enumerate(self.current_session["pages"]) if p.get("is_translated", False)]
        if not pages_to_check:
            messagebox.showinfo("Thông báo", "Chưa có trang nào được dịch để kiểm tra.")
            return

        self.spinner.start(f"Đang kiểm tra toàn bộ (0/{len(pages_to_check)})...")
        glossary = self._get_merged_glossary()
        
        def run_check():
            error_count = 0
            for i, page_idx in enumerate(pages_to_check):
                page = self.current_session["pages"][page_idx]
                res = self.checker.check(page["jp"], page["vn"], glossary)
                
                # Update status
                page["check_status"] = "error" if res else "ok"
                
                def update_ui(idx=page_idx, status=page["check_status"], mismatches=res):
                    p = self.current_session["pages"][idx]
                    p["mismatches"] = mismatches # Save to session
                    self.left_sidebar.update_page_status(idx, True, status, p.get("is_reviewed", False))
                    if idx == self.current_page_idx:
                        self.current_mismatches = mismatches
                        self._update_center_panel(self.current_page_idx)
                
                self.after(0, update_ui)
                if res: error_count += 1
                self.after(0, lambda c=i+1: self.spinner.set_text(f"Đang kiểm tra toàn bộ ({c}/{len(pages_to_check)})..."))

            self.after(0, lambda: [
                self.spinner.stop(), 
                messagebox.showinfo("Hoàn tất", f"Kiểm tra hoàn tất.\n- Số trang có lỗi: {error_count}\n- Số trang OK: {len(pages_to_check) - error_count}")
            ])

        threading.Thread(target=run_check, daemon=True).start()

    def _open_export_dialog(self):
        if not self.current_session: return
        ExportWindow(self, default_filename=os.path.basename(self.current_session["docx_path"]), on_export=self._handle_export)

    def _handle_export(self, opts, path):
        try:
            self.current_session["pages"][self.current_page_idx]["vn"] = self.center_panel.get_vietnamese_text()
            self.exporter.export(original_path=self.current_session["docx_path"], output_path=path, 
                               pages_data=self.current_session["pages"], format_metadata=self.format_metadata,
                               only_translated=opts["only_translated"], bilingual=opts["bilingual"])
            messagebox.showinfo("Thành công", f"Đã lưu tại:\n{path}")
        except Exception as e: self.show_error("Lỗi Export", str(e))

    def _open_api_settings(self):
        ApiSettingsDialog(self, self.config_manager)

    def _open_glossary_manager(self) -> None:
        """Open the Glossary Manager window."""
        active_domain = self.top_bar.cmb_domain.get()
        GlossaryManagerWindow(
            self,
            ai_client=self._get_ai_client(),
            active_domain=active_domain,
            on_change_callback=self._on_glossary_changed,
            has_session=self.current_session is not None
        )

    def _on_glossary_changed(self) -> None:
        """Callback when glossary data is modified."""
        if self.current_session:
            jp_text = self.center_panel.get_japanese_text()
            self.right_sidebar.update_terms(jp_text, self._get_merged_glossary())

    def _open_segmentation_settings(self):
        if not self.seg_dialog or not self.seg_dialog.winfo_exists():
            self.seg_dialog = SegmentationSettingsDialog(self, self.config_manager)
        else: self.seg_dialog.focus()

    def _menu_help_about(self):
        """Open the professional about window."""
        AboutWindow(self)

    def _open_user_guide(self):
        """Open the detailed user guide window."""
        UserGuideWindow(self)

    def show_error(self, title, msg, details=None):
        self.logger.error(f"{title}: {msg} ({details})")
        messagebox.showerror(title, msg, parent=self)

    def show_toast(self, msg, duration=3000):
        self.bottom_bar.lbl_status.configure(text=msg, text_color="#107C10")
        self.bottom_bar.progress_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.bottom_bar.progress_bar.pack_forget()
        self.after(duration, lambda: self.bottom_bar.progress_frame.place_forget())
    def _export_all_settings(self):
        """Handler for full settings backup export."""
        from tkinter import filedialog
        file_path = filedialog.asksaveasfilename(
            title="Export toàn bộ cấu hình",
            defaultextension=".zip",
            filetypes=[("ZIP files", "*.zip")],
            initialfile="translator_settings_backup.zip"
        )
        if not file_path: return
        
        try:
            self.config_manager.export_full_backup(file_path)
            messagebox.showinfo("Thành công", f"Đã sao lưu toàn bộ cấu hình vào:\n{file_path}")
        except Exception as e:
            self.show_error("Lỗi Export", f"Không thể sao lưu cấu hình: {e}")

    def _import_all_settings(self):
        """Handler for full settings backup import."""
        from tkinter import filedialog
        if not messagebox.askyesno("Xác nhận", "Hành động này sẽ ghi đè toàn bộ cấu hình hiện tại và thuật ngữ. Bạn có muốn tiếp tục?"):
            return
            
        file_path = filedialog.askopenfilename(
            title="Import toàn bộ cấu hình",
            filetypes=[("ZIP files", "*.zip")]
        )
        if not file_path: return
        
        try:
            self.config_manager.import_full_backup(file_path)
            messagebox.showinfo("Thành công", "Đã khôi phục toàn bộ cấu hình. Ứng dụng sẽ tự động cập nhật lại các danh sách.")
            # Refresh UI
            self._refresh_all_domains()
            self._on_glossary_changed()
            self.state("zoomed") # Restore fullscreen state
        except Exception as e:
            self.show_error("Lỗi Import", f"Không thể khôi phục cấu hình: {e}")

    def _open_preferences(self):
        """Open the application preferences dialog."""
        from src.ui.preferences import PreferencesDialog
        PreferencesDialog(self, self.config_manager)

    def _open_domain_manager(self):
        """Open the domain management window."""
        from src.ui.domain_manager import DomainManagerWindow
        DomainManagerWindow(self, on_change=self._refresh_all_domains)

    def _handle_search_all(self, text: str):
        """Search text in all JP and VN pages and highlight results in sidebar."""
        self._handle_clear_search() # Clear previous results first
        if not self.current_session or not text: return
        
        self.current_search_text = text # Store for page switching
        matches = []
        for i, page in enumerate(self.current_session["pages"]):
            jp_content = page.get("jp", "")
            vn_content = page.get("vn", "")
            if text.lower() in jp_content.lower() or text.lower() in vn_content.lower():
                matches.append(i)
        
        if matches:
            self.left_sidebar.highlight_search_results(matches)
            messagebox.showinfo("Kết quả tìm kiếm", f"Tìm thấy '{text}' tại {len(matches)} trang.")
            # Also highlight in current page immediately
            self.center_panel.highlight_search_text(text)
        else:
            messagebox.showinfo("Kết quả tìm kiếm", f"Không tìm thấy kết quả nào cho '{text}' trong tài liệu.")
            self._handle_clear_search()

    def _handle_local_search(self, text: str):
        """Update top bar search text and trigger global search."""
        self.top_bar.set_search_text(text)
        self._handle_search_all(text)

    def _handle_clear_search(self):
        """Clear search state and highlights."""
        self.current_search_text = ""
        self.left_sidebar.clear_search_highlights()
        self.center_panel.clear_search_highlights()

    def _handle_term_selection(self, jp: str, vn: str):
        """Handle term selection from RightSidebar."""
        if not jp and not vn:
            self.center_panel.clear_term_selection_highlight()
        else:
            self.center_panel.highlight_term_selection(jp, vn)

    def _handle_esc_key(self):
        """Handle Escape key to clear all highlights."""
        # Clear search
        self._handle_clear_search()
        # Clear top bar entry
        if hasattr(self, "top_bar"):
            self.top_bar.set_search_text("")
        # Clear term selection
        self.right_sidebar.clear_selection()
        self.center_panel.clear_term_selection_highlight()
