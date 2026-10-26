# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Your community, and what your classifier sorts posts into. Three or four
     sentences. -->

I decided to use a new discussion board community that is similiar to reddit but has a free API so that I am able to copy the information into the csv file in an easier way. I am going to be using the community /c/unpopularopinion and I will be sorting it by all to get the top 200 posts https://lemmy.world/c/unpopularopinion?dataType=Post&sort=TopAll this is a link to the source for the dataset. This community deals with people posting their opinions that they deem unpopular. So we will classify the types of unpopular opinions that people have. There is no login or private API needed. They have a public API 

Candidate Distinctions
1. Some posts propose a specific change. For example, "Cooking classes should be mandatory in school" argues for changing school requirements. Others simply express an opinion without asking for action.
2. Some posts include checkable facts or technical comparisons. "Game price isn't the problem, wages are" refers to 30 years of game prices and inflation. Many other posts offer no numbers or verifiable evidence.
3. Some posts focus on personal taste or experience. "I like the smell of cigarette smoke" explains the author's childhood association with the smell, whereas other posts make broad claims about society.
4. Some posts make sweeping judgments without verifiable support. "Tattoos are stupid" makes a general judgment using subjective evaluations rather than facts that could establish it.


---

## Label Taxonomy

<!-- Each label: a one-sentence definition and two real examples from your
     reading. Then your decision rule for the hardest boundary.

     The decision rule is worth a point on its own and it's the thing most
     people leave out. Every taxonomy has a hardest boundary. Name yours. -->

### `label_one`
Label 1: analysis
**Definition:**
A post that supports its central argument with at least one specific, checkable fact, such as a number, date, technical comparison, or documented event.

**Example 1:**

"Game price isn't the problem, wages are" — The author compares game prices over 30 years with inflation and discusses $70–$80 games to support their argument.

**Example 2:**
"All the articles about the Tesla stock dropping after March 10th were just wishcasting." The author gives specific stock prices, dates, and links to news articles to support their criticism.

### `label_two`

Label 2: hot_take
**Definition:**
A post that makes a strong, generalized judgment without presenting specific, checkable evidence to support it.


**Example 1:**


"Tattoos are stupid." — The author declares that tattoos are stupid and expresses disgust at particular designs, but provides no factual evidence for the broader judgment.

**Example 2:**

"The Daily Show became funny again as soon as Trevor Noah stopped being the host." — The author makes a strong evaluation of the show without explaining it through specific examples or evidence.

### `label_three`

Label 3: personal_preference
**Definition:**
A post focused primarily on the author's own likes, dislikes, feelings, or personal experiences rather than making a universal claim..


**Example 1:**


"I like the smell of cigarette smoke." — The author explains that cigarette smoke reminds them of their mother and creates positive childhood associations.

**Example 2:**



"I like the new Firefox UI (Nova)" — The author explicitly describes their opinion as a matter of taste and says they simply like the clean appearance.

<!-- Stretch Feature #2 --> 
Label 4: proposal

Definition: A post that explicitly recommends changing a rule, policy, standard, or common practice.

Real examples:

"Cooking classes should be mandatory in school." — The author argues that schools should require cooking classes, potentially across multiple grades.

"Headlight height should be regulated" — The author proposes a specific maximum headlight height of two feet to reduce glare.

Ambiguous post and decision rule

Post: "People don't hate on plane travel enough"

Between: analysis and proposal

This post could be classified as analysis because the author makes a checkable claim about airplane pollution, including a comparison of emissions per kilometer. However, the author also explicitly argues that plane travel should be discouraged in favor of high-speed trains, staycations, and other transportation alternatives.

Decision rule: If a post uses factual evidence but its central purpose is to recommend a specific change in behavior, rules, or practices, label it proposal. If its primary purpose is to explain or establish a claim using checkable evidence without requesting a specific change, label it analysis.


### The hardest boundary

**Which two labels:**
hot_take vs. personal_preference

Why it's ambiguous: The title sounds like a hot_take because it makes a strong, general statement that chocolate and fruit don't belong together. However, the author explains their own tastes and experiences, saying, "I have never tasted a combination of chocolate and fruit that wasn't significantly worse than the individual components." The post is strongly worded, but it focuses on the author's personal preferences rather than arguing that everyone should feel the same way.

**The decision rule I used every time:**
<!-- e.g. "If the post names a specific checkable fact, it's `analysis`, even
     if the tone is heated." -->
If a post primarily expresses the author's personal likes, dislikes, or experiences, label it personal_preference, even if the language is strong or exaggerated. If the post makes a broad judgment about something being objectively good, bad, right, or wrong without providing checkable evidence, label it hot_take. When the title and body suggest different labels, use the main point of the body to decide.


---

## The Dataset

<!-- Where you collected from, how you labelled, your counts, and three hard
     cases. -->

**Where the posts came from:**

https://lemmy.world/c/unpopularopinion?dataType=Post&sort=TopAll

ai201-project3-takemeter-starter-v2026\data\lemmy_unpopularopinion_200_labeled.csv

**How I labelled them:** <!-- Cold first? Pre-labelled with AI and corrected?
Say so plainly — the disclosure is required, not penalised. -->

I read some of the posts and gave some ideas to AI to see if there was enough evidence in the rest of the dataset to make an even classification using my suggestions without one dominating the dataset over another. This was how it was settled on the three labels that were chosen. Then I used AI to go in and label the dataset, and I went through and did checks to make sure they aligned correctl. 

**Counts per label:**

| Label | Count | Share |
|---|---|---|
| analysis | 51 | 25.5 |
| hot_take  | 89  | 44.5 |
| personal_preference | 60 | 30.0 |
| **Total** | 200  | 100% |

**Three hard cases**

<!-- Any post that made you pause: what it was, which two labels it could have
     been, and what you chose. These are worth more than the easy 190. -->

**1.**
> *The post:*
"I feel like I'm the only one in my life who holds this opinion, but I have never tasted a combination of chocolate and fruit that wasn't significantly worse than the individual components."
>
> *Could have been:*
hot_take or personal_preference
>
> *I chose, because:*

personal_preference — The title makes a strong statement that sounds like a hot take, but the author mainly describes their own experiences with different chocolate and fruit combinations. They also acknowledge that taste is subjective. Since the post focuses on personal likes and dislikes rather than making a broader argument, I chose personal_preference.

**2.**
> *The post:*
"Tattoos themselves are stupid. Doubly so if it's some media IP."
>
> *Could have been:*
>hot_take or personal_preference
> *I chose, because:*

 hot_take — The author clearly dislikes tattoos, which could make this a personal preference. However, they go beyond saying they personally dislike them and make the broad claim that there are no cool tattoos. Since they are making a generalized judgment without providing specific, checkable evidence, I chose hot_take.

**3.**
> *The post:*
To me, cold meals taste much better compared to hot meals. With chili, for example, the flavor becomes more rich after it has cooled down."
>
> *Could have been:*

hot_take or personal_preference
>
> *I chose, because:*
personal_preference — The title sounds like a universal claim, and the author gives several reasons why cold food is better. However, most of the explanation comes from their own eating preferences and experiences, such as enjoying the taste of cold food and disliking the risk of burning their mouth. Since the argument is primarily based on what the author personally enjoys, I chose personal_preference.

---

<!--Streth Feature #3 Expanding the datset adding  50 to the thinnest label-->

Expanding the Dataset for the thinnest datapoint

After testing my model, I noticed that analysis was my thinnest label and one of the hardest for the model to predict correctly. It originally had only 37 examples out of 271 posts, so I decided to expand the dataset to give the model more examples to learn from.

I collected additional public posts from the Unpopular Opinion community on Lemmy, using a larger dataset of up to 1,000 posts. I made sure the new posts weren't already in my original dataset and added 50 new analysis examples, bringing that label from 37 to 87 posts. I also added 30 proposal posts and 12 hot_take posts to help keep the dataset balanced.

This brought my dataset from 271 to 363 posts. My goal was to give the model a better chance of recognizing analysis instead of predicting the more common labels. The updated dataset is saved as LABELS_EXTENDED.CSV, with the same text, label, and note columns.

Before 37 after 50 additions 87. 
Which label had the fewest examples?

analysis was my smallest label, with only 37 posts.

Where did the new posts come from?

I collected more public posts from the Unpopular Opinion community on Lemmy using a larger CSV of up to 1,000 posts.

How did I expand the dataset?

I added 50 analysis, 30 proposal, and 12 hot_take posts. I made sure none were duplicates from my original dataset.

What changed after expanding?

analysis increased from 37 to 87 posts.

The total dataset increased from 271 to 363 posts.

Why did I expand the dataset?

My model was struggling to identify analysis posts, so I wanted to give it more examples to learn from and make the four labels more balanced.

Where is the updated dataset?

The expanded dataset is saved as LABELS_EXTENDED.CSV with the columns text, label, and note.

## The Training Run

<!-- Your starting model, your settings, and anything you changed and why. -->

**Base model:**
`distilbert-base-uncased` (DistilBERT), fine-tuned for sequence classification.

**Settings:** The first run used 3 epochs, a learning rate of `2e-5`, a batch
size of 16, a maximum sequence length of 128 tokens, and seed 42. The 200-post
three-label dataset was split 70/15/15: 140 training posts, 30 validation
posts, and 30 test posts.

**Anything I changed from the defaults, and why:**
I ran three versions. The first used the three labels (`analysis`, `hot_take`,
and `personal_preference`) for 3 epochs. The first stretch run kept those same
three labels and the same 200 posts, and changed only the epoch count from 3
to 6 because the first model mostly predicted `hot_take`. Accuracy changed
from 43.3% to 53.3%, and macro F1 changed from 0.202 to 0.401.

The second stretch run used four labels by adding `proposal` and expanding the
dataset to 363 posts. It also used 6 epochs. The base model, learning rate,
batch size, maximum sequence length, seed, and 70/15/15 split approach stayed
the same; the label set and dataset changed for this stretch run. This run's
test split had 55 posts. Its accuracy was 61.8% and macro F1 was 0.601.

**Note about `results.json`:** The root `results.json` contains the metrics
from the final, four-label stretch run, so it does not describe training on
the required three-label `labels.csv`. This happened because the notebook's
input was set to `LABELS_EXTENDED.csv` for that stretch run, and the notebook
writes each run's metrics to the same root `results.json` path, replacing the
previous file. The earlier three-label run's metrics are in
`data/results.json`; the root results file should be understood as evidence
for the expanded stretch experiment, not as the result for the required
200-post dataset.

**Split sizes:** For the initial 200-post, three-label run: 140 train / 30
validation / 30 test. For the final 363-post, four-label stretch run, the test
split contained 55 posts.


---

## How I Used AI

<!-- Two specific moments — what you asked, what came back, what you changed.

     ⚠️ Plus disclosure of any pre-labelling. If you had a model pre-label a
     batch and then read and corrected every one, say that. It's an allowed
     workflow and disclosing it costs you nothing. Not disclosing it is the
     problem. -->

**Moment 1**

- *What I asked for:*
I asked for help in identifying a public forum that would be interesting and easy to get data from. I did not want to sit there and manually copy and paste for 200 items. So I used chat gpt to help me search
- *What came back:*
There were a lot of different ideas and I went back and forth a few times in the search looking for the best way to get the answer. 
- *What I changed:*
I initially started out as a movie review instance on lemmy but it was mostly links to other websites so I focused on unpopularopinion because it offered the best data for what I was doing. 
**Moment 2**

- *What I asked for:*
I wanted to do a second run because it looked like my training was basically just guessing at which one it was by saying hot_take for everyone which came back with a .45 which is not good at all. So I asked it to look at the notebook and outputs and see what we could change. 
- *What came back:*
There were a few things that it suggested that I change. Which I agree with. I do not think 3 epochs was enough to learn the data so it suggested doing 6 epochs first and seeing what the results were. If that does not help then change the max_length because a lot of my posts are longer that 128 characters. 
- *What I changed:*
I changed the epoch count from 3 to 6 and kept the three-label dataset and
other settings the same for the first stretch run.

**Pre-labelling disclosure:**

I used AI to help pre label. I gave it the labels I wanted then I went in and checked them to make sure I agreed with them. 

The later stretch run added `proposal` as a fourth label and used an expanded
363-post dataset. It kept the 6-epoch setting and all the other training
settings the same. The expanded dataset had 87 `analysis`, 90 `hot_take`, 106
`personal_preference`, and 80 `proposal` posts.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy | 0.345 | 0.618 | +0.273 |
| Macro F1 | 0.296 | 0.601 | +0.305 |
| F1 — `analysis` | 0.417 | 0.560 | +0.143 |
| F1 — `hot_take` | 0.414 | 0.571 | +0.158 |
| F1 — `personal_preference` | 0.211 | 0.718 | +0.507 |
| F1 — `proposal` | 0.143 | 0.556 | +0.413 |

**What I predicted before I looked:**
<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->

     I think it will do better on overall accuracy. At least that is what I am hoping. 

**What the gap actually means:**
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->
My fine tuning increased the overall accuracy and F1 on all accounts and I think with some more fine tuning that could increase even more. 

---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | At least 0.85 | 0.618 | 0.564 | 0.545 | Fail |
| 2. Per-label F1 | Analysis ≥ 0.55; all other labels ≥ 0.60 | analysis 0.560; hot_take 0.571; personal_preference 0.718; proposal 0.556 | analysis 0.741; hot_take 0.222; personal_preference 0.579; proposal 0.593 | analysis 0.552; hot_take 0.211; personal_preference 0.821; proposal 0.348 | Fail |
| 3. Robust to capitalization / punctuation | At least 0.90 agreement after formatting changes | — | — | — | Not measured |
| 4. hot_take vs personal_preference confusion | No more than 0.20 of predictions cross between the two labels | — | — | — | Not measured |
| 5. High-confidence correctness | At least 0.85 accuracy when confidence ≥ 0.75, with at least 10 such cases | — | — | — | Not measured |

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

| true \ predicted | analysis | hot_take | personal_preference | proposal |
|---|---|---|---|---|
| **analysis** | 7 | 3 | 2 | 1 |
| **hot_take** | 1 | 8 | 5 | 0 |
| **personal_preference** | 0 | 2 | 14 | 0 |
| **proposal** | 4 | 1 | 2 | 5 |


**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->

Biggest confusion: 5 real `hot_take` posts called `personal_preference`.
The other direction: 2 real `personal_preference` posts called `hot_take`.

That's lopsided — the model leans toward `personal_preference` on this pair.
A direction like that usually points at your labelling rather than the
model. Your agreement report is the thing that can tell you which.

---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | Overall accuracy | At least 0.85 on each seed | MISSED | Accuracy was 0.618, 0.564, and 0.545 for seeds 42, 7, and 2024; none reached 0.85. |
| 2 | Per-label F1 | `analysis` ≥ 0.55; every other label ≥ 0.60 on each seed | MISSED | The lowest F1s across seeds were 0.552 (`analysis`), 0.211 (`hot_take`), 0.579 (`personal_preference`), and 0.348 (`proposal`). Only `analysis` met its threshold in all three runs. |
| 3 | Formatting robustness | At least 0.90 label agreement after capitalization/punctuation changes, on each seed | UNMEASURED | No capitalization/punctuation comparison was run or saved for any seed. |
| 4 | `hot_take` / `personal_preference` confusion | No more than 0.20 of the examples in this two-label group are cross-predicted, on each seed | MISSED | Cross-predictions were 7/30 (0.233) for seed 42, 8/30 (0.267) for seed 7, and 5/30 (0.167) for seed 2024. The target had to hold on all three seeds. |
| 5 | High-confidence correctness | At least 0.85 accuracy at confidence ≥ 0.75, with at least 10 such predictions per seed | UNMEASURED | The saved results report accuracy for the most-confident third, not accuracy and sample count at the 0.75 threshold, so this target cannot be checked. |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->

**1. Overall accuracy — missed.** All three results are well below 0.85
(0.545–0.618), so this is not a one-seed fluctuation. The four-label test
split has only 12–16 examples per label, and several labels have low F1, which
is consistent with the model not learning reliable boundaries from this
amount of data. It does not establish whether inconsistent training labels
also contributed: the agreement section below is still blank, and the staff
reference-label file needed to calculate agreement is not in the repository.

**2. Per-label F1 — missed.** `analysis` clears its 0.55 threshold in all
three runs (minimum 0.552), but `hot_take`, `personal_preference`, and
`proposal` do not consistently meet 0.60. In particular, `hot_take` F1 falls
to 0.222 and 0.211 in two seeds, while `proposal` falls to 0.348. The
per-seed changes and the cross-label errors in the confusion matrices point
to unstable learned boundaries rather than one clearly underrepresented
label; the test supports are similar (12–16). I cannot use the required
agreement evidence to decide whether those boundaries were also applied
inconsistently when labeling, because that report has not been completed.

**3. Formatting robustness — unmeasured.** There are no paired original and
format-altered predictions in the saved results, so there is no evidence to
call this either a pass or a miss.

**4. `hot_take` / `personal_preference` confusion — missed.** The pair exceeds
the 0.20 limit in seeds 42 and 7, and passes only in seed 2024. The confusion
is asymmetric in seed 42 (5 `hot_take` posts were predicted as
`personal_preference`, versus 2 in the reverse direction) and changes across
seeds, which shows the model has not learned a stable distinction. This is
evidence of a difficult model boundary, but it cannot tell me whether my
training labels were inconsistent: the staff agreement report and its
adjudications are blank.

**5. High-confidence correctness — unmeasured.** The saved “most-confident
third” accuracy is not the requested confidence-at-least-0.75 measurement,
and the number of predictions at that threshold is not recorded. I cannot
infer a verdict from the different statistic.

**Evidence limitation:** I should complete the agreement report before
deciding that any missed score was caused by inconsistent labeling rather
than a model/data limitation. The local `data/my_staff_labels.csv` contains my
labels, but the staff reference labels needed for comparison are absent.


---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** ___ / 30 = ___%

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

**1.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**2.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**What the pattern in my disagreements tells me:**



---

## The Improvement

**What I changed:** I changed the maximum sequence length from 128 to 256
tokens so the model could use more of each post instead of truncating as much
text. I kept the data, labels, and other training settings the same, set
`RUN_LABEL = "after"`, and ran the same three seeds.

**Which diagnosis pointed at it:** The low and seed-sensitive F1 scores and
the repeated cross-label errors suggested the model might not be getting
enough useful context from the posts. Increasing the token limit tests that
possibility; it does not resolve whether any training labels were inconsistent
because the agreement report is still incomplete.

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | At least 0.85 | 0.545 | 0.636 | 0.564 | Fail |
| 2. Per-label F1 | Analysis ≥ 0.55; all other labels ≥ 0.60 | analysis 0.500; hot_take 0.429; personal_preference 0.700; proposal 0.444 | analysis 0.846; hot_take 0.400; personal_preference 0.686; proposal 0.552 | analysis 0.545; hot_take 0.222; personal_preference 0.865; proposal 0.364 | Fail |
| 3. Robust to capitalization / punctuation | At least 0.90 agreement after formatting changes | — | — | — | Not measured |
| 4. hot_take vs personal_preference confusion | No more than 0.20 of the examples in this pair cross-predicted | 7/30 (0.233) | 5/30 (0.167) | 4/30 (0.133) | Fail |
| 5. High-confidence correctness | At least 0.85 accuracy at confidence ≥ 0.75, with at least 10 such predictions | — | — | — | Not measured |

**Did it help, and how do I know:** Not consistently. Mean accuracy increased
only slightly, from 0.576 before to 0.582 after, and mean macro F1 increased
from 0.539 to 0.546. Seed 42 got worse (accuracy 0.618 to 0.545; macro F1
0.601 to 0.518), while seeds 7 and 2024 improved. The overall accuracy target
still failed on all three seeds, the per-label F1 target still failed, and
the `hot_take` / `personal_preference` confusion target still failed because
seed 42 remained above 0.20. The formatting and confidence-threshold targets
were not measured, so this run cannot show whether the change affected them.

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->

**1. Overall accuracy — still missed.** I would next try a larger, more
representative set of labeled examples and evaluate it across the same three
seeds. I stopped after changing the maximum sequence length because I wanted
to test one change at a time; the 256-token run still only reached 0.545–0.636
accuracy, below the 0.85 target.

**2. Per-label F1 — still missed.** I would inspect more errors for `hot_take`
and `proposal` and add carefully labeled examples or clarify their boundary
rules before trying another training change. I stopped after the sequence
length experiment: the weakest F1s remained 0.222 for `hot_take` and 0.364
for `proposal`, and the incomplete agreement report means I cannot tell whether
more data or more consistent labels is the right next fix.

**4. `hot_take` / `personal_preference` confusion — still missed.** I would
review examples from this pair and apply the written distinction consistently:
personal likes or experiences belong in `personal_preference`, while broad
unsupported judgments belong in `hot_take`. I stopped after the one-setting
experiment; the after run still cross-predicted 7/30 examples for seed 42,
over the 0.20 limit, and I have not completed the agreement check needed to
know whether my own labels contributed.

**3. Formatting robustness — not measured.** I would create capitalization
and punctuation variants of the same held-out posts and compare predictions
for each seed. I stopped without running that separate test, so I cannot say
whether this criterion was met.

**5. High-confidence correctness — not measured.** I would calculate accuracy
and the number of predictions with confidence at least 0.75 for each seed.
I stopped without recording that threshold-specific output; the saved
most-confident-third metric is not a substitute, so this criterion remains
unverified.


**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->

I meant `analysis` to mean a claim supported by checkable evidence and
`proposal` to mean a recommendation for change, but in the seed 42 confusion
matrix the model called 4 real `proposal` posts `analysis`. It also called 5
real `hot_take` posts `personal_preference` (and 2 in the reverse direction),
so it has not reliably learned the boundary between a broad judgment and a
personal opinion.

### Stretch Feature: Confidence Check

**Declared feature:** Compare whether the most-confident predictions are
correct more often than the least-confident predictions, and report the
numbers for all three seeds before and after the improvement.

**Implementation and result:** The notebook's evaluation code ranks held-out
posts by the model's confidence and records accuracy for the most-confident
third and least-confident third (18 posts in each group). The saved results
show that the most-confident third was more accurate in all six runs:

| Seed | Before: most confident third | Before: least confident third | After: most confident third | After: least confident third |
|---|---:|---:|---:|---:|
| 42 | 0.778 | 0.556 | 0.778 | 0.222 |
| 7 | 0.778 | 0.500 | 0.778 | 0.389 |
| 2024 | 0.778 | 0.278 | 0.833 | 0.333 |

Confidence ranking was useful as a rough signal, but it does not establish the
separate criterion about predictions at a fixed confidence threshold of 0.75;
that threshold-specific accuracy and sample count were not saved.

### Stretch Feature: Per-Label Error Write-Up

**Declared feature:** Use the confusion matrix to identify the weakest label,
show which other label it is confused with, and explain the boundary the
model appears to be struggling with.

**Implementation and result:** `hot_take` had the lowest mean F1 across the
three seeds in both runs: 0.335 before and 0.350 after. The confusion matrices
show a recurring error in which true `hot_take` posts are predicted as
`personal_preference`:

| Seed | Before: `hot_take` → `personal_preference` | After: `hot_take` → `personal_preference` |
|---|---:|---:|
| 42 | 5 | 5 |
| 7 | 6 | 5 |
| 2024 | 5 | 4 |

This is a plausible boundary overlap: both labels express opinions without
requiring checkable evidence, but `hot_take` is meant to be a broad judgment
while `personal_preference` centers on the author's own likes or experiences.
The saved results contain aggregate confusion counts, not the individual
misclassified posts, so I cannot verify a shared wording or feature across
those exact examples; the interpretation here is about the label boundary,
not a claim about their specific text.

## How I Used AI — Unit 6

**Moment 1**

- *What I asked for:* I asked AI to help interpret the three-seed results and
  confusion matrices, and to suggest one improvement that could help accuracy
  and F1.
- *What came back:* It pointed out that scores varied across seeds and that
  `hot_take` was repeatedly confused with `personal_preference`. It first
  suggested adding examples to the thinnest label, then suggested increasing
  the maximum sequence length because posts may be truncated.
- *What I changed:* I had already added examples to the dataset in the
  previous week, so I pushed back on repeating that recommendation. I chose
  to test one training-setting change instead: increasing the maximum sequence
  length from 128 to 256 tokens. I kept the other settings the same and
  compared the same three seeds; the results were mixed rather than a
  consistent improvement.

**Moment 2**

- *What I asked for:* After seeing the mixed results, I asked what other
  training setting might be worth testing and whether changing the learning
  rate or batch size was a better next experiment.
- *What came back:* AI recommended testing a lower learning rate (`1e-5`
  instead of `2e-5`) first, while keeping the batch size at 16, so only one
  setting would change.
- *What I changed:* I set the notebook's learning rate to `1e-5` for a
  possible next run. I have not run or evaluated that third experiment yet,
  so I am not claiming it improved the model.


<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
