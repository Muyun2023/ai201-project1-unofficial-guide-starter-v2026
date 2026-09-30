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

"""
check_chunks.py — test tool for criterion 4 in criteria.md.

Criterion 4: every chunk begins with a Markdown heading line and ends
with a sentence-ending mark (. ? !). No exceptions.

WHY THIS FILE EXISTS
1. Evidence. The README's run log reports "94 chunks checked, 0 fail"
   for criterion 4. The other criteria are backed by run_eval.py, which
   is in the repo. This result first came from a one-off command typed
   in the terminal, which left nothing behind. Saving the check here
   means anyone can read exactly what rule was applied and re-run it to
   get the same result.

2. Re-testing. Unit 2 Milestone 4 re-runs every criterion after the
   improvement. If the improvement changes chunking, criterion 4 has to
   be checked again, and it has to be checked by the SAME rule as
   before, or the before/after comparison means nothing. Running this
   file guarantees the rule stays identical.

WHY THIS IS NOT A CHANGE TO THE SYSTEM
Unit 2 allows only one change to the system: the improvement. This file
only reads the output of chunker.py::split_documents. Nothing in the
pipeline (app.py, ingest, chunker, store, gate, generate) imports or
calls it, so it can't change any answer the system gives. It is a
measuring tool, like run_eval.py, not part of the thing being measured.

USAGE
    python check_chunks.py
Prints how many chunks were checked and how many failed, then the start
and end of each failing chunk.
"""