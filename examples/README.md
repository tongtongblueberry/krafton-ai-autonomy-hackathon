# 실행 예제

두 파일 모두 저장소를 복제한 뒤 루트에서 실행한다.

| 파일 | 입력 | 무엇을 확인하는가 |
|---|---|---|
| [current_drift.py](current_drift.py) | 파일 안에서 만드는 합성 궤적 3개. NumPy 필요 | 알려진 일정한 속도만큼 위치가 어긋난 경우와, 거기에 굽은 오차가 추가된 경우를 비교한다. |
| [read_results.py](read_results.py) | 저장소에 포함된 [집계 CSV](../results/observations.csv). Python 표준 라이브러리만 사용 | 과거 실험의 관측값, 단위, 비교 범위를 표시한다. |

<a id="drift"></a>

## 궤적 오차에서 일정한 드리프트 분리하기

```sh
python -m pip install -r requirements.txt
python examples/current_drift.py
```

예제는 세 궤적의 예측 위치에 서로 다른 일정한 속도 `v`에 의한 변위 `t × v`를 더해 가상의 관측을 만든다. 함수는 각 궤적의 x, y 방향에 대해 관측과 예측의 차이에 가장 잘 맞는 속도를 구한다. 첫 검사에서는 세 속도를 모두 복원하고 위치 잔차가 허용 오차 안에서 0인지 확인한다. 두 번째 검사에서는 첫 궤적의 x 좌표에 사인 곡선을 더한다. 일정한 속도 성분을 제거하고도 0.1 m보다 큰 오차가 남아야 통과한다.

예를 들어 1·2·3초 뒤 x 방향 위치 오차가 +0.03·+0.06·+0.09 m라면, x 방향으로 매초 0.03 m씩 누적된 셈이다. 첫 번째 합성 궤적에 넣은 x 방향 속도 차이가 바로 0.03 m/s다.

```text
Constant drift: recovered all three known offsets (m/s).
Curved perturbation: the maximum remaining position error exceeds 0.1 m.
```

직접 데이터를 넣을 때 두 위치 배열은 같은 시작점을 기준으로 한 `(에피소드, 시점, 2)` 미터 좌표여야 한다. 시간 배열은 시작 이후의 초 단위 값이고 모든 수는 유한해야 한다. 모든 시각이 0인 데이터로는 속도를 구할 수 없다. 함수가 반환하는 잔차의 부호는 `예측 위치 + 추정 속도 × 시간 − 관측 위치`다. 실제 운항에서는 유속뿐 아니라 속도 추정의 편향도 같은 패턴을 만들 수 있다. 그래서 이 값은 오차 분석에 쓰며, 물리적인 유속 측정값으로 쓰지 않는다.

## 기록된 결과 읽기

```sh
python examples/read_results.py recovery --metric mean_score
python examples/read_results.py robomimic --metric final_successes
```

지원하는 실험 이름은 `recovery`, `barn`, `rlc`, `robomimic`, `planet`이다. `--metric`을 생략하면 해당 실험의 모든 행이 표시된다. 측정값을 세 자리 정도로 읽으려면 [결과 해설](../results/README.md)을, 저장된 정밀도의 값이 필요하면 CSV를 보면 된다.
