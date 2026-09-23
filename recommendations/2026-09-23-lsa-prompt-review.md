# LSA 프롬프트 검토 — 2026-09-23

대상: `legacy-spec-agent`, revision `aabb78e`. 읽기 전용 검토. 코드 실행·새 모델 호출·성능 평가·LSA 파일 수정 없음. LSA AGENTS/CLAUDE 및 IMPLEMENTATION_ROADMAP을 먼저 확인했다. 기존 Stop 결정과 독립 감사/발행 게이트를 임의로 완화하지 않는다.

## 1. 우선 수정 후보: drift의 텍스트 일치와 의미 보증 분리

근거:
- `SKILL.md:127`: detect_drift의 deterministic 분류로 보고서를 작성하고 수동 단계는 커넥터 부재 시에만 사용하도록 안내.
- `SKILL.md:131`: intact를 ‘code still supports the claim’, moved를 ‘same behavior’, drifted를 ‘behavior changed’로 정의.
- `connector/src/drift.ts:41,91-106,145-160`: 인용 위치 주변 최대 반경 5줄의 텍스트 probe를 찾아 intact/moved/drifted를 반환. 유일한 줄은 반경 0에서 결정될 수 있음. 자연어 주장·호출 대상·전역 설정의 의미를 검증하지 않음.
- `connector/src/server.ts:218-230`: 도구 설명도 semantic 보장의 한계를 명확히 밝히지 않고 Source line을 참조.

판단: 도구 결과만으로 ‘동작 불변/변경’을 결론내릴 위험이 있다. 인용 줄이 그대로라도 참조 상수/호출 함수가 바뀔 수 있다. 반대로 서식 변경은 동작 변경을 뜻하지 않을 수 있다. 이는 정적 구현/문구 대조로 확인한 보장 범위 불일치이며 새 실험을 했다는 의미는 아니다.

최소 제안: 도구 결과는 인용 텍스트/위치 변화 신호라고 명시. 주장의 의미 유지 여부는 관련 원문·의존 조건을 따로 확인하고 미확인은 unresolved/needs-review로 보고. 커넥터가 있어도 의미 검토를 생략하지 않도록 문구 조정. API enum을 바꾸는 일은 별도 호환성 검토 없이 하지 않는다.

## 2. 우선 수정 후보: baseline 필드 불일치

근거:
- Mode A `SKILL.md:108` 부근은 `Analyzed source commit`과 `Generated at`을 분리해 출력.
- Mode B `SKILL.md:127`, `server.ts:222-226`는 오래된 `Source:` 줄을 기준으로 baseline_ref를 찾도록 안내.
- Mode A는 non_git/dirty byte snapshot도 지원하지만 detect_drift는 Git ref를 받음.

최소 제안: 실제 manifest/source provenance와 `Analyzed source commit`을 우선 읽고 `Source:`는 legacy 호환으로만 취급. 비Git·dirty snapshot에서 Git HEAD만으로 과거 실제 입력을 복원했다고 주장하지 않음. 도구 사용 불가 시 날짜로 commit을 추정하지 말고 한계 명시.

## 3. 범위 결정 후보: 광범위 trigger와 무조건 standard 발행

근거: `SKILL.md:3`은 단순 저장소 설명/온보딩 질문까지 trigger, `:29-31`은 standard 문서 전체와 독립 역할을 크기에 상관없이 요구, `:103`은 8종 문서·audit·charts/report 산출.

판단: 문서 생성 요청에는 의도된 품질 계약이지만 ‘이 저장소가 무엇을 하나’ 같은 질문에도 발행 파이프라인으로 확대될 여지가 있다. 새 모델 특유의 실측 결함은 아니다.

최소 제안: **정식 문서 생성/발행 요청과 단순 설명/탐색을 입구에서 구분**. 설명 요청에는 기본 하네스의 근거 기반 응답으로 제한. 정식 LSA 산출물을 만들기로 한 뒤에는 기존 독립성·coverage·gate 계약 유지. core 기본화나 gate 생략은 승인 없이 제안대로 적용하지 않음.

## 4. 실행 비용 후보: 커넥터가 있으면 index_symbols부터 호출

근거: `SKILL.md:55`의 call it first, `:69`의 Task/general-purpose 고정 표현. 로드맵의 2026-08-04 replay는 모든 connector run의 전역 index 재출력과 입력 토큰 증가를 관측하고 효율 확장 Stop 결정.

최소 제안: ‘도구 존재’만으로 저장소 전체 index를 우선 요청하지 않도록 현재 하위 경로·package granularity·동일 source snapshot 결과의 재사용 조건을 명시할지 검토. 의미 추출에는 실제 source 읽기가 여전히 필요함. Task라는 특정 호스트 도구명 대신 host의 사용 가능한 위임 도구를 사용하도록 표현 가능. 독립 actor를 제공할 수 없는 환경에서는 승인된 발행을 흉내 내지 말고 한계를 보고.

캐시 인프라·resolver·새 벤치마크를 만들자는 제안이 아니며 효율 개선 수치를 새로 주장하지 않음.

## 5. 유지할 부분

- file:line 근거, UV 미확인 분리, 실제 검색 범위를 포함한 Not found.
- syntax module_dependency를 runtime call graph로 과장하지 않는 계약.
- Writer/Evidence Auditor/Coverage Sentinel/Gatekeeper 분리와 caller_attested 한계.
- 변경 주장/인용/ID 및 영향받는 contract만 재확인하는 correction 규칙.
- 다운로드/설치/대상 실행의 권한 구분. 현재 syntax 분석에 SDK가 필수인 것처럼 오인되지 않게 유지.

## 적용 범위 및 후속

Root `SKILL.md`와 `references/`가 원본이며 `scripts/sync-plugin-skill.mjs`가 배포 경로로 복사한다. 이번 확인에서 root/배포 SKILL은 byte-identical이었다. 설치 캐시나 생성 문서만 수정하면 안 된다.

우선순위는 1·2의 의미 보증/필드 정합성, 이후 3·4의 실행 범위 최소화다. 실제 변경은 사용자 승인 후 LSA 프로젝트에서 그 프로젝트의 빌드·테스트·동기화 규칙을 따라 수행한다. 새 모델 출시만으로 게이트를 제거하거나 Stop 결정을 재개하지 않는다.
