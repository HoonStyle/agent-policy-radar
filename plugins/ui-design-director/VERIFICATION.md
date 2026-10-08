# Verification · 0.2.0

검증일: 2026-10-08. 실행 호스트: Mac Studio, Darwin arm64. Python 3.9.6, Node.js 22.20.0, 기존 Playwright Core와 Google Chrome을 사용했습니다. 설치·게시·개발서버·watcher·핫리로드는 실행하지 않았습니다. 이전 v0.1.0 ZIP은 그대로 보존했습니다.

## 실행 결과

| 검사 | 결과 | 범위 |
| --- | --- | --- |
| Python/CLI 테스트 | 18/18 통과 | 대비 계산·입력 오류·필수 역할·중복 JSON·CSS·이스케이프·덮어쓰기 보호·한영 메시지와 CLI 언어 선택 |
| 컬러 대비 | 84/84 조합 통과 | 2팔레트 × 2테마 × 21필수 조합, 비활성 컨트롤은 별도 참고값 |
| 브라우저 | 24/24 조건 통과 | 2팔레트 × ko/en × light/dark × 1280/390/320 CSS px |
| 정적 영어 출력 | 통과 | JavaScript를 끈 브라우저에서도 영어 기본 화면·문서 언어·선택값 확인 |
| 브라우저 오류 | 0건 | JavaScript 예외·console error·외부 HTTP 요청 없음 |
| 스킬 기본 검사 | 3/3 통과 | design-director, presentation-design, document-design의 Skill Creator 검증 |
| Portable manifest | 통과 | Agent Plugins 1.0.0 공식 JSON Schema + 기존 Ajv 2020 |
| Claude manifest | 통과 | 로컬 CLI 검증, 경고 없음 |
| 패키지 구조 | 통과 | 스킬3개, 공통/상대 참조, 어댑터 메타데이터, ZIP 경로와 CRC 검사 |
| PPTX/DOCX 실제 생성·렌더링 | 미실행 | 필수 관리형 런타임 로더가 이 세션에 없음 |

## UI 동작·시각 검수

언어별 문서 lang/title, 레이블·placeholder·접근 가능한 이름·오류·완료 메시지, 테마별 토큰, 한영 날짜/건수 표기를 확인했습니다. 테마 전환, 선택/해제, 빈 입력 실패와 포커스, 유효 입력 복구, Tab/Space 및 포커스 표시를 실행했습니다. 언어 전환 시 입력값·선택·테마·검증 상태가 유지되고 메시지만 번역되는지 확인했습니다.

긴 영문 버튼 문구를 넣어 320px에서도 버튼 글자가 잘리거나 페이지가 가로로 넘치지 않는지 검사했습니다. 초기 테스트에서는 언어 전환 뒤 이전 언어 레이블을 찾는 테스트 locator가 실패했습니다. 언어 간 상태 비교에는 고정 ID를 사용하도록 테스트를 수정했고 최종 24개 조건은 모두 통과했습니다. 이 오류를 제품의 입력 보존 실패로 기록하지 않았습니다.

각 조건의 PNG24개를 저장하고 영어 wide/narrow 및 한국어 대표 화면을 직접 검토했습니다. 네이티브 입력창에서 긴 값/placeholder가 내부 스크롤되는 동작과 페이지 가로 넘침은 구분했습니다. v0.1.0에서 수정한 placeholder muted 토큰도 두 언어에서 유지됩니다.

## 문서 스킬의 확인 범위

PPT·Word는 매체별 디자인 절차, 공통 브랜드 매핑, 한영 타이포, 템플릿 보존, 편집성·필드·페이지/슬라이드 검수 절차를 작성하고 스킬 구조와 링크를 검사했습니다. 기존 제작 엔진을 복제하거나 대체하지 않았습니다. 전방 평가 과제는 docs/behavioral-evaluation.md에 있지만 실행된 에이전트 평가 결과가 아닙니다.

현재 설치된 Presentations의 `references/implementation.md`는 “Call load_workspace_dependencies”를, Documents의 `SKILL.md`는 “Use Codex workspace dependencies for docx artifact work”를 요구합니다. 세션의 사용 가능한 도구를 확인했으나 해당 로더가 없었습니다. 따라서 시스템 Python/Node 또는 데스크톱 LibreOffice로 우회하지 않았으며, 실제 PPTX/DOCX 생성·페이지 렌더링·Office 애플리케이션 확인은 하지 않았습니다. 문서용 스킬을 구현한 것과 최종 문서를 생성해 검증한 것은 구분합니다.

## 증거 파일

최초 구현 작업공간의 로컬 artifacts/에 두 컬러셋의 기본 한국어 HTML과 -en.html, 대비 JSON2개, browser-results-v0.2.0.json, screenshots-v0.2.0/ PNG24개, 공식 portable schema가 있습니다. QA 출력은 배포 ZIP에서 제외됩니다. HTML은 포함된 도구로 재생성할 수 있습니다.

## 남은 한계

- 운영 설치 후 Codex·Claude·OpenClaw의 자동 스킬 선택과 실제 호출은 미검증입니다.
- 실제 제품 적용, 독립 에이전트 전방 테스트, 기본 에이전트/Impeccable 비교와 사용자의 심미적 선호 평가는 미실행입니다.
- Safari/Firefox/실물 모바일/스크린리더/전체 WCAG 적합성/실제 제품 CSS는 검증하지 않았습니다.
- 두 팔레트 화면은 동일한 컬러 specimen이며 서로 다른 제품 구조를 실증한 예제가 아닙니다.
- 반투명·이미지·광색역 입력은 컬러 도구 범위 밖입니다.

결론: UI 도구와 한영 예제는 실행 검증했고, PPT·Word 설계/검수 스킬까지 패키징했습니다. 문서 산출물의 실행 검증은 해당 관리형 런타임이 제공되는 환경에서 이어가야 합니다.


## 기존 마켓 통합 검사 — 2026-10-08

`HoonStyle/agent-policy-radar`의 `plugins/ui-design-director/`로 통합했습니다. Claude/Codex 마켓 항목, 패키지 파일 목록, 영어·한국어 사용 안내를 연결했습니다. 기존 플러그인의 자동 설치나 기본 스킬 변경은 없습니다.

- 통합 저장소의 오프라인 회귀 테스트 45개 통과(기존 25 + 디자인 도구 18 + 통합 경계 2).
- 세 스킬의 기본 검사, Claude 플러그인/마켓 검증 및 패키지 상대 참조 검사 통과.
- npm 배포 파일 목록에 세 스킬·언어 사전·HTML 템플릿·호환 manifest·라이선스 포함 확인. 생성 ZIP/QA artifacts는 제외.
- 공개 패키지의 개인 전용 규칙·이력서 경로를 사용자/프로젝트 지침 존중으로 일반화하고, 문서 패키지와 테스트의 UTF-8 처리를 명시.
- 실제 npm tarball을 별도 임시 경로에 풀어 도구 테스트18개, ZIP 재생성, 팔레트2종 영어 HTML 생성 통과. npm이 제외하는 `.gitignore`는 런타임 필수 파일로 취급하지 않도록 수정.
- 최초 브라우저 24조건 결과는 UI 코드가 같은 기존 근거를 재사용한 것이며 통합 후 새 브라우저 실행으로 세지 않습니다.
- PPTX/DOCX 생성·렌더링, 설치·활성화·핫리로드는 추가로 실행하지 않았습니다. 태그/Release 발행과 저장소 반영은 구분합니다.
