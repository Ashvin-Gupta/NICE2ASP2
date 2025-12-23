# Rule Reviewer Guide

This guide will help you review and evaluate the quality of automatically generated Answer Set Programming (ASP) rules from clinical guidelines. **No prior knowledge of ASP or programming is required** - we'll walk you through everything step by step.

## Table of Contents
- [What You'll Be Doing](#what-youll-be-doing)
- [Installation & Setup](#installation--setup)
- [Understanding the Task](#understanding-the-task)
- [Step-by-Step Review Process](#step-by-step-review-process)

## What You'll Be Doing

You will be reviewing how well an AI system has translated clinical cancer guidelines into formal logic rules. For each guideline statement, you'll:

1. Read the original guideline text (in plain English)
2. See the AI's translation of that guideline into ASP format
3. Rate how accurate the translation is (0-4 scale)
4. Optionally add comments explaining your rating


## Installation & Setup

### Step 1: Get the Code

If someone has given you a link to download the code:
1. Download the ZIP file and extract it to a folder on your computer
2. Open a terminal/command prompt

**OR** if you have Git installed:
```bash
git clone https://github.com/Ashvin-Gupta/NICE2ASP2.git
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
response_file = "rule_response.txt"
```

**Change this** depending on what you're reviewing:
- For the main pipeline results: `"rulegen_response.txt"`
- For in-context learning results: `"in_context_response.txt"`

You only need to complete the review for these two files, not the zero-shot response. 

**Also check** the cancer type in the config file. The notebook loads settings from `src/configs/config.yaml`. Make sure it points to the correct guidelines:
- For **pancreatic cancer**: `cancer_type: "pancreatic cancer"`
- For **lung cancer**: `cancer_type: "lung cancer"`

### Step 2: Load the Data

1. In the notebook, go to **Cell 1** and click the "Run" button (▶️) or press `Shift + Enter`
2. Then run **Cell 3** to load the guidelines and translations
3. You should see a message like:
   ```
   Reviewing: rulegen
   Loaded 50 review items (25 guidelines, 50 ASP rule translations).
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
   - **0 = No Rule**: No translation given
   - **1 = Correct**: Correct translation
   - **2 = Incorrect**: Wrong interpretation of the rule
   - **3 = Key Information Missed**: Omitted some key information in the rule
   - **4 = Information Hallucinated**: Term(s) which are not in the guidelines

5. **Add a comment** (optional but helpful):
   - Only needed for rules which were not correct


6. **Click "Next"** to move to the next guideline

### Step 5: Save Your Progress

The notebook automatically saves your ratings as you go! The file is saved to:
```
src/output_files/CLAUDE/reviews/rule_review_[name].csv
```
I would reccomend saving often so you don't lose any work. 


### Step 6: Complete the Review

After reviewing all guidelines:
1. The notebook will show a summary of your ratings
2. The CSV file contains your complete review
3. You can share this CSV file with the research team

### Understanding ASP Syntax Basics

Here are the most common patterns you'll see:

| ASP Pattern | Plain English |
|-------------|---------------|
| `head :- body.` | "head is true IF body is true" |
| `A, B` | "A AND B" (both must be true) |
| `A; B` | "A OR B" (at least one is true) |
| `not A` | "NOT A" (A is false) |
| `{A}.` | "A may or may not be true" (choice) |

