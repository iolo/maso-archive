"""Shared CD1 source recovery and conservative, source-bound block decisions."""
from copy import deepcopy
import re

from tools import inventory_cd1_rtf as inventory
from tools import map_cd1_blocks as blocks
from tools import recover_cd1_text as recovery
from tools.decode_cd1_paragraph import digest
from tools.map_cd1_topic import require


def inherited_states(raw, offsets):
    """Snapshot scoped formatting at requested byte boundaries, including across pages.

    This scanner only tracks state, never extracts visible text. Unknown visible
    formatting taints the snapshot until a full plain/pard reset. The full topic
    inventory/decoder remains responsible for every byte of selected content.
    """
    offsets = sorted(set(offsets))
    if not offsets:
        return {}
    state = {'character': recovery.reset_character(), 'paragraph': {}, 'unknown': []}
    stack, snapshots, index, skip = [], {}, 0, 0
    pattern = rb"\\'[0-9a-fA-F]{2}|\\([a-zA-Z]+)(-?\d+)? ?|\\[^a-zA-Z]|[{}]"
    for match in re.finditer(pattern, raw):
        if match.start() < skip:
            continue
        while index < len(offsets) and offsets[index] <= match.start():
            snapshots[offsets[index]] = deepcopy(state)
            index += 1
        if index == len(offsets):
            break
        token, word, value = match[0], match[1], match[2]
        if token == b'{':
            stack.append(deepcopy(state))
        elif token == b'}':
            require(bool(stack), 'Unbalanced RTF inheritance')
            state = stack.pop()
        elif word:
            word, value = word.decode(), int(value) if value else None
            if word == 'bin':
                require(value is not None and value >= 0, 'Invalid binary length')
                skip = match.end() + value
            elif word == 'plain':
                state['character'] = recovery.reset_character()
                state['unknown'] = [x for x in state['unknown'] if x != 'plain_reset_seen'] + ['plain_reset_seen']
            elif word == 'pard':
                state['paragraph'] = {}
                if 'plain_reset_seen' in state['unknown']:
                    state['unknown'] = []
            elif word in ('f', 'fs'):
                state['character']['font_id' if word == 'f' else 'fs'] = value
            elif word in ('b', 'ul'):
                state['character'][word] = value != 0
                if word == 'ul' and 'underline_style' in state['character']:
                    state['character']['underline_style'] = 'single' if value != 0 else 'none'
            elif word == 'uldb':
                state['character']['ul'] = value != 0
                state['character']['underline_style'] = 'double' if value != 0 else 'none'
            elif word == 'tx':
                state['paragraph'].setdefault('tab_stops', []).append(value)
            elif word in ('sl', 'li', 'ri', 'sa', 'sb', 'fi'):
                state['paragraph'][word] = value
            elif word in ('qr', 'keepn'):
                state['paragraph'][word] = value != 0
            elif len(stack) == 1 and word not in ('rtf', 'ansi', 'deff', 'deflang', 'par', 'page', 'tab'):
                state['unknown'] = [x for x in state['unknown'] if x != 'plain_reset_seen'] + [word]
    while index < len(offsets):
        snapshots[offsets[index]] = deepcopy(state)
        index += 1
    for snapshot in snapshots.values():
        snapshot['unknown'] = sorted(set(snapshot['unknown']) - {'plain_reset_seen'})
    return snapshots


def fixed_pitch(paragraph):
    return bool(paragraph['text'].strip()) and bool(paragraph['runs']) and all(
        r['kind'] == 'text' and r['format']['font_id'] == 15 for r in paragraph['runs'])


def map_blocks(article, profile=None, source_metadata=None):
    overrides = {(d['topic'], d['first']): d for d in (profile or {}).get('decisions', [])}
    result = {'schema_version': 1, 'cd_reference': article['cd_reference'], 'blocks': [],
              'relationships': (profile or {}).get('relationships', []),
              'verification': {'semantic_structure_verified': False}}
    used = set()
    for topic in article['topics']:
        paragraphs, ordinal = topic['paragraphs'], topic['ordinal']
        index, parent, last_heading_level = 1, None, 0
        while index <= len(paragraphs):
            paragraph = paragraphs[index - 1]
            declaration = overrides.get((ordinal, index))
            if declaration:
                used.add((ordinal, index))
            end = declaration['last'] if declaration else index
            require(index <= end <= len(paragraphs), 'Decision exceeds topic')
            automatic = {}
            if not profile and fixed_pitch(paragraph):
                # Keep contiguous fixed-pitch material preformatted, including its
                # internal blank lines. Code/table/terminal semantics await review.
                scan = index
                while scan < len(paragraphs):
                    candidate = paragraphs[scan]
                    if fixed_pitch(candidate):
                        end = scan + 1
                    elif candidate['text'].strip() or candidate['runs']:
                        break
                    scan += 1
                automatic = {'kind': 'code', 'decision': {'basis': 'contiguous_Fixedsys_source_runs',
                             'review_concerns': ['semantic_review_pending', 'fixed_pitch_layout_not_language_identification']}}
            elif not profile:
                level = blocks.heading_level(paragraph)
                visible = ''.join(r['text'] for r in paragraph['runs'] if r['kind'] == 'text').strip()
                if source_metadata and visible == source_metadata['title']:
                    automatic = {'kind': 'title'}
                elif source_metadata and index == 1 and source_metadata['opening_page'].get('label') and visible == source_metadata['opening_page']['label']:
                    automatic = {'kind': 'issue_label'}
                elif re.match(r'^글\s*/', visible):
                    automatic = {'kind': 'byline'}
                elif level and level <= last_heading_level + 1:
                    automatic = {'kind': 'heading', 'heading_level': level, 'parent_heading_id': None}
            members = paragraphs[index - 1:end]
            # Without a reviewed profile, structure is explicitly uncertain. A
            # whitespace-only paragraph is the only semantic inference made here.
            default = 'paragraph' if profile else 'unresolved'
            kind = default if paragraph['text'].strip() else 'spacing'
            block = {'id': f"cd1-{article['cd_reference']}:T{ordinal}:P{index:03d}-{end:03d}",
                     'topic_ordinal': ordinal, 'kind': kind, 'parent_heading_id': parent,
                     'decision': {'basis': 'source_paragraph', 'review_concerns': [] if profile else ['semantic_review_pending']}}
            block.update(automatic)
            if declaration:
                block.update(deepcopy(declaration['properties']))
            block.update(members=[{'paragraph_ordinal': p['ordinal'], 'run_ordinals': list(range(1, len(p['runs']) + 1)),
                                   'source_span': p['source_span']} for p in members],
                         source_span={'byte_offset': members[0]['source_span']['byte_offset'],
                                      'end_exclusive': members[-1]['source_span']['end_exclusive']},
                         content_sha256=digest(recovery.topic_text({'paragraphs': members}).encode()),
                         object_refs=[{'paragraph_ordinal': p['ordinal'], 'run_ordinal': n, 'resource': r['object']['resource'],
                                       'rtf_byte_offset': r['object']['byte_offset']} for p in members for n, r in enumerate(p['runs'], 1) if r['kind'] == 'object'])
            if declaration:
                require(block['content_sha256'] == declaration['content_sha256'], 'Source-bound decision text changed')
            if kind == 'heading' or block['kind'] == 'heading':
                parent = block['id']
                last_heading_level = block['heading_level']
            result['blocks'].append(block)
            index = end + 1
    require(used == set(overrides), 'Unused/overlapping source decisions')
    blocks.validate_map(article, result)
    return result
