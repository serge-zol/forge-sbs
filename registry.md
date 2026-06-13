# Реєстр агентів · Кузня

| Агент | Версія | Статус | Дата | Score | Папка |
|-------|--------|--------|------|-------|-------|
| КОВАЛЬ | v1.2-canonical | **frozen** | 2026-06-13 | ЧЕК 4.75/5 | agents/koval/v1/ |
| ЧЕК | v2.1-core / v1-canonical-full | **frozen (root-of-trust)** | 2026-06-13 | — | agents/chek/v1/ |
| МЕНТОР | — | deferred | 2026-06-13 | — | inbox/deferred/ |

**Статуси:** `inbox` → `draft` → `review` → `frozen`

**Примітки:**
- KOВАЛЬ: FULL = agents/koval/v1/instruction.txt · аудит = audit_koval_v1.1_pass.txt
- ЧЕК: FULL = agents/chek/v1/full.txt · CORE = agents/chek/v1/core.txt · JSON-схема = agents/chek/v1/api_schema.json
- МЕНТОР: відкладено. Seed збережено в inbox/deferred/. Founding set = KOVAL + CHEK.

> Генерувати з meta.yaml (TODO: автоматизувати).
