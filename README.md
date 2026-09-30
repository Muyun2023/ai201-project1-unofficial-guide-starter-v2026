# The Unofficial Guide

Muyun Ji · corpus: `city_guides`

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

<!-- Which corpus picked, and the kinds of questions this system answers. Write for someone who has never seen this repo.-->

This system answers practical trip-planning questions about a fictional
region, using the `city_guides` corpus: fourteen travel guides, nine on
individual towns and villages (Kestrelford, Corry Vale, Givens Mill and
others) and five that cover the whole region on eating, walking, transport,
seasons and accessibility. You can ask things like when a town's bakery sells
out, how to get between villages by bus, or which month to visit, and it
answers only from the guides, naming the file each answer came from. If
nothing in the guides is close enough to the question, it says it doesn't
have enough information instead of guessing.

## Chunking Strategy

<!-- What made you pick these numbers? Short posts and long sectioned guides don't want the same chunking, and "800 seemed reasonable" earns nothing. Point at something you noticed when you read
the documents in Milestone 1.
If you changed your mind partway through, say so and say why. That's worth more than pretending you got it right first time.
Milestone 3. -->

**Chunk size:**
app.py index
Corpus: city_guides
  loaded   14 documents, 28,958 characters, ~2,068 characters per document
  chunked  94 chunks, 322 characters on average (shortest 174, longest 762), produced by chunker.py::split_documents
  embedding 94 chunks (first run downloads the model)...
  stored   94 chunks in 4.4s

**Overlap:**
0

The `city_guides` documents are long guides that the author has already
divided into labelled sections (`## Getting there`, `## Eat and drink`,
`## When to go`...), and each section covers one subject. The starter's
800-character windows ignored those boundaries: it made 51 chunks and cut
straight through sections, often mid-sentence. So I cut where the author
did. `split_documents` follows four rules:

1. **Cut before every `## ` heading.** One section, one chunk.
2. **Keep each document's opening part** (the `# H1` title plus any text
   before the first `##`) **as its own chunk.** `guide_corry_vale.md` gives
   its population there and nowhere else, so dropping it would lose that fact.
3. **Drop any part with a heading but no body.** `guide_walking.md`,
   `guide_eating.md` and `guide_seasons.md` go straight from the title to
   the first `##`, which left 23–26 character chunks that could answer
   nothing.
4. **Add the document's `# H1` title to the top of every section chunk.**
   Nine of the fourteen guides use the same section headings, so a chunk
   like "## Eat and drink / A tearoom attached to the mill..." never says
   which place it is about. The title is what tells the search which town
   a section belongs to.

There is no overlap because overlap repairs cuts made in arbitrary places.
These cuts fall where the author put a boundary, so nothing is cut in half.

**Side effect I noticed in Milestone 4:** because every chunk carries its
town name, a question that names a town pulls in that town's unrelated
sections too. "What time does the bakery in Kestrelford sell out?" returned
Kestrelford's "When to go" and "Getting around" in its top 5.

**Known issue:** Rule 2 (keep each document's opening part as its own chunk)
can produce chunks with no facts, e.g. `guide_accessibility.md#0`. I haven't
yet checked how many of the 14 opening chunks are like this. I'm leaving the
rule in place for now and will revisit it in Unit 2.

## Sample Chunks

<!-- Five chunks, pasted as text. Label each one and name the file it came from
     AND the function that produced it — the grader checks your code against
     what you claim here.
     `python app.py chunks -n 5` prints all three for you. Copy them straight
     across.
     Milestone 3. -->

**Chunk 1** — source: `guide_accessibility.md#0` — produced by: `chunker.py::split_documents`

<!--
> ** ！！！My own Note — known weakness！！！** 
This chunk carries no facts. It is the opening
> part of `guide_accessibility.md` (the `# H1` line plus its preamble), which
> `split_documents` keeps as a chunk of its own under rule 2. That rule exists
> because `guide_corry_vale.md` states its population in the preamble and
> nowhere else. Here the preamble is only an introduction, so the chunk can't
> answer a question on its own. At retrieval time it can only act as noise: it
> may match broad questions about accessibility and take a top-k slot from a
> section that actually holds the answer.
>
> **Why I kept it for now:** a fix has to keep the Corry Vale population while
> removing empty preambles like this one. I'd rather make that change after
> Unit 2 shows whether this chunk actually shows up in retrieval results.
>
> **Possible fixes to test later:**
> 1. Merge the opening part into the first `##` section chunk instead of
>    keeping it separate.
> 2. Keep the opening part only if it is longer than a minimum length.
>    The threshold still needs to be checked against the Corry Vale preamble.
-->
```
# Getting around the region with limited mobility

An honest assessment rather than a promotional one. Some of these places are
difficult and it is better to know in advance.

```

**Chunk 2** — source: `guide_corry_vale.md#5` — produced by: `chunker.py::split_documents`

```
# Corry Vale

## Where to stay

Perhaps thirty beds in the entire valley, spread across two pubs and a handful of farmhouse rooms. In summer these are booked months ahead. Camping is permitted on two marked fields and nowhere else.

```

**Chunk 3** — source: `guide_givens_mill.md#2` — produced by: `chunker.py::split_documents`

```
# Givens Mill

## Getting around

Everything is on one street along the river. The mill is at one end and the church at the other, eight minutes apart. The riverside path continues in both directions for as far as you want to walk.

```

**Chunk 4** — source: `guide_kestrelford.md#4` — produced by: `chunker.py::split_documents`

```
# Kestrelford

## What to see

The market square on a Saturday morning is the main event and has run continuously since the 1400s. The parish church has a 13th-century tower you can climb for £2. The old trackbed walk runs six miles to the next village along an easy gradient and is the best half-day here.

```

**Chunk 5** — source: `guide_pellew_sands.md#6` — produced by: `chunker.py::split_documents`

```
# Pellew Sands

## When to go

June and September for the beach without the crowds. July and August are busy and the town is at its most itself, for better and worse. Winter is bleak, largely closed, and has a following among people who like that sort of thing.

```

## Sample Answer

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->

**Question:**
What time does the bakery in Kestrelford sell out?

**Answer:**

```
> The bakery in Kestrelford sells out by 11am.
>
> (Sources: `guide_kestrelford.md` and `guide_eating.md`)
>
> Sources retrieved: guide_eating.md, guide_kestrelford.md

```

**My relevance cutoff:**

<!-- The number you set in config.py, and how you got there.
     You ran five questions your corpus covers and the five in OUT_OF_SCOPE
     that it clearly doesn't, and wrote down the best distance for each. What
     did those two groups look like? Where was the gap? Put the actual numbers
     here — the table below wants all ten rows.
     Milestone 4. -->

**My relevance cutoff:** 0.7

| Question | In corpus? | Best distance |
| -------- | ---------- | ------------- |
| How many people live in the largest village in Corry Vale? | Yes | 0.1637 |
| What time does the bakery in Kestrelford sell out? | Yes | 0.3221 |
| In what year did Marchwood's covered market begin operating? | Yes | 0.3827 |
| Which evening meal is hardest to find across the region...? | Yes | 0.5106 |
| Why can't visitors use one bus ticket across the whole region? | Yes | 0.6374 |
| What is the capital of Mongolia? | No | 0.8026 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.8350 |
| How do I write a for loop in Rust? | No | 0.8365 |
| How do I change the oil in a diesel engine? | No | 0.8881 |
| Who won the 1994 World Cup? | No | 0.9753 |

In-corpus questions landed between 0.16 and 0.64; out-of-scope questions
between 0.80 and 0.98, leaving a gap from 0.64 to 0.80. The starter's
default of 0.6 wrongly refused the bus-ticket question (0.637), even though
the top chunk (guide_regional_transport.md, "Buses") holds the answer. Its
distance is high because the question says "one bus ticket" while the
document says "three operators". I put the cutoff at 0.7, which leaves
about 0.06 of margin below it and 0.10 above. 

The risk: The risk is near-miss questions. "Is there a cinema in Kestrelford?" isn't
covered by the guides, but it scored 0.401, closer than two of my in-corpus
questions, because the place name matches the "# Kestrelford" title on every
chunk. No cutoff could refuse it without also refusing real questions. It
passed the gate, and the grounding instruction caught it: the model said it
didn't have enough information. It still cited guide_kestrelford.md in that
refusal, which I may tighten later.

## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.
     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.
     Milestone 5. -->

**1.** After printing five chunks, I pasted them into Claude and asked
whether each could answer a question on its own. It said chunks 2–5 could,
and pointed out that chunk 1 (`guide_accessibility.md#0`) held only an
introduction and no facts. That chunk comes from my rule 2, which keeps each
document's opening part so the Corry Vale population isn't lost. Claude
suggested either merging the opening part into the first section or keeping
it and documenting the problem. I chose not to change the chunker yet,
because any fix still has to keep the Corry Vale fact, and I'd rather see in
Unit 2 whether this chunk actually shows up in retrieval. I added a note
under the chunk instead.

**2.** When I set the relevance cutoff, Claude helped me read my ten
distances and suggested 0.7, predicting that near-miss questions would land
between 0.6 and 0.8. I tested that with "Is there a cinema in Kestrelford?",
which the guides don't cover. It scored 0.401, closer than two of my real
questions, so the prediction was wrong: no cutoff could stop it. I replaced
that sentence in my README with the measured result, and wrote down that the
grounding instruction, not the gate, is what caught this question.


<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->
---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.
     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.
     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
| --- | --- | --- | --- | --- | --- |
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Chunks are whole sections (heading start, sentence end) | 0 exceptions | 94/94 | 94/94 | 94/94 | MET |
| 5. No-town questions reach the cross-cutting guide | 2 of 2 | 2/2 | 2/2 | 2/2 | MET |

Source: `results/run_2026-09-29_1810_before.md`, produced by `run_eval.py::main`
(top-k 5, cutoff 0.7, 3 runs, caching off). Criteria 1, 3, 4 and 5 depend only
on chunking and retrieval, which are deterministic, so the same number appears
in all three columns. Criterion 2 depends on the generated answer and is the
only one that could vary. The wording changed on every run, which confirms
the cache was off.

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

### Output behind each criterion (Run 1)

**Criteria 1 and 2** — `run_eval.py::main`, from `results/run_2026-09-29_1810_before.md`

```
Q: How many people live in the largest village in Corry Vale?
Best distance: 0.1637 · Sources retrieved: guide_corry_vale.md, guide_walking.md
The largest village in Corry Vale has 900 people (guide_corry_vale.md).
```

**Criterion 3** — `run_eval.py::check_out_of_scope`

```
refused  (best distance 0.803)  What is the capital of Mongolia?
refused  (best distance 0.888)  How do I change the oil in a diesel engine?
refused  (best distance 0.975)  Who won the 1994 World Cup?
refused  (best distance 0.835)  What is the recommended dosage of ibuprofen for a headache?
refused  (best distance 0.836)  How do I write a for loop in Rust?
-> gate refused 5 of 5

python app.py ask "What is the capital of Mongolia?"
I don't have enough information about that.
```

**Criterion 4** — chunks from `chunker.py::split_documents`, checked by `check_chunks.py`

```
94 chunks checked, 0 fail
```

**Criterion 5** — `run_eval.py::main`

```
Q: Why can't visitors use one bus ticket across the whole region?
Best distance: 0.6374 · Sources retrieved: guide_accessibility.md, guide_kestrelford.md, guide_marchwood.md, guide_regional_transport.md
Visitors cannot use one bus ticket across the whole region because there are three different operators running in the region, and they do not accept each other's tickets (guide_regional_transport.md).
```

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
| --- | --- | --- | --- |
| 1 | Retrieved chunk contains the answer (4 of 5) | MET | 5/5 in all three runs. For each question I checked that the expected fact (11am, 1863, Sunday, 900, three operators) appears in a chunk that was retrieved, not just in the answer. The one I flagged as the main risk, the Corry Vale population in the preamble, came back at 0.164, the closest of all five. |
| 2 | Every answer names a source (5 of 5) | MET | All 15 answers name at least one file. The format varied from run to run (`Source:`, `Sources:`, a filename in brackets), but every answer had one. The criterion checks only that a source is named, and one answer shows the gap: in run 3 of the evening-meal question the model added that Corry Vale is a place to get this meal and cited `guide_corry_vale.md`. That file says one pub "serves food seven days a week" and gives no hours, so "Sunday evening" was the model's own inference. The source was named, but the claim goes beyond it. This criterion can't catch that. |
| 3 | Gate stops out-of-corpus questions (4 of 5) | MET | 5/5 refused, closest at 0.803 against a 0.7 cutoff. Each refused question returns exactly "I don't have enough information about that", as the criterion says (checked with `python app.py ask "What is the capital of Mongolia?"`). The two questions I expected to sit closest to the boundary (ibuprofen, diesel) came back at 0.835 and 0.888; the closest was actually Mongolia at 0.803, so the result met the target but my reasoning about which questions were at risk didn't hold. |
| 4 | Chunks are whole sections (no exceptions) | MET | `check_chunks.py` reports 94 chunks checked, 0 fail. This measures format only: `guide_accessibility.md#0` passes but holds no facts. |
| 5 | No-town questions reach the cross-cutting guide (2 of 2) | MET | Both questions retrieved the right document in all three runs: `guide_eating.md` at 0.511 and `guide_regional_transport.md` at 0.637. The second is only 0.063 under my 0.7 cutoff. Under the starter's 0.6, the gate would have refused it: retrieval would still have found the right chunk, but it would never have reached the model. The criterion is met, but by a narrow margin. |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

**No criterion was missed.** All five met their targets in all three runs.
The assignment asks what that means, and I think it means some of my targets
were set too safe: they checked *whether* something happened, not *how
reliably*. I tested one of them further before deciding what to tighten.

### Were my targets too low?

| # | What the test showed | Tightened version |
| --- | --- | --- |
| 1 and 5 | The answer chunk was in the top 5 every time. But for both no-town questions it ranked first by only 0.004 and 0.005, so I tested whether that ranking survives rephrasing (below). It did. | For each question, the chunk holding the answer ranks **first under three different phrasings**. The two narrowest questions pass this (6 of 6). I haven't tested the other three yet. |
| 2 | Every answer named a file, but run 3 of the evening-meal question cited `guide_corry_vale.md` for a claim the file doesn't make. | Every factual claim in an answer appears in the file it cites, 15 of 15. My current system scores 14 of 15. |
| 3 | All five out-of-scope questions sat at 0.80 or higher, far from the cutoff. "Is there a cinema in Kestrelford?", which the guides don't cover, scored 0.401 and passed the gate; the model then declined. | Add five near-miss questions (about the region but not answered by the guides); the system refuses at least 4 of 5, whether the gate or the model does the refusing. Not yet tested beyond the one question. |

**Why rephrasing, not a fixed margin:** I first considered requiring the
answer chunk to lead by a set distance (0.02). There's no standard value for
this, because distances depend on the embedding model. So I measured how much
rephrasing moves them: the same question in three wordings moved the answer
chunk's distance by about 0.05 (bus: 0.595 to 0.647; evening meal: 0.468 to
0.511). A margin smaller than that says little either way. Checking whether
the rank survives rephrasing tests the actual risk directly.

| Question and phrasing | Answer chunk | Rank | Runner-up | Lead |
| --- | --- | --- | --- | --- |
| Bus, original | 0.6374 | 1 | Marchwood opening chunk 0.6416 | 0.004 |
| Bus, "single bus ticket work everywhere" | 0.5946 | 1 | Marchwood opening chunk 0.6599 | 0.065 |
| Bus, "buy one ticket for all the buses" | 0.6472 | 1 | Marchwood "Getting around" 0.6754 | 0.028 |
| Evening meal, original | 0.5106 | 1 | Pellew Sands "Eat and drink" 0.5151 | 0.005 |
| Evening meal, "hardest to get… still served" | 0.5022 | 1 | Pellew Sands "Eat and drink" 0.5180 | 0.016 |
| Evening meal, "difficult to find… still offer it" | 0.4684 | 1 | Corry Vale "Eat and drink" 0.4855 | 0.017 |

### Pattern: chunks match on place and topic, which puts noise in front of the model

Stage: **chunking**, which shapes what **embedding** captures and so what
**retrieval** returns. It then reaches **generation**.

Every chunk starts with `# Place` and `## Section`, and most sections are only
a few sentences long, so a chunk's embedding is carried largely by its place
and topic words. Rephrasing showed the answer chunk still ranks first. The
cost is what comes with it:

- **Same-topic sections crowd the top 5.** For the evening-meal question,
  single-town "## Eat and drink" sections took 2–3 of the top 5 slots under
  every phrasing, always within 0.02 of the answer.
- **Opening chunks get in on title words alone.** `guide_accessibility.md#0`,
  the chunk with no facts I flagged in unit 1, reached the bus question's
  top 5 under two of three phrasings. `guide_marchwood.md`'s opening chunk
  came second under two.
- **Naming a town pulls in that town's chunks.** The bakery question returned
  Kestrelford's "When to go" and "Getting around"; "Is there a cinema in
  Kestrelford?" scored 0.401 though the guides never mention a cinema.

**Where this leads:** Corry Vale's "## Eat and drink" was in the evening-meal
top 5 under all three phrasings, second under one. It says one pub "serves
food seven days a week", with no hours. In run 3 the model turned that into
"you can still get a Sunday evening meal in Corry Vale" and cited the file.
Retrieval kept handing the model a near-miss chunk, and generation filled
the gap: `GROUNDING_INSTRUCTION` says to use only the documents, but it
doesn't forbid inferring beyond them. This is the only wrong claim in 15
answers, and it's the end of the chain above, not a separate problem.

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
