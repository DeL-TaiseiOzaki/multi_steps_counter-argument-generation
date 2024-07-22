# デフォルト値の設定
MODEL="gpt-3.5-turbo"
TEMPERATURE=0.7
MAX_TOKENS=200
CONDITIONS=("x1" "x2" "x3" "x4") #("x1", "x2", "x3", "x4")
INPUT_FILE="input.json"
OUTPUT_METHOD="file" # 'print' or 'file'
OUTPUT_FILE="output.txt"

# コマンドライン引数の解析
while [[ $# -gt 0 ]]; do
  key="$1"
  case $key in
    -m|--model)
      MODEL="$2"
      shift 2
      ;;
    -t|--temperature)
      TEMPERATURE="$2"
      shift 2
      ;;
    -mt|--max-tokens)
      MAX_TOKENS="$2"
      shift 2
      ;;
    -c|--conditions)
      IFS=',' read -ra CONDITIONS <<< "$2"
      shift 2
      ;;
    -i|--input)
      INPUT_FILE="$2"
      shift 2
      ;;
    -o|--output)
      OUTPUT_METHOD="$2"
      shift 2
      ;;
    -of|--output-file)
      OUTPUT_FILE="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# 入力ファイルが指定されているか確認
if [ -z "$INPUT_FILE" ]; then
  echo "Error: Input file not specified. Use -i or --input to specify the input JSON file."
  exit 1
fi

# 出力方法が'file'の場合、出力ファイルが指定されているか確認
if [ "$OUTPUT_METHOD" == "file" ] && [ -z "$OUTPUT_FILE" ]; then
  echo "Error: Output file not specified. Use -of or --output-file to specify the output file when using file output method."
  exit 1
fi

# Pythonスクリプトの実行
python3 main.py --model "$MODEL" --temperature "$TEMPERATURE" --max-tokens "$MAX_TOKENS" --conditions "${CONDITIONS[@]}" --input "$INPUT_FILE" --output "$OUTPUT_METHOD" ${OUTPUT_FILE:+--output-file "$OUTPUT_FILE"}