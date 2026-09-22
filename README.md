# Agent Policy Radar

**에이전트 지침 점검, 개발 리뷰, 논문 연구를 위한 선택형 스킬 마켓입니다.**

Claude Code와 Codex에서 필요한 플러그인만 설치합니다. 각 회사의 기본 하네스를 우선하며, 확인된 문제에만 최소한으로 보완합니다. 설치했다고 모든 작업에 긴 절차를 강제하거나 개인 지침을 자동 수정하지 않습니다.

[릴리즈](https://github.com/HoonStyle/agent-policy-radar/releases) · [변경 이력](CHANGELOG.md) · [이슈·피드백](https://github.com/HoonStyle/agent-policy-radar/issues)

## 무엇을 설치하면 되나요?

| 플러그인 | 용도 | 현재 릴리즈 버전 |
| --- | --- | --- |
| **`agent-policy-radar`** | 공식 문서 변화 확인, 로컬 지침의 중복 후보·정리안 검토 | 0.1.14 |
| **`review-workflow`** | 리뷰 지적을 정리하고 수정·재검증이 끝없이 반복되는 상황 관리 | 0.2.1 |
| **`paper-research`** | 문헌 탐색부터 논문 집필까지 연구 단계별 보조, 간호학 참고 문서 포함 | 0.1.1 |

**논문 작업만 한다면 `paper-research`만 설치하면 됩니다.** 세 플러그인은 서로 필수 의존성이 아닙니다. 기본 플러그인 설치나 업데이트가 다른 플러그인을 자동 설치하지 않습니다.

> Policy Radar는 **지침 점검 보조 도구**입니다. 최신 모델에 맞춘 최적화를 보증하거나, 중복 문구를 자동으로 삭제하는 도구가 아닙니다.

## 설치

### 준비 사항

- Claude Code 또는 Codex CLI와 Git이 필요합니다. 해당 제품의 로그인·실행 환경을 먼저 준비하세요.
- Policy Radar CLI 및 Review Workflow의 선택형 기록 도구는 **Python 3.10 이상**이 필요합니다. CI는 Python 3.11로 검사합니다.
- Paper Research의 절차 문서 자체에는 Python이 필요하지 않습니다. 검색·문서 읽기·통계 실행 능력은 사용 중인 하네스와 도구에 따라 달라집니다.
- 공식 공개 디렉터리에 등재된 제품이 아니라 **GitHub 자체 마켓**입니다. 아래 명령은 터미널에서 실행합니다.

### Claude Code

마켓을 한 번 등록한 뒤 필요한 플러그인만 선택합니다.

```sh
claude plugin marketplace add HoonStyle/agent-policy-radar@main

# 필요한 명령만 실행
claude plugin install agent-policy-radar@agent-policy-radar
claude plugin install review-workflow@agent-policy-radar
claude plugin install paper-research@agent-policy-radar
```

### Codex

```sh
codex plugin marketplace add HoonStyle/agent-policy-radar --ref main

# 필요한 명령만 실행
codex plugin add agent-policy-radar@agent-policy-radar
codex plugin add review-workflow@agent-policy-radar
codex plugin add paper-research@agent-policy-radar
```

설치 후 **새 세션을 시작**하세요. 다음 명령으로 설치 버전과 활성화 상태를 확인할 수 있습니다.

```sh
claude plugin list
codex plugin list
```

### 앱·모바일·원격 사용

검증한 배포 경로는 **macOS/Windows의 Claude Code·Codex CLI**입니다. 일반 Claude/ChatGPT 앱의 커스텀 업로드, 공개 플러그인 디렉터리, 모바일 동기화와는 구분해야 합니다.

- PC의 CLI에 설치했다고 다른 기기나 클라우드 세션에도 자동 설치되는 것은 아닙니다.
- 원격으로 사용할 때는 **플러그인을 설치한 동일 PC/실행 환경의 세션**인지 확인하세요.
- 별도 클라우드 환경은 자체 설치·파일 접근 지원 여부를 확인해야 합니다.

### Pi 사용자

루트의 Policy Radar 스킬은 Pi 패키지로도 설치할 수 있습니다.

```sh
pi install git:github.com/HoonStyle/agent-policy-radar@v0.1.14
```

이 명령은 버전 고정 설치이며, 선택형 두 플러그인을 Pi 스킬로 자동 등록하지 않습니다. npm 배포·갤러리 등재를 의미하지도 않습니다.

## 사용하기

### 1. Agent Policy Radar — 지침 점검

Claude Code에서는 `/agent-policy-radar:agent-policy-radar`, Codex에서는 설치된 Agent Policy Radar 스킬을 명시해 요청합니다.

예시:

> 전역 지침과 프로젝트 지침을 점검해줘. 개인 선호는 유지하고, 실제 충돌이나 불필요한 중복 후보만 확인해줘.

> 공식 모델 가이드가 바뀌었는지 확인하고, 현재 지침에 영향이 있는 부분만 알려줘.

수행 범위:

- 공식 문서 인덱스에서 가이드·모델·마이그레이션·릴리즈 노트 **링크 후보 발견**
- 등록된 공식 문서의 **최초 수집 / 변경 / 변경 없음 / 실패** 구분
- 설정된 경로의 전역·프로젝트·스킬 Markdown 지침 인벤토리 및 중복 후보 분석
- 요청 관련 후보의 주변 원문과 실제 적용 범위를 확인해 **유지 / 변경 후보 / 판단 보류**로 보고
- 명시한 파일의 정리 초안·diff 생성. 원본 적용 기능은 없음

**자동 후보는 결함 판정이 아닙니다.** 숫자·버전·조건은 보존해 비교하지만, 의미 충돌이나 최신 모델 최적화 효과를 자동 검증하지 않습니다. 공식 근거와 실제 문제의 연결은 에이전트/사용자의 추가 검토가 필요합니다.

개인 선호·의도를 보존하고, 중복·길이·일반 권장사항만으로 변경을 권고하지 않습니다. 관련 없는 파일이나 전체 대화 기록으로 점검 범위를 확대하지 않습니다.

### 2. Review Workflow — 개발 리뷰

Claude Code: `/review-workflow:review-workflow`

Codex: 설치된 Review Workflow 스킬을 명시해 요청합니다.

> 이번 변경을 리뷰해줘. 실제 결함과 선택적 개선을 구분하고, 수정한 부분과 영향받는 동작만 재확인해줘.

- **작은 수정:** 변경 이유·수정 내용·검증 결과만 간단히 남깁니다.
- **복잡한 작업:** 필요하면 지적 ID, 근거, 판정, 수정, 검증을 ledger로 유지합니다.
- 기존 지적의 해결과 새 회귀를 우선 확인하고, 새 지적은 기존 누락·변경으로 발생·범위 밖 개선·미확인으로 구분합니다.
- 관련 버전·조건이 같은 이전 검증은 재사용 사실을 밝히고 활용합니다.
- ‘지적 0개’가 아니라 합의한 완료 조건과 필수 검증을 기준으로 종료합니다.

상세 기록은 선택 사항입니다. [기록 CLI 안내](plugins/review-workflow/skills/review-workflow/references/cli.md)는 `init`, `finding`, `update`, `pass`, `validate`, `compare`를 제공합니다. 없는 지적 ID 참조와 검증 수준별 근거 누락을 검사하지만, **기록의 진실성이나 사용자 승인을 보증하지 않습니다.**

팀 기준은 프로젝트의 `.review-workflow.json`에 둘 수 있습니다. [프로파일 예시](plugins/review-workflow/profile.example.json)를 참고하세요. 설정에 적힌 명령은 자동 실행하지 않습니다. [한국어 수동 양식](plugins/review-workflow/skills/review-workflow/references/ledger-template.ko.md)도 있습니다.

### 3. Paper Research — 논문 연구·집필

Claude Code: `/paper-research:paper-research`

Codex: 설치된 Paper Research 스킬을 명시해 요청합니다.

> 이 논문의 주장·방법·한계를 원문 위치와 함께 정리해줘. 읽지 못한 부분은 구분해줘.

> 두 논문을 비교해 관련 연구 문단을 써줘. 서로 다른 실험 결과를 같은 조건의 비교처럼 쓰지 마.

> 연구계획서의 지정한 부분만 다듬어줘. 확정 사항과 서식은 유지하고, 의미 변경은 별도 제안으로 보여줘.

지원하는 선택 단계:

| 단계 | 보조 내용 |
| --- | --- |
| 문헌 탐색·비교 | 검색 범위, 논문 식별·버전, 기여·방법·한계 비교 |
| 정독·비판 | 주장과 근거 대응, 가정·실험·대안 설명 검토 |
| 연구 설계·재현 | 연구 질문·가설·평가 계획, 재현 수준·자원·미실행 범위 구분 |
| 자료 수집·정제 | 출처·권한·변수·결측·제외 기준 검토 |
| 통계 분석 보조 | 설계에 맞는 방법·가정·불확실성 점검 |
| 집필·편집 | 내용 통합, 문장 수정, 인용·표·그림·본문의 대응 확인 |

**간호학 선택 참고 문서**에는 설문/도구 개발·검증, 중재, 질적·혼합연구, 체계적/범위 고찰·메타분석, 자료 보호·정제, SPSS/AMOS/R 작업 안내가 포함됩니다. [간호학 안내](plugins/paper-research/skills/paper-research/references/nursing.md)에서 시작해 필요한 단계만 읽습니다.

중요한 경계:

- 원문 접근 수준, 저자의 주장, 관측 결과, 해석을 구분합니다. 없는 DOI·인용·통계·실험 결과를 만들지 않습니다.
- 문체 수정·내용 통합 시 의미·주장 강도·조건·예외·수치·인용 대응을 보존합니다.
- 검토 질문을 변경 승인으로 해석하지 않고, 확정 사항을 임의로 바꾸지 않습니다.
- 관련 문서를 함께 수정하는 요청에서는 변경 부분의 일치를 확인합니다. 서식·페이지 검증을 수행하지 못했다면 명시합니다.
- 간단한 요약이나 문장 교정에 전체 연구 절차·별도 기록 파일을 강제하지 않습니다.
- **SPSS/AMOS/R 실행 엔진, 자동 자료 수집 서비스, IRB 판단 도구가 아닙니다.** 실제 실행·라이선스·권한이 없다면 계획/초안과 미실행 상태를 제공합니다.
- 환자·참여자 자료, 비공개 원고의 외부 전송에는 별도 권한과 기관 정책 확인이 필요합니다. 임상·통계·윤리 전문가의 판단을 대체하지 않습니다.

## 업데이트

Claude/Codex 마켓은 `main`을 추적합니다. 마켓 갱신으로 새 버전을 발견할 수 있지만 **자동 설치나 다른 기기로의 동기화를 보장하지 않습니다.** 필요한 설치 항목만 업데이트하세요.

```sh
# Claude Code
claude plugin marketplace update agent-policy-radar
claude plugin update agent-policy-radar@agent-policy-radar
claude plugin update review-workflow@agent-policy-radar
claude plugin update paper-research@agent-policy-radar

# Codex
codex plugin marketplace upgrade agent-policy-radar
codex plugin add agent-policy-radar@agent-policy-radar
codex plugin add review-workflow@agent-policy-radar
codex plugin add paper-research@agent-policy-radar
```

Codex의 `add`는 미설치 항목도 설치하므로 원하는 것만 실행하세요. 이후 새 세션을 시작하고 목록에서 버전을 확인합니다.

예전에 `@v…` 태그로 마켓을 고정했다면 `main` 등록으로 변경해야 합니다. 출처 불일치 오류가 나면 해당 마켓을 제거 후 재등록할 수 있지만, **제거 시 그 마켓의 플러그인이 함께 제거될 수 있으므로 설치 목록을 먼저 확인**하세요.

`main`에는 릴리즈 전 작업도 존재할 수 있습니다. 재현 가능한 설치가 필요하면 검증된 릴리즈 태그를 사용하되, 그 경우 버전 전환은 직접 해야 합니다.

## CLI 직접 사용

저장소를 clone한 루트 또는 실제 설치된 패키지 루트에서 실행합니다. 아래 `scripts/`는 사용자가 분석하려는 프로젝트의 경로가 아니라 **Policy Radar 패키지의 경로**입니다.

```sh
git clone https://github.com/HoonStyle/agent-policy-radar.git
cd agent-policy-radar
python3 scripts/policy_radar.py all
```

Windows PowerShell:

```powershell
py -3 scripts\policy_radar.py all
```

`py`가 없고 Python이 `python` 명령으로 설치돼 있다면 `python scripts\policy_radar.py all`을 사용합니다.

| 명령 | 동작 |
| --- | --- |
| `discover` | 공식 `llms.txt` 인덱스 4곳에서 관련 문서 링크 후보 발견 |
| `sources` | `data/source_registry.json`에 등록된 문서 확인 |
| `scan` | `data/instruction_targets.json`의 경로에서 지침 인벤토리 생성 |
| `overlap` | 기존 인벤토리로 중복 후보 분석 |
| `recommend` | 기존 분석으로 실행별 검토 초안 생성 |
| `all` | discover → sources → scan → overlap → recommend |
| `review <파일>` | 지정한 원본의 정리 초안·diff 생성 |

외부 `discover`/`sources`가 실패해도 `all`은 독립적인 로컬 분석을 계속하고 종료코드 1로 부분 실패를 보고합니다. 로컬 단계가 실패하면 그 결과에 의존하는 후속 단계는 중단합니다.

```sh
python3 scripts/policy_radar.py review "path/to/CLAUDE.md"
python3 scripts/policy_radar.py review "path/to/CLAUDE.md" --proposal "path/to/draft.md"
```

`--proposal` 없이 자동 생성하는 초안은 **코드 블록 밖 인접 동일 bullet 정리**에 한정되며 안전 키워드가 있는 문구는 유지합니다. 의미 기반 정리는 에이전트/사람이 작성한 초안을 검토하는 방식입니다. `review`에는 원본을 적용하는 명령이 없습니다.

### 스캔 범위·문서 발견의 한계

- 기본 대상에는 Claude/Codex/Pi 전역 지침, 일부 dev/Documents 프로젝트, 개인 skills와 플러그인 캐시 skills가 포함됩니다. **컴퓨터 전체나 모든 사용자 지정 경로를 자동 발견하는 것은 아닙니다.**
- 커스텀 대상은 `data/instruction_targets.json`에서 확인합니다. 설치 캐시를 직접 수정하면 업데이트 때 사라질 수 있으므로 사용자 관리 checkout에서 설정하거나 upstream 개선을 제안하세요. 범용 외부 설정 파일 지원은 아직 없습니다.
- **MCP 설정 분석은 현재 제외**됩니다. 설정값을 원문으로 수집하지 않으며, 복원 여부는 별도로 결정합니다.
- `discover`는 공식 링크 후보를 찾을 뿐 본문을 검증하거나 registry에 자동 등록하지 않습니다. ‘최초 발견’은 ‘새로 출판됨’을 뜻하지 않습니다.
- 등록된 추적 대상에는 Opus 5.5 prompting/migration, GPT-6 통합 가이드·Sol/Luna 모델 문서, 양사 릴리즈 노트 및 Codex 모델 안내가 포함됩니다. GPT-5 가이드는 과거 참고 자료로 구분합니다. API 변경과 하네스 지침을 구분하고, Astra 관측 기반 권고를 Sol/Luna에서 검증된 행동으로 간주하지 않습니다. `cadence`는 참고 메타데이터이며 스케줄러가 아닙니다. 사이트가 403 등으로 조회를 거부하면 실패로 보고하며 등록 자체가 조회 성공을 보장하지 않습니다.
- `sources`의 변경은 저장된 snapshot 대비 변화입니다. 설치 패키지의 과거 기준선과 달라진 것일 수도 있습니다.
- 문서 확인은 명시 실행형입니다. 정기 실행·새 모델 감지 알림·백그라운드 자동 최적화는 없습니다.

## 결과와 개인정보

| 위치 | 내용 |
| --- | --- |
| 패키지의 `reports/` | 최신 문서 확인·인벤토리·중복 분석 |
| 패키지의 `recommendations/current.json` | 이번 권고 실행과 파일 목록, 후보 0건도 표시 |
| 패키지의 `recommendations/runs/<id>/` | 실행별 검토 초안 |
| `~/.agent-policy-radar/discovery/` | 문서 링크 발견 기록 |
| `~/.agent-policy-radar/reviews/` | 정리 초안·diff·원본/제안/패치 해시 |
| `~/.agent-policy-radar/audit/` | 통합 CLI 시작/종료·환경·설정/코드 해시·결과 전후 기록 |

Windows의 `~`는 사용자 홈입니다. 상세 Review Workflow ledger는 사용자가 정한 경로에 별도로 저장합니다.

- `reports/`와 source state/snapshot은 다음 실행에서 덮어쓸 수 있습니다. 설치 캐시 안의 산출물도 업데이트 시 보존을 보장하지 않습니다.
- 통합 CLI의 감사 기록은 지정된 보고서·권고·snapshot의 전후 내용을 사용자 홈에 보존합니다. 개별 스크립트 직접 실행은 이 통합 감사를 우회합니다.
- 루트에 남아 있는 예전 `recommendations/*.md`는 현재 결과가 아닙니다. 반드시 `current.json`을 확인하세요.
- **기록에는 사적 지침·경로·문서 발췌가 포함될 수 있습니다.** 공개 이슈·Git·외부 모델로 자동 전송하지 말고 공유 전 점검하세요. Markdown도 비밀정보가 없다고 보장하지 않습니다.
- 과거 보고서나 Git 이력은 소급 정화하지 않습니다. 보존기간 자동 정리·위변조 방지·완전한 승인→적용 감사 연결은 아직 없습니다. Windows 접근 제어는 POSIX 권한 설정만으로 보장되지 않습니다.

자세한 범위는 [PRIVACY.md](PRIVACY.md), [TERMS.md](TERMS.md)를 참고하세요.

## 검증한 것과 아직 검증하지 않은 것

**확인한 범위**
- macOS·Windows의 CLI 플러그인 설치·활성화 및 Windows Policy Radar 전체 점검
- 오탐·결과 잔존·설정 제외·기록 도구 등의 fixture 회귀 테스트
- 논문 스킬의 모의 요청 검증, 실제 JMLR 논문 2편의 선택 페이지 기반 관련 연구 문단·인용·수치 대조

**보장하지 않는 범위**
- 스킬 단독의 성능 향상이나 최신 모델 최적화 효과
- 모든 논문·분야의 정확성, 체계적 문헌검색의 완전성
- 실제 간호학 데이터의 통계적/임상적 타당성, IRB 적합성, SPSS/AMOS 실제 실행
- 일반 앱·모바일·클라우드로의 플러그인 자동 동기화

문서 검토, 설치 검사, 실제 작업 품질 검증을 구분합니다. 구체적인 결과와 부분 실패는 [findings/](findings/)에 기록돼 있습니다.

## 피드백과 개발

문제가 생기면 [이슈](https://github.com/HoonStyle/agent-policy-radar/issues)에 **사용한 플러그인/하네스 버전, 요청 범위, 기대 결과, 실제 차이, 최소 재현 예시**를 남겨 주세요. 개인 원고·환자/참여자 정보·토큰·전체 대화 대신 비식별 발췌나 합성 예시를 사용하세요.

피드백은 자동 수정 명령이 아닙니다. 확인된 문제만 최소 변경하고 영향 범위를 검증합니다. 개인 취향은 공통 규칙보다 사용자/프로젝트 설정으로 다루고, 최신 동향만으로 지침을 늘리지 않습니다.

```sh
python3 -m unittest discover -s tests -v
```

GitHub Actions는 push·PR·수동 실행마다 Python 3.11의 macOS 및 Windows(`PYTHONUTF8=0/1`) 테스트와 패키징 검사를 수행합니다. 외부 사이트·유료 모델·로그인을 요구하는 실사용 검증은 이 CI에 포함되지 않습니다. 로그 보존기간은 14일입니다.

릴리즈는 manifest·CHANGELOG를 갱신하고 `v<버전>` 태그를 push하면, **같은 태그의 CI 통과 후 GitHub Release가 자동 생성**됩니다. 버전 결정·태그 생성·사용자 PC 업데이트까지 자동인 것은 아닙니다. 별도 GitHub 권한 정책으로 수동 우회를 차단한 구성도 아닙니다.

## 저장소 구성

```text
.claude-plugin/           Claude Code 마켓·기본 플러그인 manifest
.agents/plugins/         Codex 마켓 manifest
plugin.json              기본 portable plugin manifest
skills/agent-policy-radar/  기본 점검 스킬
plugins/review-workflow/    선택형 개발 리뷰 스킬·기록 CLI
plugins/paper-research/     선택형 논문 연구 스킬·참고 문서
scripts/                 Policy Radar CLI
tests/                   회귀 테스트
sources/                 공식 문서 기록
findings/                관측·검증 결과 및 한계
recommendations/         제안·실행별 검토 초안
notes/                   결정 기록
```

## 라이선스

프로젝트 코드와 자체 문서는 [MIT License](LICENSE)를 따릅니다. 인용·참조한 논문, 공식 문서 및 제3자 자료의 권리는 각 권리자에게 있으며, 이 저장소의 라이선스가 해당 자료의 권리를 대체하지 않습니다.
