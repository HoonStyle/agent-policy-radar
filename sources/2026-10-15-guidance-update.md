# 모델·하네스 안내 변경 — 2026-10-15

공식 문서를 확인해 추적 목록과 Radar의 로딩 조건 설명을 갱신했다. 이 기록은 개인 지침·모델·effort 기본값의 자동 변경이나 실제 행동 개선을 의미하지 않는다.

## Claude Haiku 5.5

- 10월 7일 출시. 개요·프롬프팅·마이그레이션·변경점 4개를 추가해 등록 소스를 24개에서 28개로 확대했다. 확인 시 `.md` 주소가 403을 반환한 문서는 본문 조회에 성공한 일반 공식 URL로 등록했다.
- 직접 Messages API에서는 `budget_tokens` 대신 adaptive thinking/effort를 사용하고 샘플링 파라미터, assistant prefill, 응답 content의 타입, thinking 블록의 계정·대화 결합 조건을 점검해야 한다. Managed Agents나 Claude Code 지침에 API 이행 규칙을 그대로 복사하지 않는다.
- Haiku 5.5는 강제 `tool_choice`를 허용하고, low/medium/high에서 `thinking: disabled`도 허용한다. Opus·Sonnet의 제한을 모든 5.5 모델의 규칙으로 일반화하면 안 된다.
- 초기 종료·검색 누락·검증 누락 보정 문구는 해당 환경에서 문제가 확인된 경우의 후보로 다룬다. 새 모델 출시만으로 모든 지침을 늘리거나 effort를 올리지 않는다.

근거: [릴리즈 노트](https://platform.claude.com/docs/en/release-notes/overview), [프롬프팅](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-haiku-5-5), [마이그레이션](https://platform.claude.com/docs/en/models/haiku-5-5/migration-guide).

## Claude Code 지침 로딩

Read/Write/Edit뿐 아니라 현재 하네스가 읽기로 인정하는 Bash 조회도 하위 `CLAUDE.md`와 경로 규칙을 로드할 수 있다. `cat`·`head`로 단일 파일을 조회하는 경우 등이 해당하며 파이프·리다이렉션 등 조건을 확인해야 한다. Radar의 예시를 보완했으며, 실제 로딩은 버전·세션 근거로 확인한다. Codex 등 다른 하네스에 이 동작을 가정하지 않는다.

`AGENTS.md` 내장 플러그인의 현재 ID는 `cc-plugin-agents-md@builtin`이다. Claude Code 2.1.285 이상은 이전 `agents-md@builtin`도 읽으며 이전 버전은 새 ID를 무시한다. 구버전과 설정을 공유한다면 이전 키를 무조건 교체하지 않는다.

근거: [memory](https://code.claude.com/docs/en/memory), [읽기로 인정되는 Bash 명령](https://code.claude.com/docs/en/tools-reference#edit-tool-behavior).

## OpenAI 모델 지원·종료

- 10월 8일 GPT-6.1 Sol에 Ultrafast 지원 추가. Responses API의 `service_tier: ultrafast`와 Codex/Work의 플랜·워크스페이스별 제공 조건을 구분한다. 새 모델 ID 출시가 아니다.
- GPT-5.5는 10월 14일 19:00 UTC부터 ChatGPT 로그인 Codex에서 종료. OpenAI API와 API key 인증 Codex는 제외된다.
- 10월 14일 공지된 지정 GPT-4o·4o mini·4.1·4.1 mini 스냅샷 및 해당 fine-tune의 API 종료 예정일은 2027년 1월 14일. 실제 사용 모델과 인증 경로를 확인한 뒤 해당 사용처에서 이행한다.

근거: [API 변경 이력](https://developers.openai.com/api/docs/changelog), [Codex 모델](https://learn.chatgpt.com/docs/models), [Codex 변경 이력](https://learn.chatgpt.com/docs/changelog), [API 종료 공지](https://developers.openai.com/api/docs/deprecations).

## 검증 범위

10월 6일 저장본 대비 기존 24개 문서를 모두 수집했고 20개 내용 해시가 달랐다. 메뉴·표현 변화도 포함되므로 이를 20건의 정책 변경으로 해석하지 않는다. Haiku 신규 본문 4개도 조회했다. 공식 인덱스 4개가 정상 조회됐으며 최초 발견일을 발표일로 간주하지 않았다.

문서상으로 단일 파일 Bash 읽기, 파이프를 거친 조회, 타 하네스 적용, Haiku 강제 도구 호출, API key GPT-5.5 유지 사례를 대조했다. 새 모델 호출·성능 벤치마크·실행 중 Claude 세션의 로딩 테스트는 수행하지 않았다. 개인 경로·로컬 인벤토리·원시 문서 수집 결과는 공개 패키지에 추가하지 않는다.
