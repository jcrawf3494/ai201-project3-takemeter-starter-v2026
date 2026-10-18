# Acceptance criteria — TakeMeter

Five criteria that say what "working" means for this classifier, written in
unit 5 **before** anything was trained.

**All five are yours this time.** None are given. You've had two projects of
practice.

An acceptance criterion names a number. *"The model is accurate"* is an
opinion. *"Every label has an F1 of at least 0.60 on the held-out set"* is a
criterion.

Under each, write a sentence or two on **why that number**. A reason that says
something about your data or your taxonomy earns credit — *"I picked 0.60 F1
for `reaction` because it's my smallest label and I only have about 50
examples of it"*. A reason that could be attached to any project does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

Not numbers that sound impressive. Three labels means a coin-flip guesser gets
about 33%, so a target of 0.40 is barely a target. Your number should sit
somewhere you'd honestly call useful.

**Cover at least three of these five areas.** They're here as prompts, not as a
form to fill in — a criterion that fits none of them is fine if it names a
number.

| Area | A question it could answer |
|---|---|
| Overall accuracy | How often does it need to be right to be worth using? |
| Per-label performance | Is one label allowed to be much worse than the others? |
| Balance | How lopsided can your label counts get before it's a problem? |
| Consistency | If someone else labelled the same posts, how often should you agree? |
| Confidence | Should a confident prediction be right more often than an unsure one? |

Two things worth knowing before you pick numbers, because both will affect
whether you hit them:

- **Your smallest label will have the jumpiest score.** If a label has 50
  examples, about 8 land in the test split. An F1 computed on 8 examples moves
  a lot between seeds. A target for that label should be looser than one for
  your biggest label, and saying so is a good reason.
- **Unit 6 tests across three seeds, and the target has to hold across all
  three.** A target of 0.65 against results of 0.71, 0.62, 0.68 is a **miss**.
  Pick with that in mind — it is stricter than it first sounds.

---

## 1.

<!-- Your criterion. It must name a number. -->

The classifier needs to get at least 85% accuracy for the different lables 

**Why this target:**
My dataset has 200 posts, and the largest label is hot_take at 45%. If the classifere just guessed hot_take every time, it could already get around 45% right. I think 85% is a good goal because it shows the model is actually learning the differences between the labels instead of just guessing the most common one.


---

## 2.

<!-- Your criterion. -->
Each label needs to have an F1 score of at least 0.60, except analysis, which needs at least 0.55.


**Why this target:**

I have 51 analysis, 89 hot_take, and 60 personal_preference posts. Since analysis has the fewest examples, I'm giving it a slightly lower goal. I don't want the model to get a good overall score just because it's good at predicting hot_take while struggling with the other labels.



---

## 3.

<!-- Your criterion. -->
The model should give the same label at least 90% of the time when a post's capitalization or extra punctuation is changed. I'll test this on the held-out posts across all three seeds.


**Why this target:**
A lot of posts in my dataset use capital letters or strong punctuation to make their opinions stand out. I don't want the model to automatically assume something is a hot_take just because someone uses all caps or exclamation points. It should focus on what the person is actually saying rather than how they typed it.


---

## 4.

<!-- Your criterion. -->
The model should mix up hot_take and personal_preference no more than 20% of the time on the test data for each seed.


**Why this target:**
These were the two hardest labels for me to tell apart when I was labeling the posts. Some people make really strong statements about things they personally like or dislike, which can sound like hot takes. I want to see whether the model can recognize the difference between someone's personal opinion and a broad statement about something being good or bad.


---

## 5.

<!-- Your criterion. -->
When the model is at least 75% confident in its prediction, it should be correct at least 85% of the time. It also needs to make at least 10 predictions at that confidence level in each test split.


**Why this target:**
Some posts are pretty obvious, while others could easily fit into two labels. I want the model to be more confident when the answer is clear and less confident when a post is harder to classify. I also don't want it to pass this test just because it was confident about one or two easy posts.



---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 6 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Every label performs acceptably

         The model performs well on all labels.

         **Why this target:** ...

         > **Revised in unit 6:** Every label has an F1 of at least 0.60 on
         > the held-out set.
         >
         > **Why revised:** "performs well" gave me nothing to check. I
         > couldn't produce a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "Overall accuracy of at least 0.65" → "at least 0.55", because
            0.65 turned out to be optimistic for 200 examples.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
