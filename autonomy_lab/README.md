# 구현 읽기

| 파일 | 인터페이스 | 용도 |
|---|---|---|
| [behavior_evaluation.py](behavior_evaluation.py) | `summarize_episodes`, `paired_success`, `wilson_interval` | robomimic 비교에서 사용한 평가 함수. 완료·중단·미실행을 구분하고 같은 초기 상태에서 두 정책의 결과를 짝지어 센다. 표준 라이브러리만 사용한다. |
| [world_model.py](world_model.py) | `RecurrentLatentDynamics` | 과거의 영상 특징과 그 사이의 행동으로 GRU 상태를 만들고, 현재 행동에 따른 다음 특징 격자를 예측한다. PyTorch가 필요하다. |
| [\_\_init\_\_.py](__init__.py) | 패키지 진입점 | 개별 모듈을 독립적으로 가져올 수 있게 한다. |

**행동 평가.** 초기 장면이 쉬웠던 쪽을 유리하게 평가하지 않으려면 두 정책이 같은 출발점과 첫 관측을 받았는지 확인해야 한다. `paired_success`는 평가 seed가 같고 두 초기 지문이 모두 일치하는 완료된 에피소드끼리 비교한다. 결과의 `cells`에는 둘 다 성공, 학습 모델만 성공, 비교 모델만 성공, 둘 다 실패한 횟수가 들어 있다. `incomplete_pairs`는 전체 예정 쌍에서 빠진 횟수다. [실제 Lift 비교](../results/README.md#robomimic-lift)

입력은 정책별로 seed당 한 행이어야 한다. `planned`는 계획한 서로 다른 초기 상태 수로, 0보다 크고 실제 시도 횟수 이상이어야 한다. `termination`이 `exception` 또는 `wall_censored`인 경우 미완료로 취급한다. 각 완료 행에는 `seed`, `success`, `initial_state_sha256`, `initial_observation_sha256`이 필요하다. `summarize_episodes`에는 `return`과 `length`도 전달한다. `paired_success`가 돌려주는 ‘one training seed’ 문구는 이 Lift 실험의 조건이다.

**월드 모델.** 최신 프레임이 같아도 이전 움직임과 다음 행동이 다르면 다음 상태가 달라질 수 있다. 이 모듈은 프레임 특징을 작은 벡터로 축소하고, 각 시점의 벡터와 앞선 행동을 차례로 GRU에 넣는다. 마지막 은닉 상태와 현재 행동으로 최신 특징 격자에 더할 변화를 예측한다.

입력이 `(B, T, C, G, G)`라면 과거 행동은 `(B, T-1)`, 현재 행동은 배치당 스칼라 하나, 출력은 `(B, C, G, G)`다. `T`는 생성 시 지정한 `context_length`와 같아야 한다. 아래 예시는 가상의 격자로 텐서 모양을 확인한다. 실제 영상의 인코딩이나 학습 가중치는 필요하지 않다.

```python
from types import SimpleNamespace
import torch
from autonomy_lab.world_model import RecurrentLatentDynamics

layout = SimpleNamespace(channels=4, grid=8, context_length=3)
model = RecurrentLatentDynamics(layout).eval()
with torch.no_grad():
    next_grid = model(torch.zeros(1, 3, 4, 8, 8), torch.zeros(1), torch.zeros(1, 2))
print(tuple(next_grid.shape))  # (1, 4, 8, 8)
```

프로젝트에서 사용한 PyTorch 버전은 2.2.2다. 이 모듈을 사용할 때만 해당 환경에 맞는 [PyTorch](https://pytorch.org/get-started/locally/)를 설치한다.
