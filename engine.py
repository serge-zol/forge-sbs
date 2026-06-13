"""
forge-sbs · engine.py
Генерація і аудит інструкцій через API.
"""

import anthropic
import json
import datetime
import os
from pathlib import Path

# ─── КОНФІГ МОДЕЛЕЙ ────────────────────────────────────────────────────────
KOVAL_MODEL   = "claude-opus-4-8"    # генерація / суддя
HAIKU_MODEL   = "claude-haiku-4-5-20251001"  # форматні перевірки

# Параметри Opus 4.8 з extended thinking (Правило CLAUDE.md)
# ВИПРАВЛЕНО: max_tokens > budget_tokens; temperature ПРИБРАНО (несумісне з thinking)
KOVAL_PARAMS = {
    "model": KOVAL_MODEL,
    "max_tokens": 32000,              # ✅ > budget (16000) — обов'язково
    "thinking": {
        "type": "enabled",
        "budget_tokens": 16000        # ✅ effort="high" для Opus 4.8; звірити docs
    },
    # temperature: НЕ вказувати — несумісне з extended thinking
}

# ─── ВІДТВОРЮВАНІСТЬ (Reproducibility Ledger) ──────────────────────────────
LEDGER_DIR = Path("agents") / "{agent}" / "v{version}" / "gen_log"

def log_generation(agent: str, version: str, params: dict,
                   request: str, response: str) -> Path:
    """Логує генерацію для відтворюваності."""
    log_dir = Path(LEDGER_DIR.as_posix().format(agent=agent, version=version))
    log_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    entry = {
        "timestamp": ts,
        "model_pin": params.get("model"),
        "params": {k: v for k, v in params.items() if k != "model"},
        "request": request,
        "response": response,
    }
    out = log_dir / f"{ts}.json"
    out.write_text(json.dumps(entry, ensure_ascii=False, indent=2))
    return out

# ─── PLAYBOOK-ІН'ЄКЦІЯ (KOVAL) ────────────────────────────────────────────
PLAYBOOK_PATH = Path("playbook.md")

def load_playbook_channel(channel: int) -> str:
    """Повертає вміст каналу playbook для ін'єкції в контекст KOVAL.
    Повертає порожній рядок поки playbook не наповнений."""
    if not PLAYBOOK_PATH.exists():
        return ""
    text = PLAYBOOK_PATH.read_text(encoding="utf-8")
    # Пошук каналу N
    marker = f"КАНАЛ {channel}"
    idx = text.find(marker)
    if idx == -1:
        return ""
    # Все до наступного КАНАЛ або кінця файлу
    next_idx = text.find("КАНАЛ", idx + len(marker))
    chunk = text[idx:next_idx] if next_idx != -1 else text[idx:]
    # Пропустити якщо порожній (лише заголовок + "(порожньо)")
    if "(порожньо)" in chunk:
        return ""
    return chunk.strip()

# ─── ГЕНЕРАЦІЯ (KOVAL) ────────────────────────────────────────────────────
def run_koval(spec: str, agent_name: str = "unknown", version: str = "1") -> dict:
    """Виклик KOVAL через API. Повертає {text, log_path}."""
    client = anthropic.Anthropic()

    # Завантажити інструкцію KOVAL
    koval_instr = Path("agents/koval/v1/instruction.txt").read_text(encoding="utf-8")

    # Playbook-ін'єкція (КАНАЛ 1: KOVAL-патерни)
    playbook_ctx = load_playbook_channel(1)
    if playbook_ctx:
        koval_instr += f"\n\nПРОЄКТНЕ ДЖЕРЕЛО — PLAYBOOK (КАНАЛ 1):\n{playbook_ctx}"

    params = {**KOVAL_PARAMS}
    resp = client.messages.create(
        **params,
        system=koval_instr,
        messages=[{"role": "user", "content": spec}],
    )

    text = resp.content[-1].text if resp.content else ""
    log_path = log_generation(agent_name, version, params, spec, text)
    return {"text": text, "log_path": str(log_path)}

# ─── TODO ──────────────────────────────────────────────────────────────────
# run_chek() — виклик CHEK через OpenAI API (response_format=chek_v2_api_schema.json)
# run_eval() — DeepEval harness (pairwise, golden set)
# beat_baseline_gate() — нова версія vs baseline, не мерджити якщо не б'є

if __name__ == "__main__":
    print("engine.py готовий. Моделі:", KOVAL_MODEL, "/", HAIKU_MODEL)
