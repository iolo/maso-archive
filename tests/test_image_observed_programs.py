"""Observed program joins retain damaged source labels and immutable downloads."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest

from tests import test_image_scoped_native as native_base
from tools.pdf_restore.assemble import assemble,project,read_segment
from tools.pdf_restore.assembly_observed_programs import project_observations
from tools.pdf_restore.build import build,check_export
from tools.pdf_restore.inventory import pin,write_json

S,E='utf8_byte_start','utf8_byte_end_exclusive'


class ObservedProgramTests(unittest.TestCase):
    def source_fixture(self):
        contexts=[];offset=0
        for name,listing,text,labels in [
            ('a','opening','10 PRINT "한글"\n:065 RETURN\n4215 YS = 0',['10',':065','4215']),
            ('b','ending','4220 FOR I = 1 TO ND\n19420 PRINT "---"',['4220','19420'])]:
            raw=text.splitlines(keepends=True);rows=[];units=[];cursor=0
            for i,(body,label) in enumerate(zip(raw,labels),1):
                id=f'{listing}:r{i}';uid=f'{listing}:u{i}';number=int(label) if label.isdigit() else None
                row=dict(line_id=id,listing_id=listing,block_id='code',region_id='scan',
                    printed_line=number,printed_label=label,text=body,**{S:cursor,E:cursor+len(body.encode())})
                unit=dict(line_id=uid,listing_id=listing,block_id='code',region_id='scan',
                    printed_line=number,printed_label=label,physical_line_ids=[id],physical_reading=body,
                    **{S:cursor,E:cursor+len(body.encode())})
                if number is None:
                    unit.update(line_label_candidates=[':065','1065'],line_number_certified=False)
                rows.append(row);units.append(unit);cursor+=len(body.encode())
            group=dict(listing_id=listing,block_ids=['code'],physical_rows=len(rows),logical_units=len(units),
                complete_in_segment=False,source_version=name,execute_verified=False,
                original_encoded_bytes_verified=False,**{S:0,E:cursor})
            order=([dict(type='figure',id='annotation'),dict(type='block',id='label')] if name=='b' else [])+[dict(type='block',id='code')]
            c=SimpleNamespace(name=name,listing_offset=offset,listing=text.encode(),
                blocks={'code':dict(kind='code',text=text),'label':dict(kind='prose',text='데이터')},
                package=dict(content_order=order),correction=dict(listing_groups=[group],
                    listing_line_index=rows,logical_listing_line_index=units),
                reference=lambda kind,id,name=name:f'{name}:{kind}:{id}',
                source_ref=lambda pointer,name=name:dict(scope=name,pointer=pointer))
            contexts.append(c);offset+=cursor
        boundary=dict(left_printed_label='4215',right_printed_label='4220',separator='\n',
            source_unit_complete=True,evidence='Compared distinct complete source statements.',
            intervening=[dict(segment='b',type='figure',id='annotation'),dict(segment='b',type='block',id='label')])
        spec=dict(program_id='main',fragments=[dict(segment=c.name,listing_id=id,
            first_source_unit_id=f'{id}:u1',last_source_unit_id=f'{id}:u{n}')
            for c,id,n in [(contexts[0],'opening',3),(contexts[1],'ending',2)]],boundaries=[boundary],
            ending=dict(source_unit_id='ending:u2',printed_label='19420',source_unit_complete=True,
                evidence='Final original source row, without an inferred RETURN.'),
            source_extent_complete=True,evidence='Complete observed main listing; no execution claim.')
        return [spec],contexts,b''.join(c.listing for c in contexts)

    def test_literal_reading_retains_damaged_label_and_source_bytes(self):
        specs,contexts,listing=self.source_fixture();before=deepcopy([c.correction for c in contexts])
        program=project_observations(specs,contexts,listing)[0]
        self.assertEqual(program['physical_reading'],contexts[0].listing.decode()+'\n'+contexts[1].listing.decode())
        self.assertIn(':065 RETURN',program['physical_reading']);self.assertNotIn('1065 RETURN',program['physical_reading'])
        self.assertEqual(program['physical_rows'],5);self.assertEqual(program['logical_units'],5)
        self.assertEqual(program['source_fragments'][0]['damaged_source_units'],[
            dict(source_unit_reference='a:logical:opening:u2',printed_label=':065',
                 candidates=[':065','1065'],line_number_certified=False)])
        for f in program['source_fragments']:
            self.assertEqual(listing[f['source_start_byte']:f['source_end_byte']].decode(),f['source_reading'])
            self.assertEqual(program['physical_reading'].encode()[f['reading_start_byte']:f['reading_end_byte']].decode(),f['source_reading'])
        self.assertEqual([c.correction for c in contexts],before)
        self.assertFalse(program['execute_verified']);self.assertFalse(program['original_encoded_bytes_verified'])

    def test_wrong_ownership_boundaries_endings_and_certification_reject(self):
        specs,contexts,listing=self.source_fixture()
        cases={
            'missing boundary':lambda s,c:s[0]['boundaries'].clear(),
            'invented separator':lambda s,c:s[0]['boundaries'][0].update(separator=' '),
            'lost physical newline':lambda s,c:s[0]['boundaries'][0].update(separator=''),
            'wrong literal boundary':lambda s,c:s[0]['boundaries'][0].update(left_printed_label='4210'),
            'split source unit':lambda s,c:s[0]['boundaries'][0].update(source_unit_complete=False),
            'hidden annotation':lambda s,c:s[0]['boundaries'][0]['intervening'].pop(),
            'reordered annotation':lambda s,c:s[0]['boundaries'][0]['intervening'].reverse(),
            'truncated first fragment':lambda s,c:s[0]['fragments'][0].update(first_source_unit_id='opening:u2'),
            'wrong listing':lambda s,c:s[0]['fragments'][0].update(listing_id='other'),
            'invented ending':lambda s,c:s[0]['ending'].update(printed_label='19430'),
            'uncertain extent':lambda s,c:s[0].update(source_extent_complete=False),
            'missing evidence':lambda s,c:s[0].update(evidence=''),
            'reused program':lambda s,c:s.append(deepcopy(s[0])),
            'changed physical count':lambda s,c:c[0].correction['listing_groups'][0].update(physical_rows=2),
            'wrong row ownership':lambda s,c:c[0].correction['logical_listing_line_index'][0]['physical_line_ids'].clear(),
            'shifted source range':lambda s,c:c[0].correction['listing_line_index'][0].update(utf8_byte_end_exclusive=1),
            'inferred damaged digit':lambda s,c:c[0].correction['logical_listing_line_index'][1].update(printed_line=1065),
            'certified damaged label':lambda s,c:c[0].correction['logical_listing_line_index'][1].update(line_number_certified=True),
            'lost uncertainty':lambda s,c:c[0].correction['logical_listing_line_index'][1].pop('line_label_candidates'),
            'execution inferred':lambda s,c:c[0].correction['listing_groups'][0].update(execute_verified=True),
            'encoded bytes inferred':lambda s,c:c[0].correction['listing_groups'][0].update(original_encoded_bytes_verified=True),
        }
        for fault,change in cases.items():
            a,b=deepcopy(specs),deepcopy(contexts);change(a,b)
            with self.subTest(fault=fault),self.assertRaises(ValueError):project_observations(a,b,listing)

    def test_physical_continuations_remain_one_unit_across_regions(self):
        specs,contexts,listing=self.source_fixture();c=contexts[1];rows=c.correction['listing_line_index'];units=c.correction['logical_listing_line_index']
        # A physical row may live in another region and continue the same unit.
        first='4220 FOR I = 1\n';continuation='     TO ND';c.listing=(first+continuation).encode();c.blocks['code']['text']=first+continuation
        rows[0].update(text=first,**{E:len(first.encode())})
        rows[1].update(region_id='other-scan',printed_line=None,printed_label=None,text=continuation,**{S:len(first.encode()),E:len(c.listing)})
        units[0]['physical_line_ids'].append(rows[1]['line_id']);units[0]['physical_reading']=first+continuation;units[0][E]=len(c.listing)
        units.pop();c.correction['listing_groups'][0]['logical_units']=1
        c.correction['listing_groups'][0][E]=len(c.listing);listing=contexts[0].listing+c.listing
        specs[0]['fragments'][1]['last_source_unit_id']='ending:u1';specs[0]['ending'].update(source_unit_id='ending:u1',printed_label='4220')
        program=project_observations(specs,contexts,listing)[0]
        self.assertEqual(program['physical_rows'],5);self.assertEqual(program['logical_units'],4)
        self.assertEqual(len(program['source_fragments'][1]['physical_line_references']),2)

    def indexed_row_fixture(self):
        specs, contexts, listing = self.source_fixture()
        specs[0]['source_layout'] = 'indexed-physical-rows-v1'
        for context in contexts:
            group = context.correction['listing_groups'][0]
            group.pop(S); group.pop(E); group['complete_in_segment'] = True
            by_id = {r['line_id']: r for r in context.correction['listing_line_index']}
            for unit in context.correction['logical_listing_line_index']:
                unit.pop('physical_reading')
                unit['segments'] = []
                for id in unit['physical_line_ids']:
                    row = by_id[id]
                    row.update(source_unit_id=unit['line_id'], scan=dict(path=context.name+'.png', sha256='0'*64, bytes=1))
                    unit['segments'].append(dict(region_id=row['region_id'], scan=deepcopy(row['scan']),
                                                 **{S:row[S], E:row[E]}))
        return specs, contexts, listing

    def test_indexed_rows_preserve_immutable_sources_without_duplicate_readings(self):
        specs, contexts, listing = self.indexed_row_fixture()
        before = deepcopy([c.correction for c in contexts])
        program = project_observations(specs, contexts, listing)[0]
        self.assertEqual(program['source_layout'], 'indexed-physical-rows-v1')
        self.assertEqual(program['physical_reading'], contexts[0].listing.decode()+'\n'+contexts[1].listing.decode())
        self.assertEqual([c.correction for c in contexts], before)
        self.assertFalse(program['original_encoded_bytes_verified'])

    def test_indexed_row_contract_rejects_lost_source_binding_and_contradictions(self):
        cases = {
            'missing opt-in': lambda s,c:s[0].pop('source_layout'),
            'unknown layout': lambda s,c:s[0].update(source_layout='anything'),
            'partial bounds': lambda s,c:c[0].correction['listing_groups'][0].update({S:0}),
            'contradictory bounds': lambda s,c:c[0].correction['listing_groups'][0].update({S:0,E:1}),
            'contradictory reading': lambda s,c:c[0].correction['logical_listing_line_index'][0].update(physical_reading='different'),
            'missing source segments': lambda s,c:c[0].correction['logical_listing_line_index'][0].pop('segments'),
            'changed source scan': lambda s,c:c[0].correction['logical_listing_line_index'][0]['segments'][0]['scan'].update(path='foreign.png'),
            'wrong row unit': lambda s,c:c[0].correction['listing_line_index'][0].update(source_unit_id='wrong'),
            'incomplete fragment': lambda s,c:c[0].correction['listing_groups'][0].update(complete_in_segment=False),
        }
        for fault, change in cases.items():
            specs, contexts, listing = self.indexed_row_fixture(); change(specs, contexts)
            with self.subTest(fault=fault), self.assertRaises(ValueError):
                project_observations(specs, contexts, listing)

    def export_fixture(self,root, *, indexed_rows=False):
        path=native_base.ScopedNativeTests().fixture(root);recipe=json.loads(path.read_bytes())
        recipe['source_index_mode']='scoped-observations-v1'
        for join in recipe['prose_joins']:join['intervening']=[]
        specs=[];sources=[]
        for name in ('a','b'):
            folder=root/'archive/inputs'/name;c=json.loads((folder/'native-corrections.json').read_bytes());r=json.loads((folder/'native-recipe.json').read_bytes())
            c['coverage']=dict(article_extent_verified=True,source_pages_missing=False,
                article_actual_folios=['K','L'],included_actual_folios=['K' if name=='a' else 'L'],
                deferred_actual_folios=['L'] if name=='a' else [],prior_native_actual_folios=[] if name=='a' else ['K'])
            group=c['listing_groups'][0];group.update(complete_in_segment=False,physical_rows=1,logical_units=1,original_encoded_bytes_verified=False,source_version=name,download='listing.txt')
            group.update({S:c['listing_line_index'][0][S],E:c['listing_line_index'][-1][E]})
            unit=c['logical_listing_line_index'][0];unit['physical_reading']=c['listing_line_index'][0]['text']
            if indexed_rows:
                group.pop(S); group.pop(E); group['complete_in_segment'] = True
                unit.pop('physical_reading')
                own = [r for r in c['listing_line_index'] if r['line_id'] in unit['physical_line_ids']]
                for row in own:
                    row['source_unit_id'] = unit.get('line_id', unit.get('source_unit_id'))
                unit['segments'] = [dict(region_id=row['region_id'], scan=deepcopy(row['scan']),
                                         **{S:row[S], E:row[E]}) for row in own]
            write_json(folder/'observed-corrections.json',c);r['corrections']=pin(folder,'observed-corrections.json');write_json(folder/'observed-recipe.json',r)
            output=root/'archive/observed-segments'/name;build(folder/'observed-recipe.json',output,root)
            spec=dict(name=name,manifest=pin(root,output.relative_to(root).as_posix()+'/manifest.json'));specs.append(spec);sources.append(read_segment(output,spec['manifest']))
        recipe['segments']=specs;order=[dict(segment=n,**v) for n,(p,c) in zip(('a','b'),sources) for v in p['content_order']]
        a=order.index(dict(segment='a',type='block',id='code'));z=order.index(dict(segment='b',type='block',id='code'))
        recipe['observed_programs']=[dict(program_id='main',fragments=[dict(segment=n,listing_id='code',first_source_unit_id=c['logical_listing_line_index'][0].get('line_id',c['logical_listing_line_index'][0].get('source_unit_id')),last_source_unit_id=c['logical_listing_line_index'][0].get('line_id',c['logical_listing_line_index'][0].get('source_unit_id'))) for n,(p,c) in zip(('a','b'),sources)],boundaries=[dict(left_printed_label='10',right_printed_label='10',separator='',source_unit_complete=True,intervening=order[a+1:z],evidence='Synthetic original complete source rows with existing newline.')],ending=dict(source_unit_id=sources[1][1]['logical_listing_line_index'][0]['line_id'],printed_label='10',source_unit_complete=True,evidence='Synthetic source ending.'),source_extent_complete=True,evidence='Observed source versions differ; original native scopes stay unchanged.')]
        if indexed_rows:
            recipe['observed_programs'][0]['source_layout'] = 'indexed-physical-rows-v1'
        write_json(path,recipe);return path,recipe,sources

    def test_indexed_rows_export_rebuild_and_standalone_check(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);path,recipe,sources=self.export_fixture(root,indexed_rows=True)
            before=deepcopy(sources);outputs=[]
            for name in ('one','two'):
                out=root/'work'/name;outputs.append(out);package=assemble(path,out,root)
                self.assertEqual(check_export(out),package)
                correction=json.loads((out/'corrections.json').read_bytes())
                self.assertEqual(correction['observed_programs'][0]['source_layout'],'indexed-physical-rows-v1')
                for field,records in correction['native_indexes'].items():
                    self.assertEqual([(v['scope'],v['value']) for v in records],
                                     [(n,v) for n,(p,c) in zip(('a','b'),sources) for v in c.get(field,[])])
            files=lambda p:{f.relative_to(p).as_posix():f.read_bytes() for f in p.rglob('*') if f.is_file()}
            self.assertEqual(files(outputs[0]),files(outputs[1]));self.assertEqual(sources,before)

    def test_independent_exports_and_original_native_scopes_stay_exact(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);path,recipe,sources=self.export_fixture(root);before=deepcopy(sources);outputs=[]
            for name in ('one','two'):
                out=root/'work'/name;outputs.append(out);package=assemble(path,out,root);self.assertEqual(check_export(out),package)
                c=json.loads((out/'corrections.json').read_bytes());self.assertEqual(len(c['observed_programs']),1)
                self.assertEqual((out/'listing.txt').read_bytes(),b''.join((root/s['manifest']['path']).parent.joinpath('listing.txt').read_bytes() for s in recipe['segments']))
                for field,records in c['native_indexes'].items():self.assertEqual([(v['scope'],v['value']) for v in records],[(n,value) for n,(p,source) in zip(('a','b'),sources) for value in source.get(field,[])])
            files=lambda p:{f.relative_to(p).as_posix():f.read_bytes() for f in p.rglob('*') if f.is_file()}
            self.assertEqual(files(outputs[0]),files(outputs[1]));self.assertEqual(sources,before)

    def test_legacy_mode_and_ambiguous_contracts_reject(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);path,recipe,sources=self.export_fixture(root)
            for fault in ('legacy-mode','both-contracts','unknown-field'):
                r=deepcopy(recipe)
                if fault=='legacy-mode':r['source_index_mode']='scoped-native-v1'
                elif fault=='both-contracts':r['program_links']=[]
                else:r['observed_programs'][0]['invented']=True
                with self.subTest(fault=fault),self.assertRaises(ValueError):project(r,sources)

    def test_rehashed_program_reading_and_binding_tampering_reject(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);path,recipe,sources=self.export_fixture(root)
            for fault in ('reading','binding'):
                out=root/'work'/fault;assemble(path,out,root);c=json.loads((out/'corrections.json').read_bytes());program=c['observed_programs'][0]
                if fault=='reading':program['physical_reading']+='RETURN'
                else:program['source_fragments'][0]['source_start_byte']+=1
                write_json(out/'corrections.json',c);p=json.loads((out/'article.json').read_bytes());p['corrections']=[pin(out,'corrections.json')];write_json(out/'article.json',p);m=json.loads((out/'manifest.json').read_bytes());m['files']=[pin(out,f['path']) for f in m['files']];write_json(out/'manifest.json',m)
                with self.subTest(fault=fault),self.assertRaisesRegex(ValueError,'correction projection'):check_export(out)


if __name__=='__main__':unittest.main()
