---
name: lost-in-translation
description: A fun "translation telephone" toy — takes a phrase and chain-translates it through several real, often obscure languages and back to English, showing how mangled it gets at each hop. Draws its language pool from the real belebele dataset (122 languages) in B:\AI Directories_Databases\Datasets for variety. Triggered by "lost in translation", "translation telephone", "mangle this text", "chain translate this", "translate this back and forth", "telephone game", or a request to see how a phrase survives round-trip translation.
disable-model-invocation: true
---

# Lost in Translation

This is a party trick, not a utility. You give it a sentence, it sends that
sentence on a trip through 3-6 real languages you've probably never heard
of, translating it one hop at a time, and then brings it back to English —
usually unrecognizable, and usually funny. Think of the childhood game
"telephone," but with actual languages doing the whispering.

There is no translation software involved. **You (the AI) do the
translating yourself**, one hop at a time, using your own knowledge of each
language. A small helper script only picks *which* languages to use — it
draws them from a real 122-language dataset already on this PC
(`belebele`, a language-comprehension corpus) so the chain isn't always
"French, then German, then Spanish." It can hand you Xhosa, Tibetan,
Yoruba, Khmer, or Icelandic instead.

---

## When to activate

Use this whenever the user says things like:
- *"Do the lost in translation thing with this sentence."*
- *"Chain-translate this through a few languages and back."*
- *"Play telephone with this phrase."*
- *"Mangle this text for me."*
- *"How would this sound if you translated it back and forth a bunch of times?"*
- *"Translate my [lyric / slogan / text message] into gibberish."*

If the user hasn't given you a phrase yet, ask for one — or offer to use
the last thing they said in chat as the input, which is usually funnier
than they expect.

---

## How to run it

**Step 1 — pick the language chain.** Run the helper script from this
skill's `scripts/` folder:

```bash
python scripts/pick_languages.py --count 4
```

This prints a small JSON list of real languages (name, script, and the
dataset code), e.g. `Khmer`, `Icelandic`, `Yoruba`, `Georgian`. Useful
flags:
- `--count N` — how many hops (default 4; more hops = more chaos)
- `--seed N` — reuse the same chain again (handy for comparing two phrases
  fairly)
- `--common` — allow well-known languages too (French, Spanish, German,
  etc.) — off by default because those tend to survive round-trip
  translation intact, which is less fun
- `--script Cyrl` — theme the whole chain to one writing system (Cyrillic,
  Arabic, Devanagari, Han, etc.) for a consistent "vibe"

If the backing dataset drive (`B:`) isn't plugged in, the script quietly
falls back to a built-in list of ~30 diverse languages so this still works
— it just says `"source": "offline fallback list"` instead of `"live
belebele dataset"` in its output. No need to mention this to the user
unless they ask.

**Step 2 — translate hop by hop.** Starting from the user's original
English phrase, translate it into hop 1's language, then translate *that*
result into hop 2's language, and so on — each translation only ever sees
the previous hop's output, never the original English. This is what
causes the funny drift: small ambiguities and idioms compound with every
hop. After the last hop, translate back into English.

**Step 3 — show your work.** Lay person-friendly means showing more than
just the final punchline. For each hop, show:
- the language name (in plain English, e.g. "Icelandic," not just a code)
- the translated text in that language's script
- a rough romanization or one-line gloss if the script isn't Latin, so
  someone who can't read Khmer or Tibetan can still follow along

Then show the final English result next to the original, and a short,
casual one-line summary of what changed (tone, meaning drift, an
unintentionally funny phrase that appeared, etc). Don't over-format this
with heavy tables — a simple hop-by-hop list reads better for something
meant to be fun and skimmable.

**Step 4 — offer to keep playing.** After showing the result, casually
offer a follow-up rather than just stopping: "run it again," "make it
worse" (more hops), or "try it themed" (one script/region). See
`references/example-run.md` for a full sample playthrough to match the
tone and format against.

---

## Use case ideas

Lean into these — the more playful the framing, the better this skill
lands:

- **Mangle a love note or birthday message** before sending it as a joke,
  then send the recipient the "translated" gibberish version first as a
  teaser.
- **Stress-test a slogan or tagline** before it goes on a T-shirt or a
  business card — if it survives 4 hops without turning into nonsense, it
  was probably a strong, simple phrase to begin with.
- **Turn a song lyric into new "lyrics"** — chain-translate a verse and see
  what surreal new lyric comes out the other end; good for a laugh, or as
  a genuine creative-writing prompt generator.
- **Group chat / party game** — post the original phrase, let people guess
  what it'll turn into, then reveal the chain hop by hop.
- **"How mangled can you make it?"** — race two phrases through the same
  chain (`--seed` the same value) and compare which one survives better.
- **Theme it to a mood** — `--script Cyrl` for a "Soviet spy transmission"
  vibe, or an all-Southeast-Asian-script chain for a "lost in Bangkok"
  feel, or a Nordic-only chain for something colder and stranger.
- **Test a phrase's real meaning** — folk-linguistics curiosity: does the
  *core idea* of a sentence survive translation drift, or is it more
  fragile than it seems? Good springboard for a "no really, what does this
  sentence actually mean" conversation.
- **Prank a chatbot / voice assistant persona** — feed it mangled output
  and have it respond in character as if that's genuinely what it heard.
- **Quick icebreaker** — chain-translate someone's name or a common phrase
  as a fun opener in a group setting.
- **"Reverse engineer the drift"** — show the user each hop and ask them
  to guess, before you reveal it, where exactly the meaning went sideways.

---

## Notes

- Keep the whole thing lighthearted — this is a toy, not a linguistics
  tool. Don't over-explain the mechanics unless asked.
- If a language in the chain uses an unfamiliar script, always include a
  romanization/gloss — the fun evaporates if the user can't tell what
  happened at that hop.
- Default to **not** including common languages (see `--common` above) —
  a chain through French and Spanish rarely mangles anything, and "boring"
  was the exact feedback this skill was designed to avoid.
- This skill has no dependency beyond the Python script picking language
  names; all actual translation is done by you, using your own language
  knowledge, at each hop.
