"""
Checks criterion 4: every chunk begins with a Markdown heading line
and ends with a sentence-ending mark (. ? !). No exceptions.
"""
from ingest import load_documents
from chunker import split_documents

chunks = split_documents(load_documents())
bad = [c for c in chunks
       if not c.text.lstrip().startswith('#')
       or not c.text.rstrip().endswith(('.', '?', '!'))]

print(f'{len(chunks)} chunks checked, {len(bad)} fail')
for c in bad:
    print('---', c.label)
    print('START:', repr(c.text[:60]))
    print('END:  ', repr(c.text[-60:]))