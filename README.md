# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

A user types a request like "vintage graphic tee under $30, size M". FitFindr searches a set of secondhand listings, picks the best match, suggests one or two outfits that pair it with pieces from the user's wardrobe, and writes a short caption they could post about the find. If nothing matches, it tells the user what to change instead of guessing.


---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:** Searches the listings file by keyword and ranks the matches, optionally filtering by size and max price.
- **Inputs:** `description` (str), `size` (str or None), `max_price` (float or None)
- **Returns:** A list of listing dicts, each with id, title, description, category, style_tags, size, condition, price, colors, brand, platform.
- **When it has nothing:** Returns an empty list `[]`, never None.
- **How it ranks:** Keyword match over title, description, category, style tags, colors, and brand, with extra weight for title matches. Price only breaks ties. A size like "M" also matches combined sizes such as "S/M".

### `suggest_outfit`

- **What it does:** Uses the model to suggest outfits that pair the new item with the user's wardrobe.
- **Inputs:** `new_item` (dict, one listing), `wardrobe` (dict with key "items" holding a list of wardrobe item dicts)
- **Returns:** A str of outfit ideas.
- **When it has nothing:** If `wardrobe["items"]` is an empty list, returns a str of general styling advice for the item.

### `create_fit_card`

- **What it does:** Uses the model to write a short caption someone would post.
- **Inputs:** `outfit` (str), `new_item` (dict, one listing)
- **Returns:** A str caption.
- **When it has nothing:** If `outfit` is empty, returns a short caption written from `new_item` alone.

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:** If search_listings returns an empty list, put a message in session["error"] naming what to change (size, price, or keywords), leave session["fit_card"] as None, and stop. Otherwise set session["selected_item"] to the first result and call suggest_outfit.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:**  Regex, in agent.py::_parse_query. One pattern finds a price after words like "under", "below", or "up to" (falling back to any $ amount). Another finds "size" followed by a word. Whatever text is left becomes the description. 

**What moves through the session:** query → parsed (description, size, max_price) → search_results → selected_item (first result) → outfit_suggestion → fit_card. On an empty search, error is set and the run stops, so selected_item, outfit_suggestion, and fit_card stay None. 

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask 'vintage graphic tee under $30'

Found:    Vintage Band Tee — Faded Grey — $19.0 on depop

Outfit:   Hey there! Ooh, a faded grey vintage band tee for $19 is an absolute Depop score—that worn-in charcoal look is unbeatable. 

Here are two effortless ways to style it using pieces you already own:

**Outfit 1: 90s Streetwear Edge**
Pair the band tee with your **Baggy straight-leg jeans, dark wash**. Add the **Black combat boots** for that classic grunge texture, and throw on the **Vintage black denim jacket** over top. Finish it with the **Black crossbody bag** for an easy, everyday downtown look.

**Outfit 2: High-Low Contrast**
Tuck the tee into your **Wide-leg khaki trousers** to play with proportions. Layer the **Black cropped zip hoodie** open over it, and step into your **Chunky white sneakers** for a cool mix of streetwear and minimal earth tones. 

Which vibe are you leaning toward? Total steal either way!

  Fit card: Scored this vintage band tee on Depop for just $19 and the worn-in charcoal wash is literally unbeatable.Tossed it on with baggy denim and combat boots for the ultimate lazy 90s grunge uniform. Safe to say I'll be living in this top all fall.

0 model calls this session, 2 served from cache
```

```
$ python app.py ask 'designer ballgown size XXS under $5'

  No listings matched 'designer ballgown', size XXS, under $5.00. Try a different size, a higher price limit, or different keywords.

0 model calls this session
```


**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; r = search_listings('graphic tee', max_price=30); print(len(r), [(x['id'], x['title'], x['price']) for x in r])"
7 [('lst_006', 'Graphic Tee — 2003 Tour Bootleg Style', 24.0), ('lst_002', 'Y2K Baby Tee — Butterfly Print', 18.0), ('lst_033', 'Vintage Band Tee — Faded Grey', 19.0), ('lst_017', 'Mesh Long-Sleeve Top — Black', 15.0), ('lst_015', 'Vintage Graphic Hoodie — Faded Black', 26.0), ('lst_012', 'Oversized Crewneck Sweatshirt — Vintage Navy', 20.0), ('lst_011', 'Low-Rise Cargo Pants — Khaki', 27.0)]

```

```
$ python -c "from tools import search_listings; r = search_listings('tee', size='M'); print([(x['id'], x['size']) for x in r])"
[('lst_002', 'S/M'), ('lst_017', 'S/M')]
```

```
$ python -c "from tools import search_listings; print(search_listings('designer ballgown', 'XXS', 5))"
[]

```

```
$ python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
Hey there! Oh, those vintage Levi's 501s are an absolute Depop holy grail, and at $38 in a W30 L30, that is such a win! Since you already own some amazing basics, these medium-wash jeans will slot right into your rotation and give you that effortless streetwear vibe. 

Here are two fun ways to style them using pieces you already have:

**Look 1: Casual Streetwear**
*   **New Item:** Vintage Levi's 501 Jeans
*   **Top:** White ribbed tank top
*   **Outerwear:** Oversized grey crewneck sweatshirt
*   **Shoes:** Chunky white sneakers
*   **Accessories:** Black crossbody bag

**Look 2: Edgy & Relaxed**
*   **New Item:** Vintage Levi's 501 Jeans
*   **Top:** Black cropped zip hoodie
*   **Shoes:** Black combat boots
*   **Accessories:** Brown leather belt

Which vibe are you leaning toward? Grab them before someone else does!

```

```
$ python -c "from tools import suggest_outfit; from utils.data_loader import load_listings; print(suggest_outfit(load_listings()[0], {'items': []}))"
Hey babe! Oh, those vintage 501s are an absolute holy grail find—$38 on Depop is a total steal! That medium wash goeswith literally *everything*. 

Here are two super easy ways to style them using pieces you probably already own:

**1. The Off-Duty Cool Look:**
Pair them with a classic white baby tee or a simple black tank top. Add some retro sneakers (like Converse or Adidas Sambas), and throw on a black leather jacket or oversized blazer to instantly level it up. 

**2. The Elevated Casual Vibe:**
Tuck a cozy oversized grey crewneck sweatshirt right into the waistband. Slip on some loafers or ankle boots, and layer with some simple gold jewelry. 

You’ll wear these on repeat, I promise!

```

```
$ python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
Scored these vintage Levi's 501s on Depop for just $38.00 and the fit is genuinely unreal. Obsessed with the medium wash indigo—they have that perfect, worn-in 90s streetwear vibe. Can't wait to style them with my beat-up white sneakers and a simple tee.

```

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:* A `search_listings` implementation that matches a description against the listings, filters by size and max price, and returns an empty list when nothing matches.
- *What came back:* Working keyword search with stopwords, stemming, and a price tie-break. When I ran `search_listings('graphic tee', max_price=30)`, "Mesh Long-Sleeve Top — Black" ranked first and the real "Graphic Tee — 2003 Tour Bootleg Style" ranked fourth. Many listings tied on score, and the tie went to the cheapest.
- *What I changed:* I added a title-match bonus to the score, so title matches count extra. The graphic tee now ranks first and the mesh top fourth. Price only breaks ties.

**Moment 2**

- *What I asked for:* A query parser for agent.py that pulls a description, size, and max price out of plain text like "vintage graphic tee under $30, size M", and a one-line terminal command to test it.
- *What came back:* A regex parser that worked, but the test command used `\$` to escape the dollar sign. PowerShell doesn't treat that as an escape, so the first runs failed with "SyntaxError: '(' was never closed" and the price was lost.
- *What I changed:* I switched the test command to use a backtick before the `$` and single quotes inside the double-quoted string. The parser then returned the right description, size, and max_price for both test queries.

**Moment 3**

- *What I asked for:* A diagnosis of why criterion 4 (the fit card) missed in three of five tries.
- *What came back:* The cause was in my create_fit_card prompt: it said to mention the price but not how to write it, and limited length by sentence count and not characters.
- *What I changed:* I added one instruction to the prompt (price as digits like $30.00, under 250 characters) and reran all five criteria. Criterion 4 went from 2 of 5 to 5 of 5.

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. A matching query completes all three tools | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. An impossible query stops before the second tool | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. selected_item id matches what suggest_outfit received | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card under 300 chars, has price, not empty | 4 of 5 | PASS | PASS | FAIL | FAIL | FAIL | MISSED (2/5) |
| 5. Every result under the price ceiling | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

```
Criterion 1 (agent.py::run_agent, via run_eval.py), graphic tee query:
try 1: completed — fit card 191 chars

Criterion 2 (agent.py::run_agent), ballgown query:
      out: [] (empty)
      →    branch: empty, stopping
try 1: stopped early — No listings matched 'designer ballgown', size XXS, under $5.

Criterion 3 (agent.py::run_agent, read from results file), track jacket query:
  try 1: 90s Track Jacket — Navy/White Stripe ($45.0, poshmark)

Criterion 4 (tools.py::create_fit_card), slip dress, before the fix:
  try 3: 234 chars | has $30: False | FAIL
    Found the ultimate 90s silk slip dress on Depop for just thirty bucks and I am obsessed. Threw an oversized grey crewneck right over it with some combat boots for that effortless grunge vibe. Absolute steal and literally so versatile.
  try 4: 306 chars | has $30: True | FAIL

Criterion 5 (tools.py::search_listings, via price_check.py):
Query 1: 'vintage graphic tee under $30'  ceiling=30.0  10 results
  prices: [19.0, 24.0, 18.0, 26.0, 20.0, 15.0, 18.0, 25.0, 12.0, 14.0]
  over ceiling: none  -> PASS
```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->
     
| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | A matching query completes all three tools | 4 of 5 | MET (5/5) | All five graphic tee tries returned a fit card. |
| 2 | An impossible query stops before the second tool | 5 of 5 | MET (5/5) | All five stopped at step 1; suggest_outfit never ran. |
| 3 | selected_item matches what suggest_outfit received | 5 of 5 | MET (5/5) | Same track jacket title in the search result, selected_item, and suggest_outfit input in all five. I compared titles because the trace shows titles, not ids. |
| 4 | Fit card under 300 chars, has price, not empty | 4 of 5 | MISSED (2/5) | Tries 1 and 2 passed. Tries 3 and 5 wrote "thirty bucks" with no digits; try 4 was 306 characters. |
| 5 | Every result under the price ceiling | 5 of 5 | MET (5/5) | Five queries, zero results over the ceiling (price_check.py). |

**Diagnoses** Criterion 4 missed on 3 of 5 tries. The place is the model's output, and the mechanism is the prompt in tools.py::create_fit_card. It told the model to mention the price but not how to write it, so two cards wrote "thirty bucks" even though the item text said $30.00. It also limited length by sentence count (two to four) with no character limit, so one four-sentence card reached 306 characters. The tool itself worked and returned text every time. Both failure types come from one gap in one prompt, so this is one problem and not three.



---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```
$ python app.py ask 'vintage graphic tee under $30' --trace
[1] search_listings (via MCP)
      in:  {'description': 'vintage graphic tee', 'size': None, 'max_price': 30.0}
      out: 10 items: Vintage Band Tee — Faded Grey, Graphic Tee — 2003 Tour Bootleg Style, Y2K Baby Tee — Butterfly Print … +7 more
[2] suggest_outfit
      in:  Vintage Band Tee — Faded Grey, wardrobe of 10 items
      out: Hey there! Ooh, a faded grey vintage band tee for $19 is an absolute Depop score—that worn-in charcoal look is…
[3] create_fit_card
      in:  outfit text + Vintage Band Tee — Faded Grey
      out: Scored this vintage band tee on Depop for just $19 and the worn-in charcoal wash is literally unbeatable. Toss…
```

**Empty search**

```
$ python app.py ask 'designer ballgown size XXS under $5' --trace
[1] search_listings (via MCP)
      in:  {'description': 'designer ballgown', 'size': 'XXS', 'max_price': 5.0}
      out: [] (empty)
      →    branch: empty, stopping

  No listings matched 'designer ballgown', size XXS, under $5.00. Try a different size, a higher price limit, or different keywords.
```

**On the MCP move:** I moved `search_listings` into `mcp_server.py`, registered with `@mcp.tool()` and a description that names the units and types and states the empty case (`[]`, never an error). In `agent.py::run_agent` I replaced the direct `search_listings(...)` call with `call_tool("search_listings", {...})` from `mcp_client.py`. Nothing behaved differently: `call_tool('search_listings', {'description': 'graphic tee', 'max_price': 30})` returned a `list` of 7 dicts with ids `lst_006, lst_002, lst_033, lst_017, lst_015, lst_012, lst_011`, the same count and order as the direct call. The empty-search branch still fires for the ballgown query and `fit_card` stays `None`.

**Failure modes**

Empty search (a query the data can't match):

~~~
$ python app.py ask 'designer ballgown size XXS under $5'

  No listings matched 'designer ballgown', size XXS, under $5.00. Try a different size, a higher price limit, or different keywords.
~~~

Empty wardrobe (returns general styling advice, no crash):

~~~
$ python app.py ask 'baggy cargo pants under $40' --empty-wardrobe
(running with an empty wardrobe)
[1] search_listings (via MCP)
      in:  {'description': 'baggy cargo pants', 'size': None, 'max_price': 40.0}
      out: 3 items: Low-Rise Cargo Pants — Khaki, Corduroy Wide-Leg Pants — Rust, Baggy Carpenter Jeans — Dark Wash
[2] suggest_outfit
      in:  Low-Rise Cargo Pants — Khaki, wardrobe of 0 items
      out: Hey bestie! Oh, those low-rise khaki cargos are an absolute Y2K dream, and at $27 in fair condition, they’ve g…
[3] create_fit_card
      in:  outfit text + Low-Rise Cargo Pants — Khaki
      out: Scored these khaki low-rise cargos on Poshmark for $27 and I am officially ready for my 2000s off-duty model e…
~~~

Model unavailable (one character of the key changed in .env, restored afterwards):

~~~
$ python app.py ask 'oversized denim jacket under $50'
[1] search_listings (via MCP)
      in:  {'description': 'oversized denim jacket', 'size': None, 'max_price': 50.0}
      out: 10 items: Denim Jacket — Light Wash, Cropped, Oversized Crewneck Sweatshirt — Vintage Navy, Oversized College Crewneck — Faded Red … +7 more
[2] model call failed
      →    branch: ModelUnavailable, stopping

  Found a listing, but the styling model couldn't be reached, so there's no outfit or fit card yet. Check that the API key in .env is correct and that you're online, then run the query again. (Details: The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com.)
~~~

---


## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:** In tools.py::create_fit_card I added one instruction to the prompt: write the price as digits with a dollar sign, exactly as $XX.XX, and keep the whole caption under 250 characters. Nothing else changed.

**Which failure it was meant to fix:** Criterion 4 missed at 2 of 5. Two cards spelled the price out ("thirty bucks") and one ran 306 characters. The old prompt limited length by sentence count and did not say how to write the price.

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. A matching query completes all three tools | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. An impossible query stops before the second tool | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. selected_item id matches what suggest_outfit received | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card under 300 chars, has price, not empty | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Every result under the price ceiling | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

**Did it help, and how do I know:** Yes, for the criterion it targeted. Criterion 4 went from 2 of 5 (MISSED) to 5 of 5 (MET). Before, tries 3 and 5 spelled the price out and try 4 ran 306 characters. After, all five cards contain "$30.00" and run 162 to 195 characters, and they are not word-for-word identical (check_cards.py output). Criteria 1, 2, 3, and 5 stayed at 5 of 5, so nothing else got worse. Five tries can't separate a true 5 of 5 from a rate near 90 percent. The cards are also more formulaic now: several open with "Scored this ... on Depop for $30.00 and I am obsessed."

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

All five criteria are MET after the fix, but I'd still do three things. Criterion 3 compares titles, not ids, because the trace prints titles; a state bug between two items with the same title would slip past it. The fit cards are now more formulaic and less varied, which my criterion doesn't penalize; I'd add a check that the opening sentences differ across five items. Search ranking is loose: "90s track jacket in size M" returned a leather bomber and a silk slip dress below the jacket because "90s" matches in their descriptions. I left these alone because this unit allows one improvement only.



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
