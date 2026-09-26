# Station 1 — The Interview

`Competencies: Description · Discernment` · [← Index](../README.md)

---

## What this is about

The sentence this station turns on:

> Ask badly and you get bad answers — and then you mistake that for a verdict on the tool.

That is the diagnosis for half the market. People type something arbitrary, get something arbitrary back, and conclude the whole thing is worthless.

> **New hire:** They simply interviewed badly.

## What you can do afterwards

- Hand over a task in a way that produces a usable result
- Check an answer instead of believing it

## Before you start

Have your list from Station 0 in front of you, with its three marked rows, and one real, uncritical document from your everyday work ready — a quote, a report, an extract from a manual, a contract with no personal data in it.

---

## The briefing

### The named knowledge

Anthropic lists the components of a prompt individually, with a recommended order:

*Task context · Tone context · Background data · Detailed task description and rules · Examples · Conversation history · Immediate task · Think step by step · Output formatting · Prefilled response*

Ten components. The terms are kept in the original here so that you can look them up. For the current version, always go to [Anthropic](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview).

### The briefing canvas

For most day-to-day business tasks, four of the ten carry the load. Treat them as four fields you fill in every time:

| Field | What belongs in it |
| --- | --- |
| **Task context** | Who you are, what kind of business, what role Claude is taking |
| **Background data** | Documents and facts Claude could not possibly know |
| **Detailed task description and rules** | The task plus the limits: length, tone, what must not appear |
| **Examples** | A real earlier solution from your own house |

> **New hire:** In the interview, the same four fields are describing the situation, putting the file on the table, saying what you'll be judging on, and showing how things are done here.

The rest is for developers, or rarely needed.

### The distinction most people fail on

> **Context is what Claude could not possibly know.
> Hand-holding is how it should think.**

"Reply professionally and empathetically in three paragraphs" is hand-holding. Claude does that anyway, and nobody can check an adjective. It costs space and changes little. Tone does belong in a briefing when you want something other than the default — "firm, no apology, the fault is not ours" is a rule, not hand-holding.

> **New hire:** In an interview, that is the equivalent of instructing someone to look friendly.

"The customer has been with us for six years, our goodwill limit is X, this is how we answered comparable cases" is context, and it changes everything.

---

## The worked example

`Exercise`

An invented company, a real procedure. **Hartmann Packaging GmbH**, 80 employees, family-owned, makes folding cartons. Customer: **Nordfrucht GmbH**, six years. One delivery is unusable.

The customer's email:

> **Subject:** Complaint order 24-1187 – cartons printed mirror-inverted, line stopped
>
> Dear Sir or Madam,
>
> this morning we received your delivery for order 24-1187: 12,000 folding cartons "Nordfrucht Berry Mix 250 g", four pallets. We cannot use any of it.
>
> The print is mirror-inverted against the die cut. Once the cartons are erected, our logo and the product photo sit on the back panel, the front shows the ingredients list, and the EAN barcode ends up on the glue flap, where it is covered. The retail chain will not accept goods with an unreadable barcode.
>
> We noticed it after the first 400 cartons on line 2 and stopped packing at 07:40. Photos of an erected carton and of a flat blank are attached.
>
> We expect a complete replacement delivery, in time for our delivery date to the retail chain on Friday; collection of the faulty batch; and a statement by tomorrow midday on how you intend to settle the downtime.
>
> Kind regards,
> M. Brandt, Head of Packaging, Nordfrucht GmbH

Four passes. Each one adds **one** part; nothing is taken away. Work through them yourself — reading is not enough.

### Pass 1 — the task only

```
Write a reply to this customer email:
[customer email]
```

The result reads cleanly and would suit any business on earth. **Here is the trap:** it looks good enough that most people stop. You still couldn't send it.

### Pass 2 — plus Task context and Background data

```
You are replying on behalf of Hartmann Packaging GmbH: family-owned,
80 employees, we make folding cartons for food producers. Nordfrucht has been a
customer for six years and we have never had any serious problems.

What happened internally: in prepress on 11 March, the new Nordfrucht artwork was
placed on the die-cut layout mirrored. The press check compared colours, not panel
positions, so nobody caught it. The fault is ours. A replacement run is under way,
earliest delivery Thursday midday.

Write a reply to this customer email:
[customer email]
```

For the first time it is *your* company. The cause is in there because you supplied it — not because Claude guessed it.

### Pass 3 — plus Rules

```
[everything from pass 2]

How I'll know a good reply when I see it:
- 150 words maximum
- the fault is named clearly, without a legal admission of liability
- a specific date, no vague assurances
- I can commit to a credit note up to €2,000, not above
- no subjunctive, no boilerplate
- signed by the head of sales, not by "your Hartmann team"
```

Length, tone and limits are right. The €2,000 shows up because you named it.

### Pass 4 — plus Examples

```
[everything from pass 3]

This is how we answered a comparable case last year:

"Dear Mr Weiss,
the fault is ours. When we switched to the new crease, the groove was set too
deep, and that should have been caught in the final check. The replacement run
has started and you will have the goods on Wednesday before midday. We will
collect the faulty batch on the same run.
For the downtime we are crediting you €1,400.
Call me if Wednesday is too late.
Kind regards, Andrea Hartmann, Sales"
```

Now it sounds like Andrea Hartmann. Short sentences, direct address, the phone-call line at the end.

> **New hire:** The candidate has not got better. The question has got better.

### Two habits that still matter

**Say why.** A rule with its reason works better than the bare rule. "Under 150 words" is a rule; "under 150 words, Mr Brandt reads this on his phone at the packing line" lets Claude get the rest right too: short sentences, the date up front. Anthropic's own guidance puts it this way: Claude is smart enough to generalise from the explanation.

**The colleague test.** Before you send a prompt, imagine handing it to a colleague who knows nothing about the case. If they would be confused, Claude will be too. This is Anthropic's "golden rule" for prompts.

What no longer needs a rule of its own: the order of document and question. Anthropic still recommends putting long material first and the question last, but only for very long inputs, dozens of pages. For an email, it makes no difference.

---

## Don't believe it — interrogate it

`Exercise`

Take your own document and actively try to get Claude to make a mistake. Five types:

- **Ask for something that isn't in there.** Does it say "that isn't in the document", or does it invent?
- **Build in a false premise.** "Why is the notice period in clause 7 six months?" — when the clause says something else.
- **Ask where it says that** — and then actually go and look.
- **Ask the same question twice, worded differently.** Do you get the same answer twice?
- **Ask for something outside the material.** A figure, a date, a person it cannot know.

Out of that come the three habits:

| | |
| --- | --- |
| **Cite it** | Where does it say that? |
| **Cross-check** | Again, asked differently |
| **Spot-check** | Actually verify one item, rather than trusting the whole |

> A confidently worded error is more dangerous than an obvious one.

---

## Try it yourself

`Exercise`

Write a briefing for **one of the three rows you marked in Station 0**. Fill in the four fields of the canvas, on paper or in an editor.

```
Task context:
Background data:
Task and rules:
Example:
```

## How you'll know it's good

Check it against these five points before you ask anyone:

- Is there anything in the **Background data** that Claude could not possibly know? If not, you have not supplied context — you have restated the task.
- Are the **rules checkable** — numbers, limits, formats — or are they adjectives?
- Is the **example real**, from your own house? An invented example teaches the wrong tone.
- Have you written anywhere **how** Claude should think? Cut it.
- Is the **long material at the top** and your question at the bottom?

### Getting feedback

Copy your briefing, together with this instruction, into a new chat:

```
You are the marker on a course. Below is a briefing written by a participant,
in four parts: Task context, Background data, Task and rules, Example.

Assess each part separately against these criteria:
- Task context: does it say who the business is and what role you are taking?
- Background data: is there anything in it that you could not possibly know?
- Rules: are they checkable, or just adjectives?
- Example: is it concrete enough to read a tone off it?

For each part say: usable / thin / missing — and why, in one sentence.
Name the weakest part first.

IMPORTANT: Do NOT rewrite the briefing. Do not draft an improvement.
Only describe what is missing. The participant is to repair it themselves.

Here is the briefing:
```

---

## On your own material

`Exercise`

Apply the same briefing three times to different material of your own, and note what differs. This is the part that turns watching into being able to do it.

## What goes wrong

**Hand-holding instead of context.** The most common mistake. People write down how Claude should think instead of what it cannot know — and then wonder why the result stays generic.

**Stopping at pass 1.** The first answer looks respectable. Respectable and sendable are two different things.

**Adjectives as rules.** "Professional", "customer-focused", "appropriate" are not checkable. "150 words maximum" is.

**No example.** The part almost everybody leaves out, and the one that changes the tone most.

**The fluency error.** A fluently written answer is taken for a correct one. That is why **Don't believe it — interrogate it** sits in the middle of this station rather than at the end: it belongs to the routine, not to the final inspection.

## What you keep

- One completed briefing
- The three checking habits

That is what you take into Station 2 — where the briefing becomes something permanent.

---

`Last reviewed: 2026-08-10`
