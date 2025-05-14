import asyncio
import argparse
from litellm import acompletion
import random

"""
Make this output a csv to process with o3 or o4-mini-high/claude/whatever
"""
async def get_completion(prompt, model_name: str) -> str:
    response = await acompletion(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content

async def main(models: list[str], prompt: str, repeat: int) -> None:
    print(f"Prompt: {prompt}")
    for _ in range(repeat):
        for model in models:
            response = await get_completion(prompt, model)
            print(f"{model}: {response}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--models", type=str, required=True, help="Comma-separated list of model names in litellm format")
    parser.add_argument("--prompt", type=str, required=False, help="Prompt to send to the models")
    parser.add_argument("--repeat", type=int, required=False, default=6, help="Number of times to repeat the prompt")
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

    asyncio.run(main(models, args.prompt, args.repeat))
