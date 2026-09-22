# 새 모델 대응 권고 — 2026-09-23

근거: [공식 문서 확인](../sources/2026-09-23-model-release-check.md). 제안만 기록하며 실제 설정·개인 지침 변경 없음.

## 유지

기본 하네스 우선, 확인된 문제만 최소 보정, 작은 작업의 경량 검토, 영향 범위 재검증, 기술 문체, 연구 원문 근거/개인 의도 보존은 현 공식 가이드와 충돌하지 않는다. 모델 출시만으로 Policy Radar/Review Workflow/Paper Research에 새 규칙을 추가할 근거 없음.

## 추적 소스 보완 제안

`data/source_registry.json`은 GPT-5 개별 guide 중심이라 현재 family/새 Claude guide 추적에 부족하다. GPT-5 문서는 역사 참조로 구분하고 다음을 정기 조회 대상으로 추가하는 것이 적절하다:

- Anthropic release notes, Opus 5.5 prompting / migration
- OpenAI API changelog, latest-model family guide, Codex models

discover 인덱스만으로 당일 발표를 모두 찾는다고 보장하지 않는다. 이번 조사에서 release notes의 새 모델이 읽은 index에는 없었다.

## 조건부 점검

- Opus 5.5 도입 시 오래된 high/xhigh 설정을 무조건 이식하지 않고 기본 effort부터 대표 작업으로 확인. 임의 모델 전환 없음.
- 오래된 고정 모델명/모델 호출 비율/필수 외부 위임 규칙은 별도 승인을 받아 검토. 모델 출시 자체가 기존 사용자 선호를 무효화하는 근거는 아님.
- 직접 API를 쓰는 통합이 있을 때만 thinking/tool_choice/컴퓨터 도구/응답 block 처리 호환성 검사. 이 저장소의 Python 점검 CLI는 해당 모델 API를 직접 호출하지 않음.
- GPT-5.5를 저장 설정에 고정한 사용자는 서비스별 종료 범위를 확인. 이번에 모든 계정·기기 설정을 스캔하지 않았으므로 사용 여부/영향은 미확정.

## 적용하지 않을 것

무조건 광범위 탐색, 모든 후속 답변에서 재검토 금지, 무인 자동 지속, 모델별 고정 위임 비율을 전역 규칙으로 복사하지 않는다. 공식 성능 홍보 수치는 우리 작업에서 검증한 개선 효과가 아니다.
