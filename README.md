# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.
A RAG (Retrieval-Augmented Generation) system that makes student-generated 
off-campus housing knowledge searchable and answerable for UDC students.
---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->
     Off-campus housing experiences for UDC students near Van Ness, Tenleytown, 
Connecticut Ave, and Albemarle Street in Washington DC. This knowledge is 
valuable because official UDC channels only cover on-campus housing. Students 
traditionally rely on word-of-mouth, Reddit, and Google Reviews — this system 
makes that scattered knowledge instantly searchable.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | van_ness_apartments.txt | Student review of Van Ness area apartments| |
| 2 | tenleytown_housing.txt| Review of Tenleytown area housing | |
| 3 | reddit_udc_housing_1.txt| Reddit post about off-campus living near Van Ness | |
| 4 |  reddit_udc_housing_2.txt| Reddit thread about UDC off-campus housing| |
| 5 | google_review_van_ness_1.txt| Google review of Van Ness apartment complex | |
| 6 |google_review_tenleytown_1.txt  | Google review of Tenleytown housing| |
| 7 | housing_tips_udc.txt| Student housing tips shared on Discord| |
| 8 |connecticut_ave_review.txt | Review of Connecticut Avenue apartments | |
| 9 | albemarle_street_housing.txt|  Student review of Albemarle Street housing| |
| 10 | udc_housing_facebook_group.txt|Facebook group posts about UDC housing | |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size: 300 characters**

**Overlap:50 characters**

**Why these choices fit your documents:The documents are short reviews (1-3 sentences each). 300 characters captures 
one complete thought without merging unrelated topics. The 50-character overlap 
prevents key facts from being split across chunk boundaries.**

**Final chunk count:19 chunks across 10 documents**

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used: All-MiniLM-L6-v2 via sentence-transformers (runs locally, no API key).**

**Production tradeoff reflection:- Cost: local models are free; OpenAI embeddings cost per token
- Context length: all-MiniLM-L6-v2 handles 256 tokens; larger models handle more
- Multilingual: would need a multilingual model for non-English student reviews
- Accuracy: larger models like text-embedding-3-large would improve retrieval 
  quality at higher cost and latency
**

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:Answer the user's question using ONLY the document excerpts provided below. 
Do not draw on outside knowledge. Always mention which source document the 
answer comes from. If the answer is not in the provided documents, say clearly: 
I don't have enough information in my documents to answer that.**

**How source attribution is surfaced in the response:The LLM is instructed to name the source document in its response 
text, and the Gradio interface displays a separate Sources field that 
programmatically lists the filename of every retrieved chunk.**

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What are apartments like near Van Ness? | Close to UDC metro, management issues, ~$1800/month | Described location, management issues, noise — cited van_ness_apartments.txt | Relevant | Accurate |
| 2 | When should I start looking for housing near UDC? | February for fall semester | Correctly stated February, apartments go fast — cited housing_tips_udc.txt | Relevant | Accurate |
| 3 | What is the best restaurant in DC? | System should decline | Declined, explained documents only cover housing | Relevant | Accurate |
| 4 | Are there any mold or maintenance problems? | Mold reports on Connecticut Ave | Cited mold on Connecticut Ave and security deposit issues | Relevant | Accurate |
| 5 | How much does it cost to rent near UDC? | $1500-$2200 depending on area | Correctly cited $1500-$2200 range across multiple sources | Relevant | Accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:** "What is the best restaurant in DC?"

**What the system returned:** Correctly declined to answer, but still 
retrieved 3 housing chunks before deciding — sources field showed 
van_ness_apartments.txt and others even though none were relevant.

**Root cause (tied to a specific pipeline stage):** Retrieval stage issue. 
The retriever always returns top-4 chunks with no distance threshold filter. 
Out-of-scope queries still consume retrieval resources even when all matches 
are weak.

**What you would change to fix it:** Add a distance threshold in retrieve() 
— if all chunks have cosine distance above 0.6, return empty list. The 
generator already handles empty lists correctly with a refusal message.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:** Writing the chunk size 
(300) and overlap (50) in planning.md before coding made ingest.py 
straightforward to implement. There were no decisions to make mid-coding — 
I just translated the spec directly into the sliding window loop.

**One way your implementation diverged from the spec, and why:** The spec 
did not anticipate that only 19 chunks would be produced from 10 short 
documents. In hindsight the spec should have estimated chunk count based 
on actual document length. Smaller 150-character chunks might have produced 
more granular retrieval.
---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**
- *What I gave the AI:* The Chunking Strategy section of planning.md 
  (chunk size 300, overlap 50) and the list of 10 .txt document filenames.
- *What it produced:* ingest.py with load_documents() and chunk_document() 
  using a sliding window of 300 characters with 50-character overlap.
- *What I changed or overrode:* Verified output produced 19 chunks and 
  confirmed content was readable. No changes needed.

**Instance 2**
- *What I gave the AI:* The grounding requirement (answer only from retrieved 
  documents, cite sources) and Gradio interface requirement (Answer + Sources fields).
- *What it produced:* generator.py with grounding system prompt and app.py 
  with Gradio UI.
- *What I changed or overrode:* Tested by asking an out-of-scope question 
  to confirm grounding worked. System declined correctly with no changes needed.