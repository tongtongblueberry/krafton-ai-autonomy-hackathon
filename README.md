# KRAFTON Autonomy Lab

[KRAFTON AI Autonomy Hackathon](https://kraftonai-autonomy-hackathon.com/)에서 조종 입력으로 배의 궤적을 예측했다. 조종 정책을 학습할 때는 정상 주행 시연만 쓴 경우와 항로를 벗어났다가 복귀하는 시연을 섞은 경우의 성능을 비교했다. 영상 과제에서는 과거 화면과 행동으로 다음 화면의 특징을 예측하는 모델을 구현했다.

[궤적 오차 예제](examples/README.md#drift)는 세 개의 합성 궤적으로 두 가지 오차를 비교한다. 예측 위치와 관측 위치의 차이가 시간에 비례하면 일정한 속도 차이로 설명할 수 있다. 여기에 사인 곡선 모양의 오차를 더하면 속도 보정 뒤에도 오차가 일부 남는다. Python과 NumPy로 CPU에서 실행할 수 있다.

```sh
git clone https://github.com/tongtongblueberry/krafton-ai-autonomy-hackathon.git
cd krafton-ai-autonomy-hackathon
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python examples/current_drift.py
```

두 로봇 조종 정책이 같은 출발점 50개에서 몇 번씩 성공했는지는 `python3 examples/read_results.py robomimic --metric final_successes`로 확인할 수 있다. 이 명령은 Python 표준 라이브러리만 사용한다.

| 프로젝트에서 다룬 질문 | 여기서 볼 수 있는 것 |
|---|---|
| **1 · 항법.** 같은 상황에서 어떤 조종이 충돌 없이 목적지까지 이어지는가? | [공개 BARN 코스에서 비교한 두 플래너의 완주 시간과 점수](results/README.md#barn) |
| **2-1 · 동역학.** 위치 오차가 일정한 드리프트인지, 다른 운동을 놓쳤기 때문인지 어떻게 구분할까? | [실제 보정 과정에서 사용한 잔차 함수와 합성 반례](examples/current_drift.py) |
| **2-2 · 데이터 설계.** 학습기를 고정해도 복구 시연을 섞으면 행동이 바뀔까? | [복구 시연 0%·50%·100% 자체 비교](results/README.md#recovery) · [초기 상태를 맞춰 정책을 비교하는 코드](autonomy_lab/behavior_evaluation.py) |
| **3 · 월드 모델.** 같은 화면에서 다른 행동을 하면 다음 상태가 어떻게 달라질까? | [과거 행동을 함께 읽는 GRU 예측기](autonomy_lab/world_model.py) · [예측 모델을 제어에 사용한 PlaNet 비교](results/README.md#planet) |

예를 들어 선박 조종 비교에서 복구 시연을 절반 섞자 복구 출발 점수가 **62.695에서 64.948**로 올랐다. 정상 출발 점수는 **64.742에서 64.678**로 거의 같았다. 같은 학습기와 고정된 자체 평가 장면에서 얻은 값이다. [결과표와 해석 범위](results/README.md) · [집계 CSV](results/observations.csv)

[예제 사용법](examples/README.md) · [구현별 입력과 출력](autonomy_lab/README.md) · [외부 벤치마크 비교와 학습 곡선](results/README.md#robomimic-lift)

## 컴퓨팅 지원

KRAFTON AI Autonomy Hackathon 참가를 위한 이 프로젝트의 일부 GPU 실험은 Deepest를 통해 지원받은 [VESSL AI](https://vessl.ai/)의 컴퓨팅 자원으로 수행했습니다. 컴퓨팅 자원을 지원해 주신 VESSL AI와 지원을 연결해 주신 Deepest에 감사드립니다.
