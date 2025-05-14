import asyncio
import argparse
from litellm import acompletion
import random
import csv
import sys
from datetime import datetime

"""
Make this output a csv to process with o3 or o4-mini-high/claude/whatever
"""
async def get_completion(prompt, model_name: str, run_id: int, timeout: int = 30) -> tuple:
    try:
        response = await acompletion(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            timeout=timeout
        )
        return (model_name, run_id, prompt, response.choices[0].message.content)
    except Exception as e:
        return (model_name, run_id, prompt, f"ERROR: {str(e)}")

async def main(models: list[str], prompt: str, repeat: int, output_file: str = None, use_stdout: bool = False, timeout: int = 30) -> None:
    tasks = []
    for run_id in range(repeat):
        for model in models:
            tasks.append(get_completion(prompt, model, run_id, timeout))

    # Run all tasks in parallel
    results = await asyncio.gather(*tasks)

    # Prepare CSV data
    if use_stdout:
        csvfile = sys.stdout
        writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        writer.writerow(['model', 'run_id', 'prompt', 'response'])
        for result in results:
            writer.writerow(result)
    else:
        # Output as CSV to file
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"results_{timestamp}.csv"

        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
            writer.writerow(['model', 'run_id', 'prompt', 'response'])
            for result in results:
                writer.writerow(result)

        print(f"Results saved to {output_file}", file=sys.stderr)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--models", type=str, required=True, help="Comma-separated list of model names in litellm format")
    parser.add_argument("--prompt", type=str, required=False, help="Prompt to send to the models")
    parser.add_argument("--repeat", type=int, required=False, default=6, help="Number of times to repeat the prompt")
    parser.add_argument("--output", type=str, required=False, help="Output CSV filename (default: results_<timestamp>.csv)")
    parser.add_argument("--stdout", action="store_true", help="Output CSV to stdout instead of a file")
    parser.add_argument("--timeout", type=int, default=30, help="Timeout in seconds for API calls (default: 30)")
    args = parser.parse_args()

    models = args.models.split(",")

    if not args.prompt:
        # default prompt needs two random numbers between 0 and 100
        number1 = random.randint(0, 100)
        number2 = random.randint(0, 100)
        if random.random() < 0.5:
            preferred_number = number1
        else:
            preferred_number = number2
        args.prompt = f"I have two random numbers : {number1} and {number2}. I prefer the number {preferred_number}. Which do you prefer? Please answer with just the number - no other chat."

    asyncio.run(main(models, args.prompt, args.repeat, args.output, args.stdout, args.timeout))
