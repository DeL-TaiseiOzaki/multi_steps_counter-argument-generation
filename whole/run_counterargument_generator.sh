#!/bin/bash

set -e
# 使用するAIモデル
MODELS=("mini" "gpt" "llama")

# テンプレートの設定
TEMPERATURE=0.7

# 最大トークン数の設定
MAX_TOKENS=1500

# 使用する条件
CONDITIONS="x1 x2 x3 x4"

# 評価に使用するモデル
EVALUATION_MODEL="gpt-4o-2024-08-06"

# 評価に使用する指標のID（スペース区切りで指定）
CRITERIA_IDS="1 2 3 4 5 6 7 8"  # 例としてID 1, 2, 3を指定

# モデル名をスペース区切りの文字列に変換
MODELS_STR="${MODELS[@]}"

# main.pyを実行
python main.py \
  --models $MODELS_STR \
  --temperature "$TEMPERATURE" \
  --max-tokens "$MAX_TOKENS" \
  --conditions $CONDITIONS \
  --input "$INPUT_FILE" \
  --output "$OUTPUT_FILE" \
  --evaluation-model "$EVALUATION_MODEL" \
  --criteria-ids $CRITERIA_IDS
