"""Application entry point for TranslatorApp."""

import traceback
import logging
import customtkinter as ctk

from src.ui.app_window import AppWindow
from src.utils.logger import setup_logger


def main() -> None:
    # 1. Initialize Logging system immediately
    logger = setup_logger()
    
    try:
        # 2. Configure default appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # 3. Launch Application
        logger.info("Starting TranslatorApp v1.2.0...")
        app = AppWindow()
        app.mainloop()
        logger.info("Application closed normally.")
        
    except Exception as e:
        # 4. Catch and log catastrophic failures
        error_msg = f"CRITICAL CRASH: {str(e)}\n{traceback.format_exc()}"
        logging.getLogger("TranslatorApp").critical(error_msg)
        
        # Try to show a simple error dialog if possible
        try:
            import tkinter.messagebox as mb
            mb.showerror("Lỗi Nghiêm Trọng", 
                         "Ứng dụng đã gặp lỗi không thể phục hồi và phải đóng lại.\n"
                         "Vui lòng kiểm tra file data/logs/error.log để biết chi tiết.")
        except:
            pass
        
        # Exit with error code
        import sys
        sys.exit(1)


if __name__ == "__main__":
    main()
