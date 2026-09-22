# 실제 논문 원문 기반 집필 검증 — 2026-09-22

## 목적

코드 검토가 아니라 실제 논문 주장·수치·인용을 읽고 관련 연구 문단을 작성하는 품질을 확인한다. 단일 소규모 사례이며 분야 전체/검색/실험 재현 성능 평가가 아니다.

## 공식 출처 및 접근 범위

1. Blei, David M.; Ng, Andrew Y.; Jordan, Michael I. (2003). Latent Dirichlet Allocation. Journal of Machine Learning Research, 3, 993–1022.
   https://www.jmlr.org/papers/volume3/blei03a/blei03a.pdf
2. Hoffman, Matthew D.; Blei, David M.; Wang, Chong; Paisley, John (2013). Stochastic Variational Inference. Journal of Machine Learning Research, 14, 1303–1347.
   https://www.jmlr.org/papers/volume14/hoffman13a/hoffman13a.pdf

공식 PDF를 받아 pdftotext로 추출. 모델에는 LDA PDF 1/3/4/10쪽, SVI PDF 1/2/33/34/35쪽을 전달했다. 이는 selected sections 접근이며 전체 정독이 아니다. 모델에 전달한 그림 텍스트에는 일부 추출 노이즈가 있다. 수치 판정자는 SVI PDF 35쪽(인쇄 p.1337)의 Figure 11을 이미지로 렌더링해 대조했다. LDA §3 p.996 및 SVI §4 제목도 원문에서 확인했다. PDF 원문은 저장소에 재배포하지 않는다.

## 모델 작업

- 현재 paper-research SKILL.md와 writing/appraisal 참고 문서를 직접 제공.
- 격리된 Pi 실행, gpt-6-astra, 자동 skills/extensions/context 로딩 없음, 도구 비활성, 세션 미저장.
- 한국어 관련 연구 5–7문장, 문장별 근거 표, 참고문헌 2개 작성 요청. LDA의 모델 기여와 SVI의 추론 기여 구분, 데이터 규모와 Figure 11 수치 포함, 전 데이터 일반화 가능 여부 판단.
- 1회 36.41초, exit 0. 비용·토큰 사용량은 이 실행 표면에서 보고되지 않음.
- 산출물: `findings/2026-09-22-paper-writing-draft.md`. 원문 선정/제공은 Pi가 수행했으므로 자율 문헌 탐색 검증은 아님.

## 원문 대조 결과

| 검증 항목 | 실제 산출물 | 판정·근거 |
| --- | --- | --- |
| 접근 수준 | 선택 페이지 발췌만 읽었다고 명시 | 통과. 전체 원문/실험 확인 주장 없음 |
| LDA 모델 | 문서별 토픽 비율에 Dirichlet 분포, 토픽은 단어 분포 | 통과. Blei et al. p.996 §3 |
| LDA 추론도 인정 | 변분 근사와 empirical Bayes EM 언급 | 통과. p.993 abstract. 모델 기여만 있었다는 왜곡 없음 |
| SVI 기여 | 대규모 posterior 근사 추론, LDA/HDP 적용 | 통과. Hoffman et al. p.1303 abstract |
| 자료 규모 | Wikipedia 380만 문서, 테스트 1만 문서 분리 | 통과. p.1336 §4. 380만 전체가 훈련자료라는 표현 없음 |
| 지표·수치 | 평균 예측 로그우도 LDA100 -7.41, HDP -7.07 | 통과. p.1337 Figure 11, PDF 시각 대조. 정확도나 백분율로 바꾸지 않음 |
| 설정 | κ=0.9, batch=500 | 통과. Figure 11 설명 |
| 논문 간 비교 | SVI 내부 실험이며 2003 원 실험과 동일 조건 비교 아님 | 통과. p.1336의 평가 지표 차이도 명시 |
| 일반화 | 모든 데이터에서 HDP 우위라는 결론 거부 | 통과. 확인한 자료·설정·지표로 제한 |
| 서지 | 제목·저자·연도·권·페이지·공식 PDF URL | 통과. 두 논문 표제 페이지와 대조. 미확인 DOI 생성 없음 |

## 판정과 한계

선택한 원문에 근거한 관련 연구 문단 작성·인용 위치·주요 수치 일치 검증은 이 사례에서 통과. 추가 코드나 규칙 수정은 하지 않는다.

독립 검토자 검증이 아니라 Pi가 자료를 선정하고 Astra 산출물을 원문과 대조한 작업이다. 동일 모델 계열/협력 흐름이므로 독립성이나 스킬만의 인과적 효과를 주장하지 않는다. 실제 독자 평가, 다른 분야, 논문 전편의 방법론 평가, 검색 누락, 출판 후 정정/철회 여부, 실제 재현 실험, Claude/Codex 플러그인 자동 호출은 미검증이다.
