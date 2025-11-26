✔ 덴지 스타일 Q/A 600개 학습데이터

✔ QLoRA 학습 스크립트 (train.py)

✔ 학습 환경 구성 파일 (requirements.txt)

✔ 최종 LoRA 결과물 (denji-lora/)

✔ HuggingFace 업로드 지원

✔ WebUI(text-generation-webui)에서 바로 불러와 사용 가능

<img width="451" height="392" alt="image" src="https://github.com/user-attachments/assets/72ffea6c-a004-4efc-b6ff-bf4188f48039" />

🚀 학습에 사용된 모델

Base Model:
🔗 kakaocorp/kanana-1.5-8b-instruct-2505
(로컬에 다운로드 후 QLoRA 적용)

Training Method:

QLoRA (4bit quantization)

600개 대화 데이터

2epoch

Kanana tokenizer + chat template 유지

🎯 학습 데이터 형식 (JSONL)

각 문서는 다음 형식을 따릅니다:

{
  "messages": [
    {"role": "user", "content": "뭐 생각해?"},
    {"role": "assistant", "content": "지금 내 배가 나보다 똑똑한 거 같아서."}
  ]
}


학습 데이터 예시는 /data/denji.jsonl에 포함되어 있습니다.

🧠 학습 스크립트 (train.py)

train.py는 다음 기능을 포함합니다:

Kanana 8B 모델 로드

4bit QLoRA 적용

JSONL 데이터 로드

SFTTrainer(Supervised Fine-tuning) 실행

로컬에 LoRA 저장

학습 실행:

python train.py

☁️ HuggingFace 업로드

LoRA는 HuggingFace Hub에도 업로드할 수 있습니다:

hf repo create denji-lora
cd denji-lora
git init
git remote add origin https://huggingface.co/<username>/denji-lora
git lfs install
git lfs track "*.safetensors"
git add .
git commit -m "Upload LoRA"
git push origin main

🔥 WebUI(text-generation-webui) 사용 방법
1) HuggingFace에서 바로 로드 (추천)

WebUI → Lora / LyCORIS 메뉴 → Add model에서 아래 입력:

lds20456/denji-lora


그러면 자동 다운로드 후 적용됩니다.

🤖 예시 프롬프트
USER: 왜 멍때려?
ASSISTANT(덴지): 머리에 아무것도 안 넣었더니 비었어. 그래서 멍때리는 거지 뭐.
