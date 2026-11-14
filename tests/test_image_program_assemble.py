"""Cross-segment program/routine identity, typed graphs and offline rebuild."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

from tests import test_image_assemble as base_tests
from tools.pdf_restore.assemble import assemble,project,read_segment
from tools.pdf_restore.build import build,check_export
from tools.pdf_restore.inventory import pin,write_json

S,E='utf8_byte_start','utf8_byte_end_exclusive'


class ImageProgramAssemblyTests(unittest.TestCase):
    def fixture(self,root):
        old_path=base_tests.ImageAssemblyTests().fixture(root);recipe=json.loads(old_path.read_bytes());specs=[]
        for i,name in enumerate(['a','b']):
            base=root/'archive/inputs'/name;p=json.loads((base/'map.json').read_bytes());c=json.loads((base/'corrections.json').read_bytes())
            c.pop('segment');code=next(b for b in c['blocks'] if b['id']=='code')
            if i:
                code['text']=code['text'].replace('10 PRINT','11 PRINT')
                next(r for r in c['records'] if r['id']=='code-region')['corrected_text']=code['text']
                c['regional_text_ranges'][2]['text']=code['text']
                row=c['listing_line_index'][0];row.update(text=code['text'],printed_line=11)
                c['logical_listing_line_index'][0]['printed_line']=11
            length=len(code['text'].encode());scan=c['records'][2]['scan']
            group=dict(kind='source-routine-group',group_id='routine',listing_id='code',block_id='code',source_label='SUB:',region_id='code-region',region_ids=['code-region'],scan=scan,start_byte=0,end_byte=length,literal=code['text'],physical_line_ids=['code:r1'],first_printed_row=10+i,last_printed_row=10+i,continuation_pending=i==0,incoming_continuation=i==1)
            if i==0:
                boundary=dict(kind='listing-continuation',listing_id='code',code_block_id='code',source_region_id='code-region',last_printed_row=10,next_printed_row=11,next_folio='L',open_source_label='SUB:')
            else:
                boundary=dict(kind='incoming-listing-continuation',listing_id='code',code_block_id='code',source_region_id='code-region',previous_last_printed_row=10,first_printed_row=11,previous_folio='K',previous_package=dict(manifest=specs[0]['manifest']),open_source_label='SUB:')
            c['content_associations'] += [group,boundary]
            fig=c['figure_structures'][0]
            fig.update(axes=[dict(id='axis')],vertical_guides=[dict(id='guide')],solid_dot_positions=[dict(axis_id='axis',guide_id='guide')],legend_label_id='figure:l1',nodes=[dict(node_id='node',label_id='figure:l1')],edges=[dict(edge_id='edge',from_node='node',to_node='node',branch_label_id='figure:l1')])
            fig['nodes'].append(dict(node_id='junction',label_id=None,printed_node=False))
            write_json(base/'program-corrections.json',c)
            original_recipe=json.loads((base/'recipe.json').read_bytes());original_recipe['corrections']=pin(base,'program-corrections.json')
            order=['table','@figure','body','code'] if i==0 else ['code','body','table','@figure']
            original_recipe['content_order']=[dict(type='figure' if id.startswith('@') else 'block',id=id.removeprefix('@')) for id in order]
            write_json(base/'program-recipe.json',original_recipe)
            output=root/'archive/program-segments'/name;build(base/'program-recipe.json',output,root)
            specs.append(dict(name=name,manifest=pin(root,output.relative_to(root).as_posix()+'/manifest.json')))
        recipe.update(index_mode='structured-programs-v1',segments=specs,prose_joins=[],program_links=[dict(id='program',left=dict(segment='a',listing_id='code',last_printed_row=10,association=3),right=dict(segment='b',listing_id='code',first_printed_row=11,association=3))],group_links=[dict(id='joined-sub',program_id='program',left=dict(segment='a',association=2),right=dict(segment='b',association=2))],example_links=[])
        # Existing table/figure relationship requires the updated previous segment pin.
        bbase=root/'archive/inputs/b';c=json.loads((bbase/'program-corrections.json').read_bytes())
        c['content_associations'][1]['from_package']['manifest']=specs[0]['manifest']
        write_json(bbase/'program-corrections.json',c);r=json.loads((bbase/'program-recipe.json').read_bytes());r['corrections']=pin(bbase,'program-corrections.json');write_json(bbase/'program-recipe-2.json',r)
        output=root/'archive/program-segments/b-final';build(bbase/'program-recipe-2.json',output,root);recipe['segments'][1]['manifest']=pin(root,output.relative_to(root).as_posix()+'/manifest.json')
        recipe['example_links']=[dict(id='example-program',source=dict(segment='a',association=0),listing_targets=[dict(segment='a',listing_id='code')],note='Synthetic source example retains its unified program context.')]
        path=root/'archive/program-assembly.json';write_json(path,recipe);return path

    def test_independent_rebuild_unifies_program_and_group_without_changing_bytes(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);path=self.fixture(root);outputs=[root/'work/one',root/'work/two']
            for out in outputs:
                p=assemble(path,out,root);self.assertEqual(check_export(out),p)
                c=json.loads((out/'corrections.json').read_bytes());blocks={r['id']:r for r in p['blocks']}
                self.assertNotIn('b-code',blocks);self.assertEqual(blocks['a-code']['text'],'10 PRINT "한글"\n11 PRINT "한글"\n')
                self.assertEqual(len(c['listing_groups']),1);self.assertEqual(len(c['listing_groups'][0]['source_parts']),2)
                rows=c['listing_line_index'];offset=len('10 PRINT "한글"\n'.encode())
                self.assertEqual([r['listing_id'] for r in rows],['a-code','a-code']);self.assertEqual([r['physical_line'] for r in rows],[1,2]);self.assertEqual(rows[1]['block_start_byte'],offset)
                self.assertEqual(rows[1]['fields'][0]['block_start_byte'],offset+3)
                group=next(r for r in c['content_associations'] if r.get('group_id')=='joined-sub')
                self.assertEqual(group['literal'],blocks['a-code']['text']);self.assertFalse(group['continuation_pending']);self.assertEqual(len(group['source_parts']),2)
                self.assertEqual(c['resolved_groups'][0]['source_label'],'SUB:')
                for row in c['basic_source_fields']:
                    self.assertEqual((out/'listing.txt').read_bytes()[row[S]:row[E]].decode(),'한글')
                    self.assertEqual(blocks[row['block_id']]['text'].encode()[row['start_byte']:row['end_byte']].decode(),'한글')
                a,b=c['figure_structures'];self.assertNotEqual(a['axes'][0]['id'],b['axes'][0]['id'])
                self.assertEqual(a['solid_dot_positions'][0]['axis_id'],a['axes'][0]['id'])
                self.assertEqual(a['legend_label_id'],'a:figure:l1');self.assertEqual(b['edges'][0]['branch_label_id'],'b:figure:l1')
                self.assertEqual(len(c['resolved_programs']),1)
                self.assertEqual(c['resolved_examples'][0]['code_block_ids'],['a-code'])
            files=lambda p:{f.relative_to(p).as_posix():f.read_bytes() for f in p.rglob('*') if f.is_file()}
            self.assertEqual(files(outputs[0]),files(outputs[1]))

    def test_source_boundaries_groups_and_graph_reference_failures_reject(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);path=self.fixture(root);recipe=json.loads(path.read_bytes());segments=[read_segment((root/s['manifest']['path']).parent,s['manifest']) for s in recipe['segments']]
            cases={
                'omit program':lambda r,s:r['program_links'].clear(),
                'omit group':lambda r,s:r['group_links'].clear(),
                'wrong row':lambda r,s:r['program_links'][0]['right'].update(first_printed_row=12),
                'wrong manifest':lambda r,s:s[1][1]['content_associations'][3]['previous_package']['manifest'].update(sha256='0'*64),
                'wrong label':lambda r,s:s[1][1]['content_associations'][2].update(source_label='OTHER:'),
                'wrong folio':lambda r,s:s[0][1]['content_associations'][3].update(next_folio='wrong'),
                'duplicate group':lambda r,s:r['group_links'].append(deepcopy(r['group_links'][0])),
                'bad guide':lambda r,s:s[0][1]['figure_structures'][0]['solid_dot_positions'][0].update(guide_id='missing'),
                'bad branch label':lambda r,s:s[0][1]['figure_structures'][0]['edges'][0].update(branch_label_id='missing'),
                'bad node':lambda r,s:s[0][1]['figure_structures'][0]['edges'][0].update(to_node='missing'),
                'intervening figure':lambda r,s:s[0][0]['content_order'].append(s[0][0]['content_order'].pop(1)),
                'missing first unit':lambda r,s:s[0][1]['logical_listing_line_index'].clear(),
                'bad example target':lambda r,s:r['example_links'][0]['listing_targets'][0].update(listing_id='missing'),
                'duplicate example occurrence':lambda r,s:r['example_links'].append(dict(deepcopy(r['example_links'][0]),id='duplicate')),
            }
            for name,mutate in cases.items():
                r,s=deepcopy(recipe),deepcopy(segments);mutate(r,s)
                with self.subTest(case=name),self.assertRaises(ValueError):project(r,s)

    def test_rehashed_outer_program_projection_is_checked_against_originals(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);path=self.fixture(root);out=root/'work/one';assemble(path,out,root)
            c=json.loads((out/'corrections.json').read_bytes());c['listing_line_index'][1]['fields'][0]['block_start_byte']=3;write_json(out/'corrections.json',c)
            p=json.loads((out/'article.json').read_bytes());p['corrections']=[pin(out,'corrections.json')];write_json(out/'article.json',p)
            manifest=json.loads((out/'manifest.json').read_bytes());manifest['files']=[pin(out,r['path']) for r in manifest['files']];write_json(out/'manifest.json',manifest)
            with self.assertRaisesRegex(ValueError,'correction projection'):check_export(out)


if __name__=='__main__':unittest.main()
