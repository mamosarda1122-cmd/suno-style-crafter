import os
from groq import Groq

def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found. Please set it in Streamlit secrets.")
    return Groq(api_key=api_key)

def build_system_prompt():
    return """You are a professional music producer and prompt engineer specializing in AI music generation.
Your ONLY job is to write extremely detailed music style descriptions that generate high-quality songs from AI platforms like Suno AI and Udio.

Rules:
1. ALWAYS write style descriptions in English (this is what AI music platforms understand best).
2. Be extremely specific: mention exact BPM, key if relevant, instrument layers, vocal tone, mixing style, mood, and sonic texture.
3. Use professional music production terminology.
4. NEVER describe the lyrics or story — only the SOUND and MUSIC.
5. The output must be rich enough to guide the AI to produce a professional result.
"""

def build_user_prompt(lyrics: str, mood: str, genre: str, tempo: str, voice: str, instruments: str, mixing: str) -> str:
    return f"""Write a detailed music style description (max 5000 chars) based on these inputs:

LYRICS LANGUAGE / VIBE: {mood}
GENRE: {genre}
TEMPO: {tempo}
VOICE / VOCALS: {voice}
INSTRUMENTS: {instruments}
MIXING / PRODUCTION: {mixing}

Here are the lyrics for context (DO NOT describe the story, only use them to match the musical mood):
---
{lyrics[:2000]}
---

Write the style description now."""

def generate_detailed_style(lyrics, mood, genre, tempo, voice, instruments, mixing, model="llama-3.3-70b-versatile"):
    client = get_groq_client()
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": build_system_prompt()},
            {"role": "user", "content": build_user_prompt(lyrics, mood, genre, tempo, voice, instruments, mixing)}
        ],
        temperature=0.7,
        max_tokens=4000,
    )
    return response.choices[0].message.content.strip()

def compress_for_suno(detailed_style: str, model="llama-3.3-70b-versatile") -> str:
    client = get_groq_client()
    prompt = f"""Compress the following detailed music style description into a maximum of 1000 characters.
Preserve ONLY the most critical elements that affect the song's quality: genre, BPM, vocal style, key instruments, and mixing approach.
Remove redundant adjectives and filler words.

Original:
{detailed_style}

Compressed (≤1000 chars):"""
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a music prompt compression expert. Keep the soul of the style but make it concise."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=800,
    )
    compressed = response.choices[0].message.content.strip()
    return compressed[:1000]
