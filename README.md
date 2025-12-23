# NICE2ASP2: Clinical Guidelines to Answer Set Programming

This repository contains the implementation of a pipeline for translating clinical guidelines (specifically NICE cancer guidelines) into Answer Set Programming (ASP) rules using Large Language Models (LLMs).

## Table of Contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Pipeline](#running-the-pipeline)
- [Project Structure](#project-structure)
- [Experiments](#experiments)

## Overview

The NICE2ASP2 project implements a Data-to-Knowledge (D2K) pipeline that:
1. Extracts constants from clinical guidelines
2. Identifies predicates and their relationships
3. Generates ASP rules that formalize the guidelines
4. Evaluates the generated rules against ground truth
5. Performs Knowledge-to-Patient (K2P) analysis to test rule application on patient vignettes

The system supports multiple LLM backends (GPT, Claude, etc.) and various prompting strategies (zero-shot, in-context learning, and the full D2K pipeline).

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Python 3.12** or higher
- **pip** (Python package manager)
- **Git** (for cloning the repository)
- **Clingo** (ASP solver) - Install via:
  ```bash
  # macOS
  brew install clingo
  
  # Ubuntu/Debian
  sudo apt-get install gringo
  
  # Or download from: https://potassco.org/clingo/
  ```

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Ashvin-Gupta/NICE2ASP2.git
cd NICE2ASP2
```

### 2. Create a Virtual Environment

It's strongly recommended to use a virtual environment to avoid dependency conflicts:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will install all required packages including:
- LLM APIs (OpenAI, Anthropic, Groq)
- Data processing libraries (pandas, numpy, PyYAML)
- Graph analysis tools (networkx, GraKeL)
- Jupyter notebook support (for rule review)
- And more (see `requirements.txt` for full list)

### 4. Configure API Keys

**Important:** You need to set up your API keys for the LLM services you plan to use.

Edit the file `src/resources/API_KEYS.py` and add your own API keys:

```python
API_KEYS = {  
    'ANTHROPIC_API_KEY': 'your-anthropic-key-here',
    'GROQ_API_KEY': 'your-groq-key-here',
    'OPENAI_API_KEY': 'your-openai-key-here',
    'OPENROUTER_API_KEY': 'your-openrouter-key-here'
}
```

**Note:** Never commit your API keys to version control. Consider using environment variables or a `.env` file for production use.

## Configuration

The main configuration file is located at `src/configs/config.yaml`. This file controls:

- **Experiment settings**: model selection, temperature, output directory
- **Cancer type**: which guidelines to process (pancreatic cancer, lung cancer, etc.)
- **Pipeline version**: D2K-Pipeline, In-Context, or No-Pipeline (zero-shot)
- **Input/output file paths**

### Example Configuration

```yaml
experiment:
  name: "pancreatic_cancer_guidelines"
  output_dir: "src/output_files/CLAUDE"
  model: "claude-opus-4-1-20250805"
  family: "claude"
  temperature: 0.0
  version: D2K-Pipeline  # Options: No-Pipeline, In-Context, D2K-Pipeline
  cancer_type: "pancreatic cancer"

input_files:
  problem_text: "src/input_files/input_guidelines/pancreatic_cancer_guidelines.txt"
  constant_prompt: "src/input_files/prompt_files/PC/constant_prompt2.txt"
  predicate_prompt: "src/input_files/prompt_files/PC/predicate_prompt2.txt"
  rule_generation_prompt: "src/input_files/prompt_files/PC/rule_generation_prompt2.txt"
  ground_truth: "src/input_files/ground_truths/GT_PC.lp"
  # ... more paths
```

### Switching Between Cancer Types

To switch between pancreatic cancer and lung cancer guidelines:

1. Change `cancer_type` in `config.yaml` to either:
   - `"pancreatic cancer"` or
   - `"lung cancer"`

2. Update the corresponding input file paths:
   - For lung cancer: `lung_cancer_guidelines.txt`
   - For pancreatic cancer: `pancreatic_cancer_guidelines.txt`

3. Update the ground truth file:
   - For lung cancer: `GT_LC.lp`
   - For pancreatic cancer: `GT_PC.lp`

## Running the Pipeline

### 1. Verify Installation

First, ensure all imports work correctly:

```bash
python -c "import yaml, pandas, anthropic, openai; print('All dependencies loaded successfully!')"
```

### 2. Run the Main Pipeline

The main pipeline is executed via `main.py`:

```bash
python main.py
```

**Note:** Most of the pipeline code in `main.py` is commented out by default. You'll need to uncomment the sections you want to run:

- **Constant extraction** (lines 66-71)
- **Predicate extraction** (lines 73-79)
- **Rule generation** (lines 81-91)
- **Baseline methods** (lines 92-112)
- **Graph analysis** (lines 114-141)
- **K2P analysis** (lines 143-169) - Currently active

### 3. Pipeline Stages

The pipeline executes the following stages:

#### a. D2K Pipeline (Data-to-Knowledge)

1. **Constant Extraction**: Identifies domain constants from guidelines
2. **Predicate Extraction**: Extracts predicates and relationships
3. **Rule Generation**: Generates ASP rules based on constants and predicates

#### b. Baseline Methods

- **Zero-shot**: Direct ASP generation without intermediate steps
- **In-context**: ASP generation with examples
- **LLM-only**: Natural language recommendations without ASP

#### c. Graph Analysis

Compares generated ASP programs with ground truth using:
- Structural similarity metrics
- Graph kernel methods
- Predicate and rule overlap

#### d. K2P Analysis (Knowledge-to-Patient)

1. Extract atoms from patient vignettes
2. Run Clingo solver on patient cases
3. Generate explanations for fired rules

### 4. Output Files

Results are saved in `src/output_files/[MODEL]/[cancer_type]/`:

```
src/output_files/CLAUDE/pancreatic cancer/
├── config.yaml                    # Copy of experiment configuration
├── constant_response.txt          # Extracted constants
├── predicate_response.txt         # Extracted predicates
├── rulegen_response.txt           # Generated ASP rules
├── rulegen_response_fired.lp      # Rules with fired/1 atoms
├── atoms.txt                      # Patient vignette atoms
├── clingo_output.txt              # Solver output
├── explanation.txt                # Human-readable explanations
├── graph_metrics.csv              # Similarity metrics
├── zero_shot_response.txt         # Zero-shot baseline
└── in_context_response.txt        # In-context baseline
```

## Project Structure

```
NICE2ASP2/
├── main.py                        # Main pipeline entry point
├── requirements.txt               # Python dependencies
├── README.md                      # This file
├── README_REVIEWER.md             # Guide for rule reviewers
├── notebooks/
│   └── rule_reviewer.ipynb        # Interactive review interface
├── src/
│   ├── configs/
│   │   └── config.yaml            # Main configuration file
│   ├── input_files/
│   │   ├── input_guidelines/      # Clinical guideline texts
│   │   ├── ground_truths/         # Human-authored ASP ground truth
│   │   ├── prompt_files/          # LLM prompts
│   │   └── K2P/                   # Patient vignettes
│   ├── output_files/              # Generated results
│   │   ├── CLAUDE/
│   │   └── GPT/
│   ├── processing/                # Core processing modules
│   │   ├── LLM_Inferencer.py      # LLM API wrapper
│   │   ├── FileManager.py         # File I/O utilities
│   │   ├── RuleProcessor.py       # ASP rule processing
│   │   ├── ASPRuleParser.py       # ASP parsing utilities
│   │   ├── graph_analysis.py      # Graph similarity metrics
│   │   └── graph_utils.py         # Graph construction
│   ├── resources/
│   │   └── API_KEYS.py            # API keys (DO NOT COMMIT!)
│   └── review/
│       └── review_data.py         # Review dataset builder
└── venv/                          # Virtual environment (not in repo)
```

## Experiments

### Running Different Experiment Variants

Edit `config.yaml` to change the experiment type:

```yaml
experiment:
  version: D2K-Pipeline  # Change this
```

Options:
- **D2K-Pipeline**: Full 3-stage pipeline (constants → predicates → rules)
- **In-Context**: Single-stage generation with examples
- **No-Pipeline**: Zero-shot generation

### Running Multiple Models

To compare different LLMs:

1. Run with GPT:
```yaml
model: "gpt-4o"
family: "gpt"
output_dir: "src/output_files/GPT"
```

2. Run with Claude:
```yaml
model: "claude-opus-4-1-20250805"
family: "claude"
output_dir: "src/output_files/CLAUDE"
```

### Evaluating Results

After generating ASP rules, review them using the Jupyter notebook:

```bash
jupyter notebook notebooks/rule_reviewer.ipynb
```

See [README_REVIEWER.md](README_REVIEWER.md) for detailed review instructions.

## Troubleshooting

### Common Issues

1. **Import errors**: Make sure virtual environment is activated and all dependencies are installed
   ```bash
   source venv/bin/activate  # Activate venv
   pip install -r requirements.txt
   ```

2. **API errors**: Verify your API keys are correct in `src/resources/API_KEYS.py`

3. **Clingo not found**: Install Clingo ASP solver (see Prerequisites)

4. **CUDA/PyTorch errors**: The requirements include CUDA support. If you don't have NVIDIA GPU, PyTorch will fall back to CPU automatically.

5. **Memory issues**: Some graph analysis operations can be memory-intensive. Close other applications if needed.

