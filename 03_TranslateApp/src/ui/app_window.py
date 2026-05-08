"""Main application window for the TranslatorApp (v1.0 Final)."""

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
from src.ui.api_settings import ApiSettingsDialog
from src.ui.segmentation_settings import SegmentationSettingsDialog
from src.ui.components.left_sidebar import LeftSidebar
from src.ui.components.right_sidebar import RightSidebar
from src.ui.components.top_bar import TopBar
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
        self._auto_save_timer_id = None
        
        # ── UI Setup ───────────────────────────────────────────────────────
        self._configure_window()
        self._build_menu_bar()
        self._build_layout()
        
        # ── Startup ────────────────────────────────────────────────────────
        self.after(500, self._check_for_resume_session)
        self._start_auto_save_timer()

    def _configure_window(self) -> None:
        self.title("TranslatorApp — Dịch tài liệu chuyên ngành Nhật-Việt")
        self.minsize(self._MIN_WIDTH, self._MIN_HEIGHT)
        self.geometry(f"{self._MIN_WIDTH}x{self._MIN_HEIGHT}")

    def _build_menu_bar(self) -> None:
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=False)
        file_menu.add_command(label="Mở file…", command=self._handle_file_upload)
        file_menu.add_separator()
        file_menu.add_command(label="Thoát", command=self.destroy)
        menubar.add_cascade(label="File", menu=file_menu)

        settings_menu = tk.Menu(menubar, tearoff=False)
        settings_menu.add_command(label="Segmentation Settings", command=self._open_segmentation_settings)
        settings_menu.add_command(label="API Settings", command=self._open_api_settings)
        menubar.add_cascade(label="Settings", menu=settings_menu)

        tools_menu = tk.Menu(menubar, tearoff=False)
        tools_menu.add_command(label="Quản lý thuật ngữ", command=self._open_glossary_manager)
        menubar.add_cascade(label="Tools", menu=tools_menu)

        help_menu = tk.Menu(menubar, tearoff=False)
        help_menu.add_command(label="About", command=self._menu_help_about)
        menubar.add_cascade(label="Help", menu=help_menu)
        self.config(menu=menubar)

    def _build_layout(self) -> None:
        self.rowconfigure(1, weight=1)
        self.columnconfigure(1, weight=1)

        self.top_bar = TopBar(self, on_upload_callback=self._handle_file_upload, on_export_callback=self._open_export_dialog)
        self.top_bar.grid(row=0, column=0, columnspan=3, sticky="ew")

        self.left_sidebar = LeftSidebar(self, on_page_selected=self._on_page_selected)
        self.left_sidebar.grid(row=1, column=0, sticky="ns", padx=(4, 0), pady=4)

        self.center_panel = CenterPanel(self)
        self.center_panel.grid(row=1, column=1, sticky="nsew", padx=4, pady=4)

        self.right_sidebar = RightSidebar(self, on_term_click=self.center_panel.highlight_japanese_term)
        self.right_sidebar.grid(row=1, column=2, sticky="ns", padx=(0, 4), pady=4)

        self.bottom_bar = BottomBar(
            self, 
            on_check_page_callback=self._handle_consistency_check,
            on_translate_callback=self._handle_translate,
            on_get_prompt_callback=self._handle_get_prompt,
            on_save_callback=self._handle_save
        )
        self.bottom_bar.grid(row=2, column=0, columnspan=3, sticky="ew")

    # ── Logic ──────────────────────────────────────────────────────────────

    def _handle_file_upload(self) -> None:
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
                
                segs = self.segmenter.segment(texts)
                pages = self.segmenter.paginate(segs)
                pages_text = ["\n".join(p) for p in pages]
                
                self.after(0, lambda: progress.set_progress(0.8, "Khởi tạo session..."))
                dom = self.top_bar.cmb_domain.get()
                self.current_session = self.session_manager.create_session(docx_path=file_path, segments=pages_text, domain=dom)
                self.current_page_idx = 0
                
                def on_done():
                    progress.complete()
                    self.title(f"TranslatorApp — {tk.os.path.basename(file_path)}")
                    self.left_sidebar.populate_pages(len(pages_text), 0)
                    self._update_center_panel()
                    # AI Detect
                    threading.Thread(target=self._run_domain_detection, args=("\n".join(texts)[:5000],), daemon=True).start()

                self.after(0, on_done)
            except Exception as e:
                self.after(0, lambda: [progress.complete(), self.show_error("Lỗi nạp file", str(e))])

        threading.Thread(target=run_load, daemon=True).start()

    def _on_page_selected(self, index: int) -> None:
        if not self.current_session: return
        self.current_session["pages"][self.current_page_idx]["vn"] = self.center_panel.get_vietnamese_text()
        self.current_page_idx = index
        self.token_tracker.reset_page_counter()
        self._update_center_panel()

    def _update_center_panel(self) -> None:
        if not self.current_session: return
        page = self.current_session["pages"][self.current_page_idx]
        self.center_panel.set_japanese_text(page["jp"])
        self.center_panel.set_vietnamese_text(page["vn"])
        self.right_sidebar.update_terms(page["jp"], self._get_merged_glossary())
        self.bottom_bar.update_tokens(self.token_tracker.get_formatted_status())

    def _handle_translate(self) -> None:
        if not self.current_session: return
        jp = self.center_panel.get_japanese_text()
        if not jp.strip(): return
        self.bottom_bar.show_progress("Đang dịch...")
        def run():
            try:
                translated, tokens = self._get_ai_client().translate(jp, self._get_merged_glossary())
                self.after(0, lambda: self._on_translation_complete(translated, tokens))
            except Exception as e:
                self.after(0, lambda: [self.bottom_bar.hide_progress(), self.show_error("Lỗi Dịch", str(e))])
        threading.Thread(target=run, daemon=True).start()

    def _on_translation_complete(self, text, tokens):
        self.bottom_bar.hide_progress()
        self.center_panel.set_vietnamese_text(text)
        self.current_session["pages"][self.current_page_idx]["vn"] = text
        self.token_tracker.add_usage(tokens)
        self.bottom_bar.update_tokens(self.token_tracker.get_formatted_status())
        self.show_toast("Dịch thành công!")

    # ── Functional Handlers ────────────────────────────────────────────────

    def _handle_save(self) -> None:
        if not self.current_session: return
        try:
            self.current_session["pages"][self.current_page_idx]["vn"] = self.center_panel.get_vietnamese_text()
            self.current_session["current_page"] = self.current_page_idx
            self.session_manager.save_session(self.current_session)
            self.show_toast("Đã lưu tiến độ!")
        except Exception as e: self.show_error("Lỗi Lưu", str(e))

    def _handle_get_prompt(self) -> None:
        if not self.current_session: return
        jp = self.center_panel.get_japanese_text()
        glos = self._get_merged_glossary()
        p = "Dịch đoạn văn tiếng Nhật sau sang tiếng Việt chuyên ngành:\n"
        if glos:
            p += "THUẬT NGỮ:\n"
            for k, v in glos.items():
                if k in jp: p += f"- {k}: {v}\n"
        p += f"\nGỐC:\n{jp}\n\nDỊCH:"
        self.clipboard_clear(); self.clipboard_append(p)
        messagebox.showinfo("Prompt", "Đã copy prompt vào clipboard.")

    def _check_for_resume_session(self) -> None:
        sessions = self.session_manager.list_sessions()
        if not sessions: return
        latest = sessions[0]
        if messagebox.askyesno("Tiếp tục?", f"Tiếp tục phiên làm việc cũ cho '{tk.os.path.basename(latest['source_file'])}'?"):
            try:
                data = self.session_manager.load_session(latest["id"])
                self.current_session = data; self.current_page_idx = data.get("current_page", 0)
                self.left_sidebar.populate_pages(len(data["pages"]), self.current_page_idx)
                self.top_bar.set_selected_domain(data["domain"])
                self._update_center_panel()
                self.show_toast("Đã khôi phục phiên!")
            except Exception as e: self.show_error("Lỗi Tải", str(e))

    def _start_auto_save_timer(self):
        self._auto_save_session()

    def _auto_save_session(self):
        if self.current_session:
            try: self._handle_save()
            except: pass
        self._auto_save_timer_id = self.after(300000, self._auto_save_session) # Every 5 mins

    # ── Helper Utils ───────────────────────────────────────────────────────

    def _get_ai_client(self) -> GeminiClient:
        cfg = self.config_manager.load_api_config()
        key = cfg.get("gemini_api_key", "")
        model = cfg.get("gemini_model", "gemini-1.5-pro")
        return GeminiClient(api_key=key, model_name=model)

    def _get_merged_glossary(self) -> Dict[str, str]:
        common = GlossaryRepository("common").get_terms().copy()
        curr = self.top_bar.cmb_domain.get()
        if curr != "common": common.update(GlossaryRepository(curr).get_terms())
        return common

    def _run_domain_detection(self, text):
        try:
            suggested = self._get_ai_client().detect_domain(text)
            self.after(0, self._process_domain_result, suggested)
        except: pass

    def _process_domain_result(self, suggested):
        repo = GlossaryRepository("common")
        existing = repo.get_all_domains()
        matched = next((d for d in existing if d.lower() == suggested.lower().strip()), None)
        if matched:
            self.top_bar.set_selected_domain(matched)
            if self.current_session: self.current_session["domain"] = matched
        else:
            DomainSuggestionWindow(self, suggested_name=suggested, on_confirm=self._handle_create_domain)

    def _handle_create_domain(self, name):
        try:
            repo = GlossaryRepository(name)
            repo.save_glossary({"terms": {}, "domain": name})
            self.top_bar.refresh_domain_list(repo.get_all_domains())
            self.top_bar.set_selected_domain(name)
            if self.current_session: self.current_session["domain"] = name
        except Exception as e: self.show_error("Lỗi", str(e))

    def _handle_consistency_check(self):
        if not self.current_session: return
        res = self.checker.check(self.center_panel.get_japanese_text(), self.center_panel.get_vietnamese_text(), self._get_merged_glossary())
        CheckResultWindow(self, res, self.current_page_idx + 1)

    def _open_export_dialog(self):
        if not self.current_session: return
        ExportWindow(self, default_filename=tk.os.path.basename(self.current_session["docx_path"]), on_export=self._handle_export)

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

    def _open_segmentation_settings(self):
        if not self.seg_dialog or not self.seg_dialog.winfo_exists():
            self.seg_dialog = SegmentationSettingsDialog(self, self.config_manager)
        else: self.seg_dialog.focus()

    def _menu_help_about(self):
        messagebox.showinfo("About", "TranslatorApp v1.0\nAntigravity Agent Edition", parent=self)

    def show_error(self, title, msg, details=None):
        get_logger("UI").error(f"{title}: {msg} ({details})")
        messagebox.showerror(title, msg, parent=self)

    def show_toast(self, msg, duration=3000):
        self.bottom_bar.lbl_status.configure(text=msg, text_color="#107C10")
        self.bottom_bar.progress_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.bottom_bar.progress_bar.pack_forget()
        self.after(duration, lambda: self.bottom_bar.progress_frame.place_forget())
