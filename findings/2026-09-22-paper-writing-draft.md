### 관련 연구

제공된 선택 페이지 발췌만 읽었으며, 원문 전체 열람이나 외부 검색·실험은 수행하지 않았다.  
① Blei 등(2003)의 LDA는 문서를 잠재 토픽의 확률적 혼합으로, 각 토픽을 단어 분포로 표현하고 문서별 토픽 비율에 디리클레 분포를 부여한 생성모형이라는 **모델 기여**를 갖는다(Blei 등, 2003, 인쇄 p. 996, §3). ② 이 연구는 모델 제안뿐 아니라 변분 근사 추론과 경험적 베이즈 모수 추정을 위한 EM 알고리즘도 제시했다(Blei 등, 2003, 인쇄 p. 993, 초록). ③ 반면 Hoffman 등(2013)의 SVI는 새로운 토픽 모델 자체보다 대규모 자료의 사후분포를 근사하는 확장 가능한 알고리즘이라는 **추론 기여**에 초점이 있으며, LDA와 HDP 토픽 모델에 이를 적용했다(Hoffman 등, 2013, 인쇄 p. 1303, 초록). ④ 이들의 실험에는 Wikipedia 문서 **380만 개**가 포함되었고, 해당 컬렉션에서 문서 1만 개를 학습에 사용하지 않는 테스트 세트로 분리했다(Hoffman 등, 2013, 인쇄 p. 1336, §4). ⑤ Figure 11에서 망각률 κ=0.9, 미니배치 크기 500문서일 때 Wikipedia의 평균 예측 로그우도는 **LDA100 −7.41, HDP −7.07**로, 값이 클수록 좋은 해당 지표에서 HDP가 더 높았다(Hoffman 등, 2013, 인쇄 pp. 1336–1337, §4 및 Figure 11). ⑥ 다만 이는 SVI 논문 내부의 모델 비교이며, 평가 방식도 LDA 원 논문의 held-out perplexity와 구분되므로, 두 논문의 원 실험을 동일 조건에서 직접 비교한 결과로 해석해서는 안 된다(Hoffman 등, 2013, 인쇄 pp. 1336–1337, §4 및 Figure 11).

### 문장별 근거 대조표

| 문장 | 발췌에서 확인한 근거 | 주장 범위 |
|---|---|---|
| ① | Blei 등(2003), p. 996, §3: 문서·토픽 표현 및 θ∼Dir(α) | 모델 구조 |
| ② | Blei 등(2003), p. 993, 초록: 변분 추론 및 EM | 저자가 제시한 방법 |
| ③ | Hoffman 등(2013), p. 1303, 초록: 확장 가능한 사후 근사, LDA·HDP 적용 | 추론 기여 |
| ④ | Hoffman 등(2013), p. 1336, §4: Wikipedia 3.8M, 테스트 10,000문서 | 보고된 자료·분할 |
| ⑤ | Hoffman 등(2013), pp. 1336–1337, §4·Figure 11: 지표 방향, 설정, 두 수치 | 특정 설정의 보고 결과 |
| ⑥ | Hoffman 등(2013), pp. 1336–1337: 평가 방식 구분 및 논문 내부 비교 | 비교 범위에 대한 해석 |

### 참고문헌

- Blei, D. M., Ng, A. Y., & Jordan, M. I. (2003). Latent Dirichlet Allocation. *Journal of Machine Learning Research, 3*, 993–1022. https://www.jmlr.org/papers/volume3/blei03a/blei03a.pdf
- Hoffman, M. D., Blei, D. M., Wang, C., & Paisley, J. (2013). Stochastic Variational Inference. *Journal of Machine Learning Research, 14*, 1303–1347. https://www.jmlr.org/papers/volume14/hoffman13a/hoffman13a.pdf

**추가 질문 판정:** 아니요—Figure 11의 특정 자료·설정·지표에서 관찰된 우위를 모든 데이터에서의 HDP 우위로 일반화할 수 없습니다(Hoffman 등, 2013, p. 1337, Figure 11).
