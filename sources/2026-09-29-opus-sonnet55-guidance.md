# Opus 5.5 / Sonnet 5.5 공식 지침 확인 — 2026-09-29

## 출시 사실

[Claude Platform release notes](https://platform.claude.com/docs/en/release-notes/overview): Opus 5.5 (`claude-opus-5-5`)는 2026-09-22, Sonnet 5.5 (`claude-sonnet-5-5`)는 2026-09-28 출시. Opus는 9월 23일 기록을 재확인했으며 Sonnet을 새로 추가한다. 발견일과 출시일을 구분한다.

## 공식 모델별 prompting 안내

- [Opus 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5): 기존 Opus 5 프롬프트는 대체로 유지 가능. API 기본 effort는 medium이며 이전 모델과 같은 effort가 같은 사고량은 아니다. 무인 실행의 텍스트 종료는 완료 증거가 아니며, 진행 표시에는 thinking block 처리 확인이 필요하다. 무인 실행 보완 예시를 사람과 대화하는 모든 세션에 복사하지 않는다.
- [Sonnet 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5): 기존 Sonnet 5 프롬프트는 대체로 유지 가능. API 기본 effort는 high, 명확한 에이전트 코딩은 medium부터 평가하도록 안내한다. 낮은 effort의 조기 확인/검증 생략, 높은 effort의 범위 확대/추가 리뷰는 조건부 관찰이며 로컬 실측이 아니다. JSON 추론에는 adaptive thinking을 사용하고, 유효한 JSON이어도 max_tokens 종료를 성공으로 처리하지 않도록 안내한다.

## 직접 API 통합에서 구분할 사항

[Sonnet migration](https://platform.claude.com/docs/en/models/sonnet-5-5/migration-guide)과 [Opus 변경 사항](https://platform.claude.com/docs/en/models/opus-5-5/whats-new-opus-5-5)을 해당 통합의 플랫폼과 출발 모델 기준으로 확인한다.

- Opus 5.5의 always-on thinking과 Sonnet 5.5의 `between_tools`를 혼동하지 않는다. Sonnet의 `between_tools`는 low/medium/high에서만 가능하며 사고 전체를 끄는 모드가 아니다. 이 모드에서 effort를 대화 중 바꾸거나 display/budget_tokens/block_binding을 함께 보내면 오류다.
- Sonnet 5.5는 forced tool_choice any/tool을 받지 않는다. auto/strict의 사용 가능 여부는 플랫폼에 의존하며 Bedrock에 strict를 일괄 적용하지 않는다.
- thinking blocks는 원형으로 전달하고 content의 type으로 분기한다. 모델·대화·계정의 호환 조건을 확인한다. Sonnet 5.5 블록의 계정 간 재사용 제한도 출시 노트에 추가됐다.
- computer-use 도구와 advisor 조합 변경은 API 통합 항목이다. CLI의 전역 지침에 API 설정을 복사하는 사유가 아니다.

## 접근 및 검증 한계

공식 인덱스 discover: 101 후보, 인덱스 실패 0. 이는 모두 검증된 신규 문서라는 뜻이 아니다. 직접 urllib로 prompting 2개와 Sonnet migration의 .md 본문을 요청한 결과 403; 웹 조회 도구로 공식 HTML 본문을 확인했다. 검색 캐시의 출시 예정 문구보다 9월 28일 공식 출시 노트를 우선했다.

모델 호출·성능 비교·설치 업데이트·외부 프로젝트 API 수정은 수행하지 않았다. 이전 Opus 합성 검증을 Sonnet 실측으로 재사용하지 않는다. 공식 권고와 로컬 판단은 별도 findings에 기록한다.
