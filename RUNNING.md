# Running TakeMeter

Everything about how the starter works.

This pair is different from the last two: **you train a model.** It runs on
your own machine, in a notebook, from inside this repo. No accounts, no keys,
nothing hosted.

---

## Before your first class

One setup, one virtual environment, everything in this repo. The
[environment setup page](../pages/ide_setup) has the per-operating-system
commands.

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python test.py
```

**`python test.py` passing is what you need before your first session.** It
checks your Python version against the pins, your disk, your memory, and
whether the packages import.

**Your disk needs about 9 GB free, up from 2 in the last two pairs.** The baseline model is roughly
1.6 GB and PyTorch is not small.

**Your machine needs about 6 GB of RAM.** Two things here are memory-hungry:
`baseline.py` peaks around 1.8 GB loading the zero-shot model, and the training
run peaks around 2.1 GB. Neither is comfortable beside an editor and a browser
on a 4 GB machine. `test.py` warns you.

You'll see one `[WARN] Baseline model — not downloaded yet`. That's expected in
unit 5. **Clear it before the unit 6 session** by running `python baseline.py`
once — downloading 1.6 GB during class is not how you want to spend a breakout.

> **No API key and no accounts for this pair.** Nothing here calls a hosted
> model. The baseline and the training both run on your own machine.

### What you'll be training on

`test.py` tells you, and so does section 1 of the notebook. There are three
possibilities and all of them work:

| Device | What it means | Speed |
|---|---|---|
| `cuda` | An NVIDIA GPU | Under a minute per seed |
| `mps` | Apple Silicon — M1 and later | Fast; much quicker than the CPU path |
| `cpu` | Everything else | A few minutes per seed. Three seeds is a coffee, not an afternoon |

⚠️ **Write down which one you get.** It is part of your result, not a detail
about your laptop. Two people running the same notebook on the same data with
the same seed can get different numbers, because different hardware does the
arithmetic in a slightly different order. Unit 6 asks you to report it beside
your three seeds, and `results.json` records it for you.

---

## The notebook

`takemeter.ipynb` runs **on your own machine**, from inside this repo.

1. Open it in VS Code (or `jupyter notebook`, if you prefer).
2. **Pick the kernel: the `.venv` inside this project.** In VS Code that's the
   selector in the top right. Getting this wrong is the most common way the
   first cell fails — it will say a package isn't installed when it is,
   because it's looking at a different Python.
3. Fill in the two lines at the top of section 1's second cell — your name and
   email. They only label your results.

> ⚠️ **Open it from your repo, not from a copy.** The notebook writes next to
> your code and expects `labels.csv` to be there. If you open a copy from your
> Downloads folder, it will tell you so rather than failing strangely.

### It reads and writes this folder

There is nothing to upload and nothing to download. `labels.csv` is already
here; `results.json`, `test_split.csv` and `results_three_seeds_*.json` land
here when the notebook writes them.

**Commit them yourself**, the way you commit anything else. Nothing is pushed
for you.

- Section 5 writes `results.json` and `test_split.csv` — **unit 5**
- Section 6 writes `results_three_seeds_<label>.json` — **unit 6**.
  Set `RUN_LABEL = "after"` in that cell before the Milestone 5 re-run, or the
  improvement overwrites the numbers you're comparing against.

> **Add rows to `labels.csv` mid-session?** Re-run section 2, which is what
> reads the file. The notebook holds the data in memory once it has read it.

> **Your edits to the notebook itself are yours to commit too.** `LABELS`, the
> settings and the seed live in the file — if you change them, that's a change
> to your repo like any other.

### What's in it

| Section | When | What it does |
|---|---|---|
| 1. Setup | unit 5 | Reports your device, and confirms it can see your files |
| 2. Your labels | unit 5 | `LABELS`, the settings, and **the seed** |
| 3. Split | unit 5 | 70/15/15, stratified |
| 4. Train | unit 5 | Minutes on a laptop CPU, under one on a GPU |
| 5. Results | unit 5 | Writes `results.json` and `test_split.csv` |
| 6. Three seeds | **unit 6** | Retrains three times in one cell |
| 7. Confusion matrix | **unit 6** | Prints a markdown table to paste |

Sections 6 and 7 are next unit. Nothing in unit 5 needs them.

---

## Your data

`labels.csv` in your repo. Three columns:

| Column | What's in it |
|---|---|
| `text` | The whole post. Don't trim it to fit |
| `label` | One of your labels, spelled **exactly** as in `LABELS` |
| `note` | `cold` for the 20 you labelled unaided, and a note on any you pre-labelled |

`labels_template.csv` shows the shape. `data/practice_labels.csv` is the set
used in class — 60 posts from a fictional running forum, already labelled, so
you can run the whole notebook before you have data of your own.

**One file, unsplit.** Don't split it yourself — the notebook does the 70/15/15
split, and splitting twice is how examples leak between training and test.

### The check before training

Section 2's last cell looks for the things that break a run or quietly ruin it:

| It says | What it means |
|---|---|
| `[FIX ME] Labels in your CSV that aren't in LABELS` | A spelling or capital mismatch. `Hot_take` and `hot_take` are different |
| `[FIX ME] 'x' is 78% of your data` | Over the brief's 70% cap. The model will learn to guess it |
| `[look at] N duplicate posts` | They'll land in different splits and inflate your score. That's leakage |
| `[look at] Only 12 examples of 'x'` | Its test split will be tiny, so its F1 will jump between seeds |
| `[look at] 60 rows` | Under the submission floor. Training still runs — fine for the practice data |

---

## The baseline — unit 6

```bash
python baseline.py
python baseline.py --trained results.json
```

This runs a general model over your posts using **only your label
definitions**, with no training. It's the fair opponent your fine-tuned model
has to beat.

**It scores `test_split.csv`** — the held-out posts the notebook saved in unit 5,
the same ones your trained model was measured on. Two numbers from two different
sets of posts aren't a comparison, which is why it reads that file rather than
picking its own sample. If the file isn't there it says so, falls back to a
random sample of `labels.csv`, and tells you to disclose that in your README.

Runs **on your machine**. No account, no key. A few seconds per post, so 30
posts takes a couple of minutes — that slowness is itself part of the finding.

Put your definitions in `label_definitions.txt`, one per line as
`label: definition`, copied from your README. **The definitions are the prompt** —
they're the entire input the model gets.

Without the file it falls back to bare label names, which is a much weaker
prompt. Worth doing on purpose once: run it both ways and the gap between the
two accuracies is what your definitions were worth, measured instead of assumed.
If you report the bare-names run as your baseline, say so in your README.

The second command adds a Trained column and prints the **Baseline vs.
Trained** table ready to paste.

---

## The agreement check — unit 6

Staff labelled 30 posts under the taxonomy in `data/staff_taxonomy.md`. You
label the same 30 under **those** definitions — not the ones you designed in
unit 5 — and then compare.

```bash
python agreement.py
```

Four files. The posts and the rules ship with the starter; only the answers
come from your TF, and only after yours are done. Posts and labels join on `id`:

| File | Where it comes from |
|---|---|
| `data/staff_taxonomy.md` | **Ships in the starter.** The three definitions and the decision rules staff used. Read it first — you label under *these*, not your own |
| `data/staff_posts.csv` | **Ships in the starter.** The 30 posts, no labels |
| `data/staff_labels.csv` | **Your TF gives you this**, once your own labels are done |
| `my_staff_labels.csv` | You make it: the same posts, labelled by you, with `text` and `label` columns |

**You label the staff set under the staff taxonomy, not the one you designed in
unit 5.** Your own taxonomy was yours to invent; this one is somebody else's to
apply, and whether you can apply a written rule the way its authors did is the
only evidence you have about whether your own 200 labels were consistent.

Put both staff files in `data/` under those names and the bare command finds
them. Anywhere else, point at them:

```bash
python agreement.py --staff-posts posts.csv --staff-labels labels.csv
```

Posts are matched on their text, so **paste it unchanged**. Retype or trim a
post and it won't match — the script tells you which ones didn't.

It works out the rate and lists every disagreement. **It stops there on
purpose.** The rate is arithmetic; the adjudication is the graded part, and your
README has a block to fill in for each one.

> This is the only instrument you have that can tell a labelling problem from a
> model problem. Milestone 4 asks you to use it as exactly that — a label pair
> you disagreed with staff about, and that your matrix also confuses, is a
> finding about your labels rather than about the model.

---

## Every command

| Command | What it does |
|---|---|
| `python test.py` | Checks your environment |
| `python baseline.py` | The zero-shot baseline on your held-out posts — **unit 6** |
| `python agreement.py` | Your labels vs. the staff set — **unit 6** |
| `python baseline.py --help` | All the options |
| Notebook: sections 1–5 | Train once, write `results.json` — **unit 5** |
| Notebook: sections 6–7 | Three seeds and the matrix — **unit 6** |

---

## Which piece goes with which milestone

### Unit 5 — the build

| Milestone | What you're doing | Where |
|---|---|---|
| 1 | Pick a community and read it | Nothing to run. Read for 20 minutes |
| 2 | Design your labels | README, **Label Taxonomy** |
| 3 | Write your criteria | `criteria.md` — all five are yours this time |
| 4 | Collect and label 200 | `labels.csv` |
| 5 | Run the training | Notebook, sections 1–5 |
| 6 | Write it up | README |

### Unit 6 — the test

| Milestone | What you're doing | Where |
|---|---|---|
| 1 | Run the baseline | `baseline.py` |
| 2 | Retrain three times, read the matrix | Notebook, sections 6–7 |
| 3 | Check yourself against the staff labels | `agreement.py` |
| 4 | Call each criterion, diagnose the misses | README |
| 5 | Fix one thing and re-run | Notebook, section 6 with `RUN_LABEL = "after"` |
| 6 | Say what's still broken | README |

---

## Where everything lives

| File | What it does |
|---|---|
| `takemeter.ipynb` | The training notebook. Runs here, on your machine |
| `baseline.py` | The zero-shot baseline. Runs on your machine |
| `agreement.py` | Your labels against the staff set. **Unit 6** |
| `criteria.md` | Your five criteria. **You write all five** |
| `labels.csv` | Your labelled data. **You create this** |
| `labels_template.csv` | The shape it needs |
| `label_definitions.txt` | Your definitions, for the baseline |
| `data/practice_labels.csv` | The 60-post practice set used in class |
| `data/staff_taxonomy.md` | The staff set's definitions and decision rules. Ships here |
| `data/staff_posts.csv` | The staff set's 30 posts. Ships here |
| `data/staff_labels.csv` | The staff set's labels. **Your TF gives you this** |
| `README.md` | Your submission |
| `results.json` | Written and committed by the notebook |
| `test_split.csv` | Your held-out posts, committed by the notebook. `baseline.py` reads it |
| `results_three_seeds_before.json` | Written and committed in unit 6, section 6 |
| `results_three_seeds_after.json` | The same cell re-run with `RUN_LABEL = "after"`, in Milestone 5 |
| `baseline_results.json` | Written by `baseline.py`. **Commit it** |
| `agreement_results.json` | Written by `agreement.py`. **Commit it** |
| `my_staff_labels.csv` | Your labels on the staff set. **You create this** |

---

## When something goes wrong

| What you see | What it means |
|---|---|
| Section 1 says `cpu` | Correct on most laptops, and fine. A three-seed run is minutes. Nothing to fix |
| `ModuleNotFoundError` in the notebook | Wrong kernel. Pick the `.venv` inside this project, top right in VS Code |
| `FileNotFoundError: labels.csv` | Either you haven't created it yet, or the notebook is open from a copy rather than from your repo. Section 1's second cell says which |
| The machine crawls during training | Close the browser and anything heavy. Training peaks around 2.1 GB |
| `KeyError` during training | A label in your CSV isn't in `LABELS`. Check capitals and spaces |
| Training takes an hour | You're on CPU. See the first row |
| Accuracy swings 15 points between seeds | Your dataset is too small or too lopsided for a stable measure. **That's a diagnosis, not a mistake** — write it down |
| A label's F1 is 0.00 | It probably has almost nothing in the test split. Check the split table |
| `baseline.py` says no `test_split.csv` | Unit 5's results section never finished. Re-run it, or note in your README that your comparison isn't like-for-like |
| `baseline.py` is downloading forever | First run only, ~1.6 GB. Do it before class |
| The baseline is very slow | Expected. A few seconds per post is what no fine-tuning costs at runtime |

The three usual causes when the notebook fails, in order: the kernel is the
system Python rather than this project's `.venv`, the notebook was opened from
a copy outside the repo, or a label in your CSV doesn't match `LABELS` exactly.

If none of those fix it, commit your CSV and criteria and write down the error.
**You have a labelled dataset and a filed standard, which is most of the
unit's grade.**

---

## A note on committing

At least four new commits in unit 5, four more in unit 6. Your commit history is
what shows your criteria existed before your results did.

The `results*.json` files are deliberately **not** in `.gitignore`. They're
evidence the run happened, and so are `test_split.csv` and `labels.csv`. The
notebook writes them; you commit them, along with `criteria.md`,
`baseline_results.json` and your README.

**One machine, one repo.** Everything happens here, so there's nothing to pull
before you push.

**Do not delete and recreate this repository.** You submit the same URL both
units.


---

## Capstone — opinion input and optional free hosting

### Purpose

Run the existing four-label fine-tuned TakeMeter classifier on a visitor's own
opinion using the Streamlit form in `app.py`. The input form is the single
new capability. Deploying that same app to Streamlit Community Cloud is
optional hosted extra credit, not a second classification capability.

### Local prerequisites

- Python 3.11–3.13, project environment active
- `pip install -r requirements.txt`
- The original fine-tuned **four-label** model weights exported from the
  notebook (not just the publicly available base DistilBERT model)

The repository intentionally does not contain trained model weights, user
submissions, passwords, or API tokens.

### 1. Export the trained classifier

Open `takemeter.ipynb` in the project folder and run the existing training
cell (section 4) using the four labels. Immediately after the cell finishes,
run this extra notebook cell:

```python
trainer.save_model("deployment_model")
tokenizer.save_pretrained("deployment_model")
```

This writes the fine-tuned model and tokenizer to `deployment_model/`. That
directory is ignored by Git, because the weights are large and must not be
stored in ordinary Git commits. Check that it contains `config.json`, model
weights (`model.safetensors` or `pytorch_model.bin`), and tokenizer files.

Do not substitute the base `distilbert-base-uncased` checkpoint: that would
not be your trained classifier. Make sure the checkpoint has the labels
`analysis`, `hot_take`, `personal_preference`, `proposal`.

### 2. Start the new capability locally

From the repository root:

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python test.py
streamlit run app.py
```

Open the local URL Streamlit prints, enter your own opinion, and select
**Classify opinion**. It displays one predicted category and model confidence.
Invalid inputs show a message. The initial model load can take longer; the
model is cached for subsequent classifications.

The previous notebook, baseline, CSVs, and test harness remain available;
the new app does not replace them.

### 3. Collect required measurements and log evidence

Criteria are in `criteria.md` under the Capstone heading, committed before
extension results. Use the actual fine-tuned checkpoint for the three before
trials:

```bash
python measure_extension.py --model ./deployment_model --phase before
```

The command performs three independent batches of ten synthetic valid
opinions and six deliberately invalid inputs, prints five trial verdicts,
saves `capstone_results_before.json`, and writes JSONL events under
`logs/`. It also reports measured warm-request **wall-clock seconds**
(no inference API charges). The 100/day compute estimate is calculated as
`100 * measured seconds/request`, not from a pricing page.

Paste at least ten **actual sanitized** JSONL records, including a rejected
submission, into `README.md` under Capstone > **Instrumentation**. Never
paste real visitors' opinions, keys, or unsanitized error messages. Report
MET or MISSED for all five criteria, and diagnose the exact stage/mechanism
of every miss.

Make one targeted improvement **after** inspecting the first three trials,
then repeat without changing criteria or test cases:

```bash
python measure_extension.py --model ./deployment_model --phase after
```

Add the second three-trial table, measured cost, and side-by-side before/after
comparison to the Capstone README. Do not claim results before they exist.

### 4. Free hosted extra credit: Streamlit Community Cloud

The free tier may have CPU/RAM and uptime limits; verify real deployment
before marking hosted extra credit complete.

The ordinary GitHub repo contains code, not weights. Host the model files
separately as a **public Hugging Face model repository** (model storage rather
than a paid inference service), after confirming that the checkpoint includes
no confidential training data or secrets.

1. Create a Hugging Face account and a public model repository of your choosing.
2. Upload the exported `config.json`, weights, and tokenizer files
   to that model repository, either directly at its root or inside a folder
   such as `deployment_model/`. Do not upload `training_args.bin`, labeled
   CSVs, logs, credentials, or visitor opinions. The code supports both
   layouts; set the optional subfolder secret if using the second layout.
3. Sign into https://share.streamlit.io with GitHub and create a Streamlit
   application from repository
   `jcrawf3494/ai201-project3-takemeter-starter-v2026`,
   branch `main`, entrypoint `app.py`.
4. In the **app's Streamlit secret settings** (not GitHub), configure:

   ```toml
   TAKEMETER_MODEL_ID = "jcrawf1077/takemeter-distilbert"
   TAKEMETER_MODEL_SUBFOLDER = "deployment_model"
   ```

   This example matches the existing hosted model layout where files are
   inside `deployment_model/`. If your model files are instead at the
   repository root, omit `TAKEMETER_MODEL_SUBFOLDER`. Do not append
   `/deployment_model` to `TAKEMETER_MODEL_ID`; the folder must be a
   separate configuration value. For local `./deployment_model` use,
   leave the subfolder unset.

   The model repository ID is public and is not a credential. If any real access
   tokens are ever needed, store them in the hosted secret manager; never
   publish or commit them.
5. Deploy, open the actual public URL, enter a new opinion, and verify the
   category and confidence are from your trained model.
6. Copy the **real URL** to `README.md` under Capstone > **Running It** and
   describe the deployment path. Do not invent a URL before deployment.

**Hosting fallback:** GitHub Pages and Firebase Hosting serve static assets,
not this Python/PyTorch app; they need a separate inference server or
browser-model conversion. Supabase Edge Functions are not a Python/PyTorch
hosting replacement. Check free-tier limitations before switching away from
Streamlit. There is no requirement to pay for a model inference API.

### Logging, privacy, and hosting limits

`takemeter_inference.classify_opinion()` writes structured JSONL events to
`logs/inference.jsonl` for both successes and failures. Fields include
timestamp, input length/SHA-256, output or sanitized error, status, model ID,
and measured duration. Raw visitor text is **not logged by default**. Leave
`TAKEMETER_LOG_TEXT` unset on a public deployment.

Files under `logs/`, `deployment_model/`, `.env`, and
`.streamlit/secrets.toml` are Git-ignored. Keep all sensitive information
out of public commits. Streamlit Community Cloud's local filesystem is
ephemeral; logs may disappear after restart, so save privacy-safe assignment
measurements locally. Persistent hosted logs would require separate private
storage and are not implemented yet.

### Capstone submission checklist

The uploaded brief requires all five numeric acceptance criteria, three
before and three after trials, at least ten real structured log entries plus
a failure, measured cost and 100/day arithmetic, diagnoses, one measured
improvement, and the Capstone README sections. Preserve the repo history
and use at least eight meaningful new commits. The implementation alone
does not establish that the runtime criteria passed.


### Capstone: complete the before/after evidence on Windows PowerShell

These commands run locally because the model weights and private JSONL logs are
deliberately excluded from GitHub. Use the project root in VS Code.

First, download the latest Capstone changes and verify the initial trial files:

~~~powershell
git pull origin main
.\.venv\Scripts\Activate.ps1
python -m unittest discover -s tests -v
Test-Path .\capstone_results_before.json
Test-Path .\logs\before_trial_events.jsonl
~~~

Both Test-Path commands must print True before publishing the original
measurement evidence. Do not invent or replace the initial measurements.
If either is missing, recover the original local files, or carefully repeat
the unchanged before trial with the CPU-thread setting unset; if a new before
measurement differs, update the documented before values accordingly.

**The one measured improvement experiment** limits the CPU inference worker
to one PyTorch thread. The original five criteria already passed, so the
hypothesis is that reducing CPU thread overhead may lower mean warm latency
for short posts. This setting could also make it slower; both outcomes are
valid, and the actual measured result should decide.

~~~powershell
$env:TAKEMETER_TORCH_THREADS="1"
python measure_extension.py --model ./deployment_model --phase after
python publish_capstone_evidence.py --include-after
Remove-Item Env:\TAKEMETER_TORCH_THREADS
~~~

The measurement command writes actual three-trial after results to the
Git-ignored capstone_results_after.json and local logs/after_trial_events.jsonl.
The evidence publisher reads the original before JSON and JSONL logs, verifies
known synthetic test inputs using their SHA-256 hashes, and inserts eleven
privacy-reviewed real log entries (ten successes plus a rejected input) into
README.md under **Instrumentation**. It also inserts the three-trial after table
and observed mean latency comparison under **The Improvement**. It will refuse
to publish if the measurement files are missing or it cannot find the real
test events.

Before committing, review README.md and the results. For any MISSED after
criterion, replace the diagnostic note with the actual failing stage and
mechanism as required by the assignment. Then commit only the public README,
not the private input logs, weights, or secrets:

~~~powershell
git diff -- README.md
git status --short
git add README.md
git commit -m "Capstone: document after trials and sanitized log evidence"
git push origin main
~~~

If nothing has been committed yet and only the original log excerpt should
be inserted, run the publisher without the flag:

~~~powershell
python publish_capstone_evidence.py
~~~

This is an instrumentation and optimization experiment, **not evidence of
hosting**. Hosted extra credit still requires an independently working public
URL, a free Streamlit deployment, and tested operational behavior.
