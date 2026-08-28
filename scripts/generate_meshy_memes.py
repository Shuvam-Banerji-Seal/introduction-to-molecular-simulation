#!/usr/bin/env python3
"""
Meshy Text-to-Image meme generator for the Molecular Simulation talk.

Best model: `nano-banana-pro` (9 credits, enhanced quality) or `gpt-image-2` (9 credits, high fidelity).
We use `nano-banana-pro` as the default (docs: https://docs.meshy.ai/en/api/text-to-image)

Usage:
  export MESHY_API_KEY=msy_...  # from .env
  python scripts/generate_meshy_memes.py --prompt "funny cat doing molecular dynamics" --out slides/assets/memes/cat_md.png
  python scripts/generate_meshy_memes.py --batch prompts.txt

API flow: POST /openapi/v1/text-to-image -> GET /openapi/v1/text-to-image/<id> polling -> download image_urls[0]
"""
import os, time, argparse, requests, pathlib

API = "https://api.meshy.ai/openapi/v1/text-to-image"
BEST_MODEL = "nano-banana-pro"  # 9 credits, enhanced quality (docs best model)
FALLBACK = "nano-banana-2"      # 6 credits, balanced
CHEAP = "nano-banana"           # 3 credits

def load_key():
    # load from .env or env
    env_path = pathlib.Path(".env")
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            if line.startswith("MESHY_API_KEY="):
                os.environ["MESHY_API_KEY"] = line.split("=",1)[1].strip()
    key = os.environ.get("MESHY_API_KEY")
    if not key:
        raise SystemExit("MESHY_API_KEY not found in env or .env")
    return key

def generate(prompt, out_path, model=BEST_MODEL, aspect="16:9", poll_interval=5):
    key = load_key()
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    payload = {"ai_model": model, "prompt": prompt, "aspect_ratio": aspect}
    print(f"[mesh] POST {model} :: {prompt[:80]}")
    r = requests.post(API, headers=headers, json=payload, timeout=30)
    if r.status_code != 200:
        print(f"[mesh] POST failed {r.status_code}: {r.text[:500]}")
        # fallback to cheaper model if 402
        if r.status_code == 402 and model != CHEAP:
            return generate(prompt, out_path, model=CHEAP, aspect=aspect)
        r.raise_for_status()
    task_id = r.json().get("result")
    print(f"[mesh] task {task_id} created, polling...")
    for _ in range(120):
        time.sleep(poll_interval)
        gr = requests.get(f"{API}/{task_id}", headers={"Authorization": f"Bearer {key}"}, timeout=30)
        j = gr.json()
        status = j.get("status")
        prog = j.get("progress", 0)
        print(f"  {status} {prog}%")
        if status == "SUCCEEDED":
            url = j["image_urls"][0]
            img = requests.get(url, timeout=60).content
            pathlib.Path(out_path).parent.mkdir(parents=True, exist_ok=True)
            pathlib.Path(out_path).write_bytes(img)
            print(f"[mesh] saved {out_path} ({len(img)} bytes)")
            return out_path
        if status == "FAILED":
            print(f"[mesh] FAILED: {j.get('task_error')}")
            return None
    print("[mesh] timeout")
    return None

def batch(prompts_file, model=BEST_MODEL):
    for line in pathlib.Path(prompts_file).read_text().splitlines():
        line=line.strip()
        if not line or line.startswith("#"): continue
        # format: out_path|prompt
        if "|" in line:
            out, prompt = line.split("|",1)
            generate(prompt.strip(), out.strip(), model=model)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt", help="single prompt")
    ap.add_argument("--out", help="output png")
    ap.add_argument("--model", default=BEST_MODEL, choices=[BEST_MODEL, FALLBACK, CHEAP, "gpt-image-2"])
    ap.add_argument("--aspect", default="16:9")
    ap.add_argument("--batch", help="file with out|prompt per line")
    args = ap.parse_args()
    if args.batch:
        batch(args.batch, model=args.model)
    elif args.prompt and args.out:
        generate(args.prompt, args.out, model=args.model, aspect=args.aspect)
    else:
        ap.print_help()
