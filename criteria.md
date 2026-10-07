# Acceptance criteria — FitFindr

Five criteria that say what "working" means for this agent, written in unit 3
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"The agent handles errors"* is an opinion.
*"When search returns nothing, the agent stops before calling the second tool,
in 5 of 5 tries"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter one. A reason that says something about your tools, your loop, or the
data earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

**Two are written for you. You write three.**

---

## 1. A matching query completes all three tools

Given a query that matches at least one listing, the agent completes all three tool calls and returns a fit card — in at least 4 of 5 tries.

**Why this target:**
<!-- Why 4 of 5 and not 5 of 5? Something about your search, probably —
     "my search is a plain keyword match and some phrasings will miss" is a
     real answer. -->

My search will be a plain keyword match on title, description, category, style tags, colors, and brand. The data has 40 listings, and sizes aren't uniform ("S/M", "W30 L30", "XL (oversized)"), so a size filter can miss a real match. The fit card and outfit steps also call the model, which can fail on a rate limit. I picked 4 of 5 so one miss is allowed, but not more.

---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling `suggest_outfit` and returns a message naming what to change — 5 of 5 tries.

**Why this target:**
<!-- Why is 5 of 5 reasonable here when criterion 1 isn't? What's different
     about this path? -->

This path has no model call before the stop. It's one if-check on an empty list from search_listings, so the same input should give the same result every time. If the loop reaches suggest_outfit on an empty search, the branch is broken, so I allow zero misses. The stop message is a fixed string built in agent.py, not written by the model, so it names what to change (size, max price, or keywords) the same way every time.


---

## 3. Something about state

<!-- YOU WRITE THIS ONE.

     How would you know that the item your search found is the same item the
     next tool received? Name something countable or observable.

     This is the criterion people find hardest, because state failure doesn't
     look like state failure — it looks like a tool problem. Something that
     compares session["selected_item"] against what actually reached
     suggest_outfit is the shape you're after. -->

In 5 of 5 tries on a matching query, the id in session["selected_item"] equals the id of the item received by suggest_outfit, and that id is the first result returned by search_listings.

**Why this target:** Passing the item along is plain code with no model call, so it should work every time. A mismatch means a bug in my loop, not random model variation. I set 5 of 5 because there is no reason for this to fail occasionally.



---

## 4. Something about the fit card

<!-- YOU WRITE THIS ONE.

     The fit card calls a model, so the same input can produce different words
     each time. That's not a bug — it's the nature of the tool. So what would
     make it acceptable?

     Think about what you'd actually be unhappy to see. A caption that never
     mentions the price? Two different items producing the same opening
     sentence? A card longer than a caption anyone would post? Any of those can
     be turned into a number. -->

For 5 runs of create_fit_card on the same item, at least 4 of 5 captions are under 300 characters, include the item's price, and are not empty. The 5 captions are not all word-for-word identical.

**Why this target:** The caption comes from a model, so the wording changes and I can't check for exact text. I check things I can count instead: length, price, and not empty. I picked 4 of 5 because the model sometimes leaves out the price. The "not all identical" check catches a cache or a temperature of 0 (CACHE_ENABLED and TEMPERATURE in config.py).



---

## 5. Your choice

<!-- YOU WRITE THIS ONE TOO.

     Pick something you actually care about getting right. Speed, the empty
     wardrobe path, what happens when the model can't be reached, whether the
     search respects a price ceiling — anything, as long as it names a number
     or an observable outcome. -->
     
For 5 queries that include a price ceiling, every listing returned by search_listings has price <= max_price, in 5 of 5 queries.

**Why this target:** The price filter is a plain number comparison on a float field, with no model involved. A listing over the ceiling is always a bug, so I allow zero misses. A user who sets a budget needs the ceiling respected every time.



---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 4 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 4. Something about the fit card

         The fit card is different every time.

         **Why this target:** ...

         > **Revised in unit 4:** For 5 different items, the 5 fit cards share
         > no opening sentence.
         >
         > **Why revised:** "different" wasn't checkable — two cards that
         > differed by one word still counted. The new version is something I
         > can actually score.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said the empty search stops it 5 of 5 times, but I got 3 of 5,
            so 3 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
