import os
from typing import Tuple, List, Dict, Any

from docx import Document
from docx.shared import Pt, RGBColor
from docx.text.paragraph import Paragraph


class DocumentProcessor:
    """Handles DOCX to Markdown conversion and vice versa with format preservation."""

    def __init__(self) -> None:
        self.default_font = "Times New Roman"

    def extract_docx(self, file_path: str) -> Tuple[List[str], List[Dict[str, Any]]]:
        """
        Extracts text and format metadata from a DOCX file.
        
        Args:
            file_path: Path to the DOCX file.
            
        Returns:
            A tuple containing a list of extracted texts and a list of metadata dictionaries.
            
        Raises:
            FileNotFoundError: If the input file does not exist.
            ValueError: If the file is corrupted or not a valid DOCX.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        try:
            doc = Document(file_path)
        except Exception as e:
            error_str = str(e)
            if "Package not found" in error_str or "Permission denied" in error_str:
                raise ValueError("Không thể mở file. Có thể file đang được mở trong một ứng dụng khác (như Word). Vui lòng đóng file và thử lại.")
            raise ValueError(f"Lỗi nạp file: {error_str}")

        texts: List[str] = []
        metadata: List[Dict[str, Any]] = []

        # Extract from standalone paragraphs
        for p_idx, para in enumerate(doc.paragraphs):
            text = para.text.strip()
            if not text:
                continue
                
            format_meta = self._extract_format_from_paragraph(para)
            
            texts.append(text)
            metadata.append({
                "type": "paragraph",
                "index": p_idx,
                "format": format_meta
            })

        # Extract from tables
        for t_idx, table in enumerate(doc.tables):
            for r_idx, row in enumerate(table.rows):
                for c_idx, cell in enumerate(row.cells):
                    for p_idx, para in enumerate(cell.paragraphs):
                        text = para.text.strip()
                        if not text:
                            continue
                            
                        format_meta = self._extract_format_from_paragraph(para)
                        
                        texts.append(text)
                        metadata.append({
                            "type": "table_cell",
                            "table_index": t_idx,
                            "row_index": r_idx,
                            "cell_index": c_idx,
                            "paragraph_index": p_idx,
                            "format": format_meta
                        })

        return texts, metadata

    def _extract_format_from_paragraph(self, para: Paragraph) -> Dict[str, Any]:
        """
        Extracts formatting metadata from the first non-empty run of a paragraph.
        
        Args:
            para: The docx Paragraph object.
            
        Returns:
            A dictionary containing bold, italic, font_size, font_name, and font_color.
        """
        meta: Dict[str, Any] = {
            "bold": False,
            "italic": False,
            "font_size": None,
            "font_name": None,
            "font_color": None
        }
        
        if not para.runs:
            return meta
            
        # Extract from the first run that contains actual text
        for run in para.runs:
            if run.text.strip():
                meta["bold"] = bool(run.bold)
                meta["italic"] = bool(run.italic)
                
                if run.font.size:
                    meta["font_size"] = run.font.size.pt
                if run.font.name:
                    meta["font_name"] = run.font.name
                if run.font.color and run.font.color.rgb:
                    meta["font_color"] = str(run.font.color.rgb)
                break
                
        return meta

    def export_docx(self, original_path: str, translated_texts: List[str], metadata: List[Dict[str, Any]], output_path: str) -> None:
        """
        Creates a new DOCX file by modifying the original to preserve layout and applying new text.
        
        Args:
            original_path: Path to the original DOCX file to use as a template.
            translated_texts: List of translated strings.
            metadata: List of format metadata dictionaries corresponding to the texts.
            output_path: Path to save the output DOCX file.
            
        Raises:
            ValueError: If the lengths of translated_texts and metadata do not match.
        """
        if len(translated_texts) != len(metadata):
            raise ValueError("Length of translated texts and metadata must match.")
            
        doc = Document(original_path)
        
        for text, meta in zip(translated_texts, metadata):
            if meta["type"] == "paragraph":
                para = doc.paragraphs[meta["index"]]
            elif meta["type"] == "table_cell":
                table = doc.tables[meta["table_index"]]
                para = table.rows[meta["row_index"]].cells[meta["cell_index"]].paragraphs[meta["paragraph_index"]]
            else:
                continue
                
            # Clear existing runs
            para.clear()
            
            # Create a new run with the translated text
            run = para.add_run(text)
            fmt = meta["format"]
            
            # Apply original formatting
            if fmt.get("bold") is not None:
                run.bold = fmt["bold"]
            if fmt.get("italic") is not None:
                run.italic = fmt["italic"]
            if fmt.get("font_size"):
                run.font.size = Pt(fmt["font_size"])
                
            # Force Vietnamese font
            run.font.name = self.default_font
            
            if fmt.get("font_color"):
                try:
                    run.font.color.rgb = RGBColor.from_string(fmt["font_color"])
                except ValueError:
                    # Fallback if color string is invalid
                    pass
                
        try:
            doc.save(output_path)
        except Exception as e:
            if "Permission denied" in str(e) or "PermissionError" in str(e):
                raise ValueError(f"Không thể lưu file vào '{output_path}'. Vui lòng đóng file nếu nó đang được mở và thử lại.")
            raise e
