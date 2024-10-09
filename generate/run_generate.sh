#!/bin/bash

set -e

# ===============================
# 変数の設定
# ===============================

# 使用するAIモデル
MODELS=("mini" "gpt" "llama")

# テンプレートの設定
TEMPERATURE=0

# 最大トークン数の設定
MAX_TOKENS=150

# 使用する条件
CONDITIONS="x1 x2 x3 x4 x5 x6 x7"

# 入力ファイルのパス
INPUT_FILE="input.json"

# 出力ファイルのパス
OUTPUT_FILE="generated_counterarguments.json"

# ID範囲の初期化
ID_RANGE=""

# ===============================
# コマンドライン引数の処理
# ===============================

while getopts "r:" opt; do
  case ${opt} in
    r )
      ID_RANGE=$OPTARG
      ;;
    \? )
      echo "Usage: $0 [-r id_range]"
      echo "id_range can be a single ID, a range (e.g., '1-3'), or a comma-separated list (e.g., '2,4,6')"
      exit 1
      ;;
  esac
done

# ===============================
# スクリプトの実行
# ===============================

# モデル名をスペース区切りの文字列に変換
MODELS_STR="${MODELS[@]}"

# generate.pyを実行
if [ -z "$ID_RANGE" ]; then
  # ID範囲が指定されていない場合、全てのデータを処理
  python3 generate/generate.py \
    --models $MODELS_STR \
    --temperature "$TEMPERATURE" \
    --max-tokens "$MAX_TOKENS" \
    --conditions $CONDITIONS \
    --input "$INPUT_FILE" \
    --output "$OUTPUT_FILE"
else
  # 指定されたID範囲のデータのみを処理
  python3 generate/generate.py \
    --models $MODELS_STR \
    --temperature "$TEMPERATURE" \
    --max-tokens "$MAX_TOKENS" \
    --conditions $CONDITIONS \
    --input "$INPUT_FILE" \
    --output "$OUTPUT_FILE" \
    --id-range "$ID_RANGE"
fi