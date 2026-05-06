import re
from typing import List

class TextSegmenter:
    def __init__(
        self,
        split_on_enter: bool = True,
        split_on_soft_return: bool = False,
        custom_markers: List[str] = None,
        max_chars_per_page: int = 1500
    ):
        self.split_on_enter = split_on_enter
        self.split_on_soft_return = split_on_soft_return
        self.custom_markers = custom_markers or []
        self.max_chars_per_page = max_chars_per_page

    def _get_plain_text_length(self, text: str) -> int:
        """Calculate the length of the text without Markdown formatting."""
        # Remove bold/italic (**text**, *text*, __text__, _text_)
        text = re.sub(r'(\*\*|__)(.*?)\1', r'\2', text)
        text = re.sub(r'(\*|_)(.*?)\1', r'\2', text)
        # Remove strikethrough (~~text~~)
        text = re.sub(r'~~(.*?)~~', r'\1', text)
        # Remove inline code (`text`)
        text = re.sub(r'`(.*?)`', r'\1', text)
        # Remove links [text](url)
        text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)
        return len(text)

    def _is_marker_at_start(self, line: str) -> bool:
        """Check if the line starts with any of the custom markers (ignoring leading whitespace)."""
        if not self.custom_markers:
            return False
        
        stripped_line = line.lstrip()
        for marker in self.custom_markers:
            if stripped_line.startswith(marker):
                return True
        return False

    def segment(self, paragraphs: List[str]) -> List[str]:
        """Split paragraphs into segments based on configuration."""
        if not paragraphs:
            return []

        segments = []
        current_segment = []

        for paragraph in paragraphs:
            if not paragraph.strip():
                continue

            lines = paragraph.split('\n')
            
            for i, line in enumerate(lines):
                is_first_line_of_para = (i == 0)
                
                # Determine if we should split at this line
                should_split = False
                
                has_marker = self._is_marker_at_start(line)
                
                if has_marker:
                    # If marker exists at the start of any line (after Enter or Soft Return), split
                    should_split = True
                else:
                    if self.custom_markers:
                        # "Combination" logic: if markers are defined, ONLY split if there is a marker.
                        should_split = False
                    else:
                        # Basic logic: no custom markers defined.
                        if is_first_line_of_para and self.split_on_enter:
                            should_split = True
                        elif not is_first_line_of_para and self.split_on_soft_return:
                            should_split = True

                if should_split:
                    # Save current segment if it has content
                    if current_segment:
                        segments.append('\n'.join(current_segment))
                        current_segment = []
                    current_segment.append(line)
                else:
                    # Do not split.
                    # If this is the very first line overall, start the first segment anyway
                    if not segments and not current_segment:
                        current_segment.append(line)
                    else:
                        current_segment.append(line)

        # Append the last segment
        if current_segment:
            segments.append('\n'.join(current_segment))

        return segments

    def paginate(self, segments: List[str]) -> List[List[str]]:
        """Distribute segments into pages based on max_chars_per_page limit."""
        if not segments:
            return []

        pages = []
        current_page = []
        current_page_chars = 0

        for segment in segments:
            segment_length = self._get_plain_text_length(segment)
            
            if not current_page:
                current_page.append(segment)
                current_page_chars += segment_length
            else:
                if current_page_chars + segment_length > self.max_chars_per_page:
                    # Start a new page
                    pages.append(current_page)
                    current_page = [segment]
                    current_page_chars = segment_length
                else:
                    # Add to current page
                    current_page.append(segment)
                    current_page_chars += segment_length

        if current_page:
            pages.append(current_page)

        return pages
