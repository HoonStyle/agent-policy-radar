# 공식 안내 보완 — 2026-10-06

공식 문서 확인과 로컬 동작 검증은 구분한다. 아래 안내는 사용자 설정을 변경하지 않는다.

- [Claude Code 2.1.290](https://code.claude.com/docs/en/changelog), 10월 5일: 긴 WebFetch 본문 누락 표시·이어 읽기, 압축 후 예약 작업 복원, 재개된 하위 에이전트 상태, 외부 심볼릭 링크 지침의 읽기 제한 관련 수정 공지. 설치 버전별 재현 검증은 수행하지 않았다.
- [Codex CLI 0.160.1](https://learn.chatgpt.com/docs/changelog), 10월 5일: 명시적 원격 환경변수 사용 시 Windows stdio MCP의 SYSTEMROOT/TEMP/TMP 보존 수정. API 모델 행동 변경과 구분한다.
- [OpenAI API 종료 공지](https://developers.openai.com/api/docs/deprecations), 10월 1일: GPT-5.3-Codex·GPT-5.1·GPT-5.4-Nano 종료 예정일 2027-04-01. tts-1·tts-1-hd·gpt-4o-mini-tts-2025-03-20·gpt-4o-mini-tts-2025-12-15 종료 예정일 2027-01-06. 실제 사용처를 확인한 후 해당 API만 이행하며 ChatGPT/Codex 제품 종료와 혼동하지 않는다.
- [Claude Code memory](https://code.claude.com/docs/en/memory): 하위 지침·경로 규칙은 Read/Write/Edit 시 로드될 수 있다. 로컬과 self-hosted 세션의 자동 메모리 기본값이 다르고 background/nested 세션에는 재활성화 제한이 있다. 실제 환경·로딩 범위를 확인하며 설정을 일괄 변경하지 않는다.
- [Opus 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5) 및 [Sonnet 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5): 내부 추론 재현 요구와 짧은 답변 설명·작업 요약은 다르다. 후자를 일괄 제거할 이유가 아니다.

## 적용 범위

정기 추적에 변경 이력·종료 공지 3곳을 추가한다. 모델 출시나 문서 문구 변화만으로 공통 행동 규칙·effort·모델 기본값을 바꾸지 않는다. 이 확인일은 rolling 문서의 정확한 수정일을 뜻하지 않는다. 새 모델 호출이나 유료 품질 평가는 수행하지 않았다.
