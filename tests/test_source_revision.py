"""Distinct PDF/JPEG geometry, observed joins, deterministic exports and tamper rejection."""
from copy import deepcopy
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from PIL import Image

from tools.pdf_restore.build import build, check_export
from tools.pdf_restore.inventory import pin, write_json
from tools.pdf_restore.package import page_transform, image_transform, validate_package
from tools.pdf_restore.source_revision import export, project, check_revision, file_inventory

ROOT = Path(__file__).resolve().parents[1]


class SourceRevisionTests(unittest.TestCase):
    def fixture(self, root):
        (root/'TOC.md').write_text('Synthetic canonical title')
        (root/'source.pdf').write_bytes(b'Synthetic original PDF')
        Image.new('RGB',(100,150),'blue').save(root/'source.jpg')
        runtime=root/'archive/toolchains/ocr';write_json(runtime/'runtime.json',{'synthetic':True})
        specs=[];originals=[]
        for name,version,folio,text in [('pdf',1,'7','1000 PRINT "한글"\n1010 PRINT\n'),
                                         ('jpeg',2,'8','"continuation"\n1020 END\n')]:
            folder=root/'archive'/name;folder.mkdir(parents=True)
            p=json.loads((ROOT/'examples/pdf-article.json').read_bytes())
            if version==1:
                page=dict(pdf_index=3,pdf_page=4,printed_page=folio,width_pt=100,height_pt=150,
                    rotation=0,MediaBox=[0,0,100,150],CropBox=[0,0,100,150])
                page['pdf_to_upright_normalized']=page_transform(page)
                source={**p['source'],**pin(root,'source.pdf')};selector={'pdf_index':3};selection={'pdf_index':3,'pdf_page':4}
            else:
                page=dict(source_index=3,image=pin(root,'source.jpg'),width_px=100,height_px=150,
                    reading_order=9,source_filename_number=99,printed_page=folio)
                page['image_to_upright_normalized']=image_transform(page)
                write_json(root/'source-set.json',dict(kind='jpeg-set',issue_id=p['issue_id'],cleanup={},pages=[page]))
                source=dict(id='jpeg-synthetic',kind='jpeg-set',**pin(root,'source-set.json'))
                selector={'source_index':3};selection={**selector,'image':page['image']}
            p.update(schema_version=version,source=source,toc_pin=pin(root,'TOC.md'),pages=[page],
                regions=[dict(id='body',kind='code',bbox=[0,0,1,1],notes='Synthetic complete column',**selector)],
                excluded_regions=[],mapping=dict(status='mapped',evidence=['Synthetic observed extent'],uncertainties=[]))
            write_json(folder/'map.json',p)
            inventory=folder/'inventory'
            pages=[{}, {}, {}, page] if version==1 else [page]
            write_json(inventory/'sources.json',dict(sources=[dict(source,scope='toc-entries-and-cover',pages=pages)]))
            inventory.mkdir(exist_ok=True);(inventory/'queue.jsonl').write_text(json.dumps(dict(toc_entry_id=p['toc_entry_id'],issue_id=p['issue_id'],source_id=source['id']))+'\n')
            ocr=folder/'ocr';ocr.mkdir();Image.new('RGB',(20,30),'blue').save(ocr/'body.png')
            (ocr/'raw.txt').write_text('Original OCR\n');(ocr/'raw.tsv').write_text('Original TSV\n')
            write_json(ocr/'raw.settings.json',dict(package={'sha256':pin(folder,'map.json')['sha256']},source_sha256=source['sha256'],region_ids=['body'],**selection))
            write_json(ocr/'evidence.json',dict(source_sha256=source['sha256'],runtime=pin(runtime,'runtime.json'),
                **({'pdf_page':4} if version==1 else selection),images=[pin(ocr,'body.png')],results=[dict(region_ids=['body'],text=pin(ocr,'raw.txt'),positions=pin(ocr,'raw.tsv'),settings=pin(ocr,'raw.settings.json'))]))
            block=dict(id='program',kind='code',text=text,region_ids=['body'],correction_evidence=['corrections.json#body'],uncertainties=[])
            corrections=dict(article_id=p['id'],map=pin(folder,'map.json'),records=[dict(id='body',scan=pin(folder,'ocr/body.png'),raw_ocr=pin(folder,'ocr/raw.txt'))],blocks=[block],regional_transcription={'body':text})
            write_json(folder/'corrections.json',corrections)
            native_recipe=dict(map=pin(folder,'map.json'),corrections=pin(folder,'corrections.json'),
                inventory={k:pin(root,(inventory/n).relative_to(root).as_posix()) for k,n in [('sources','sources.json'),('queue','queue.jsonl')]},
                runtime_directory='archive/toolchains/ocr',runtime=pin(runtime,'runtime.json'),ocr_bundles=[dict(directory='ocr',manifest=pin(folder,'ocr/evidence.json'))],
                figures=[],content_order=[dict(type='block',id='program')],availability='partial',
                verification=dict(status='sample-reviewed',reviewed_region_ids=['body'],evidence=['Source compared'],uncertainties=['Glyph unknown.']),gaps=['Other source part absent.'])
            write_json(folder/'recipe.json',native_recipe);out=root/'work'/name;native=build(folder/'recipe.json',out,root)
            specs.append(dict(name=name,manifest=pin(root,(out/'manifest.json').relative_to(root).as_posix()),inventory=native_recipe['inventory'],toc_snapshot=pin(root,'TOC.md')))
            originals.append((native,corrections))
        recipe=dict(kind='source-supplement-assembly-v1',components=specs,
            expected_views=[dict(component=name,source_kind=name,source_index=3,printed_page=f) for name,f in [('pdf','7'),('jpeg','8')]],
            join=dict(from_component='pdf',from_block='program',to_component='jpeg',to_block='program',separator='',printed_line=1010,
                from_suffix='1010 PRINT\n',to_prefix='"continuation"\n',from_printed_folio='7',to_printed_folio='8',next_printed_line=1020,last_printed_line=1020,reason='Observed wrapped statement.'),
            resolved_notes=[dict(component=name,field='gaps',note='Other source part absent.',reason='Both supplied source parts included.') for name in ['pdf','jpeg']],
            evidence=['Exact source join compared.'],uncertainties=['Encoding and execution unverified.'])
        write_json(root/'recipe.json',recipe)
        return recipe,originals

    def test_export_rebuild_and_check_without_external_inputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);recipe,originals=self.fixture(root)
            one=root/'work/revision';two=root/'work/repeat'
            p=export(root/'recipe.json',one,root);export(root/'recipe.json',two,root)
            self.assertEqual(file_inventory(one),file_inventory(two))
            self.assertEqual(p['availability'],'readable')
            self.assertEqual([v['original_page'].get('pdf_page') for v in p['pages']],[4,None])
            self.assertEqual([v['original_page'].get('source_filename_number') for v in p['pages']],[None,99])
            self.assertEqual(len(p['blocks']),1)
            self.assertIn('Glyph unknown.',' '.join(p['gaps']))
            c=json.loads((one/'corrections.json').read_bytes())
            self.assertEqual(len(c['listing_line_index']),4)
            self.assertEqual([v['printed_line'] for v in c['logical_listing_line_index']],[1000,1010,1020])
            self.assertEqual({v['component'] for v in c['logical_listing_line_index'][1]['source_parts']},{'pdf','jpeg'})
            (root/'source.pdf').unlink();(root/'source.jpg').unlink();(root/'source-set.json').unlink();shutil.rmtree(root/'archive')
            self.assertEqual(check_revision(one),p)
            self.assertEqual(check_export(one),p)
            self.assertEqual(validate_package(p),p)

    def test_rehashed_source_index_and_reading_tampering_reject(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);self.fixture(root);base=root/'work/revision';export(root/'recipe.json',base,root)
            for name,change in [
                ('region',lambda p:p['regions'][0].update(view_id='jpeg--view-3')),
                ('geometry',lambda p:p['pages'][1]['original_page'].update(source_filename_number=8)),
                ('availability',lambda p:p['components'][0].update(original_availability='readable')),
                ('block',lambda p:p['blocks'][0].update(text='fabricated'))]:
                with self.subTest(name=name):
                    target=root/'work'/name;shutil.copytree(base,target)
                    p=json.loads((target/'article.json').read_bytes());change(p);write_json(target/'article.json',p)
                    m=json.loads((target/'manifest.json').read_bytes());m['files']=file_inventory(target);write_json(target/'manifest.json',m)
                    with self.assertRaises(ValueError):check_revision(target)
            target=root/'work/index';shutil.copytree(base,target);c=json.loads((target/'corrections.json').read_bytes());c['listing_line_index'][1]['source_parts'][0]['component']='jpeg';write_json(target/'corrections.json',c)
            m=json.loads((target/'manifest.json').read_bytes());m['files']=file_inventory(target);write_json(target/'manifest.json',m)
            with self.assertRaisesRegex(ValueError,'source indexes'):check_revision(target)

    def test_wrong_sources_folios_join_and_dispositions_reject(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);recipe,originals=self.fixture(root)
            mutations=[lambda r:r['join'].update(printed_line=1000),lambda r:r['join'].update(to_prefix='invented'),
                lambda r:r['join'].update(from_printed_folio='4'),lambda r:r['expected_views'][1].update(source_index=99),
                lambda r:r['resolved_notes'][0].update(note='Different historical gap'),
                lambda r:r['components'][1].update(name='pdf'),lambda r:r['join'].update(separator='repaired'),
                lambda r:r['expected_views'].reverse()]
            for change in mutations:
                revised=deepcopy(recipe);change(revised)
                with self.assertRaises(ValueError):project(revised,originals)
            reversed_sources=list(reversed(originals))
            with self.assertRaisesRegex(ValueError,'PDF opening'):project(recipe,reversed_sources)

    def test_changed_master_rejected_before_publication(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);self.fixture(root);(root/'source.pdf').write_bytes(b'changed')
            with self.assertRaisesRegex(ValueError,'hash/size'):export(root/'recipe.json',root/'work/rejected',root)
            self.assertFalse((root/'work/rejected').exists())


if __name__=='__main__':unittest.main()
