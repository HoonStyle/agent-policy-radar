# Design Director · 0.2.0

에이전트가 **한국어·영어 UI, PPT, Word**의 구조·심미성·컬러셋을 함께 다루도록 돕는 스킬형 플러그인입니다. 공통 디자인 기준을 공유하고, 매체별 설계·검수를 나눕니다. 기존 패키지 식별자 `ui-design-director`는 유지합니다. 문서 생성·렌더링 엔진은 포함하지 않습니다.

| 스킬 | 역할 |
| --- | --- |
| `design-director` | 제품별 UI 아트 디렉션, 컬러셋, 한영 타이포, 반응형·상태·상호작용 검수 |
| `presentation-design` | PPT의 메시지·발표 흐름, 슬라이드 구도, 테마·마스터, 편집성, 슬라이드별 검수 |
| `document-design` | Word의 제목·문단 스타일, 표·캡션, 페이지 흐름, 링크·필드 보존, 페이지별 검수 |

## 포함 기능

- **맥락 정리:** 주요 과업, 실제 콘텐츠, 기존 브랜드와 보존할 기능을 확인합니다.
- **방향 설계:** 구도·타이포·색·이미지·모션을 제품에 맞게 결합합니다. 작은 수정에는 기존 디자인을 보존합니다.
- **화면 비평:** 심미적 매력, 제품 고유성, 사용성·접근성을 따로 판단하고 위치와 근거를 남깁니다.
- **수정·재검수:** 허용된 범위만 수정한 뒤 실제 화면과 행동을 확인합니다.
- **컬러셋 도구:** 역할별 색 대비 검사, CSS 변수 출력, 상호작용 가능한 로컬 HTML 샘플을 만듭니다.
- **한영 지원:** 영어/한국어 전용 타이포 기준과 예제 화면의 언어 전환. 입력값·선택·테마·검증 상태를 보존합니다.
- **PPT·Word 디자인:** 공통 브랜드를 각각의 테마/스타일에 연결하고, 기존 템플릿과 호스트 제작 도구를 활용합니다. 문서 생성 결과의 실증은 별도입니다.

## 기존 마켓에서 선택 설치

`HoonStyle/agent-policy-radar`의 `plugins/ui-design-director/`에서 관리합니다. 별도 저장소나 필수 의존 플러그인이 아닙니다. 기존 마켓을 갱신한 뒤 원하는 호스트의 명령만 실행하세요.

```sh
# Claude Code
claude plugin marketplace update agent-policy-radar
claude plugin install ui-design-director@agent-policy-radar

# Codex
codex plugin marketplace upgrade agent-policy-radar
codex plugin add ui-design-director@agent-policy-radar
```

마켓에 추가한 것과 로컬 설치·활성화는 별개입니다. 패키지 설치로 제작·렌더링 엔진이 추가되지는 않습니다.

## 에이전트에서 사용

설치 전에도 에이전트에게 다음 파일을 읽고 작업하도록 요청할 수 있습니다.

> `skills/design-director/SKILL.md`를 읽고 이 화면의 디자인을 검토해 주세요. 기존 기능은 유지해 주세요.

호스트에서 스킬을 로드한 후에는 다음과 같이 요청합니다. 호출 UI와 명령 표기는 호스트별로 다릅니다.

> `$design-director`로 이 화면의 컬러셋을 맞춰 주세요. 배치와 기능은 유지하고 상태색까지 확인해 주세요.

> `$design-director`로 제품별 구조가 드러나는 방향을 잡고 구현해 주세요. 한글 UI와 모바일 화면도 검수해 주세요.

> `$design-director`로 화면을 비평만 해 주세요. 아직 코드는 수정하지 마세요.

> Use `$design-director` to refine this English UI while preserving the layout and behavior.

> `$presentation-design`으로 이 PPT의 메시지 흐름과 구도를 정리해 주세요. 기존 템플릿과 편집 가능한 차트는 유지해 주세요.

> `$document-design`으로 이 Word 보고서의 제목·표·페이지 흐름을 다듬어 주세요. 내용과 링크는 유지해 주세요.

패키지 전체를 함께 유지하세요. 세 스킬은 같은 패키지의 공통 디자인 참조를 공유합니다. 단일 스킬 폴더만 복사하면 공통 참조가 누락될 수 있습니다.

## 패키지와 호스트

| 호스트 | 제공 형식 | 이 빌드의 확인 범위 |
| --- | --- | --- |
| Agent Plugins / 최신 Codex | 루트 `plugin.json` + `skills/` | 공식 JSON Schema 및 로컬 구조 검사 |
| Codex 호환 경로 | `.codex-plugin/plugin.json` | 동일 스킬 경로와 메타데이터 일치 검사 |
| Claude Code | `.claude-plugin/plugin.json` | 로컬 `claude plugin validate` 검사 |
| OpenClaw | 루트 portable bundle 재사용 | 설치된 OpenClaw의 번들 문서 확인; 실제 활성화 미실행 |

OpenClaw가 portable bundle을 지원하므로 별도 `openclaw.plugin.json`이나 빈 런타임 엔트리를 추가하지 않았습니다. MCP 서버·자동 편집 훅·백그라운드 프로세스·외부 API·자동 설치 기능은 없습니다. 브라우저와 문서 작성/렌더링 도구는 호스트가 제공하는 것을 사용합니다. 각 호스트의 기존 스킬과 런타임 계약을 우선하며 임의로 다른 패키지를 설치하지 않습니다.

**패키지 제작과 실제 설치는 별개입니다.** 현재 사용자 환경에는 설치·활성화·핫리로드하지 않았습니다. 호스트와 사용자의 설치·핫리로드 승인 규칙을 따르세요.

## 컬러셋 도구 실행

Python 3.9 이상, 추가 의존성 없음. 아래 명령은 플러그인 루트에서 실행합니다.

```bash
python3 skills/design-director/scripts/palette.py check skills/design-director/assets/palettes/paper-olive.json
python3 skills/design-director/scripts/palette.py css skills/design-director/assets/palettes/paper-olive.json --theme light
python3 skills/design-director/scripts/palette.py preview skills/design-director/assets/palettes/paper-olive.json --output /tmp/paper-olive.html
python3 skills/design-director/scripts/palette.py preview skills/design-director/assets/palettes/paper-olive.json --lang en --output /tmp/paper-olive-en.html
```

`mineral-violet.json`도 같은 방법으로 사용할 수 있습니다. 두 예시는 제품별 팔레트를 설계하는 출발 자료이지 공통 기본 테마가 아닙니다. 출력 파일이 있으면 덮어쓰지 않으며, 필요할 때만 `--force`를 사용합니다.

`--lang ko|en`은 첫 화면 언어를 지정합니다(기본 `ko`). 생성된 HTML 안에서는 두 언어를 전환할 수 있습니다. 예제 날짜·숫자 표기는 `ko-KR`/`en-US`를 사용하며 실제 제품의 지역 규칙을 대신 정하는 것은 아닙니다.

- 지원 입력: 불투명 sRGB `#RGB` / `#RRGGBB`, 역할별 토큰, 테마, 추가 검사 쌍.
- `check` 종료 코드: 0=선언된 필수 대비 검사 통과, 1=대비 미달, 2=잘못된 입력.
- 컬러칩뿐 아니라 버튼·입력·선택·경고·오류·키보드 포커스를 샘플 화면에서 확인할 수 있습니다.
- 자동 검사는 색의 조화, 실제 제품 CSS, 반투명·이미지 배경, 전체 WCAG 준수를 판정하지 않습니다.

전체 입력 규칙은 [컬러셋 지침](skills/design-director/references/color-system.md)을 참고하세요.

## 개발 검증

```bash
python3 -m unittest discover -s tests -v
python3 scripts/package.py
```

선택적 브라우저 검증은 기존 Playwright와 Google Chrome을 사용합니다. `artifacts/`에 `paper-olive.html`, `mineral-violet.html` 및 `paper-olive-en.html`을 생성한 뒤 아래 명령을 실행합니다. 브라우저 검증을 위해 패키지가 의존성을 자동 설치하지 않습니다.

```bash
DESIGN_PLAYWRIGHT_PATH=/absolute/path/to/playwright-core node tests/check-preview.cjs
```

검증 시 로컬 파일을 열며 서버·watcher·핫리로드를 사용하지 않습니다. 결과와 PNG는 `artifacts/`에 저장됩니다. [검증 기록](VERIFICATION.md)에서 실제 실행 범위와 미검증 항목을 구분합니다. 문서 스킬의 [전방 평가 과제](docs/behavioral-evaluation.md)는 실행 계획이며 통과 결과가 아닙니다.

## 설계 근거와 범위

[Impeccable](https://github.com/pbakaus/impeccable)이 UI 작업의 가장 가까운 기존 후보임을 확인했습니다. 이를 대체하는 엔진을 만들지 않고 제품 맥락·한영 UI·기존 화면 보존·컬러 역할·검수 기록에 집중했습니다. 기존 후보보다 디자인 품질이 낫다는 비교 실험 결과는 아직 없습니다.

PPT·Word는 설치된 제작 스킬, Microsoft 공식 문서, PptxGenJS·python-docx·Pandoc·Quarto·Marp를 비교했습니다. [문서 디자인 조사](docs/document-design-research.md)에 용도·한계·출처·저장소 상태와 채택 범위를 정리했습니다.

상세 참고 출처와 재사용 범위는 [SOURCES.md](SOURCES.md)에 기록했습니다. 이 플러그인의 원본 코드·문서는 [MIT License](LICENSE)를 따르며, 제3자 참고 자료의 권리는 각 권리자에게 있습니다.
