#!/bin/bash

set -e

# ===============================
# 変数の設定
# ===============================

# 評価に使用するモデル
EVALUATION_MODEL="gpt-4o-2024-08-06"

# 評価に使用する指標のID（スペース区切りで指定）
CRITERIA_IDS="6 7 8"

# テンプレートの設定
TEMPERATURE=0

# 最大トークン数の設定
MAX_TOKENS=1000

# 入力ファイルのパス（生成された反論のファイル）
INPUT_FILE="generated_counterarguments.json"

# 出力ファイルのパス
OUTPUT_FILE="evaluation_results_4-7.json"

# 評価対象のx（カンマ区切りで指定）
EVALUATION_TARGETS="x4,x5,x6,x7"

# ===============================
# スクリプトの実行
# ===============================

# evaluate.pyを実行
python3 evaluate/evaluate.py \
  --input "$INPUT_FILE" \
  --output "$OUTPUT_FILE" \
  --evaluation-model "$EVALUATION_MODEL" \
  --criteria-ids $CRITERIA_IDS \
  --temperature "$TEMPERATURE" \
  --max-tokens "$MAX_TOKENS" \
  --evaluation-targets "$EVALUATION_TARGETS"