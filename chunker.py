"""
Stage 2 of the pipeline: splitting documents into chunks.

⚠️ THIS IS THE FILE YOU CHANGE IN MILESTONE 3.

`split_documents` below is deliberately plain. It cuts every document into
fixed-size pieces with a fixed overlap and pays no attention to where sentences
or paragraphs end. It works, and it is not good.

On a corpus of short posts it may not cut anything at all: `campus_life` comes
out as 88 documents and 88 chunks, because almost nothing in it reaches 800
characters. That is the baseline, not a bug — Milestone 3 is where you decide
whether one post should stay one chunk.

Your job in Milestone 3 is to replace the *body* of `split_documents` with a
strategy that fits the documents you actually read in Milestone 1. Keep the
name and the shape of what it returns — the rest of the pipeline calls it, and
your README has to name the function that produced your chunks.

If you get stuck for 30 minutes, `fallback_split` is the original. Switch back
to it, write down what you saw, and move on. That's a real observation about
your pipeline, not giving up.
"""

import re
from dataclasses import dataclass

import config
from ingest import Document


@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.

    Keep this function. Milestone 3's stop rule points back at it, and having
    something to compare your own strategy against is useful in unit 2.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks


# A line that opens a level-2 section, e.g. "## Getting around".
_SECTION_BREAK = re.compile(r"\n(?=## )")


def _document_title(text: str) -> str:
    """
    The document's `# H1` line, or "" if it hasn't got one.

    Every guide in city_guides opens with the place or theme it covers —
    `# Brightwater`, `# Eating across the region`. That line is the only thing
    in the file that says which place a section belongs to, so it gets carried
    onto every chunk below.
    """
    first_line = text.lstrip().split("\n", 1)[0].strip()
    return first_line if first_line.startswith("# ") else ""


def _has_body(section: str) -> bool:
    """True if there is anything under the section's heading line."""
    return any(line.strip() for line in section.strip().split("\n")[1:])


def split_documents(documents: list[Document]) -> list[Chunk]:
    """
    Split on Markdown section headings instead of on a character count.

    These documents are sectioned guides: the author already marked where one
    subject ends and the next begins, with `## Getting there`, `## Eat and
    drink` and so on. Cutting at those marks means the boundaries are the
    author's rather than a ruler's, so no chunk starts or ends mid-sentence.

    Four rules, and each one exists because of something in this corpus:

    1. Cut immediately before every `## ` line. One section, one chunk.

    2. Keep the opening part — the `# H1` line plus any preamble above the
       first `## ` — as a chunk of its own. `guide_corry_vale.md` states its
       population there and nowhere else, so a splitter that only recognised
       `## ` would lose that fact entirely.

    3. Drop any part with nothing under its heading. `guide_walking.md`,
       `guide_eating.md` and `guide_seasons.md` go straight from `# H1` to the
       first `## `, which leaves a 23-26 character chunk that is a title and
       no content. It can answer nothing and would only ever be retrieved as
       noise.

    4. Prepend the `# H1` line to every section chunk. On its own, "A tearoom
       attached to the mill..." never names Givens Mill, and nine of the
       fourteen documents have a section with the same heading as it. Carrying
       the title down is what tells the embedding which place the section is
       about — and since it is itself a heading line, the chunk still opens
       with one.

    There is no overlap. Overlap exists to repair cuts made in arbitrary
    places; these cuts are made where the author put a boundary, so there is
    nothing to repair.
    """
    chunks: list[Chunk] = []

    for doc in documents:
        text = doc.text.strip()
        title = _document_title(text)
        index = 0

        for position, section in enumerate(_SECTION_BREAK.split(text)):
            section = section.strip()

            # Rule 3 — a heading with no body is not worth storing.
            if not section or not _has_body(section):
                continue

            # Rule 2 — the opening part already carries the title.
            # Rule 4 — every later section gets it prepended.
            body = section if position == 0 or not title else f"{title}\n\n{section}"

            chunks.append(
                Chunk(
                    text=body,
                    source=doc.source,
                    index=index,
                    produced_by="chunker.py::split_documents",
                )
            )
            index += 1

    return chunks


def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))
