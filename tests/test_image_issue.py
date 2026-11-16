"""Whole-issue ownership, byte preservation, portable checks and failure gates."""
from collections import Counter
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

from PIL import Image

from tests import test_image_source as image_fixture
from tools.pdf_restore.build import build as build_article
from tools.pdf_restore.image_covers import build as build_covers
from tools.pdf_restore.image_issue import build, check_export, inventory, read, validate_accounting
from tools.pdf_restore.inventory import pin, write_json
from tools.pdf_restore.package import image_transform


class ImageIssueTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = r = Path(self.temporary.name)
        self.inputs = base = r/'inputs'; base.mkdir()
        recipe_path = image_fixture.ImageSourceTests().fixture(r)
        recipe = read(recipe_path); article_base = recipe_path.parent
        mapped = read(article_base/'map.json'); issue = mapped['issue_id']
        toc_id = mapped['toc_entry_id']; heading_id = issue + '-toc-0002'
        source = read(r/'source-set.json'); faces = []
        for index,role,order in [(10,'front',1),(11,'inside-front',2),(12,'inside-back',5),(13,'back',6),(14,'form',4)]:
            Image.new('RGB',(80,100),(index*10,40,80)).save(base/(role+'.jpg'))
            page = dict(source_index=index,image=pin(r,'inputs/'+role+'.jpg'),width_px=80,height_px=100,
                        reading_order=order,source_filename_number=None)
            page['image_to_upright_normalized']=image_transform(page); source['pages'].append(page)
            if role=='form':continue
            faces.append(dict(role=role,source_index=index,material_kind='cover-artwork' if role=='front' else 'advertisement',
                role_basis='Synthetic reviewed role.',condition=['Original raster.'],observations=[],groups=[],
                full_text_transcription=False,cosmetic_reconstruction_applied=False))
        toc=[dict(id=toc_id,issue_id=issue,title_candidate=mapped['title'],parent_id=None),
             dict(id=heading_id,issue_id=issue,title_candidate='Synthetic heading',parent_id=None)]
        (base/'toc.jsonl').write_text(''.join(json.dumps(t)+'\n' for t in toc))
        source['toc_inputs']=[pin(r,'inputs/toc.jsonl')]; write_json(base/'source.json',source)
        source_pin=dict(id='jpeg-synthetic',kind='jpeg-set',**pin(r,'inputs/source.json'))
        mapped['source']=source_pin;write_json(article_base/'map.json',mapped); recipe['map']=pin(article_base,'map.json')
        inventory_root=r/'private/pdf-restoration/inventory';sources=read(inventory_root/'sources.json')
        sources['sources'][0].update(source_pin,pages=source['pages']);write_json(inventory_root/'sources.json',sources)
        recipe['inventory']['sources']=pin(r,'private/pdf-restoration/inventory/sources.json')
        corrections=read(article_base/'corrections.json');corrections['map']=recipe['map']
        write_json(article_base/'corrections.json',corrections);recipe['corrections']=pin(article_base,'corrections.json')
        for bundle in recipe['ocr_bundles']:
            evidence_path=article_base/bundle['manifest']['path'];evidence=read(evidence_path)
            evidence['source_sha256']=source_pin['sha256']
            for row in evidence['results']:
                settings_path=evidence_path.parent/row['settings']['path']; settings=read(settings_path)
                settings['source_sha256']=source_pin['sha256']; settings['package']={'sha256':recipe['map']['sha256']}
                write_json(settings_path,settings);row['settings']=pin(evidence_path.parent,settings_path.name)
            write_json(evidence_path,evidence);bundle['manifest']=pin(article_base,evidence_path.relative_to(article_base).as_posix())
        write_json(recipe_path,recipe);build_article(recipe_path,r/'work/article',r)
        a=read(r/'work/article/article.json')
        write_json(base/'cover-review.json',dict(faces=faces,missing_faces=[],limitations=['Selected labels only.']))
        write_json(base/'cover-recipe.json',dict(issue_id=issue,source=source_pin,review=pin(base,'cover-review.json')))
        build_covers(base/'cover-recipe.json',r/'cover',r)
        manifest=pin(r,'work/article/manifest.json');cover_manifest=pin(r,'cover/manifest.json')
        heading=dict(issue_id=issue,toc_entry_id=heading_id,title='Synthetic heading',parent_id=None,
            classification='group-heading',body_owner=False,availability='not-applicable',restoration=None,child_toc_entry_ids=[])
        write_json(base/'heading.json',heading);write_json(base/'heading-validation.json',dict(result='passed'))
        entries=[dict(toc_entry_id=toc_id,title=mapped['title'],parent_id=None,classification='article',body_owner=True,
            availability='readable',verification=a['verification']['status'],package=dict(path='work/article',manifest=manifest)),
            dict(heading,toc_entry_id=heading_id,verification='sample-reviewed',group_reference=dict(
                owns_standalone_body=False,evidence=pin(r,'inputs/heading.json'),validation=pin(r,'inputs/heading-validation.json')))]
        rows=[]
        for p in sorted(source['pages'],key=lambda p:p['reading_order']):
            row=dict(source_index=p['source_index'],source_image=p['image'],width_px=p['width_px'],height_px=p['height_px'],
                reading_order=p['reading_order'],source_filename_number=p.get('source_filename_number'))
            if p['source_index']==7:
                row.update(classification='selected-article-source',article_owners=[dict(toc_entry_id=toc_id,article_id=a['id'],
                    package_manifest=manifest,region_ids=[v['id'] for v in a['regions']])])
            elif p['source_index']==14:
                row.update(classification='unlisted-form',visual_disposition=dict(source_index=14,source_image=p['image'],
                    source_filename_number=None,reading_order=4,classification='unlisted-form',body_owner_toc_entry_id=None,
                    complete_text_transcription=False,printed_folio_observed=None,observed_label='Synthetic form',
                    notes='Original blank form retained.',group_id=None))
            else:
                face=next(f for f in faces if f['source_index']==p['source_index'])
                row.update(classification='cover',face=face['role'],cover_package_manifest=cover_manifest)
            rows.append(row)
        accounting=dict(kind='jpeg-issue-source-accounting',issue_id=issue,source_descriptor=source_pin,
            cover_package_manifest=cover_manifest,total_source_images=6,all_source_images_visually_disposed=True,
            remaining_visual_dispositions=0,records=rows,groups=[],counts=dict(Counter(x['classification'] for x in rows)))
        write_json(base/'accounting.json',accounting)
        ledger=dict(issue_id=issue,entries=entries,canonical_identities=2,readable_articles=1,group_headings=1,
            partial_articles=0,identitiesAwaitingDisposition=0,cover_set=dict(path='cover',manifest=cover_manifest),
            source_accounting=dict(status='complete',accounting=pin(r,'inputs/accounting.json')))
        write_json(base/'ledger.json',ledger)
        self.recipe=base/'issue-recipe.json';write_json(self.recipe,dict(issue_id=issue,source=source_pin,
            ledger=pin(r,'inputs/ledger.json'),toc=pin(r,'inputs/toc.jsonl'),accounting=pin(r,'inputs/accounting.json')))
        self.ledger,self.toc,self.source,self.accounting,self.articles,self.covers=ledger,toc,source,accounting,{toc_id:a},read(r/'cover/cover-set.json')

    def export(self,name='out'):
        build(self.recipe,self.root/name,self.root)
        return self.root/name

    def reseal(self,out):
        manifest=read(out/'manifest.json');manifest['files']=inventory(out);write_json(out/'manifest.json',manifest)

    def test_exact_rebuild_and_original_components_preserved(self):
        a,b=self.export('a'),self.export('b')
        self.assertEqual(inventory(a),inventory(b));self.assertEqual((a/'manifest.json').read_bytes(),(b/'manifest.json').read_bytes())
        issue=check_export(a);self.assertEqual(issue['counts']['source_images'],6)
        self.assertEqual((a/'other-sources/source-14.jpg').read_bytes(),(self.inputs/'form.jpg').read_bytes())
        self.assertEqual((a/'articles'/self.toc[0]['id']/'manifest.json').read_bytes(),(self.root/'work/article/manifest.json').read_bytes())
        self.assertFalse((a/'index.html').exists())
        with self.assertRaises(ValueError):self.export('a')

    def test_portable_checker_with_original_workspace_unavailable(self):
        out=self.export(); moved=Path(self.temporary.name+'-portable')
        out.rename(moved); self.addCleanup(lambda:__import__('shutil').rmtree(moved))
        __import__('shutil').rmtree(self.root)
        self.assertEqual(check_export(moved)['availability'],'complete')

    def test_source_and_recipe_pin_drift_rejected(self):
        (self.inputs/'form.jpg').write_bytes(b'drift')
        with self.assertRaises(ValueError):self.export('bad')
        self.assertFalse((self.root/'bad').exists())
        recipe=read(self.recipe);recipe['toc']['sha256']='0'*64;write_json(self.recipe,recipe)
        with self.assertRaises(ValueError):self.export('bad-toc')

    def test_accounting_rejects_identity_ownership_and_completion_damage(self):
        for name in ['lost','duplicate','owner','folio','claim','cover','pending','count','group','canonical','heading','range']:
            with self.subTest(name=name):
                l,t,s,a,p,c=deepcopy((self.ledger,self.toc,self.source,self.accounting,self.articles,self.covers))
                selected=next(x for x in a['records'] if x['classification']=='selected-article-source')
                other=next(x for x in a['records'] if x['classification']=='unlisted-form')
                if name=='lost':a['records'].pop()
                if name=='duplicate':a['records'][1]=deepcopy(a['records'][0])
                if name=='owner':selected['article_owners'][0]['region_ids']=[]
                if name=='folio':other['visual_disposition']['printed_folio_observed']=241
                if name=='claim':other['visual_disposition']['complete_text_transcription']=True
                if name=='cover':next(x for x in a['records'] if x['classification']=='cover')['face']='other'
                if name=='pending':a['remaining_visual_dispositions']=1
                if name=='count':a['counts']['cover']=3
                if name=='group':other['visual_disposition']['group_id']='lost'
                if name=='canonical':t[0]['title_candidate']='wrong'
                if name=='heading':l['entries'][1]['body_owner']=True
                if name=='range':next(iter(p.values()))['pages'][0]['width_px']=1
                with self.assertRaises((ValueError,KeyError)):validate_accounting(l,t,s,a,p,c)

    def test_manifest_reseal_does_not_hide_component_or_input_drift(self):
        for name in ['extra','raster','ledger','article','cover']:
            with self.subTest(name=name):
                out=self.export('damaged-' + name)
                target={'extra':'unreferenced.txt','raster':'other-sources/source-14.jpg','ledger':'ledger.json',
                    'article':'articles/'+self.toc[0]['id']+'/article.txt','cover':'covers/faces/front.jpg'}[name]
                (out/target).write_bytes(b'tampered');self.reseal(out)
                with self.assertRaises((ValueError,json.JSONDecodeError)):check_export(out)

    def test_unsafe_paths_and_output_overlap_rejected(self):
        recipe=read(self.recipe);recipe['source']['path']='../outside.json';write_json(self.recipe,recipe)
        with self.assertRaises(ValueError):self.export()
        recipe['source']=dict(self.accounting['source_descriptor']);write_json(self.recipe,recipe)
        with self.assertRaises(ValueError):build(self.recipe,self.root/'work/article/inside',self.root)


if __name__=='__main__':unittest.main()
