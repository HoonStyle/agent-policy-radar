# Ledger CLI / 기록 도구

상세 기록이 필요할 때만 사용하는 선택 도구입니다. 작은 수정은 변경 이유·수정 내용·검증 결과를 응답이나 기존 작업 메모에 남기면 됩니다. 프로젝트가 요구하는 기록·검증 기준은 유지합니다. CLI를 선택한 경우에는 아래 구조 검증 규칙을 그대로 적용합니다.

Python 3.10+ required. Resolve `scripts/review.py` relative to this skill's directory; examples below run from that directory. Windows: replace `python3` with `py -3`. No third-party dependencies.

## Project profile / 프로젝트 설정

A team may commit `.review-workflow.json` at the target repository root. Copy and adapt the plugin's `profile.example.json` with user approval. No profile is installed automatically. Missing profile uses language `ko` and `.review-notes` storage. `reviewers`, `checks`, and `additional_requirements` are declarative review context; their commands are never executed by this CLI. The chosen profile and its hash are copied into the ledger at creation.

Default ledger paths are project-relative and cannot escape via `..` or symlinks. An explicit `--output` may choose an external local folder. Ledger/history contain private paths and review text; do not commit automatically. Set up an ignored location by agreement, or use an external folder: otherwise newly created untracked ledgers correctly cause baseline comparison to differ. The tool does not silently ignore its own output or modify `.gitignore`.

```sh
python3 scripts/review.py init --repo "<repository>" --output "<private-dir>/task.json"
python3 scripts/review.py finding "<private-dir>/task.json" --input finding.json
python3 scripts/review.py update "<private-dir>/task.json" --id R-001 --input revised-finding.json
python3 scripts/review.py pass "<private-dir>/task.json" --input pass.json
python3 scripts/review.py validate "<private-dir>/task.json"
python3 scripts/review.py compare "<private-dir>/task.json"
```

`finding` assigns the next R-ID. `update` replaces one finding with supplied full content, preserving its ID and prior states in history. `pass` assigns P-ID. Complete ledger states are kept in a sibling `<ledger>.history/` directory with random names and UTC events; the latest file is atomically replaced. A lock prevents cooperating concurrent CLI writers. A crash may leave a lock; investigate and remove only after confirming no writer remains. History is local and user-editable, not authenticated approval or tamper-proof storage.

## Finding JSON / 지적 입력

```json
{
  "title": "반환 값 불일치",
  "status": "open",
  "classification": "needs investigation",
  "requirement_reference": "spec §2",
  "observed_boundary": "함수 반환까지",
  "unconfirmed_scope": "직렬화 및 외부 응답 미확인",
  "verification": {"level": "unverified"}
}
```

`verified` requires `outcome: pass` and evidence for the declared level:

| level | Required fields in verification |
| --- | --- |
| unverified | Cannot have verified status |
| source | code_location, reasoning |
| execution | command, result, environment |
| simulator / device | command, result, environment, device_id, configuration_id |

A verified finding also requires requirement_reference, observed_boundary, unconfirmed_scope (write an explicit `none` if appropriate). Validation checks record structure, not truth. Nonempty result text is not execution proof. Unknown fields are retained for project-specific context.

## Pass JSON / 검토 입력과 출처

```json
{
  "reviewer": "reviewer-B",
  "initial_reviewer": "author-A",
  "agent": "project-reviewer",
  "model": null,
  "execution_reference": "local-run-123",
  "input_inventory_complete": true,
  "inputs": [
    {"kind": "source", "reference": "commit/path#lines"},
    {"kind": "requirements", "reference": "spec §2"}
  ],
  "finding_ids": ["R-001"],
  "checks": [{"name": "build", "command": "example only", "baseline": "0 errors", "current": "not run", "result": "not-run", "evidence": null}]
}
```

Classification is derived, not accepted from the input's classification field:
- Same reviewer: self.
- Distinct reviewers, complete source/requirements-only inventory and execution reference: independent.
- Distinct reviewers with a complete input inventory including briefing or initial-judgment: comparative.
- Otherwise: unknown. `other` inputs preclude independent classification.

This reflects declared inputs only; it cannot inspect hidden/shared context or establish actual independence. Record the full provided input scope honestly. Model identity is optional and must not be guessed.

## Baseline limits

HEAD, index blob SHA-256, worktree SHA-256 and nonignored untracked SHA-256 are recorded separately. Content is never saved by the baseline collector. Deletions are explicit; renames can appear as delete/add. Symlinks hash link text, not target contents. All tracked files are included to detect later changes to previously clean files. Unmerged indexes and submodules fail with an explicit limitation. Ignored files are excluded. Concurrent file writes require pausing writers; this is not an atomic snapshot. Same hashes establish matching recorded content, not that a reviewer read it. Paths may identify private projects or people.
