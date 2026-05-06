import unittest
from src.core.segmenter import TextSegmenter

class TestTextSegmenter(unittest.TestCase):
    def test_split_on_enter_only(self):
        segmenter = TextSegmenter(split_on_enter=True, split_on_soft_return=False)
        paragraphs = ["Para 1", "Para 2", "Para 3"]
        segments = segmenter.segment(paragraphs)
        self.assertEqual(segments, ["Para 1", "Para 2", "Para 3"])

    def test_split_on_soft_return_only(self):
        segmenter = TextSegmenter(split_on_enter=False, split_on_soft_return=True)
        paragraphs = ["Para 1\nLine 2", "Para 2"]
        segments = segmenter.segment(paragraphs)
        self.assertEqual(segments, ["Para 1", "Line 2\nPara 2"])

    def test_combo_enter_and_marker(self):
        segmenter = TextSegmenter(split_on_enter=True, custom_markers=["【"])
        paragraphs = ["【Intro】 Hello", "World", "【Method】 Test"]
        segments = segmenter.segment(paragraphs)
        self.assertEqual(segments, ["【Intro】 Hello\nWorld", "【Method】 Test"])

    def test_combo_soft_return_and_marker_with_spaces(self):
        segmenter = TextSegmenter(split_on_soft_return=True, custom_markers=["※"])
        paragraphs = ["Text\n  ※ Note 1", "Another\n※ Note 2"]
        segments = segmenter.segment(paragraphs)
        self.assertEqual(segments, ["Text", "  ※ Note 1\nAnother", "※ Note 2"])

    def test_marker_in_middle_does_not_split(self):
        segmenter = TextSegmenter(split_on_enter=True, custom_markers=["【"])
        paragraphs = ["This is a 【Marker】 inside", "And another line"]
        segments = segmenter.segment(paragraphs)
        self.assertEqual(segments, ["This is a 【Marker】 inside\nAnd another line"])

    def test_plain_text_length(self):
        segmenter = TextSegmenter()
        self.assertEqual(segmenter._get_plain_text_length("**Bold** and *italic*"), 15)
        self.assertEqual(segmenter._get_plain_text_length("[Link](http://test.com)"), 4)
        self.assertEqual(segmenter._get_plain_text_length("`code`"), 4)
        self.assertEqual(segmenter._get_plain_text_length("~~strike~~"), 6)

    def test_pagination(self):
        segmenter = TextSegmenter(max_chars_per_page=10)
        segments = ["12345", "1234", "1234567"]
        pages = segmenter.paginate(segments)
        self.assertEqual(pages, [["12345", "1234"], ["1234567"]])

    def test_pagination_large_segment(self):
        segmenter = TextSegmenter(max_chars_per_page=10)
        segments = ["12345", "123456789012", "123"]
        pages = segmenter.paginate(segments)
        self.assertEqual(pages, [["12345"], ["123456789012"], ["123"]])

    def test_empty_input(self):
        segmenter = TextSegmenter()
        self.assertEqual(segmenter.segment([]), [])
        self.assertEqual(segmenter.paginate([]), [])

    def test_empty_paragraph(self):
        segmenter = TextSegmenter(split_on_enter=True)
        paragraphs = ["Para 1", "   ", "Para 2"]
        segments = segmenter.segment(paragraphs)
        self.assertEqual(segments, ["Para 1", "Para 2"])

if __name__ == '__main__':
    unittest.main()
