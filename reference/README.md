# AI生成の参考実装

[`ai-generated-self-play-dqn/`](ai-generated-self-play-dqn/) は、元実装の失敗分析に使用した、AI生成の自己対戦DQN実装を保存したものです。

## 出典

- 元ディレクトリ: `/home/kazuya/sandbox/20260921_160548`
- ブランチ: `pokemon-dqn`
- コミット: `ea9ca84f2bc6bbc8f23aebf04866fd0d14c3880b`
- 保存方法: 上記コミットのGit管理対象ファイルを `git archive` で展開

ソース、テスト、`pyproject.toml`、`uv.lock` を含みます。元ディレクトリの `.git/`、`.venv/`、キャッシュ、学習ログ、学習済みモデルは生成物のため含めていません。

この実装は元の6対6実装を直接修正したものではなく、固定3対3に問題を縮小して、DQNが学習できる構成を検証した独立した参考実装です。そのため「同じ条件での置き換え」ではありません。

関連資料:

- [設計と実装の図解](../docs/reports/reference-implementation.html)
- [4,000試合の実験レポート](../docs/reports/reference-experiment.html)
- [元実装との比較・失敗分析](../docs/reports/failure-analysis.html)
