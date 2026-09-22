# GPT-6 Sol / Luna 별도 확인 — 2026-09-23

## 직접 확인한 공식 문서

- https://developers.openai.com/api/docs/models/gpt-6-sol.md
- https://developers.openai.com/api/docs/models/gpt-6-luna.md
- https://developers.openai.com/api/docs/guides/latest-model.md
- https://developers.openai.com/codex/models.md (같은 날짜 선행 조회)

## 모델별 사실

Sol: complex coding and agentic workflows 용도로 설명.
Luna: focused, high-volume tasks 용도로 설명; Codex 문서에는 요약·추출·집중된 코딩 작업이 예시로 제시됨.

둘 다 reasoning effort none/low/medium/high/xhigh/max 지원, API 기본 medium. 텍스트·이미지 입력과 텍스트 출력. Responses API에서 도구 사용, Chat Completions function calling은 reasoning_effort none일 때만 지원.

공통 migration 문서는 reasoning이 none이 아닐 때 temperature/top_p/top_logprobs 및 해당 logprobs 설정을 제거하도록 안내. 직접 API 통합에 해당하며 CLI 기본 구현을 프롬프트로 대체할 사항이 아님.

## 프롬프트 가이드의 적용 범위

latest-model은 GPT-6 family 전체의 출발점으로 프롬프트 예시를 제공하지만, 행동 관측 근거는 GPT-6 Astra임을 명시한다. Sol/Luna의 동일 행동을 입증한 별도 자료로 인용하지 않는다.

개별 `/guides/latest-model/gpt-6-sol.md`, `/gpt-6-luna.md` 경로는 404. 확인한 인덱스에서는 별도 prompting guide를 찾지 못함. 이는 별도 가이드가 어디에도 없다는 증명이 아니다.

## 운영 해석 (효과 미검증)

- 모델 선택 참고: Sol은 복합 구현/설계, Luna는 범위가 좁고 결과 확인이 쉬운 반복 작업 후보. 비용만으로 자동 위임·검토 대체를 결정하지 않는다.
- Luna에 맡길 작업은 입력/출력/완료 조건을 좁혀 정의하는 방안을 검토할 수 있으나, 공식적 필수 프롬프트 규칙으로 강제하지 않는다.
- 새 모델만을 이유로 medium을 max로 올리거나 Astra의 조기 중단 보정 문구를 모든 모델에 복사하지 않는다.
- 현재 스킬의 요청 범위·원문 근거·검증 수준·개인 의도 보존 규칙은 유지. 실제 대표 작업에서 확인된 실패만 추가 보정.

실제 Sol/Luna 호출, 모델 전환, 사용자 설정·외부 API 통합 코드 수정은 수행하지 않았다.
