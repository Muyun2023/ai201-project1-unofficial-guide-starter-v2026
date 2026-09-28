# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**

Two of my five questions are near-certain. The bakery closing time and the
1863 market date each sit in one clearly named town guide, and the question
names the town, so retrieval has an easy target. The other three are not:
two name no town at all and have to beat nine single-town `## Eat and drink`
or bus sections to reach the cross-cutting guide that holds the answer, and
the fifth asks for a population figure that sits in the preamble of
`guide_corry_vale.md`, above the first `##` heading. That last one is the
reason I am not claiming 5 of 5: once I split on headings, a preamble with no
`##` of its own is the piece most likely to be attached to the wrong chunk or
dropped altogether, and I would rather name the risk now than discover it in
unit 2. So 4 of 5 means I expect at most one of my three hard questions to
fail, not that I am leaving myself an easy one.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**

Unlike criterion 1, this one does not depend on my corpus or my chunking at
all, which is why it is the one place I will not allow a single miss.
`build_prompt` in `generate.py` labels every excerpt it sends as
`[from <filename>]`, and `GROUNDING_INSTRUCTION` tells the model in as many
words to name the document its answer came from. The filename is therefore
always in front of the model. For an answer to arrive without a source, the
model would have to ignore an explicit instruction about information it was
handed — and if that can happen even once in five, the instruction is not
doing its job and I want to know, rather than having averaged it away. I have
already seen the mechanism work: my first end-to-end question came back with
"Source: `guide_brightwater.md`", and it volunteered the second document the
same fact appeared in. Refusals are not counted here, since a refusal is not
an answer.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

**Why this target:**

I am writing this before Milestone 4, so I have one measurement and an
expectation. The measurement: an in-corpus question came back at distance
0.302 against the shipped cutoff of 0.6, which suggests real matches sit well
below the line and leaves room for a gap. The expectation: three of the five
`OUT_OF_SCOPE` questions — the capital of Mongolia, the 1994 World Cup, a for
loop in Rust — share no vocabulary and no subject with a regional travel
guide, so they should land far above any cutoff I could reasonably pick. The
other two worry me, and they are why this says 4 of 5 and not 5 of 5. Every
one of my documents ends with a `## Practical notes` section naming a minor
injuries unit and the nearest hospital, which gives the ibuprofen question
something medical to be near; and every town guide has a `## Driving` section
about road surfaces and single-track approaches, which gives the diesel
engine question something vehicular to be near. Those are the two I expect to
sit closest to the boundary, so allowing one failure is an honest allowance
for a specific overlap I can point at, not padding.

---

## 4. Chunks are whole sections, not fragments
Every chunk begins with a Markdown heading line and ends with a
sentence-ending mark (`.`, `?`, or `!`). No exceptions.

**Why this target:**
These documents are Markdown town guides whose author already divided them
into labelled sections — `## Getting there`, `## Eat and drink`, and so on.
Splitting on those headings means the chunk boundaries are the author's, not
a character count's. If a chunk does not start with a heading, it did not come
from a heading boundary — that is a bug in the splitter, not bad luck, so the
right allowance is zero rather than "a few". The baseline chunker shows what
the alternative costs: it ended a chunk of `guide_accessibility.md` at
"The station is a 15-", opened a chunk of `guide_givens_mill.md` with
"nd drink", and produced a shortest chunk of 24 characters.

I know this target is not free. Splitting the corpus on headings gives 98
chunks, and three of them — the opening lines of `guide_walking.md`,
`guide_eating.md` and `guide_seasons.md` — are an `# H1` line with no body
underneath it, because those three documents go straight from the title to the
first `##`. A heading with nothing under it ends in a letter, not a full stop,
so it fails this criterion, and it deserves to: it cannot answer anything and
would only ever be retrieved as noise. Keeping the allowance at zero is what
forces the splitter to deal with them rather than ship them.

---

## 5. Questions that name no town still reach the cross-cutting guide

For both of my test questions that name no town — "Which evening meal is
hardest to find across the region, and where can you still get it?" and
"Why can't visitors use one bus ticket across the whole region?" — the
retrieved chunks include one from the document that actually holds the
answer: `guide_eating.md` and `guide_regional_transport.md` respectively.
2 of 2.

**Why this target:**

Nine of my fourteen documents are single-town guides, and every one of them
has a `## Eat and drink` section. A question about finding a meal therefore
has nine plausible-looking competitors before it reaches `guide_eating.md`,
which is the only document that says Sunday evening is the hard meal. Buses
are the same shape: each town guide describes its own service, and only
`guide_regional_transport.md` explains that three operators refuse each
other's tickets. I wrote both questions without a town name deliberately, to
take away the shortcut of matching a place name, so this criterion measures
retrieval rather than keyword luck. The target is 2 of 2 because the group
only has two questions in it — allowing one failure would mean accepting a
50% hit rate on exactly the case I built these questions to test.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
