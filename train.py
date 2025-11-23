from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from trl import SFTTrainer, SFTConfig
from datasets import load_dataset
from peft import LoraConfig
import torch

MODEL_NAME = "D:/denji_training/models/kanana-8b"

# -------------------------
# 1. Load dataset
# -------------------------
dataset = load_dataset("json", data_files="data/denji.jsonl")["train"]

# Convert messages -> text
def format_messages(example):
    msgs = example["messages"]
    text = ""
    for m in msgs:
        if m["role"] == "user":
            text += f"User: {m['content']}\n"
        else:
            text += f"Assistant: {m['content']}\n"
    example["text"] = text
    return example

dataset = dataset.map(format_messages)

# -------------------------
# 2. Tokenizer
# -------------------------
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token

# -------------------------
# 3. QLoRA quantization config
# -------------------------
quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4"
)

# -------------------------
# 4. Load base model (4bit)
# -------------------------
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    device_map="auto",
    quantization_config=quant_config,
    torch_dtype=torch.float16
)

# -------------------------
# 5. LoRA config
# -------------------------
lora_config = LoraConfig(
    r=64,
    lora_alpha=16,
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

# -------------------------
# 6. SFT config
# -------------------------
sft_config = SFTConfig(
    output_dir="denji-lora",
    per_device_train_batch_size=1,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    num_train_epochs=2,
    fp16=True,
    bf16=False,
    logging_steps=10,
    max_steps=-1
)

# -------------------------
# 7. Trainer
# -------------------------
trainer = SFTTrainer(
    model=model,
    args=sft_config,
    peft_config=lora_config,
    train_dataset=dataset
)

# -------------------------
# 8. Train
# -------------------------
trainer.train()

trainer.model.save_pretrained("denji-lora")
tokenizer.save_pretrained("denji-lora")

print("🎉 Training complete! LoRA saved to ./denji-lora")
