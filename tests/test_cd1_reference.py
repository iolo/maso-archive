"""Readable extraction and safe, whitespace-preserving portable exports."""
from copy import deepcopy
from pathlib import Path
import tempfile
import unittest

from tools.reference import text as recovery, export, check
from tools.decode_cd1_paragraph import digest


def source(raw):
    return {'id':'cd1:topic:1','native':{'ordinal':1},
            'rtf':{'byte_offset':0,'byte_length':len(raw),'sha256':digest(raw)}}


def recover(raw):return recovery.recover(raw,source(raw))


class ReferenceTextTests(unittest.TestCase):
    def test_split_korean_and_fullwidth_characters_cross_ordinary_formatting(self):
        for raw,expected in [(rb"\f4 \'b8\f15 \'a6\par ",'를\n'),
                             (rb"\f4 \'a3\cf2\qc\f15 \'a1\par ",'！\n')]:
            value=recover(raw)
            self.assertEqual(recovery.text_for(value['paragraphs']),expected)
            self.assertFalse(value['issues']);self.assertEqual(value['source_bytes'],len(raw))
            fragments=value['paragraphs'][0]['runs'][0]['source_fragments']
            self.assertEqual([x['font_id'] for x in fragments],[4,15])

    def test_code_operators_tabs_blank_lines_and_literal_rtf_syntax(self):
        raw=rb'\f15  if (a < b && s[0] == "\\") \{\-\tab  x++;\}\par \par '
        value=recover(raw)
        self.assertEqual(recovery.text_for(value['paragraphs']),' if (a < b && s[0] == "\\") {\t x++;}\n\n')
        self.assertFalse(value['issues'])

    def test_unknown_bytes_are_localized_instead_of_discarding_a_listing(self):
        value=recover(rb"\f15 before \'80 after\par ")
        self.assertEqual(recovery.text_for(value['paragraphs']),'before ⟦bytes:80⟧ after\n')
        self.assertEqual(value['issues'][0]['bytes_hex'],'80')
        with self.assertRaises(ValueError):recovery.recover(b'changed',source(b'original'))

    def test_symbol_fonts_are_marked_and_do_not_reinterpret_neighboring_text(self):
        value=recover(rb'\f4 before \f2 AB\f4  after\par ')
        self.assertEqual(recovery.text_for(value['paragraphs']),'before ⟦symbol font 2: 4142⟧ after\n')
        self.assertEqual(value['issues'][0]['kind'],'symbol_font_ambiguous')

    def test_line_and_table_controls_preserve_visible_text_and_boundaries(self):
        value=recover(rb'\trowd\trgaph10\trleft0\cellx100\cellx200\intbl a\cell b\cell\row c\line d\par ')
        self.assertEqual(recovery.text_for(value['paragraphs']),'a\tb\t\nc\nd\n')
        self.assertFalse(value['issues'])

    def test_metadata_is_hidden_and_images_keep_source_position(self):
        raw=rb'{\up #}{\footnote\pard\plain{\up #} ALIAS}{\v LINK}before \{bmc bm54.wmf\} after\par '
        value=recover(raw)
        self.assertEqual(recovery.text_for(value['paragraphs']),'before [image:bm54.wmf] after\n')
        self.assertFalse(value['issues'])

    def test_last_document_brace_and_unterminated_text_do_not_lose_content(self):
        value=recover(b'last line}')
        self.assertEqual(recovery.text_for(value['paragraphs']),'last line')
        self.assertEqual(value['normalizations']['document_closing_brace'],1)
        self.assertFalse(value['paragraphs'][0]['terminated'])
        with self.assertRaises(ValueError):recover(b'bad}middle')

    def test_unknown_visible_controls_and_embedded_controls_are_explicit(self):
        value=recover(rb"abc\mystery xyz\'01\par ")
        self.assertIn('⟦RTF control:mystery⟧',recovery.text_for(value['paragraphs']))
        self.assertIn('⟦control:01⟧',recovery.text_for(value['paragraphs']))
        self.assertEqual({x['kind'] for x in value['issues']},{'unknown_control','embedded_control'})


class ReferenceExportTests(unittest.TestCase):
    def test_article_and_listing_downloads_match_rendered_literal_code(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);value='<script>alert("x")</script>\t& ->  \\'
            blocks=[{'id':'b','type':'code','preformatted':True,'paragraphs':[
                {'id':'p1','runs':[{'type':'text','text':value}],'terminated':True},
                {'id':'p2','runs':[],'terminated':True}]}]
            job={'source_reference':'sample','issue_id':'maso-1988-02','title':'<Test>', 'candidate_article_id':'cd1:article:sample'}
            row=export.export_article(root,job,blocks,'normalized','',lambda *x:None,{})
            page=check.Page();page.feed((root/row['path']).read_text())
            self.assertEqual(page.code,[value+'\n\n'])
            self.assertEqual((root/row['text']).read_text(),value+'\n\n')
            self.assertIn('&lt;script&gt;', (root/row['path']).read_text())
            position=export.read((root/row['path']).parent/'paragraphs.json')
            self.assertEqual((position[0]['first_line'],position[0]['last_line'],position[1]['first_line']),(1,1,2))

    def test_blocked_candidate_has_no_invented_article_text(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);job={'source_reference':'blocked','issue_id':'maso-1988-02','title':'Unknown','candidate_article_id':'cd1:article:blocked'}
            row=export.export_article(root,job,[],'blocked','Source boundaries unresolved',lambda *x:None,{})
            self.assertIsNone(row['text']);self.assertFalse(((root/row['path']).parent/'article.txt').exists())

    def test_prepared_projection_preserves_marks_and_maps_images_without_mutation(self):
        article={'sections':[{'blocks':[{'id':'b','layout':'flow','paragraphs':[{'id':'p','runs':[
            {'type':'text','text':'a\t b','marks':['bold']},{'type':'media','media_id':'m'}]}]}]}]}
        before=deepcopy(article);blocks=export.prepared_blocks(article,{'m':{'source':{'resource':'bm1.bmp'}}})
        self.assertEqual(article,before)
        self.assertEqual(recovery.text_for(blocks[0]['paragraphs']),'a\t b[image:bm1.bmp]\n')
        self.assertIn('<strong>a\t b</strong>',export.render_runs(blocks[0]['paragraphs'][0]['runs']))


@unittest.skipUnless(export.RECORD.exists(),'Readable reference has not been built')
class ReferenceArtifacts(unittest.TestCase):
    def test_complete_export_links_text_listings_and_gap_accounting(self):
        record=export.read(export.RECORD);root=export.ROOT/record['output_root']
        if not root.exists():self.skipTest('Private readable reference unavailable')
        result=check.check(root)
        self.assertEqual(result['articles'],1088)
        self.assertEqual(record['counts']['article_status'],{'blocked':8,'normalized':52,'prepared':995,'reference_with_gaps':33})
        self.assertEqual(record['counts']['articles_with_text'],1080)
        index=(root/'index.html').read_text()
        self.assertLess(index.index('issues/1988-01/'),index.index('issues/1983-11/'))
        review=export.read(export.ROOT/'data/catalog/batch-runs/cd1-codec-review.json')
        boundaries=export.read(export.ROOT/review['output_root']/'boundaries.json')
        for ref,char in [('8901110','를'),('9103202','！')]:
            row=next(r for r in export.read(root/'catalog.json') if r['reference']==ref)
            self.assertEqual(row['status'],'normalized');self.assertIn(char,(root/row['text']).read_text())
            candidate=next(r for r in boundaries if r['reference']==ref)['candidate_text']
            self.assertIn(candidate,(root/row['text']).read_text())
