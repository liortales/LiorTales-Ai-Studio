# LIORTALES — ПОЛНЫЙ АУДИТ ТЕКУЩЕЙ СИСТЕМЫ

Дата аудита: 2026-08-11
Режим: только исследование. Ничего не изменено, не удалено, не переписано, не создано — кроме этого файла.
Ветка репозитория на момент аудита: `claude/liortales-repo-architecture-omtewy`.

Аудит охватывает **две реально существующие, независимо работающие системы**, которые обе относятся к LiorTales:

- **Система A — репозиторий `LiorTales-Ai-Studio`** (git, 8 "агентов" как md-спецификации, `workflows/`, `shared/`, `tools/`, `product-assets/`). Это то, над чем шла вся предыдущая работа в этой сессии.
- **Система B — глобальный Skill `liortales-growth-engine`** (`/root/.claude/skills/synced/liortales-growth-engine/`, не в git-репозитории, не версионируется вместе с ним). Использован в этой сессии впервые и всего один раз (см. K и раздел "ЧТО НЕ РАБОТАЕТ").

Это — главный структурный факт всего аудита: **обе системы описывают один и тот же бизнес, но независимо друг от друга**, почти без связей между собой, кроме одного узкого моста (раздел E, конфликт C4). Все находки ниже нужно читать с учётом этого.

---

## 1–2. INVENTORY (что реально существует)

### Система A — репозиторий

| NAME | TYPE | PURPOSE | ACTUALLY USED | OVERLAPS WITH | POTENTIAL PROBLEM |
|---|---|---|---|---|---|
| `agents/01-content-director/README.md` | Reference File (роль, не Subagent SDK-механизм) | Оркестрация всего прогона, финальное одобрение концепции, эскалации | YES (использовался этой сессией как ролевая инструкция) | growth-engine "AI Director / Orchestrator" (другая роль под тем же именем "Agent 01") | Коллизия номера "Agent 01" с системой B (см. Conflict C6) |
| `agents/02-competitor-trend-intelligence/README.md` | Reference File | Research/intel, PER-REFERENCE EVIDENCE | YES | growth-engine "Market & Customer Researcher (Agent 02)" | То же — номер "Agent 02" в growth-engine означает то же самое по функции (единственная пара, где номер совпал по смыслу) |
| `agents/03-content-strategist/README.md` | Reference File | Стратегия, Creative Blueprint | YES | growth-engine "Content Strategist (Agent 03)" | Номер совпал по смыслу здесь тоже — но это скорее совпадение, а не согласованная нумерация |
| `agents/04-copywriter-storytelling/README.md` | Reference File | Финальный копирайтинг | YES | growth-engine "Product & Listing Optimizer (Agent 04)" — **другая функция** | Коллизия: "Agent 04" в системе A = копирайтер, в системе B = продукт/листинг |
| `agents/05-visual-creative-director/README.md` | Reference File | Визуальное направление + финальная статика; STORYBOARD; PRODUCT ASSET LOCK; §12-маршрут OpenAI-primary | YES, только что расширен в этой сессии | growth-engine "Performance & Experiment Analyst (Agent 05)" — **другая функция** | Коллизия номера; см. Conflict C4 (расхождение по OpenAI-primary охвату) |
| `agents/06-reels-video-producer/README.md` | Reference File | Видео/Reels, KLING/REMOTION routing | YES | growth-engine "Automation Manager (Agent 06)" — **другая функция**; growth-engine `reels.md` | Коллизия номера; см. Conflict C3 (Remotion отсутствует в growth-engine) |
| `agents/07-quality-control-brand-guardian/README.md` | Reference File | QC/Brand Guardian, 17 QC-областей | YES | growth-engine "Brand & Visual Guardian (Agent 01)" — та же функция, но под номером **01**, не 07 | См. раздел N (QC STATUS) — структурный риск самопроверки |
| `agents/08-publisher-performance-analyst/README.md` | Reference File | Публикация + аналитика | YES | growth-engine не имеет отдельного "Agent 08"; публикация — часть Automation Manager (06) | — |
| `workflows/pipeline-control-rules.md` | Rule / canonical reference | §1–§12: revision cap, block-состояния, anti-repetition, Handoff-контракты, Product Asset Lock, Handheld Gate, video routing, OpenAI-primary route | YES, только что расширен (§12) | Частично дублируется по смыслу growth-engine `approvals-and-agents.md` | Не имеет аналога в системе B почти ни по одному пункту, кроме §9/§10 (см. G, Missing) |
| `workflows/daily-content/README.md` | Workflow (последовательность вызовов) | Полный 9-стадийный прогон одного дневного контента | YES | growth-engine "Mandatory workflow" (8 шагов, другая структура) | Два параллельных, несовместимых по шагам workflow (см. раздел 3) |
| `workflows/manual-content/`, `workflows/performance-feedback/` | пустые стабы (`.gitkeep`) | Заявлены, но не реализованы | NO | — | Unused (см. H) |
| `shared/brand/brand-bible.md` | Reference File | Позиционирование, аудитория, tone of voice | YES | growth-engine `brand-and-product.md` | См. Conflict C1, C2, C5 |
| `shared/brand/visual-identity-guide.md` | Reference File | Визуальный стандарт, §12 карусели, production learnings | YES, дважды обновлён в этой сессии | growth-engine `visual-identity.md` | См. Conflict C4, C5 |
| `shared/brand/language-policy.md` | Reference File | RU/EN язык | YES | growth-engine language-раздел в `reels.md`/SKILL.md | Не конфликтует — совпадает по сути |
| `shared/product/product-bible.md` | Reference File | Подтверждённые факты о продукте, §18 registry обложек | YES | growth-engine `brand-and-product.md` | См. Conflict C1, C2 — **самое серьёзное расхождение во всём аудите** |
| `shared/platform-rules/platform-and-publishing-policy.md` | Reference File | Список платформ, Etsy-классификация, владение расписанием | YES | growth-engine `platforms-and-content.md` | См. Conflict C7 |
| `shared/production-tools/openai-image-pipeline.md` | Reference File / contract | Полный контракт двухэтапного OpenAI-пайплайна | YES, только что обновлён | growth-engine `automation-openai-images.md` (ссылается на этот же файл как источник истины — единственный настоящий мост между системами) | См. Conflict C4 (growth-engine не в курсе нового §12) |
| `shared/production-tools/remotion-video-pipeline.md` | Reference File / contract | Как Agent 06 использует Remotion | YES | Нет аналога в growth-engine | См. Conflict C3, Missing D6 |
| `tools/openai-image-pipeline/*.py` (5 скриптов + 4 теста) | Script | Stage A (генерация сцены), Stage B (детерминированный композитинг обложки), registry, verify | Частично — код написан и протестирован (22 юнит-теста), но **ни разу не выполнялся против реального OpenAI API** (нет ключа) | growth-engine `automation-openai-images.md` описывает тот же инструмент операционно | `OPENAI_API_KEY` не задан в текущем окружении (см. P0 №4) |
| `product-assets/approved-master-covers/` | Reference data (committed assets) | Хранилище approved обложек с SHA-256 pin | Частично — только 1 из 4 обложек (`Olivia and the Enchanted Bunny`) реально закреплена (pinned) | — | 3 из 4 зарегистрированных названий не могут пройти детерминированный композитинг прямо сейчас (см. P0 №5) |
| `.agents/skills/` + `.claude/skills/` (12 Remotion-скиллов) | Skill (сторонний, github `remotion-dev/skills`) | Remotion API reference | Частично — сам факт установки подтверждён (`skills-lock.json`), реальный рендер в этой сессии не выполнялся | `shared/production-tools/remotion-video-pipeline.md` явно указывает, какие 6 из 12 скиллов реально нужны LiorTales, а какие (maps/saas/interactivity/upgrade) — нет | Не проблема — уже самодокументировано как "не всё используется", см. H |
| `outputs/{drafts,approved,published,reports}/` | пустые стабы | Заявленная структура хранения | NO (только .gitkeep) | — | Referenced (`daily-content/README.md` §OUTPUT STORAGE), но реально ни разу не заполнялось |
| "Improvement Log" | упомянут по имени в `visual-identity-guide.md`, но **файла не существует** | Должен накапливать production learnings | Фактически подменён: learnings руками вписываются прямо в текст `visual-identity-guide.md` §12 ("Production learning (2026-08-11, round 1/2)") | — | Ссылка на несуществующий артефакт; см. G (Missing) — по инструкции пользователя файл **не создаётся** в рамках этого аудита |

### Система B — global Skill `liortales-growth-engine` (вне git-репозитория)

| NAME | TYPE | PURPOSE | ACTUALLY USED | OVERLAPS WITH | POTENTIAL PROBLEM |
|---|---|---|---|---|---|
| `SKILL.md` (~4 КБ) | Skill entrypoint | REVIEW_MODE/AUTO_MODE, mandatory 8-step workflow, one-time publish commands (`PUBLISH`, `ПУБЛИКУЙ`) | YES — **usageCount: 1** во всём аккаунте (см. `~/.claude.json` → `skillUsage`), вызван мной же в предыдущем ходе этой сессии | `workflows/daily-content/README.md` (система A) — покрывает ту же задачу другой последовательностью | Два несовместимых entry-point для "сделать контент LiorTales" (см. раздел 3) |
| `references/brand-and-product.md` | Reference File | Brand + Product Bible v2.0/v1.0 (по названию файла — другая версия, чем в репозитории) | YES (загружается по требованию) | `shared/brand/brand-bible.md` + `shared/product/product-bible.md` | Conflict C1, C2, C5 — самые серьёзные во всём аудите |
| `references/visual-identity.md` | Reference File | Visual Identity Guide v2.0 (тоже другая версия) | YES | `shared/brand/visual-identity-guide.md` | Conflict C4, C5 |
| `references/platforms-and-content.md` | Reference File | Social Media Playbook v2.0 | YES | `shared/platform-rules/platform-and-publishing-policy.md` | Conflict C7 |
| `references/approvals-and-agents.md` | Reference File | LiorTales AI Team Manual v2.0 — своя ролевая модель "Agent 01–06" | YES | Все 8 agents/*/README.md системы A | Conflict C6 |
| `references/automation-metricool-canva.md` | Reference File | Automation Blueprint v2.0 — Metricool/Canva/KlingAI execution | YES | Нет прямого аналога в системе A (там это разбросано по Agent 05/06/08) | Хорошо: явно ссылается на "core skill" и явно требует, чтобы уже готовое OpenAI-изображение просто передавалось в Canva — концептуально совпадает с новым §12, но не знает о его существовании |
| `references/automation-openai-images.md` | Reference File | Операционная выжимка OpenAI-пайплайна | YES | `shared/production-tools/openai-image-pipeline.md` | **Единственный настоящий мост между системами** — но устарел относительно нового §12 (см. C4) |
| `references/analytics-and-learning.md` | Reference File | Market/Customer/Performance Intelligence Manual v1.1 | YES | `agents/02`, `agents/08` (система A) | Разные пороги/формулы для "что считать успехом поста" — не противоречат по духу, но дают разные конкретные числа |
| `references/reels.md` | Reference File | Reels workflow (KlingAI-only) | YES | `agents/06-reels-video-producer/README.md` + `remotion-video-pipeline.md` | Conflict C3 — **отсутствует Remotion вообще**, отсутствует fallback-цепочка |

### Прочее (session/platform-level, не специфично для LiorTales)

| NAME | TYPE | PURPOSE | ACTUALLY USED | RELEVANT? |
|---|---|---|---|---|
| `custom-picture-book` (global Skill) | Skill | Реальный флоу заказа книги для Etsy (сюжет + DALL-E промпты + печатный HTML) | UNVERIFIED в этой сессии | Смежная, но **отдельная** система — продукт (сама книга), а не маркетинг. Не конфликтует с A/B, т.к. решает другую задачу |
| `session-start-hook`, `morning`, `skill-creator`, `docx`, `pdf`, `pptx`, `xlsx` (global Skills) | Skill | Общие Anthropic/пользовательские утилиты | N/A | Не относятся к LiorTales, не создают конфликтов |
| `stop-hook-git-check.sh`, `stop-hook-reply-gate.py`, `user-prompt-submit-reply-reminder.py` | Hook (platform-level, `~/.claude/`) | Git-гигиена перед завершением хода; Slack-специфичная подсказка (не активна вне Slack) | YES, `stop-hook-git-check.sh` реально срабатывал в этой сессии (требовал commit/push) | Не настраиваются проектом, не специфичны для LiorTales; не найдено `hooks` в `~/.claude.json` или в каком-либо `settings.json` — эти хуки зашиты в runtime, а не в конфиг проекта |
| MCP-коннекторы: `Canva`, `KlingAi`, `github`, `metricool`, `Gmail`, `Google_Drive`, `Claude_Code_Remote` | MCP / Connector | Внешние инструменты | UNVERIFIED в моменте — в течение этой самой сессии наблюдалось и отключение, и переподключение сервера | Управляются платформой (Cowork/CCR), не файлами репозитория; `~/.claude.json` → `projects["/home/user/LiorTales-Ai-Studio"].mcpServers` пуст — то есть ни один из них не задан на уровне проекта |
| `OPENAI_API_KEY` | Env var (не MCP) | Ключ для `generate_scene.py` | **NO — подтверждено `NOT SET`** в этой сессии дважды (при первой попытке и непосредственно перед последним тестом) | Блокирует Stage A обеих систем (P0 №4) |
| `CLAUDE.md` / `CLAUDE.local.md` | — | — | **Не существует ни в репозитории, ни глобально** | См. Missing G |
| `.claude/rules`, `.claude/agents`, repo-level `settings.json` | — | — | **Не существует** | См. Missing G |

---

## 3. ТЕКУЩИЙ WORKFLOW (как система работает СЕЙЧАС, фактически)

Существует не один, а **два** фактических workflow. Какой из них выполняется — зависит от того, как пришёл запрос, а не от содержания задачи.

### Workflow A — прямая работа с репозиторием (использовался всю эту сессию до предыдущего хода)

```
Сообщение пользователя в Claude Code-сессии с открытым LiorTales-Ai-Studio
  → Claude вручную читает нужные agents/*/README.md и workflows/*.md по необходимости
    (никакого автозагруженного контекста нет — нет CLAUDE.md)
  → Claude последовательно "играет" роли Agent 01→02→03→04→05→(06)→07→08,
    строго по workflows/daily-content/README.md (9 стадий + pre-production gate)
  → инструменты по мере надобности: tools/openai-image-pipeline/*.py (Bash),
    Canva MCP, KlingAI MCP, Metricool MCP, Remotion-скиллы
  → Agent 07 (QC) — тот же самый Claude-поток, что производил контент, применяет
    17 QC-областей к тому, что сам только что произвёл
  → AWAITING_OWNER_APPROVAL → Daryna одобряет текстом в чате
  → Agent 08 = снова тот же поток, публикация через доступные инструменты
  → изменения правил коммитятся и пушатся в git (это единственная персистентность)
```

### Workflow B — вызов Skill `liortales-growth-engine` (использован один раз, в предыдущем ходе этой сессии)

```
Сообщение пользователя (или срабатывание триггера Skill по описанию/имени/Routine)
  → инструмент Skill загружает SKILL.md (~4 КБ) целиком
  → по необходимости подгружаются references/*.md (8 файлов, ~74 КБ суммарно) —
    не всегда все сразу, задача определяет какие
  → внутренний 8-шаговый Mandatory workflow (свой, НЕ совпадает по шагам с Workflow A):
    load context → тренды → Metricool → recency guard → objective → content package
    → IG→FB адаптация → создание ассета по "правильному маршруту" → gate check
    → REVIEW_MODE: показать пакет и остановиться
  → внутри себя Skill переключается между 6 своими ролями ("Agent 01"–"Agent 06" —
    другие роли, чем в системе A, см. Conflict C6)
  → для Reels — читает references/reels.md (KlingAI ТОЛЬКО, без Remotion)
  → для картинок с обложкой — читает references/automation-openai-images.md,
    которая корректно указывает на тот же репозиторий tools/openai-image-pipeline/
  → публикация — напрямую через metricool:createScheduledPost, без отдельного
    "Agent 08"; либо ждёт одну из явных команд (PUBLISH/ПУБЛИКУЙ/SCHEDULE/ЗАПЛАНИРУЙ)
```

**Главный вывод раздела 3:** это не варианты одного процесса — это две **разные** реализации, с разной нумерацией ролей, разными файлами источника правды, разным поведением при сбое Kling (см. Conflict C3), и почти без связи друг с другом. Какая из них "сработает" в следующий раз — зависит от формулировки запроса и от того, распознает ли триггер Skill свою собственную зону ответственности первым.

---

## 4. ЧТО УЖЕ РАБОТАЕТ ХОРОШО (не трогать)

- **Внутренняя согласованность системы A.** Все 8 `agents/*/README.md` и `workflows/pipeline-control-rules.md` перекрёстно ссылаются друг на друга без обнаруженных внутренних противоречий: единая таксономия anti-repetition (§5), единый Handoff-контракт к Agent 05 (§6), единая ревизионная кап-политика (§1), единый Product Asset Lock (§9), единый Handheld Gate (§10), единая video-routing логика (§11), единый новый static-routing (§12). Ни одного дублирования правила с расхождением формулировки внутри самой системы A не найдено.
- **Product Asset Lock механизм (§9) и его инструментальная реализация** (`covers_registry.json` + SHA-256 pin + `compose_cover.py`, отказ при несовпадении хэша, `.manifest.json` как аудиторский след, `verify_composite.py` как повторная проверка). Логика проверена 22 юнит-тестами, работает без реального API-ключа (тесты синтетические). Чёткое разделение "что генерирует OpenAI" / "что композитит детерминированный скрипт" нигде не нарушается ни в одном прочитанном файле системы A.
- **Handheld Capability Gate (§10)** — редкий пример правила, которое явно признаёт границу возможностей инструмента вместо того, чтобы делать вид, что проблемы нет.
- **Committed product-assets вместо gitignore** — решает реальную проблему эфемерных контейнеров; обоснование задокументировано прямо в `product-assets/approved-master-covers/README.md`.
- **Разделение FACT / INFERENCE / OBSERVED_PATTERN / RECOMMENDATION**, последовательно применяемое в Agent 02/03/08 системы A и в growth-engine `analytics-and-learning.md` одинаково — рабочий, повторяющийся паттерн, не проблема.
- **Anti-repetition как отдельная каноническая таксономия (§5)**, на которую ссылаются, а не которую копируют — хороший пример правильного применения "reference, not restate".
- **Remotion-интеграция (§11)** явно документирует, какие 6 из 12 установленных скиллов реально нужны, а какие — нет, и почему. Не создаёт лишней когнитивной нагрузки.
- **growth-engine `automation-openai-images.md`** — единственный файл в системе B, который явно и корректно признаёт репозиторий источником истины, а не пытается заново описать логику по-своему. Это правильная модель для остальных файлов системы B (но она не была применена к остальным семи).

---

## 5. ЧТО НЕ РАБОТАЕТ ИЛИ РАБОТАЕТ ПЛОХО

### CONTENT QUALITY

Это не гипотеза — это **уже подтверждённая, дважды повторившаяся история** внутри самого репозитория:

- `visual-identity-guide.md` §12, "Production learning (round 1)": реальная карусель провалила QC — плоские кремовые фоны на 4 из 6 слайдов, почти нет живых изображений.
- То же, "Production learning (round 2)": после фикса round 1 карусель снова провалила QC — на этот раз из-за повторяющейся композиции (3 слайда подряд с одинаковой структурой "фото + тёмный оверлей + текст").
- Round 3 (OpenAI-primary, §12 + STORYBOARD) реализован в правилах **в этой же сессии, прямо перед данным аудитом**, но **ни разу не проверен на реальном сгенерированном изображении** — блокировано отсутствующим `OPENAI_API_KEY` (см. P0 №4). Это значит: третий раунд исправления content quality существует только как текст правил, не как проверенный результат.

### PRODUCT ASSET FIDELITY

Механизм защиты — сильный (см. раздел 4), но:
- Он **полностью отсутствует в системе B**, кроме одного узкого моста (`automation-openai-images.md`), который сам устарел относительно нового §12 (Conflict C4). Остальные файлы growth-engine (`visual-identity.md`) описывают генерацию картинок в общих словах ("Generate 3–4 options; select by brand fit"), без единого упоминания SHA-256, registry, `compose_cover.py`, или запрета на масштабируемую generative-правку обложки.
- Реально запинена только **1 из 4** зарегистрированных обложек (см. P0 №5) — значит формально существующая защита сейчас работоспособна только для одной книги.

### VIDEO

- Система A: Agent 06 + §11 реализуют полноценный KLING/REMOTION/KLING_PLUS_REMOTION маршрут с обязательной проверкой Remotion перед статичным fallback (§4). Это именно то, что просил пользователь ("не должно останавливать workflow, если Kling недоступен").
- Система B (`reels.md`): при недоступности Kling — **жёсткая остановка** (`AI_REEL_GENERATION_STOPPED`), без единого упоминания Remotion где-либо в файле, без static-fallback. Это прямо противоречит цели, ради которой в этой сессии строилась Remotion-интеграция (см. Conflict C3, P0 №2).
- Конкретный чек-лист, который просил пользователь (realistic AI child, vertical 9:16, first-second hook, direct camera engagement, expressive facial reactions, natural gestures, natural lip-sync, energetic delivery, warm lifestyle environment) — **частично покрыт**, но не как единый явный список ни в одной из систем. Vertical 9:16 и first-second hook — есть в обеих. "Direct camera engagement", "natural lip-sync" как явно названный критерий, "energetic delivery" — не сформулированы отдельно нигде, есть только более общие "REALISTIC EMOTION" (Agent 06) и "Voiceover... warm, genuine, calm" (growth-engine `reels.md`) без явного требования энергичности. UNVERIFIED, реально ли сгенерированное видео этому соответствует — ни один реальный Kling-рендер в этой сессии не оценивался.

### QC

- **Формально** независимая проверка существует в обеих системах: Agent 07 (система A) прямо запрещено генерировать что-либо ("reviews only"); growth-engine прямо пишет "**The Guardian may not approve its own earlier creative work**".
- **Структурно** это правило соблюдается только на уровне текста инструкции, а не на уровне реальной изоляции контекста: и в системе A, и в системе B "Agent 05" (или growth-engine's "Content agent") и "Agent 07"/"Brand & Visual Guardian" — это **одна и та же модель в одном и том же потоке диалога**, без раздельных Subagent-контекстов (в репозитории нет `.claude/agents/`, никакой из "агентов" не оформлен как настоящий SDK Subagent). Это значит: QC-шаг физически видит собственные предыдущие рассуждения по производству того же ассета. Это не нарушение написанных правил, но это реальный риск для их духа ("не проверяет ли основной creator фактически сам себя" — да, в текущей архитектуре структурно да, компенсируется только дисциплиной следования инструкции, а не изоляцией).
- PASS/FAIL существует чётко в обеих системах. После FAIL: система A — чёткий revision-cycle cap (§1, max 3), эскалация в Agent 01. Система B — менее формализовано ("Manual review after second failure"), нет явного числового потолка ревизий.

### CONTEXT

- Явного context overload не выявлено внутри одной системы (A или B по отдельности) — каждая написана с явной практикой "canonical file, reference not restate".
- Overload риск существует **между системами**: если задача требует прочитать оба источника правды (что не было явно указано ни разу до этого аудита), суммарный объём — вся система A (десятки файлов) + весь growth-engine (SKILL.md + 8 reference-файлов, ~78 КБ) одновременно.
- Дублирование критических правил (child safety, no-fabrication, Etsy-not-a-platform) присутствует, но признано пользователем нормальным и не автоматически ошибкой — см. раздел 7.

---

## 6. CONFLICTS

**CONFLICT C1 — Personalization mechanics**
FILE/RULE A: `shared/product/product-bible.md` §3 — "Any specific personalization field or option... `STATUS: TBD`, `PUBLIC CLAIM: PROHIBITED UNTIL CONFIRMED`".
FILE/RULE B: growth-engine `references/brand-and-product.md`, "Personalization depth standard" — заявляет как подтверждённое: "Personalization must affect setting, central challenge, helper/companion, choices, payoff, resolution... At least three meaningful story elements beyond the name must respond to customer inputs."
WHAT CLAUDE MAY DO BECAUSE OF THIS: работая через систему B, заявить публично конкретный, детальный механизм персонализации, который система A прямо запрещает утверждать до подтверждения Дарьей.
SEVERITY: **CRITICAL**

**CONFLICT C2 — Etsy: уже открыт или ещё нет**
FILE/RULE A: `shared/product/product-bible.md` §6 — "Confirmed: Etsy is the primary sales destination **currently used** by LiorTales."
FILE/RULE B: growth-engine `references/platforms-and-content.md` — "Do not imply the Etsy shop is open until approval is confirmed"; `references/brand-and-product.md` hard rule — "Etsy / shop / purchase CTA when no approved Etsy link exists."
WHAT CLAUDE MAY DO BECAUSE OF THIS: в системе A — законно использовать Etsy CTA как уже подтверждённый канал; в системе B — обязано его блокировать как неподтверждённый. Прямое противоречие о текущем статусе бизнеса, не просто о стиле формулировки.
SEVERITY: **CRITICAL**

**CONFLICT C3 — Что делать при недоступности Kling**
FILE/RULE A: `workflows/pipeline-control-rules.md` §4/§11 + `agents/06-reels-video-producer/README.md` — сначала проверить Remotion, потом (если не подходит) статичный fallback через Agent 01/05, концепция сохраняется.
FILE/RULE B: growth-engine `references/reels.md` — "If the KlingAI connector or a required generation function is unavailable, return only: `AI_REEL_GENERATION_STOPPED`... NEED: enable the KlingAI connector." Remotion нигде в файле не упомянут; static fallback не упомянут.
WHAT CLAUDE MAY DO BECAUSE OF THIS: работая через систему B, полностью останавливать рабочий день/концепцию при недоступности Kling, вместо использования уже построенной в этой сессии Remotion/static-fallback инфраструктуры.
SEVERITY: **CRITICAL** (прямо противоречит цели, ради которой строилась Remotion-интеграция)

**CONFLICT C4 — Охват OpenAI-primary для карусели**
FILE/RULE A: `workflows/pipeline-control-rules.md` §12 + `agents/05-visual-creative-director/README.md` §STORYBOARD / §PRIMARY VISUAL GENERATION ROUTE (только что добавлены в этой сессии) — OpenAI обязателен как основной генератор **для всего core imagery карусели**, не только для слайдов с обложкой; обязателен storyboard до генерации.
FILE/RULE B: growth-engine `references/automation-openai-images.md` — область применения ограничена явно: "for any content depicting an approved LiorTales book cover"; `references/visual-identity.md` — "Image generation rules" не называет конкретный движок вообще, storyboard не требуется.
WHAT CLAUDE MAY DO BECAUSE OF THIS: работая через систему B, для 5 из 6 типичных слайдов карусели (без обложки в кадре) не применять OpenAI-primary маршрут вообще — вернуться к тому самому паттерну (неясный/Canva-driven генератор), из-за которого произошли оба зафиксированных провала QC (round 1 и round 2, см. раздел 5).
SEVERITY: **HIGH** (риск свежий — правило системы A написано только что и физически не могло попасть в систему B)

**CONFLICT C5 — Статус цветовой палитры бренда**
FILE/RULE A: `shared/brand/visual-identity-guide.md` §8 — "No official brand-color system... `STATUS: TBD`... Do not invent or present any color as an official brand color."
FILE/RULE B: growth-engine `references/visual-identity.md` — таблица с конкретными hex-значениями, одно из них помечено `Status: Active` ("Warm charcoal #2C2C2C").
WHAT CLAUDE MAY DO BECAUSE OF THIS: через систему B трактовать конкретный hex как минимум частично официальный, хотя система A явно это запрещает.
SEVERITY: **MEDIUM**

**CONFLICT C6 — Нумерация "Agent 0N" означает разное**
FILE/RULE A: `agents/01`…`agents/08` — Content Director, Competitor Intel, Strategist, Copywriter, Visual Director, Video Producer, QC, Publisher.
FILE/RULE B: growth-engine `references/approvals-and-agents.md` — "Agent 01" = Brand & Visual Guardian (≈ QC системы A, там это Agent 07!), "Agent 04" = Product & Listing Optimizer (в системе A Agent 04 — копирайтер).
WHAT CLAUDE MAY DO BECAUSE OF THIS: инструкция вида "передай это Agent 01" или "почини правило Agent 04" неоднозначна между системами и может быть направлена не туда.
SEVERITY: **MEDIUM** (процессный риск, не риск прямого вывода контента)

**CONFLICT C7 — Список платформ**
FILE/RULE A: `shared/platform-rules/platform-and-publishing-policy.md` — Instagram, Facebook, Pinterest, TikTok, YouTube, Reddit, **Threads**.
FILE/RULE B: growth-engine `references/platforms-and-content.md` — те же 6, без Threads; при этом описание самого Skill в манифесте сужает область ещё сильнее: "for US Instagram and Facebook" (то есть даже собственные 6 платформ growth-engine не совпадают с описанием самого Skill).
WHAT CLAUDE MAY DO BECAUSE OF THIS: неясно, входит ли Threads (и вообще TikTok/Pinterest/YouTube/Reddit) в объём работы, когда используется growth-engine.
SEVERITY: **LOW–MEDIUM**

---

## 7. DUPLICATIONS

**RULE: Anti-repetition / recency guard**
Где повторяется: `workflows/pipeline-control-rules.md` §5 + `agents/02/03/07` (система A, единая таксономия NEW/ACCEPTABLE_ITERATION/TOO_REPETITIVE) **и** growth-engine `platforms-and-content.md` ("Recency and repetition guard": конкретные числа — 7/14 дней, "не тот же visual mode два дня подряд") **и** `reels.md` (свои требования к объёму research).
IS THIS HARMFUL: **YES, частично** — не вредно как принцип (двойная защита — это нормально), но вредно в том, что конкретные пороги разные и метод разный (классификация vs. жёсткие числовые окна). Один и тот же контент-план может пройти проверку в одной системе и не пройти в другой.

**RULE: No-fabrication / product-truth**
Где повторяется: почти в каждом `agents/*/README.md` системы A (HARD RULES каждого агента) **и** growth-engine `brand-and-product.md`, `reels.md`, `analytics-and-learning.md`.
IS THIS HARMFUL: **NO** — это ровно тот случай, который сам пользователь просил не считать ошибкой: критическое правило безопасности, повторённое в разных местах намеренно.

**RULE: Child safety**
Где повторяется: `brand-bible.md` §12, `agents/06` (CHILD SAFETY), `agents/07` (area 9) **и** growth-engine `brand-and-product.md`, `reels.md`.
IS THIS HARMFUL: **NO**, по той же причине.

**RULE: "Etsy — не социальная платформа"**
Где повторяется: `agents/01`, `02`, `03`, `04`, `08` (каждый раз коротким напоминанием + ссылкой на канонический файл `platform-and-publishing-policy.md`).
IS THIS HARMFUL: **NO** — образцовый пример "ссылка + короткое локальное напоминание", а не полное копирование правила.

**RULE: OpenAI image-pipeline описание**
Где повторяется: `shared/production-tools/openai-image-pipeline.md` (контракт) + `tools/openai-image-pipeline/README.md` (CLI-справка) — оба в системе A, разные уровни детализации, не конфликтуют. Плюс growth-engine `automation-openai-images.md`, который явно ссылается на репозиторий как источник истины.
IS THIS HARMFUL: **NO** сам по себе — вред не в дублировании, а в том, что скилл-версия отстала по содержанию (см. Conflict C4, это уже посчитано там, не второй раз).

---

## 8. АРХИТЕКТУРА ПО ПРИНЦИПУ (где что должно жить)

| Категория (по инструкции) | Где сейчас | На своём ли месте? |
|---|---|---|
| Permanent project rule → CLAUDE.md / project context | **Нет ни одного CLAUDE.md** ни в репозитории, ни глобально | **НЕТ** — постоянные правила живут в обычных `.md`-файлах, которые Claude должен явно прочитать; ничего не подгружается автоматически при открытии проекта. Реальная проблема обнаружения (discoverability), не проблема содержания. |
| Repeatable workflow → Skill | `workflows/daily-content/README.md` (система A, НЕ оформлен как Skill) vs. `SKILL.md` growth-engine (система B, оформлен как настоящий Skill) | **Частично не на месте**: в системе A повторяемый workflow оформлен просто как markdown, который нужно вручную инициировать построчным чтением — не как вызываемый Skill. В системе B — правильно оформлен как Skill, но с несовпадающим содержанием. |
| Independent specialist reasoning → Subagent | 8 "агентов" системы A и 6 ролей системы B — оба реализованы как **роли внутри одного потока**, не как настоящие SDK Subagents (`.claude/agents/` не существует нигде) | **Не на месте относительно буквального принципа**, но это осознанный, работающий компромисс (см. раздел N/QC) — не факт, что нужно менять, см. K ниже |
| External tool/data → MCP / Connector | Canva/KlingAI/GitHub/Metricool/Gmail/Google Drive — управляются платформой, не файлами репозитория | **На своём месте** |
| Guaranteed deterministic action → Hook / permission | `compose_cover.py` — не hook, а обычный Python-скрипт, вызываемый вручную через Bash | **Частично не на месте**: гарантированность (отказ при несовпадении хэша) реализована внутри самого скрипта — это работает, но не является настоящим platform-level hook/permission gate, который нельзя обойти случайным альтернативным путём (например, ничто не мешает буквально вставить картинку в Canva руками, минуя скрипт) |
| Reference knowledge → reference file | `shared/*.md` — да, корректно | **На своём месте** |
| Learned recurring observation → Memory / Improvement Log | Записывается вручную прямо в `visual-identity-guide.md` §12 ("Production learning...") вместо отдельного лога | **Не на своём месте относительно того, что сам файл подразумевает** ("add to the existing Improvement Log if one exists") — лога не существует, поэтому это разумный, но незапланированный обходной путь |

---

## 9. ERROR / IMPROVEMENT LOG (реконструирован для этого аудита, отдельного файла-лога в проекте не существует)

| PROBLEM | OBSERVED BEHAVIOR | LIKELY ROOT CAUSE | CURRENT LOCATION OF RULE | CORRECT PLACE TO FIX | PRIORITY |
|---|---|---|---|---|---|
| Две несовместимые системы правил для одного бизнеса | Разные ответы на "актуален ли Etsy", "подтверждена ли персонализация", "что делать при сбое Kling" | Growth-engine Skill создан/синхронизирован независимо от репозитория, без единого источника правды между ними | `references/*.md` (growth-engine) vs `shared/*.md` + `workflows/*.md` (репозиторий) | Нужно явное решение, какая система — канонический источник правды, и мост от другой к ней (не в рамках этого аудита — только фиксация факта) | **P0** |
| `OPENAI_API_KEY` не задан | Обе попытки реального теста в этой сессии остановились на этом | Ключ так и не был предоставлен через секрет-хранилище окружения после первого запроса | `tools/openai-image-pipeline/openai_client.py` (корректно требует env var, не баг кода) | Настройка окружения (вне контроля Claude) | **P0** |
| Только 1 из 4 обложек реально запинена | `covers_registry.json`: 3 записи с `sha256: null` | Файлы обложек для остальных 3 книг ещё не были получены/загружены человеком | `product-assets/approved-master-covers/` | Получить файлы от Дарьи, подтвердить визуально, запинить `covers_registry.py pin` | **P0** (для этих 3 конкретных книг — не блокирует уже готовую Olivia) |
| growth-engine `reels.md` не знает про Remotion | Жёсткая остановка при недоступности Kling, без проверки Remotion/static fallback | Growth-engine Skill написан/обновлялся до (или независимо от) добавления Remotion в репозиторий в этой сессии | `references/reels.md` | `references/reels.md` (growth-engine) | **P0** |
| growth-engine устарел относительно нового §12 (OpenAI-primary для всей карусели) | `automation-openai-images.md` и `visual-identity.md` описывают более узкий/более неопределённый охват генерации изображений | §12 добавлен в этой же сессии, непосредственно перед этим аудитом; growth-engine не мог быть синхронизирован | `references/automation-openai-images.md`, `references/visual-identity.md` | Те же файлы | **P0** (свежий риск дрейфа) |
| Agent 07 (или "Brand & Visual Guardian") структурно не изолирован от создателя контента | Нет отдельных Subagent-контекстов; всё — один поток | Архитектурный выбор с самого начала (роли как md-инструкции, не SDK subagents) | Обе системы | Не факт, что требует изменения — см. K; как минимум стоит явно признать это ограничение в самих QC-разделах | **P1** |
| Конфликт по цветовой палитре | Repo: TBD/запрещено изобретать; growth-engine: таблица с "Active" hex | Обновления в разное время, без синхронизации | `visual-identity-guide.md` §8 vs growth-engine `visual-identity.md` | growth-engine `visual-identity.md`, либо repo, в зависимости от того, что реально утверждено Дарьей | **P1** |
| Коллизия нумерации "Agent 0N" | Одинаковые номера — разные роли между системами | Growth-engine спроектирован независимо, с собственной 6-ролевой моделью | `references/approvals-and-agents.md` | Там же — переименовать роли growth-engine, чтобы не пересекались с номерами системы A | **P1** |
| Список платформ не совпадает (Threads) | Repo включает Threads, growth-engine — нет; собственное описание Skill сужает до IG+FB | Независимые редакции | `platform-and-publishing-policy.md` vs growth-engine `platforms-and-content.md` + сам SKILL.md | growth-engine файлы | **P2** |
| "Improvement Log" упомянут, но не существует | Ссылка в `visual-identity-guide.md` §12 указывает на артефакт, которого нет | Возможно, предполагался, но не был создан; вместо этого learnings пишутся прямо в текст | `shared/brand/visual-identity-guide.md` §12 | Либо создать файл, либо убрать формулировку "if one exists" (сама формулировка это уже предвидела) | **P2** |
| Пустые нереализованные заглушки (`workflows/manual-content/`, `workflows/performance-feedback/`, `shared/analytics/`, `shared/research/`) | Только `.gitkeep`, нигде не упоминаются в реальной логике | Зарезервированы заранее, не реализованы | Структура директорий | Не срочно — не создают конфликтов | **P3** |
| Разные пороги/формулы "что считать успешным постом" | Repo (`agents/08`) — качественное описание (FACT/INFERENCE и т.д.); growth-engine — конкретные численные пороги (2.0×, ≥10 постов baseline, opportunity score-формула) | Независимые редакции разного уровня детализации | `agents/08-publisher-performance-analyst/README.md` vs growth-engine `analytics-and-learning.md` | Не обязательно конфликт — growth-engine просто детальнее; стоит решить, наследует ли repo эти пороги как канонические | **P2** |

---

## 10. (см. преамбулу) — PRESERVE WHAT WORKS. FIX WHAT DOESN'T.

Этот аудит **не предлагает** пересборку, новый проект, массовое переписывание Skills или удаление Agents. Все находки выше сформулированы как факты + серьёзность, без предложенных исправлений — по прямой инструкции.

---

## 11. ФИНАЛЬНЫЙ ОТЧЁТ

### A. WHAT EXISTS NOW
См. разделы 1–2 (полный inventory). Кратко: 1 git-репозиторий с 8 ролевыми md-"агентами", каноническим `pipeline-control-rules.md` (§1–§12), брендовыми/продуктовыми reference-файлами, Python-инструментом детерминированного композитинга обложек, 12 установленными Remotion-скиллами, product-assets с частичным hash-pinning; + 1 независимый глобальный Skill `liortales-growth-engine` с 8 собственными reference-файлами и собственной 6-ролевой моделью; + смежный, не пересекающийся Skill `custom-picture-book` (реальное производство книг для Etsy); + platform-level hooks и MCP-коннекторы, не специфичные для LiorTales.

### B. CURRENT WORKFLOW
См. раздел 3. Два независимых workflow (A — репозиторий, B — Skill), не синхронизированных между собой.

### C. WHAT WORKS — DO NOT TOUCH
См. раздел 4.

### D. WHAT IS BROKEN
См. раздел 5.

### E. CONFLICTS
См. раздел 6 — 7 задокументированных конфликтов, 3 CRITICAL, 1 HIGH, 2 MEDIUM, 1 LOW-MEDIUM.

### F. DUPLICATIONS
См. раздел 7 — 5 найдено, 3 признаны безвредными (по критерию самого запроса), 2 признаны вредными.

### G. MISSING COMPONENTS
- `CLAUDE.md` / `CLAUDE.local.md` — не существует нигде (ни в репозитории, ни глобально).
- `.claude/rules`, `.claude/agents`, project-level `settings.json`/permissions в этом репозитории — не существуют.
- Отдельный файл "Improvement Log" — упомянут по имени, не создан.
- Мост от growth-engine к большей части системы A (§9/§10/§11/§12 pipeline-control-rules, Handheld Gate, Storyboard-требование, Competitor Comparison Gate, revision-cycle cap) — не существует, кроме одного узкого файла про OpenAI images.
- Remotion — полностью отсутствует в growth-engine.

### H. UNUSED COMPONENTS
- `workflows/manual-content/`, `workflows/performance-feedback/`, `shared/analytics/`, `shared/research/`, `outputs/*` — пустые стабы.
- 4 из 12 Remotion-скиллов (`remotion-maps`, `remotion-saas`, `remotion-interactivity`, `remotion-upgrade`) — установлены, но сам репозиторий уже документирует их как ненужные для LiorTales.
- 3 из 4 зарегистрированных обложек книг — без файла/пина, нефункциональны для детерминированного композитинга прямо сейчас.
- growth-engine Skill в целом — **usageCount: 1** за всё время аккаунта (вызван мной в предыдущем ходе этой сессии) — то есть фактически не использовался в реальном производстве до сих пор.

### I. CONNECTORS / MCP STATUS
Canva, KlingAI, GitHub, Metricool, Gmail, Google Drive, Claude_Code_Remote — предоставляются платформой (Cowork/CCR), не конфигурируются файлами репозитория (`~/.claude.json` → `projects[...].mcpServers` пуст). В течение самой этой сессии наблюдалось как минимум одно отключение и повторное подключение MCP-сервера — реальная надёжность в любой конкретный момент **UNVERIFIED**. `OPENAI_API_KEY` — не MCP, обычная переменная окружения; подтверждено **NOT SET**.

### J. SKILLS STATUS
- `liortales-growth-engine` — описание/триггер понятен ("AI Reels with KlingAI, posts, Canva assets, Metricool analytics, trend research, publishing, brand or child-safety audits"), но не пересекается по формулировке с системой A явно. Внутренняя структура (INPUT→PROCESS→OUTPUT→VALIDATION→DONE) присутствует по сути (Mandatory workflow, 11 шагов), но не оформлена в этих терминах явно.
- Remotion-скиллы (12 шт.) — сторонние, из `remotion-dev/skills`, описания/триггеры их собственные, не LiorTales-специфичные; уже отфильтрованы репозиторием до нужных 6.
- `custom-picture-book` — чёткий, узкий триггер, не пересекается с маркетинговыми скиллами.
- Референсные данные внутри Skill (`references/*.md`) правильно вынесены из `SKILL.md` как reference data, а не втиснуты в сам SKILL.md — структурно это сделано верно.

### K. AGENTS STATUS
Все 8 "агентов" системы A и 6 ролей системы B реализованы одинаково — как md-инструкции для ролевой игры внутри одного потока диалога, не как изолированные SDK Subagents (`.claude/agents/` не существует). Нужен ли им реально отдельный context/tools — **не факт**: для последовательного pipeline с явными контрольными точками (Daryna review, revision-cycle cap) текущая модель работает и уже показала себя (round 1/round 2 production learnings были найдены и исправлены). Главный реальный минус этой модели — не производительность, а QC-независимость (см. раздел N) и риск, что при очень длинном контексте "агент" по факту видит рассуждения предыдущих "агентов" вместо чистого входного контракта. Нет доказательств, что это уже вызвало реальную ошибку — отмечается как структурный риск, не как подтверждённый баг.

### L. PRODUCT ASSET FIDELITY STATUS
Сильный, специфичный, протестированный (22 юнит-теста) механизм в системе A: SHA-256 registry pin + отказ компоновщика при несовпадении + manifest как аудиторский след + повторная проверка. Слабые места: (1) реально работает только для 1 из 4 книг прямо сейчас; (2) не может быть проверен на реальном OpenAI-выводе без ключа; (3) практически не существует в системе B за пределами одного файла, который уже отстаёт от последних правил системы A.

### M. VIDEO / REELS STATUS
Система A: полный, современный KLING/REMOTION/KLING_PLUS_REMOTION маршрут с fallback-цепочкой. Система B: только KlingAI, жёсткая остановка при сбое, без Remotion вообще — прямой конфликт с целью, ради которой строилась Remotion-интеграция (Conflict C3, P0). Ни одна система не даёт результата, который уже был бы проверен на реальном рендере в рамках этой сессии — **UNVERIFIED** по факту исполнения.

### N. QC STATUS
Независимая проверка существует **как написанное правило** в обеих системах ("Agent 07 reviews only", "Guardian may not approve its own work") и **не существует как структурная изоляция контекста** ни в одной из них — оба "QC-агента" исполняются тем же потоком, что производил контент. PASS/FAIL — чёткий в обеих. После FAIL: система A формализована (revision-cycle cap = 3, эскалация), система B — менее формализована, без явного числового потолка.

### O. CONTEXT / INSTRUCTION OVERLOAD
Внутри каждой системы по отдельности — нет overload, обе явно практикуют "reference, not restate". Overload и рассинхронизация возникают только **между** системами, если обе когда-либо читаются в одной задаче.

### P. PRIORITIZED ERROR LIST

**P0** — ломает продукт/публикацию/brand fidelity:
1. Две несовместимые системы правды (Etsy-статус, персонализация, video fallback, OpenAI-охват) — см. C1–C4.
2. `OPENAI_API_KEY` не задан — блокирует весь OpenAI-primary пайплайн в обеих системах.
3. growth-engine `reels.md` не знает про Remotion — прямая остановка вместо fallback.
4. growth-engine устарел относительно нового §12 — свежий риск, возник в этой самой сессии.
5. 3 из 4 книг не запинены — детерминированный композитинг для них сейчас невозможен.

**P1** — сильно снижает качество:
6. QC структурно не изолирован от создателя контента ни в одной системе.
7. Конфликт по цветовой палитре бренда (C5).
8. Коллизия нумерации "Agent 0N" (C6).

**P2** — снижает эффективность:
9. Список платформ не совпадает (C7).
10. "Improvement Log" упомянут, но не существует.
11. Разные пороги performance-аналитики между системами.

**P3** — косметическое:
12. Пустые нереализованные директории-заглушки.

### Q. MINIMUM CHANGES REQUIRED

Ниже — не выполненные исправления (по инструкции ничего не менялось), а зафиксированные для будущего решения минимальные изменения, каждое размером в одно точечное редактирование, без переписывания архитектуры:

1. **CHANGE:** Явно обозначить, какая система (A или B) — канонический источник правды для каждой из зон конфликта (Etsy-статус, персонализация, video fallback, охват OpenAI-primary, цветовая палитра).
   **WHY:** сейчас оба источника формально валидны и противоречат друг другу.
   **WHERE:** решение Дарьи; техническая правка — в проигравшем файле каждой пары.
   **WHAT SHOULD BE PRESERVED:** обе системы продолжают существовать как есть в остальном.
   **RISK:** низкий — это уточнение, не перестройка.
   **EXPECTED RESULT:** пропадают C1, C2, C5.

2. **CHANGE:** Добавить Remotion-маршрут и static-fallback в growth-engine `references/reels.md`, синхронно с §4/§11 репозитория.
   **WHY:** сейчас Kling-сбой = полная остановка в системе B, что отменяет весь смысл Remotion-интеграции этой сессии.
   **WHERE:** `references/reels.md` (growth-engine).
   **WHAT SHOULD BE PRESERVED:** весь остальной, работающий контент `reels.md` (originality rules, voiceover/subtitles, production specs — они не конфликтуют ни с чем).
   **RISK:** низкий.
   **EXPECTED RESULT:** пропадает C3, P0 №3.

3. **CHANGE:** Обновить `automation-openai-images.md` и `visual-identity.md` (growth-engine) под новый §12/§STORYBOARD.
   **WHY:** правило только что расширено в репозитории, growth-engine физически не мог это узнать.
   **WHERE:** growth-engine `references/automation-openai-images.md`, `references/visual-identity.md`.
   **WHAT SHOULD BE PRESERVED:** существующая правильная практика этого файла — явная ссылка на репозиторий как источник истины, а не копирование логики.
   **RISK:** низкий.
   **EXPECTED RESULT:** пропадает C4, P0 №4.

4. **CHANGE:** Переименовать 6 внутренних ролей growth-engine так, чтобы не совпадать по номеру с 8 агентами репозитория (например, буквы или собственные имена вместо "Agent 01–06").
   **WHY:** предотвратить неоднозначную маршрутизацию инструкций между системами.
   **WHERE:** `references/approvals-and-agents.md` (growth-engine).
   **WHAT SHOULD BE PRESERVED:** сама модель "одна роль = одна ответственность", она рабочая.
   **RISK:** низкий, чисто номенклатурное изменение.
   **EXPECTED RESULT:** пропадает C6.

5. **CHANGE:** Либо создать файл Improvement Log, либо убрать формулировку "if one exists" из `visual-identity-guide.md` §12 в пользу явного "learnings are recorded inline in this section".
   **WHY:** убрать ссылку на несуществующий артефакт.
   **WHERE:** `shared/brand/visual-identity-guide.md` §12.
   **RISK:** минимальный.
   **EXPECTED RESULT:** пропадает P2 №10.

6. **CHANGE:** Получить оставшиеся 3 файла обложек от Дарьи и запинить их.
   **WHY:** сейчас деterministic-композитинг работает только для одной из четырёх книг.
   **WHERE:** `product-assets/approved-master-covers/` + `covers_registry.py pin`.
   **RISK:** нет (чисто операционный шаг, не архитектурный).
   **EXPECTED RESULT:** пропадает P0 №5.

7. **CHANGE:** Настроить `OPENAI_API_KEY` в секрет-хранилище окружения сессии.
   **WHY:** без него весь OpenAI-primary пайплайн (обе системы) не может быть проверен на реальном выводе.
   **WHERE:** конфигурация окружения (вне git-репозитория).
   **RISK:** нет.
   **EXPECTED RESULT:** пропадает P0 №2.

### R. THINGS THAT SHOULD NOT BE CHANGED
- Внутренняя структура и нумерация 8 агентов системы A — работает, нет доказательств проблем.
- Product Asset Lock механизм (§9/§10) и его код — работает, протестирован, не трогать.
- `workflows/pipeline-control-rules.md` как единый канонический файл — не дробить.
- Практика "ссылка, а не копия" для критических правил (child safety, no-fabrication, Etsy-classification) — не менять, не консолидировать искусственно.
- Remotion-скиллы как есть, включая неиспользуемые 4 — не удалять, они не создают проблем, удаление ради красоты не требуется.
- `custom-picture-book` — отдельная, не пересекающаяся система, не трогать в рамках этой задачи.

### S. RECOMMENDED ORDER OF FIXES
1. Решение Дарьи по каждому CRITICAL-конфликту (C1, C2, C3) — без этого любое техническое исправление рискует закрепить неверный ответ.
2. Синхронизировать `reels.md` growth-engine с Remotion/fallback-логикой репозитория (C3) — самое конкретное, самое проверяемое исправление.
3. Синхронизировать `automation-openai-images.md`/`visual-identity.md` growth-engine с новым §12 (C4) — тоже конкретно и срочно, риск свежий.
4. Настроить `OPENAI_API_KEY` и получить оставшиеся 3 обложки — операционные, не архитектурные шаги, разблокируют реальную проверку round-3 content-quality фикса.
5. Разрешить конфликт по цветовой палитре (C5) и переименовать роли growth-engine (C6) — не срочно, не блокирует продакшн.
6. Список платформ (C7), Improvement Log (P2 №10), пороги аналитики (P2 №11) — низкий приоритет, можно отложить.

---

*Аудит проведён в режиме только чтения. Ни один файл системы A или системы B не был изменён. Этот отчёт — единственный созданный файл.*
