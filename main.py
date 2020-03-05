import json
import re
import yaml
from htmldom import htmldom

ATTRS = {
    'href': (r"""<a\s+(?:[^>]*?\s+)?href=(["'])(.*?)\1""", 2),
}

spec = yaml.safe_load(open('spec.yaml'))

page = htmldom.HtmlDom(spec['youtube']['base_url']).createDom()

parsed = []
for r in spec['youtube']['items']:
    selector = spec['youtube']['items'][r].split('|')
    sequences = selector[1:] if len(selector) > 1 else []
    selector = selector[0]
    items = page.find(selector)
    _parsed = []
    for item in items:
        attr = re.match('\[(\S*)\]', selector)
        if attr:
            if attr[1].lower() in ATTRS.keys():
                _parsed.append(re.match(ATTR[attr[1]][0], item.html())[ATTR[attr[1]])
            else:
                # not supported attr
                pass
        else:
            i = item.text()
            for attr in sequences:
                i = eval(f'i.{attr}')
            _parsed.append(i)
    parsed.append(_parsed)

_parsed = []
parsed = list(zip(*parsed))
for prsd in parsed:
    row = {}
    for i, d in enumerate(spec['youtube']['items'].keys()):
        row[d] = prsd[i]
    _parsed.append(row)

with open('youtube_parsed.json', 'w') as f:
    f.write(json.dumps(_parsed, indent=4))
