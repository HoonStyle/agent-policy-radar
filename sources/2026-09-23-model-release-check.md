# 모델 출시·지침 영향 확인 — 2026-09-23

## 공식 확인 사실

- Anthropic release notes의 2026-09-22 항목: Claude Opus 5.5 (`claude-opus-5-5`) 출시.
  https://platform.claude.com/docs/en/release-notes/overview
- OpenAI API changelog의 2026-09-22 항목: GPT-6 Sol (`gpt-6-sol`), GPT-6 Luna (`gpt-6-luna`) 출시. Astra 출시 항목은 2026-09-03으로 별개.
  https://developers.openai.com/api/docs/changelog
- Codex models 문서: Sol은 복잡한 코딩·에이전트 작업, Luna는 집중된 반복 작업에 권장. 제공 여부는 계정·클라이언트·rollout에 의존. GPT-5.5의 ChatGPT/Work/Codex 종료일은 2026-10-14로 안내하며 API에는 적용하지 않음.
  https://developers.openai.com/codex/models

## Prompting 근거

### Claude Opus 5.5

https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5

- 기존 Opus 5 프롬프트는 대체로 수정 없이 사용 가능하다고 안내.
- effort 기본값 medium (Opus 5는 high). 같은 effort 이름이 같은 사고량을 뜻하지 않으며 xhigh/max는 측정된 이득이 있을 때 사용 권고.
- 과도한 사고 지시를 줄이는 예시, 장시간 작업 중 조기 종료·진행 표시 문제에 대한 조건부 보완 예시 제공.
- 이전 답변을 재검토하지 말라는 예시는 장기 분석/뒤늦은 오류 발견이 필요한 에이전트 작업에는 적용하지 말라고 명시.
- 여러 앱을 폭넓게 탐색하는 예시와 무인 자동 지속 예시는 특정 작업에 대한 것으로 사용자 환경 전반에 무조건 적용할 규칙은 아님.

https://platform.claude.com/docs/en/models/opus-5-5/whats-new-opus-5-5

- API의 thinking disabled/manual enabled, forced tool_choice any/tool 불가. thinking blocks와 대화/모델 간 호환, progress update 수신 방식, 구 computer-use 도구의 플랫폼별 변경 주의.
- 이는 직접 API 통합을 점검할 항목이며 일반 CLI 사용자의 전역 프롬프트에 추가할 규칙이 아님.

### GPT-6 family

https://developers.openai.com/api/docs/guides/latest-model

- 현재 가이드는 Astra/Sol/Luna family를 다루지만 prompting 예시의 관측 근거는 Astra라고 명시하며 선택 모델/작업에서 평가하도록 안내.
- 지침/skill 모순이 작업을 멈추게 할 수 있어 원인 지침을 확인하도록 권고.
- 기술 문장을 명료하게, 불필요한 서식·상투어를 줄이는 예시 제공.
- 변경에 적절한 검증을 수행하고, 새 변경·실패·미해결 우려 없이 테스트를 반복/확장하지 않도록 안내.
- API effort/tool calling/비지원 parameter 호환성은 직접 통합 시 확인. CLI에서는 하네스 기본 구현과 계정별 가용 설정을 우선.

## 접근·한계

Anthropic 인덱스 직접 조회는 403이었고 로컬 공개 웹 조회 도우미로 공식 URL 본문을 확보했다. 인덱스보다 릴리즈 페이지가 먼저 갱신되어 새 모델 링크가 늦게 반영될 수 있음을 이번 조회에서 관측했다. OpenAI latest-model/API changelog/Codex models는 직접 조회 성공. 시도한 Codex changelog 경로는 404로 사용하지 않음.

이번 작업은 문서와 현재 로컬 지침·스킬의 대조다. 새 모델 실행 비교, 설치/모델 전환, 외부 프로젝트 API 코드 검사, Windows 재점검은 수행하지 않았다. API 가이드에서 확인한 사실을 CLI에서 실측한 결과로 간주하지 않는다.
