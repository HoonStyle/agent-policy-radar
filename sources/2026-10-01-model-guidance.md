# 모델·문서 추적 업데이트 — 2026-10-01

## 공식 사실

- [OpenAI API changelog](https://developers.openai.com/api/docs/changelog): GPT-6.1 Sol은 2026-09-29 출시. [모델 문서](https://developers.openai.com/api/docs/models/gpt-6.1-sol)는 effort low/medium(기본)/high/xhigh/max, none/minimal 미지원, 도구 호출에는 Responses API 필요, Chat Completions는 도구 없이 지원한다고 안내한다. 기존 GPT-6 Sol과 별도로 추적한다.
- [GPT-6 통합 가이드](https://developers.openai.com/api/docs/guides/latest-model)는 GPT-6.1 Sol을 포함하지만 prompting 관찰은 여전히 Astra 기반임을 밝힌다. 이를 Sol/6.1 Sol/Luna에서 검증된 결과로 해석하지 않는다.
- [ChatGPT & Codex changelog](https://learn.chatgpt.com/docs/changelog)의 9월 29일 안내에서 6.1 Sol 가용성은 요금제·클라이언트·워크스페이스 설정에 의존한다. 이 문서는 특정 사용자 계정의 설치나 선택 가능 여부를 확인한 기록이 아니다.
- [Claude Platform release notes](https://platform.claude.com/docs/en/release-notes/overview): 9월 30일 Sonnet 4.5 종료 예고. Claude API 종료 예정일은 2026-11-30이며 Sonnet 5.5로의 이행을 권한다. 사용처가 있을 때 해당 API 연동에서 검토한다.

## 문서 추적 복구

기존 registry에서 HTTP 308로 실패한 URL 3개를 Location 헤더의 공식 목적지로 교체한다. 동일 환경의 Python urllib 요청에서 각 목적지의 HTTP 200과 문서 제목을 확인했다.

- Codex 모델: `https://learn.chatgpt.com/docs/models.md`
- Codex CLI: `https://learn.chatgpt.com/docs/codex/cli.md`
- 과거 GPT-5 prompting: `https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide.md`

새 GPT-6.1 Sol 모델 `.md` URL도 HTTP 200 확인. 이는 확인 시점의 접근 결과이며 향후 조회 성공을 보장하지 않는다. 과거 GPT-5 문서는 계속 역사적 참고로 표시한다.

## 운영 판단과 한계

추적 누락과 실제 수집 실패를 해결하는 최소 유지보수 변경이다. 모델 이름·API 기본값을 CLI 전역 설정에 복사하지 않으며 기존 행동 지침과 모델 선택을 유지한다. 6.1 Sol 신규 호출, 성능 비교, 실사용 행동 검증 또는 설치 업데이트는 수행하지 않았다.

이전 검토 당시 등록 문서 20개 중 17개 수집 성공, 3개 실패였다. first-seen 11 / changed 5 / unchanged 1 / failed 3을 신규 변경 19건으로 해석하지 않는다. 과거 snapshot과의 변경 시점은 9월 29일 이후로 특정할 수 없다. 수정 후 2026-10-01 10:36 KST 재수집에서는 21개 모두 성공했다(first-seen 2 / unchanged 19). 이는 모델 작업 품질 검증이 아니다.
