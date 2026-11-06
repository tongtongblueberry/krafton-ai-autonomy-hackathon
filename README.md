# KRAFTON Autonomy Lab

[KRAFTON AI Autonomy Hackathon](https://kraftonai-autonomy-hackathon.com/)에 참가하며 만든 실험 중, 외부에서도 살펴볼 수 있는 코드와 결과를 모았다. 프로젝트에서는 선박이 장애물을 피해 목적지에 가는 항법, 조종 입력에 따른 움직임 예측, 영상에서 다음 상태와 행동을 추정하는 월드 모델을 다뤘다.

**처음이라면 [궤적 오차 예제](examples/README.md#drift)부터 보세요.** 예측한 배의 위치와 관측한 위치가 매초 일정하게 벌어진다면 하나의 속도 차이로 설명할 수 있다. 오차가 시간에 따라 곡선을 그리면 같은 보정을 해도 일부가 남는다. 작은 합성 궤적으로 두 경우를 확인한다. 실제 선박 데이터나 GPU는 필요하지 않다.

```sh
git clone https://github.com/tongtongblueberry/krafton-ai-autonomy-hackathon.git
cd krafton-ai-autonomy-hackathon
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python examples/current_drift.py
```

설치 없이 숫자부터 보려면 저장소 루트에서 `python examples/read_results.py robomimic --metric final_successes`를 실행하면 된다. 표와 그림은 로그인 없이 읽을 수 있다. 공개한 범위는 직접 작성한 구현, 합성 예제, 집계 결과다. [대회와 세 문제의 공식 소개](https://kraftonai-autonomy-hackathon.com/)

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
