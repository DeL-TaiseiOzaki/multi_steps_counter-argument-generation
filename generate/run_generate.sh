#!/bin/bash

set -e

# ===============================
# 変数の設定
# ===============================

# 使用するAIモデル
MODELS=("mini" "gpt" "llama")

# テンプレートの設定
TEMPERATURE=0.7

# 最大トークン数の設定
MAX_TOKENS=150

# 使用する条件
CONDITIONS="x1 x2 x3 x4 x5 x6"

# 入力ファイルのパス
INPUT_FILE="sample_input.json"

# 出力ファイルのパス
OUTPUT_FILE="generated_counterarguments.json"

# ===============================
# スクリプトの実行
# ===============================

# モデル名をスペース区切りの文字列に変換
MODELS_STR="${MODELS[@]}"

# generate.pyを実行
python3 generate/generate.py \
  --models $MODELS_STR \
  --temperature "$TEMPERATURE" \
  --max-tokens "$MAX_TOKENS" \
  --conditions $CONDITIONS \
  --input "$INPUT_FILE" \
  --output "$OUTPUT_FILE"
