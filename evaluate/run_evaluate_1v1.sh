#!/bin/bash

set -e

# ===============================
# 変数の設定
# ===============================

# 評価に使用するモデル
EVALUATION_MODEL="gpt-4o-2024-08-06"

# 評価に使用する指標のID（スペース区切りで指定）
CRITERIA_IDS="6 7 8"

TEMPERATURE=0

# 最大トークン数の設定
MAX_TOKENS=1000

# 入力ファイルのパス（生成された反論のファイル）
INPUT_FILE="generated_counterarguments.json"

# 出力ファイルのパス
OUTPUT_FILE="evaluation_results_3v6.json"

# 比較する2つの反論
X1="x3"
X2="x6"

# ===============================
# スクリプトの実行
# ===============================

# evaluate.pyを実行
python3 evaluate/evaluate_1v1.py \
  --input "$INPUT_FILE" \
  --output "$OUTPUT_FILE" \
  --evaluation-model "$EVALUATION_MODEL" \
  --criteria-ids $CRITERIA_IDS \
  --temperature "$TEMPERATURE" \
  --max-tokens "$MAX_TOKENS" \
  --x1 "$X1" \
  --x2 "$X2"