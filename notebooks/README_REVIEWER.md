# Rule Reviewer Guide

This guide will help you review and evaluate the quality of automatically generated Answer Set Programming (ASP) rules from clinical guidelines. **No prior knowledge of ASP or programming is required** - we'll walk you through everything step by step.

## Table of Contents
- [What You'll Be Doing](#what-youll-be-doing)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Understanding the Task](#understanding-the-task)
- [Step-by-Step Review Process](#step-by-step-review-process)
- [Rating Guidelines](#rating-guidelines)
- [Tips for Reviewers](#tips-for-reviewers)
- [Troubleshooting](#troubleshooting)
- [FAQs](#faqs)

## What You'll Be Doing

You will be reviewing how well an AI system has translated clinical cancer guidelines into formal logic rules. For each guideline statement, you'll:

1. Read the original guideline text (in plain English)
2. See the AI's translation of that guideline into ASP format
3. Rate how accurate the translation is (0-3 scale)
4. Optionally add comments explaining your rating

**Don't worry if you've never seen ASP before!** The interface will show you both the original text and the translation side-by-side, and we'll teach you the basics below.

## Prerequisites

You only need:
- A computer (Mac, Windows, or Linux)
- Internet connection (for initial setup)
- A web browser
- About 2-4 hours of focused time (depending on the guideline set)

## Installation & Setup

### Step 1: Get the Code

If someone has given you a link to download the code:
1. Download the ZIP file and extract it to a folder on your computer
2. Open a terminal/command prompt

**OR** if you have Git installed:
```bash
git clone https://github.com/YOUR_USERNAME/NICE2ASP2.git
cd NICE2ASP2
```

### Step 2: Open Terminal/Command Prompt

- **Mac**: Press `Cmd + Space`, type "Terminal", press Enter
- **Windows**: Press `Win + R`, type "cmd", press Enter
- **Linux**: Press `Ctrl + Alt + T`

### Step 3: Navigate to the Project Folder

```bash
cd path/to/NICE2ASP2
```

Replace `path/to/NICE2ASP2` with the actual location where you extracted/cloned the files.

### Step 4: Set Up Python Environment

We need to install Python and all required libraries.

**Check if Python is installed:**
```bash
python3 --version
```

If you see a version number like `Python 3.12.x`, you're good! If not, download Python from [python.org](https://www.python.org/downloads/).

**Create a virtual environment** (this keeps everything isolated):
```bash
python3 -m venv venv
```

**Activate the virtual environment:**
```bash
# On Mac/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

You should see `(venv)` appear at the start of your command prompt.

**Install required packages:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will take 3-5 minutes. You'll see lots of text scrolling by - that's normal!

### Step 5: Start Jupyter Notebook

Now we'll open the review interface:

```bash
jupyter notebook notebooks/rule_reviewer.ipynb
```

Your web browser should automatically open showing the notebook interface. If it doesn't, look in the terminal for a URL like `http://localhost:8888/...` and paste that into your browser.

## Understanding the Task

### What is ASP?

**Answer Set Programming (ASP)** is a way to write logical rules that a computer can reason with. Think of it like a very precise way of writing "if-then" statements.

For example, a clinical guideline might say:
> "If a patient has suspected pancreatic cancer, refer them to a specialist."

In ASP, this becomes something like:
```
refer_to_specialist(Patient) :- suspected_cancer(Patient, pancreatic).
```

**You don't need to write any ASP code!** You just need to judge if the AI's translation captures the meaning of the original guideline.

### What Makes a Good Translation?

A good translation should:
1. ✅ Capture all the important information from the guideline
2. ✅ Use appropriate medical terminology
3. ✅ Correctly represent the logical structure (if/then, and/or conditions)
4. ✅ Be complete (not missing parts of the guideline)

A poor translation might:
1. ❌ Miss important conditions or actions
2. ❌ Add things that weren't in the original guideline
3. ❌ Get the logic backwards (confuse causes with effects)
4. ❌ Be too vague or too specific

## Step-by-Step Review Process

### Step 1: Configure the Review

In the notebook, find **Cell 3** (the one that starts with `PROJECT_ROOT = Path.cwd().parent`).

You'll see this line:
```python
response_file = "zero_shot_response.txt"
```

**Change this** depending on what you're reviewing:
- For the main pipeline results: `"rulegen_response_fired.lp"`
- For in-context learning results: `"in_context_response.txt"`
- For zero-shot results: `"zero_shot_response.txt"`

**Also check** the cancer type in the config file. The notebook loads settings from `src/configs/config.yaml`. Make sure it points to the correct guidelines:
- For **pancreatic cancer**: `cancer_type: "pancreatic cancer"`
- For **lung cancer**: `cancer_type: "lung cancer"`

### Step 2: Load the Data

1. In the notebook, go to **Cell 1** and click the "Run" button (▶️) or press `Shift + Enter`
2. Then run **Cell 3** to load the guidelines and translations
3. You should see a message like:
   ```
   Reviewing: rulegen
   Loaded 150 review items (75 guidelines, 150 ASP rule translations).
   ```

### Step 3: Start the Review Interface

Run **Cell 5** to start the interactive review interface.

You'll see:
- **Left side**: The original guideline text
- **Right side**: The ASP translation(s)
- **Bottom**: Rating buttons and comment box

### Step 4: Review Each Guideline

For each guideline:

1. **Read the original guideline** carefully in the left panel
2. **Look at the ASP translation** in the right panel
   - You'll see code that looks something like:
     ```
     recommend(Patient, test, ct_scan) :- 
         suspected_cancer(Patient, pancreatic),
         symptom(Patient, jaundice).
     ```
   - Read this as: "Recommend CT scan for Patient IF Patient has suspected pancreatic cancer AND Patient has jaundice symptom"

3. **Ask yourself**:
   - Does the translation capture the main idea?
   - Are all the important conditions included?
   - Is anything important missing?
   - Does the logic make sense?

4. **Select a rating** (0-3):
   - **0 = Completely Wrong**: The translation doesn't match the guideline at all
   - **1 = Poor**: Major problems, misses key information or has wrong logic
   - **2 = Acceptable**: Mostly correct but has minor issues or missing details
   - **3 = Excellent**: Accurately captures the guideline completely

5. **Add a comment** (optional but helpful):
   - Explain why you gave that rating
   - Note what's missing or wrong if rating 0-2
   - This helps us improve the system!

6. **Click "Next"** to move to the next guideline

### Step 5: Save Your Progress

The notebook automatically saves your ratings as you go! The file is saved to:
```
src/output_files/CLAUDE/reviews/rule_review_[name].csv
```

If you need to stop and come back later:
1. Just close the browser tab
2. When you return, re-run the notebook cells
3. Your previous ratings will be loaded automatically

### Step 6: Complete the Review

After reviewing all guidelines:
1. The notebook will show a summary of your ratings
2. The CSV file contains your complete review
3. You can share this CSV file with the research team

## Rating Guidelines

Here are detailed criteria for each rating level:

### 3 - Excellent ⭐⭐⭐
The translation is accurate and complete:
- ✅ All conditions from the guideline are present
- ✅ All actions/recommendations are captured
- ✅ The logical structure is correct (if/then, and/or)
- ✅ Medical terminology is appropriate
- ✅ Nothing extra was added that wasn't in the guideline

**Example:**
```
Guideline: "Offer CT scan to patients with suspected pancreatic cancer and jaundice."

ASP: recommend(Patient, ct_scan) :- 
       suspected_cancer(Patient, pancreatic), 
       has_symptom(Patient, jaundice).
```
Rating: **3** - Perfect translation!

### 2 - Acceptable ⭐⭐
The translation captures the main idea but has minor issues:
- ✅ Main logic is correct
- ⚠️ Some details might be missing or slightly imprecise
- ⚠️ Could be more specific or more general than the guideline
- ✅ Still useful and mostly accurate

**Example:**
```
Guideline: "Offer urgent CT scan within 2 weeks to patients with suspected pancreatic cancer."

ASP: recommend(Patient, ct_scan) :- suspected_cancer(Patient, pancreatic).
```
Rating: **2** - Correct but missing the "urgent" and "within 2 weeks" details.

### 1 - Poor ⭐
The translation has major problems:
- ❌ Missing important conditions or actions
- ❌ Logic might be partially backwards or incorrect
- ❌ Significant information loss from the original guideline
- ⚠️ Would need major corrections to be useful

**Example:**
```
Guideline: "Do NOT offer CT scan to patients under 18 with suspected pancreatic cancer."

ASP: recommend(Patient, ct_scan) :- suspected_cancer(Patient, pancreatic).
```
Rating: **1** - Wrong! Missing the age restriction and "do not" is reversed to "recommend".

### 0 - Completely Wrong ❌
The translation doesn't match the guideline at all:
- ❌ Completely different meaning
- ❌ Wrong medical condition or intervention
- ❌ Nonsensical or contradictory
- ❌ Cannot be salvaged

**Example:**
```
Guideline: "Refer patients with suspected pancreatic cancer to a specialist."

ASP: has_symptom(Patient, pain) :- age(Patient, Age), Age > 50.
```
Rating: **0** - This talks about age and pain symptoms, not referrals!

## Tips for Reviewers

### General Tips

1. **Take breaks**: Reviewing 100+ guidelines is mentally taxing. Take a 5-10 minute break every 30 minutes.

2. **Focus on meaning, not syntax**: Don't worry if you don't fully understand ASP syntax. Focus on whether the meaning matches.

3. **Look for keywords**: Watch for important words like:
   - **Conditions**: "if", "when", "in patients with"
   - **Actions**: "offer", "refer", "recommend", "do not"
   - **Urgency**: "urgent", "immediate", "within X weeks"
   - **Populations**: age ranges, specific patient groups

4. **Common translation patterns**:
   - `recommend(X, Y) :- condition1, condition2.` means "Recommend Y for X if condition1 AND condition2"
   - `symptom(Patient, S) :- ...` means "Patient has symptom S if ..."
   - `not` in ASP means logical negation

5. **When in doubt**: Use the comment box to explain your uncertainty. Comments like "Not sure if this captures the urgency" are very helpful!

### Understanding ASP Syntax Basics

Here are the most common patterns you'll see:

| ASP Pattern | Plain English |
|-------------|---------------|
| `head :- body.` | "head is true IF body is true" |
| `A, B` | "A AND B" (both must be true) |
| `A; B` | "A OR B" (at least one is true) |
| `not A` | "NOT A" (A is false) |
| `{A}.` | "A may or may not be true" (choice) |

**Example walkthrough:**
```
refer(Patient, specialist) :- 
    suspected_cancer(Patient, pancreatic),
    not previous_diagnosis(Patient),
    age(Patient, Age),
    Age >= 40.
```

Reading this step by step:
- `refer(Patient, specialist)` - "Refer Patient to specialist"
- `:-` - "IF"
- `suspected_cancer(Patient, pancreatic)` - "Patient has suspected pancreatic cancer"
- `not previous_diagnosis(Patient)` - "AND Patient does NOT have previous diagnosis"
- `age(Patient, Age), Age >= 40` - "AND Patient's age is 40 or above"

Full sentence: "Refer Patient to specialist IF Patient has suspected pancreatic cancer AND Patient does NOT have previous diagnosis AND Patient is 40 or older."

## Troubleshooting

### Problem: "Jupyter command not found"

**Solution**: Make sure you activated the virtual environment:
```bash
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate     # Windows
```

Then try again:
```bash
jupyter notebook notebooks/rule_reviewer.ipynb
```

### Problem: "Module not found" errors

**Solution**: Install dependencies again:
```bash
pip install -r requirements.txt
```

### Problem: Notebook won't run/cells show errors

**Solution**: 
1. Click "Kernel" → "Restart Kernel" in the Jupyter menu
2. Re-run all cells from the beginning (Cell → Run All)

### Problem: Can't see the review interface

**Solution**: 
1. Make sure you ran Cell 3 to load the data
2. Then run Cell 5 to start the interface
3. Check that `response_file` is set correctly in Cell 3

### Problem: Notebook crashes or freezes

**Solution**:
1. Save your work (File → Save and Checkpoint)
2. Close the browser tab
3. In terminal, press `Ctrl+C` twice to stop Jupyter
4. Restart: `jupyter notebook notebooks/rule_reviewer.ipynb`
5. Your progress should be automatically loaded

### Problem: Reviews aren't being saved

**Solution**:
Check that you have write permissions in the project folder. The CSV file should appear at:
```
src/output_files/CLAUDE/reviews/rule_review_[name].csv
```

Try running this cell in the notebook:
```python
print(review_csv_path)
```
to see where it's trying to save.

## FAQs

**Q: How long will this take?**

A: Plan for 2-4 hours depending on the number of guidelines:
- Pancreatic cancer: ~75 guidelines (~2-3 hours)
- Lung cancer: ~100+ guidelines (~3-4 hours)

**Q: What if I don't understand a medical term?**

A: That's okay! Focus on the logical structure. If you're uncertain about the medical content, note that in the comments and rate based on whether the structure seems to match.

**Q: What if there are multiple ASP rules for one guideline?**

A: You'll review each ASP rule separately. The interface will show "Rule 1 of 3", "Rule 2 of 3", etc. Rate each one individually.

**Q: Can I change a rating after I've moved to the next guideline?**

A: Yes! Use the "Previous" button to go back, or just scroll up in the interface.

**Q: What if the guideline text is confusing or ambiguous?**

A: Rate based on whether the translation reasonably interprets the guideline. If the guideline itself is ambiguous, mention that in your comment.

**Q: Should I rate based on perfect ASP syntax?**

A: No! Focus on whether the meaning is captured correctly. Minor syntax variations are okay as long as the logic is right.

**Q: What if a guideline has no translation?**

A: You'll see "No ASP translation available" in the right panel. Just note this and move on - it's important data that the system couldn't translate this guideline.

**Q: Can I do this review in multiple sessions?**

A: Absolutely! Your progress is saved automatically. Just restart the notebook when you return and your previous ratings will load.

**Q: Who can I contact if I have questions?**

A: [Add contact information here - email, Slack, etc.]

## Summary Checklist

Before you start:
- [ ] Python 3.12+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Jupyter notebook opened (`jupyter notebook notebooks/rule_reviewer.ipynb`)
- [ ] Correct `response_file` selected in Cell 3
- [ ] Correct cancer type configured in `config.yaml`

During review:
- [ ] Read original guideline carefully
- [ ] Examine ASP translation(s)
- [ ] Select appropriate rating (0-3)
- [ ] Add comments when helpful
- [ ] Take breaks every 30 minutes

After review:
- [ ] Check that CSV file was created
- [ ] Review summary statistics if available
- [ ] Share CSV file with research team

---

Thank you for contributing to this research! Your careful evaluation helps us improve AI systems for clinical decision support.

If you have any questions or encounter problems not covered in this guide, please reach out to the research team.

