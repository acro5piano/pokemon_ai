# IDをone-hotにするアブレーション実験

入力を0〜1にそろえた前回の実験から、さらにポケモンIDと技IDの表現だけを変えて比較した。

## one-hotとは

元実装では、ポケモンの種類を図鑑IDで表していた。

```text
Rhydon   = 112
Starmie  = 121
Jolteon  = 135
```

この表現では、ニューラルネットから見ると `135 > 121 > 112` という順序と距離がある。one-hotでは、種類ごとに専用のスイッチを1つ用意する。

```text
Rhydon   = [1, 0, 0]
Starmie  = [0, 1, 0]
Jolteon  = [0, 0, 1]
```

これなら、種類同士に存在しない大小関係を作らない。ニューラルネットの第1層も、各種類に別々の重みを持てる。

実装は次のとおり。

```python
SPECIES_IDS = (112, 121, 135)


def one_hot(value, categories):
    return [1.0 if value == category else 0.0 for category in categories]


def species_onehot_to_array(pokemon):
    return [
        *one_hot(pokemon.id, SPECIES_IDS),
        max(0, pokemon.actual_hp) / max_hp,
        *[move.id / 9 for move in pokemon.actual_moves],
    ]
```

## 比較した3方式

| 方式 | ポケモン | HP | 技 | 全入力数 |
|---|---|---|---|---:|
| `scaled` | `id / 135` | HP割合 | `id / 9` | 84 |
| `species_onehot` | 3要素のone-hot | HP割合 | `id / 9` | 108 |
| `onehot` | 3要素のone-hot | HP割合 | 各技枠を9要素のone-hot | 492 |

隠れ層はすべて10×10のままにした。相手の切り替え、報酬、Replay Buffer、1試合1更新、違法行動を含むTDターゲットも変更していない。

## 条件

- 各方式を1,000試合学習
- seed 0〜4の5回
- 学習後は更新と探索を停止
- Random/Attack相手へ各seed 300戦
- Python 3.10.20 / NumPy 1.23.2 / scikit-learn 1.1.2

## 結果

| 入力表現 | vs Random | vs Attack |
|---|---:|---:|
| IDを0〜1化 | 94.1 ± 9.5% | 65.1 ± 19.5% |
| **ポケモンだけone-hot** | **99.0 ± 0.6%** | **80.3 ± 1.5%** |
| ポケモン＋技をone-hot | 96.9 ± 4.0% | 76.9 ± 5.1% |

### seedごとのAttack勝率

| seed | IDを0〜1化 | ポケモンだけone-hot | ポケモン＋技one-hot |
|---:|---:|---:|---:|
| 0 | 54.7% | 78.3% | 84.0% |
| 1 | 77.3% | 80.3% | 75.3% |
| 2 | 83.3% | 82.3% | 79.7% |
| 3 | 36.0% | 79.7% | 70.3% |
| 4 | 74.0% | 81.0% | 75.3% |

ポケモンだけをone-hotにすると、Attack相手の平均勝率が65.1%から80.3%へ上がった。さらに標準偏差が19.5%から1.5%へ下がり、seedによる当たり外れが大幅に減った。

## なぜ「全部one-hot」が一番ではなかったのか

この環境では、各ポケモンが覚えている技が種類によって固定されている。そのため、ポケモン種類が分かれば技構成もほぼ分かり、技のone-hotは重複情報になりやすい。

また、全入力が108から492へ増えた一方、隠れ層は10×10のままである。小さなネットワークに対して入力だけを大きくしすぎたため、ポケモンだけをone-hotにした方が効率よく学習できた可能性がある。

one-hot化では入力層のパラメータ数も増えるため、改善のすべてを「大小関係を消した効果」だけとは断定できない点にも注意が必要である。

## embeddingならどうするか

embeddingは、カテゴリごとに短い学習可能なベクトルを割り当てる方法である。

```python
# PyTorchの例。3種類を4個の数字で表現する
embedding = torch.nn.Embedding(num_embeddings=3, embedding_dim=4)

species_index = torch.tensor([2])  # Jolteon
species_vector = embedding(species_index)
```

最初はランダムなベクトルだが、対戦の学習と一緒に更新される。似た役割のポケモンは似たベクトルになる可能性がある。何百・何千種類もある場合はone-hotより省スペースだが、今回のように3種類しかない場合はone-hotの方が単純で解釈しやすい。

`scikit-learn`の`MLPRegressor`にはembedding層がないため、試すならPyTorchやTensorFlowなどでネットワークを組み直す必要がある。

## 結論

この小さな環境では、**ポケモンIDだけをone-hotにする方法が最も強く、最も安定した**。昔の実装で必要だったのは、図鑑番号を割り算することではなく、「3種類のどれか」を3個の独立したスイッチとして渡すことだった。

ただし、本物の多数のポケモンを扱うなら、one-hotは巨大になる。種類が少なければone-hot、種類が多ければembedding、という使い分けが現実的である。

## 再現方法

```bash
python -m experiments.input_scaling_ablation \
  --episodes 1000 \
  --battles 300 \
  --seeds 0 1 2 3 4 \
  --modes scaled species_onehot onehot \
  --output docs/reports/categorical-encoding-ablation.json
```

生データは [`categorical-encoding-ablation.json`](categorical-encoding-ablation.json) に保存している。
