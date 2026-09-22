# 변경 이력

릴리즈별 변경 이유·Git 근거·검증 한계를 기록한다. Git diff가 코드 변경의 원본 근거이며, 이 문서는 요약이다.

아래 v0.1.0–v0.1.4 항목은 2026-09-22에 Git 이력과 당시 작업 기록을 바탕으로 **사후 작성**했다. 실시간 감사 로그나 승인 증명으로 간주하지 않는다.

## Unreleased

- Claude/Codex 설치 안내를 릴리즈 태그 고정에서 `main` 추적으로 변경. 자동 설치 설정과는 별개이며 마켓 갱신 후 플러그인을 업데이트한다.
- 플러그인 및 마켓 manifest 버전 일치 회귀 테스트 추가.

## v0.1.5 — 2026-09-22

- 구현 근거: `99d0dfe`, `821d8fa`. 기존 사용자 지침이나 설치 플러그인을 자동 수정하지 않음.

- 릴리즈별 변경 이력과 감사 로그 개발 제안 추가.
- `review` CLI 추가: 명시한 파일의 정리 초안·diff·원본/제안/패치 해시를 실행별 로컬 폴더에 보존. 원본 적용 기능 없음.
- 제공된 정리 초안을 diff로 검토하는 `--proposal`과 skill의 의미 검토 절차 추가. 기본 자동 초안은 인접 동일 bullet만 처리하며 의미 분석은 하지 않음.
- fixture 회귀 테스트 5개 통과. Windows 실제 실행은 미검증. 전체 scan/승인/적용 감사 체계는 아직 미구현.

## v0.1.4 — 2026-09-22

- 이유: 사용자 PC에서 기본 대상이 Pi/dev 경로에 치우쳐 Claude 전역 지침·Documents 프로젝트·설치 플러그인 skills가 누락됨.
- 변경: Claude/Codex 전역 지침, Documents 프로젝트, 개인 skills 및 플러그인 캐시 skills 대상 추가.
- 근거: `fab9cad` — Expand Claude and Codex scan targets for v0.1.4.
- 검증: 임시 홈의 11개 파일 탐지 및 중복 제거 회귀 테스트, Claude 마켓 manifest 검증 통과.
- 한계: Windows 실제 실행 미검증. 기본 경로 밖의 사용자 지정 위치나 모든 중첩 skill 구조를 포괄하지 않음. 설치 캐시를 직접 수정하지 않았음.

## v0.1.3 — 2026-09-22

- 이유: 사용자가 요청한 마켓은 Pi가 아니라 Claude/Codex였음.
- 변경: Claude 플러그인/마켓 manifest, OpenAI portable plugin manifest, Codex 마켓 manifest 추가. LICENSE·PRIVACY·TERMS 추가.
- 근거: `5b28648` — Add Claude and Codex plugin marketplaces.
- 검증: Claude manifest/skill validation, 양쪽 CLI의 격리된 설정 디렉터리에서 설치·활성화 확인.
- 한계: 마켓 설치 검증은 분석 정확도 검증이 아님. 공식 디렉터리 제출·승인 없음. 사용자가 이후 자체 마켓 설치까지만 요청함.

## v0.1.2 — 2026-09-22

- 이유: 배포 skill에 작성자 Mac의 절대 경로가 남아 있었음.
- 변경: 패키지 상대 경로 안내, Windows 실행 예시 및 경로 후보 추가.
- 근거: `cecbf06` — Make package paths cross-platform.
- 검증: Mac에서 scan·Python 구문 검사·npm pack dry-run·Pi skill 로드 확인.
- 한계: Windows 호환성 보장 아님. v0.1.4에서 기본 대상 누락을 추가 수정함.

## v0.1.1 — 2026-09-22

- 변경: Pi package metadata 및 설치 안내 추가.
- 근거: `f71c8c7` — Add Pi package metadata.
- 검증: metadata JSON, npm pack dry-run, Pi skill 로드 확인.
- 한계: npm publish나 마켓 등재가 완료된 것은 아님. Claude/Codex 마켓 요청을 잘못 해석한 단계였음.

## v0.1.0 — 2026-09-22

- 변경: 공식 문서 확인, 지침 인벤토리, 휴리스틱 중복 후보 분석, 권고안 생성 CLI 및 Pi wrapper.
- 근거: `5d9a610`, `91af541`.
- 검증: Python 구문 검사, CLI 실행, fresh clone 실행, Pi skill 경유 scan 확인.
- 한계: 의미 충돌 탐지 정확도·실제 권고 효과는 미검증. 첫 문서 수집은 기준선 생성이지 과거 대비 변경 없음의 증명이 아님. 산출물을 덮어쓰므로 실행별 감사 이력은 보존하지 않음.

## 이후 릴리즈 기록 규칙

- 버전·날짜·변경 이유·대상·커밋·실제 수행한 검증·알려진 한계를 기록한다.
- 미실행 검증을 성공으로 기록하지 않는다. 사후 보완은 사후 기록이라고 표시한다.
- 지침 적용 승인 기록은 릴리즈 노트와 분리하고, 승인 대상/범위/패치에 연결한다.
- 공개 이력에 로컬 지침 원문·개인 경로·자격증명·사적 대화를 추가하지 않는다.
