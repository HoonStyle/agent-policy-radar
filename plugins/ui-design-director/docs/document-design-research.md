# PPT와 Word 디자인 확장 조사

조사일 2026-10-08. 목적은 문서 생성 엔진을 새로 만드는 것이 아니라 기존 에이전트용 플러그인에 PPT·Word 디자인 워크플로를 추가하는 것입니다. 공개 공식 문서10개, 저장소 메타데이터5개와 설치된 Presentations·Documents 스킬을 확인했습니다. 후보별 결과물을 생성해 품질을 비교한 조사는 아닙니다.

## 결론

**공통 디자인 기준과 매체별 전용 스킬을 분리합니다.** 컬러 의미·서체 성격·브랜드 자산·콘텐츠 사실은 공유하되, 화면의 인터랙션과 발표의 메시지 흐름, 문서의 페이지 흐름은 각각 검수합니다. 이는 이번 패키지의 설계 판단입니다.

PPT는 테마와 마스터를 통해 반복 형식을 관리할 수 있고, Word는 내장 제목 스타일로 읽기·탐색 구조를 유지할 수 있습니다. 같은 색을 쓰더라도 UI CSS 변수를 그대로 복사하는 것이 아니라 각 매체의 스타일 체계에 연결하는 편이 적절합니다. [PowerPoint 테마](https://support.microsoft.com/en-us/powerpoint/create-your-own-theme-in-powerpoint), [Word 접근성](https://support.microsoft.com/en-us/accessibility/word/make-your-word-documents-accessible-to-people-with-disabilities)

## 기존 구현 비교

| 후보 | 확인한 용도 | 채택 범위와 한계 |
| --- | --- | --- |
| 설치된 Codex Presentations | Artifact Tool 기반 PPTX 작성·구조 검사·렌더 검수 절차 | 이 호스트의 우선 실행 절차. 관리형 런타임 로더가 제공되는 세션에서 사용 |
| 설치된 Codex Documents | DOCX 작성·OOXML 작업·페이지 렌더 검수 절차 | 이 호스트의 우선 실행 절차. 기존 템플릿/변환기 보존 |
| PptxGenJS | JS에서 마스터·placeholder·슬라이드 작성 | 다른 실행 환경의 기존 프로젝트가 이미 사용할 때 후보. 여기서는 설치나 대체 실행하지 않음. [문서](https://gitbrent.github.io/PptxGenJS/docs/masters.html) |
| python-docx | DOCX 문단·문자·표 스타일 조작 | 기존 문서 워크플로의 기반 후보. 자체 페이지 렌더 검증을 대체하지 않음. [문서](https://python-docx.readthedocs.io/en/stable/user/styles-using.html) |
| Pandoc / Quarto | 구조화된 콘텐츠를 참조 DOCX/PPTX 스타일에 맞춰 출력 | 반복 보고서·정해진 템플릿에 적합한 후보. 자유 배치를 보편적으로 대체한다고 보지 않음. [Pandoc](https://pandoc.org/MANUAL.html#option--reference-doc), [Quarto PPT](https://quarto.org/docs/presentations/powerpoint.html), [Quarto Word](https://quarto.org/docs/output-formats/ms-word.html) |
| Marp CLI | Markdown 중심 슬라이드와 여러 출력 형식 | 기본 PPTX는 렌더된 이미지 중심. 편집형 PPTX는 실험 기능이며 제약이 있어, 편집 가능한 자료가 필요한 작업의 기본값으로 삼지 않음. [공식 저장소](https://github.com/marp-team/marp-cli) |

새 패키지는 이 도구의 소스·바이너리를 복제하거나 자동 설치하지 않습니다. 필요한 도구는 호스트 또는 기존 프로젝트가 제공합니다. 특정 호스트가 지정한 런타임을 다른 후보로 몰래 대체하지 않습니다.

## 적용한 디자인·검수 기준

### PPT

발표용과 읽는 자료를 구분하고, 슬라이드별 목적·메시지·근거·구도를 먼저 정합니다. 같은 카드 배열을 반복하지 않되 기존 템플릿의 의도적 반복은 보존합니다. 슬라이드 제목, 읽기 순서, 명료한 데이터 표, 색 이외의 구별 수단을 검수에 포함합니다. 편집성과 데이터 정확성도 시각적 완성도와 별도로 확인합니다. [Microsoft PPT 접근성](https://support.microsoft.com/en-us/accessibility/powerpoint/make-your-powerpoint-presentations-accessible-to-people-with-disabilities)

### Word

문서 종류와 독자의 행동에 맞춰 제목·본문·표·캡션 스타일과 문단 간격을 정합니다. 제목의 다음 문단 연결, 문단 내 줄 유지, 고아줄 방지, 명시적인 페이지 시작을 구분해 적용하며, 모든 문단을 무조건 묶지 않습니다. 마지막 페이지까지 렌더링하여 빈 공간·표 분할·줄바꿈을 확인하는 절차를 둡니다. [Word 줄·페이지 나눔](https://support.microsoft.com/en-us/word/line-and-page-breaks)

### 한국어와 영어

문서 언어를 대화 언어와 구분합니다. 한글/영문 글리프, 번역 길이, 날짜·숫자·단위를 확인하고, 두 언어의 의미와 정보 위계를 보존합니다. 혼합 병기와 별도 언어 버전은 사용 목적에 따라 결정하며 무조건 모든 내용을 두 번 쓰지 않습니다. python-docx 내장 스타일은 현지화된 Word UI 표기와 달리 영어 식별자를 사용한다는 점도 기록했습니다. [python-docx 스타일](https://python-docx.readthedocs.io/en/stable/user/styles-using.html)

## 저장소 상태 확인

GitHub 공식 API로 확인한 값입니다. 최근 push는 품질·지원·현재 릴리스 호환성의 증명이 아닙니다. 라이선스 값만으로 재배포 검토를 끝내지 않습니다.

| 저장소 | archived | 최근 push UTC | API license |
| --- | --- | --- | --- |
| [PptxGenJS](https://github.com/gitbrent/PptxGenJS) | false | 2025-11-28T20:17:14Z | MIT |
| [python-docx](https://github.com/python-openxml/python-docx) | false | 2026-08-01T14:59:42Z | MIT |
| [Pandoc](https://github.com/jgm/pandoc) | false | 2026-10-08T01:41:26Z | GPL-2.0 |
| [Quarto](https://github.com/quarto-dev/quarto-cli) | false | 2026-10-08T13:42:58Z | NOASSERTION |
| [Marp CLI](https://github.com/marp-team/marp-cli) | false | 2026-09-08T14:24:15Z | MIT |

Quarto의 `NOASSERTION`은 라이선스가 없다는 판정이 아니라 이 API 값만으로 확정하지 못했다는 뜻입니다. 이 작업에서는 어느 후보도 배포 패키지에 포함하지 않았습니다.

## 구현 및 검증 경계

- 구현: 공통 기준1개, UI/PPT/Word 전용 스킬3개, 한영 타이포와 매체별 검수 참조, 스토리보드·문서 계획 템플릿.
- UI: 한영 문구·접근 가능한 이름·테마 선택·오류·상태·날짜/숫자 및 입력 보존을 실제 브라우저에서 검사하는 테스트 추가.
- PPT/Word: 스킬 구조·참조 경로·패키징 검사. 실제 PPTX/DOCX 생성과 렌더링은 미실행.

설치된 문서 도구 지침이 요구하는 `load_workspace_dependencies`가 이번 세션의 도구 목록에 없었습니다. 관리형 런타임을 임의의 시스템 패키지로 대체하지 않았습니다. 따라서 문서 스킬은 디자인·작업 절차가 구현된 상태이며, 문서 산출물 실증은 해당 실행 환경이 제공되는 세션에서 이어가야 합니다. 설치·게시·핫리로드는 하지 않았습니다.
