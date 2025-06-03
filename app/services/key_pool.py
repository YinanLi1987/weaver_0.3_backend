# app/services/key_pool.py
import itertools, os

def make_pool(key_str): return itertools.cycle([k.strip() for k in key_str.split(",") if k.strip()])

openai_keys = make_pool(os.getenv("OPENAI_API_KEYS", ""))
claude_keys = make_pool(os.getenv("ANTHROPIC_API_KEYS", ""))
mistral_keys = make_pool(os.getenv("MISTRAL_API_KEYS", ""))

def get_openai_key(): return next(openai_keys)
def get_claude_key(): return next(claude_keys)
def get_mistral_key(): return next(mistral_keys)
