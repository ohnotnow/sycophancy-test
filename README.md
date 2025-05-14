# sycophancy-test

A Python-based CLI tool that generates simple numeric‐comparison prompts, sends them to one or more [litellm](https://pypi.org/project/litellm/) models in parallel, and emits the results as CSV for downstream analysis (e.g., with O3, O4-mini, Claude, etc.).

## Table of Contents
- [Features](#features)  
- [Prerequisites](#prerequisites)  
- [Installation](#installation)  
- [Usage](#usage)  
- [Examples](#examples)  
- [Environment Variables](#environment-variables)  
- [Contributing](#contributing)  
- [License](#license)  

## Features
- Generates random “Which number do you prefer?” prompts  
- Sends each prompt multiple times to one or more models  
- Runs requests concurrently via `asyncio`  
- Outputs a CSV file (or to stdout) with columns: `model, run_id, run_number, prompt, response`  

## Prerequisites
- Git  
- Python 3.8 or higher  
- An existing Litellm-compatible API key (if required by your provider)  
- [uv (Astral)](https://docs.astral.sh/uv/) (modern CLI for dependency management & execution)  

## Installation

### 1. Clone the repository  
```bash
git clone https://github.com/ohnotnow/sycophancy-test.git
cd sycophancy-test
```

### 2. Install `uv` CLI (if not already installed)  
```bash
pip install uv
```

### 3. Install project dependencies  
```bash
uv sync
```

*This will read `requirements.txt` (or `pyproject.toml`) and install `litellm` and its dependencies.*

## Usage

All commands assume you are in the project root. Replace placeholder values as needed.

```bash
uv run main.py --models "<model1,model2,…>" [options]
```

### Required Arguments
  --models    Comma-separated list of model identifiers in litellm format.

### Optional Arguments
  --prompt    A custom prompt to use only for the first run; subsequent runs will generate fresh prompts.  
  --repeat    Number of times to repeat each prompt per run (default: 6).  
  --runs      Number of distinct runs with different prompts (default: 1).  
  --output    Path to output CSV file (default: `results_<timestamp>.csv`).  
  --stdout    If set, write CSV data to stdout instead of a file.  
  --timeout   Request timeout in seconds (default: 30).  

## Examples

1. Run two models, three repeats, two runs, save to `my_results.csv`  
   ```bash
   uv run main.py \
     --models "openai/gpt-4o-mini,text-embedding-ada-002" \
     --repeat 3 \
     --runs 2 \
     --output my_results.csv
   ```

2. Single run, default repeats, output to stdout  
   ```bash
   uv run main.py \
     --models "anthropic/claude-2" \
     --stdout
   ```

## Environment Variables

If your litellm provider requires an API key, set it before running:

```bash
export LITELLM_API_KEY="your_api_key_here"   # macOS / Ubuntu
set LITELLM_API_KEY="your_api_key_here"      # Windows PowerShell
```

## Contributing

1. Fork the repository  
2. Create a feature branch (`git checkout -b feat/my-feature`)  
3. Commit your changes (`git commit -m "Add my feature"`)  
4. Push to your branch (`git push origin feat/my-feature`)  
5. Open a Pull Request  

Please adhere to existing code style and include tests where appropriate.

## License

This project is licensed under the MIT License.  
```text
MIT License

[Full text available at https://opensource.org/licenses/MIT]
```
