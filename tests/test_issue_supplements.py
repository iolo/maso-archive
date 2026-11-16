"""Cover/source-selection companions must match the retained mixed-source article views."""
from copy import deepcopy
import json
from pathlib import Path
import unittest

from tests import test_image_covers as cover_fixtures
from tools.pdf_restore.inventory import pin,write_json
from tools.pdf_restore.issue import copy_supplements,check_supplements


class IssueSupplementTests(unittest.TestCase):
    def fixture(self):
        fixture=cover_fixtures.ImageCoversTest();fixture.setUp();self.addCleanup(fixture.doCleanups)
        root=fixture.root;source=json.loads((fixture.inputs/'source.json').read_bytes());source['cleanup']={}
        for p in source['pages']:
            p.update(source_filename_number=None,printed_page=None)
        for index in [4,5]:
            p=deepcopy(source['pages'][0]);p.update(source_index=index,reading_order=index+1,source_filename_number=100+index)
            source['pages'].append(p)
        write_json(fixture.inputs/'source.json',source);fixture.save_review();covers=fixture.export()
        package=json.loads((covers/'cover-set.json').read_bytes());rows=[]
        for p in source['pages']:
            disposition='selected-cover-face' if p['source_index']<4 else 'selected-article-supplement' if p['source_index']==4 else 'retained-other-supplementary-source'
            rows.append(dict(source_index=p['source_index'],source_image=p['image'],reading_order=p['reading_order'],source_filename_number=p['source_filename_number'],printed_page=None,disposition=disposition,cross_source_equivalence_verified=False,body_owner_toc_entry_id='maso-1984-11-toc-0001' if p['source_index']==4 else None))
        selection=dict(kind='supplementary-source-selection',issue_id='maso-1984-11',source=package['source'],cleanup={},total_images=6,records=rows,counts={'selected-cover-face':4,'selected-article-supplement':1,'retained-other-supplementary-source':1})
        write_json(root/'selection.json',selection)
        ledger=dict(issue_id='maso-1984-11',supplements=dict(cover_set=dict(directory=covers.relative_to(root).as_posix(),manifest=pin(root,(covers/'manifest.json').relative_to(root).as_posix())),source_selection=pin(root,'selection.json')))
        native=dict(schema_version=3,toc_entry_id='maso-1984-11-toc-0001',components=[dict(name='jpeg',source=package['source'])],pages=[dict(component='jpeg',source_kind='jpeg',original_page=source['pages'][4])])
        return root,ledger,{native['toc_entry_id']:native},selection

    def test_companions_copy_exactly_and_check_without_original_inputs(self):
        root,ledger,packages,selection=self.fixture();stage=root/'issue';stage.mkdir()
        records=copy_supplements(stage,ledger,packages,root)
        self.assertEqual((stage/'supplements/source-selection.json').read_bytes(),(root/'selection.json').read_bytes())
        (root/'selection.json').unlink()
        check_supplements(stage,records,ledger,packages)
        self.assertIsNone(copy_supplements(stage,{'issue_id':'maso-1984-11'},packages,root))
        with self.assertRaisesRegex(ValueError,'Undeclared'):check_supplements(stage,records,{'issue_id':'maso-1984-11'},packages)

    def test_rehashed_selection_damage_rejects_against_actual_article_and_cover_views(self):
        root,ledger,packages,selection=self.fixture();stage=root/'issue';stage.mkdir();records=copy_supplements(stage,ledger,packages,root)
        for name,change in [
            ('owner',lambda s:s['records'][4].update(body_owner_toc_entry_id='other')),
            ('geometry',lambda s:s['records'][4].update(source_filename_number=4)),
            ('omission',lambda s:s['records'].pop()),
            ('equivalence',lambda s:s['records'][5].update(cross_source_equivalence_verified=True)),
            ('cover',lambda s:s['records'][0].update(disposition='retained-other-supplementary-source')),
            ('counts',lambda s:s['counts'].update(**{'selected-cover-face':3})),
            ('extra-owner',lambda s:s['records'][5].update(body_owner_toc_entry_id='maso-1984-11-toc-0001'))]:
            with self.subTest(name=name):
                damaged=deepcopy(selection);change(damaged);write_json(stage/'supplements/source-selection.json',damaged)
                p=pin(stage,'supplements/source-selection.json');r=deepcopy(records);r['source_selection']=p;l=deepcopy(ledger);l['supplements']['source_selection']=p
                with self.assertRaises(ValueError):check_supplements(stage,r,l,packages)

    def test_article_views_cannot_be_reassigned_or_omitted(self):
        root,ledger,packages,_=self.fixture();stage=root/'issue';stage.mkdir();records=copy_supplements(stage,ledger,packages,root)
        for change in [lambda p:p['pages'][0]['original_page'].update(source_index=5),lambda p:p['pages'].clear(),lambda p:p['components'][0]['source'].update(id='other')]:
            bad=deepcopy(packages);change(next(iter(bad.values())))
            with self.assertRaises(ValueError):check_supplements(stage,records,ledger,bad)


if __name__=='__main__':unittest.main()
