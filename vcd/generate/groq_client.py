"""Ask Groq to solve a puzzle, showing its reasoning.

Given a puzzle prompt, we tell the model to think step by step and put its
final answer inside \\boxed{}. We return the full text response so the next
step can extract and verify the answer.
"""

import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

_client = Groq(api_key=os.environ["GROQ_API_KEY"])

MODEL = "llama-3.3-70b-versatile"

# instruction added to every puzzle so the model reasons and boxes its answer
INSTRUCTION = (
    "\n\nSolve this step by step. "
    "Put your final answer inside \\boxed{}. "
    "For example: \\boxed{your answer}"
)


def solve_puzzle(prompt: str, temperature: float = 0.7) -> str:
    """Send one puzzle to Groq and return its full reasoning + answer."""
    response = _client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt + INSTRUCTION}],
        temperature=temperature,
    )
    return response.choices[0].message.content
