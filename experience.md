# Досвід проекту · Кузня

> Наві: читати на початку кожної сесії. Оновлювати після значущих операцій.

## Формат запису
```
[YYYY-MM-DD] Тема
Що зробили / Що спрацювало / Що ні / Висновок
```

---

## Записи

[2026-06-13] Ініціалізація проекту
Що зробили: структуру forge-sbs, CLAUDE.md, registry.md, experience.md, .gitignore, meta.yaml 3 агентів, репо serge-zol/forge-sbs запушено.
Що спрацювало: bash heredoc з Dispatch — надійно, без code-task.
Що не спрацювало: code-сесії застрягали в Plan mode — запитували і чекали; не могли виконувати. Обхід — bash напряму.
Висновок: file scaffold → bash з Dispatch. Plan mode → змінити на Auto mode (Dispatch Settings → Code permissions).

[2026-06-13] Кирилиця в назвах папок
Ризик: git/Windows проблеми з кирилицею в путях.
Рішення: agents/koval/, agents/mentor/, agents/chek/ — тільки ASCII для папок і файлів.

[2026-06-13] CLAUDE.md перезаписаний code-сесією
Проблема: code-сесія зробила git commit зі старою версією CLAUDE.md, перетерши Edit-правки з Dispatch.
Висновок: Edit-патчі в Dispatch втрачаються після git commit в code-сесії. Критичні зміни → Write tool повністю, не накопичувати Edit-патчами.

[2026-06-13] API params Opus 4.8 + extended thinking
effort:"high" замість budget_tokens. temperature — не вказувати (несумісно з thinking). max_tokens: 32000+.
Haiku 4.5 — легкі задачі (конформність схеми, форматні перевірки). Opus 4.8 — генерація і суддя.

[2026-06-13] Ландшафт eval/оптимізація — стратегічний аудит
Висновок: TEST шар і реєстр вже зроблено краще за нас — адаптувати, не будувати.
DeepEval (Apache 2.0, self-host) → TEST шар (pairwise, golden set, adversarial, агентські метрики). Обрано через незалежність від OpenAI.
Promptfoo: з 03.2026 під OpenAI — не використовувати.
DSPy → ядро moat: один spec → компіляція під Claude/GPT/Gemini. Усуває прив'язку промпту до моделі.
MLflow Prompt Registry → патерн реєстру (версіонований store, не markdown вручну).
Перший тест: Коваль v0.1 → DeepEval 3 рубрики → ручний vs DSPy-скомпільований. Якщо DSPy б'є — архітектура на DSPy core.

[2026-06-13] Інституційна недовіра + замикання петлі
inbox-карантин: inbox/ = вектор ін'єкції. Чужі інструкції → санітизувати до GENERATE.
Beat-baseline gate: нова версія мусить бити голу базову модель. Не б'є → не мерджиться.
Reproducibility ledger: пін версії моделі + повний лог per vN.
Судді потребують калібрування: звіряти з human-labeled набором (20-50 прикладів).
Data flywheel (після v0.1): провали в продакшені → автоматичний golden-case.
Локальний суддя (Llama/Qwen): рутинне eval без API-токенів.

[2026-06-13] Незалежний аудит inbox payload — Opus 4.8 (claude.ai, не Fable — відключено)
Scan: всі три clean (bytes, unicode, injection). KOVAL v1 чистий і якісний. CHEK v1 найзрілішій. MENTOR v2 потребує правок (системні конфлікти).
Критичні знахідки:
1. Desync шаблонів: CHEK(16 секцій) vs KOVAL+MENTOR(13). Рішення: canonical schema.md з 16 секціями.
2. KOVAL↔MENTOR дублюють функцію написання → pipeline: MENTOR(ескіз 1-4) → KOVAL(фінал 16) → CHEK(аудит).
Важливі: XML→plain text для тексту інструкцій. Нема test_cases — потрібні при першому eval. CHEK markdown у звітах ок, у продукті ні.

[2026-06-13] Правильний bootstrap-порядок — розрив циркулярності
Проблема: KOVAL переписує CHEK = editorial control над своїм аудитором. Тиха втрата змісту при LLM-переписуванні може ослабити CHEK непомітно.
Правило: CHEK НІКОЛИ не пишеться KOVAL. Незалежність = незалежна рука на весь life-cycle.
Правильний порядок bootstrap:
  1. CHEK до 16-схеми: людина + Opus 4.8 у claude.ai (не KOVAL). Заморозити як еталон.
  2. KOVAL переписує себе + MENTOR під schema.md.
  3. Заморожений CHEK + людина аудитують KOVAL v1 (self-rewrite теж потребує незалежного ока).
  4. MENTOR — звичайний аудит замороженим CHEK.
Conservation-diff обов'язковий: v1 містить ВСІ суттєві правила seed, лише реструктуровані.
v1 без test_cases = v1-draft (pre-eval), не v1. Beat-baseline gate ще не пройдено.
Engine config: пофікшено (effort:"high", без temperature, max_tokens:32000).

[2026-06-13] virtiofs/mount — Edit tool не зберігає зміни надійно
Edit tool до файлів у mounted sb-projects може не зберігати зміни якщо після цього git операції копіюють стан. Критичні зміни → bash heredoc напряму в mount.

[2026-06-13] JSON-схема для API-виклику ЧЕКа — крос-модельна угода
Контекст: потрібен єдиний формат для автоматизованих викликів ЧЕКа через OpenAI API.
Рішення: JSON-схема узгоджена між Opus 4.8 і GPT-5.5 незалежно — обидві моделі підтвердили сумісність.
Застосування: JSON лише для API-envelope (передача задачі, отримання структурованого звіту). Текст інструкцій всередині — plain text (правило schema.md).
Кроки відтворення: структуру JSON-envelope описано в chek_gpt_briefing.txt (секція 4).
