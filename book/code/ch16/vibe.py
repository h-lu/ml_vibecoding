# 请在运行 Python 脚本的终端中，执行以下命令：
# export PYTORCH_ENABLE_MPS_FALLBACK=1

import os
import torch
from datasets import Dataset
from transformers import AutoModelForCausalLM, AutoTokenizer
from trl import DPOConfig, DPOTrainer
import warnings

# 忽略一些不影响核心功能的警告
warnings.filterwarnings("ignore")

def main():
    """
    一个完整的DPO（Direct Preference Optimization）训练脚本，
    用于微调语言模型使其回答更礼貌。
    """
    # 1. 模型选择
    model_name = "Qwen/Qwen3-0.6B"
    
    # 确定设备，优先使用MPS (Apple Silicon GPU)
    device = "mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")
    
    # 2. 模型加载
    # 加载策略模型 (policy model)，这是我们将在DPO中进行训练和更新的模型。
    print(f"Loading policy model from: {model_name}")
    policy_model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16,  # 使用 float16 避免在旧版macOS上的bfloat16错误
        trust_remote_code=True       # Qwen模型需要信任远程代码
    ).to(device)
    
    # 显式地创建参考模型 (reference model)。
    # 在DPO中，参考模型是策略模型优化前的一个固定快照，用于计算KL散度来约束策略模型的更新幅度。
    print(f"Loading reference model from: {model_name}")
    ref_model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16, # 同样使用 float16
        trust_remote_code=True
    ).to(device)
    
    # 加载分词器 (Tokenizer)
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    # 如果分词器没有定义填充符 (pad_token)，则使用句末符 (eos_token) 作为填充符
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
        
    # 3. 偏好数据集
    # 直接在脚本中创建一个小型的、内存中的偏好数据集。
    # 数据集围绕“礼貌”这一主题，每个样本包含一个提示(prompt)、一个偏好的回答(chosen)和一个不偏好的回答(rejected)。
    print("Creating in-memory preference dataset...")
    preference_dataset = [
        {
            "prompt": "我的代码运行不了，你能帮我看看吗？",
            "chosen": "当然可以，我很乐意帮助你。为了更好地理解问题，你能否分享一下你的代码片段、你期望它实现的功能，以及它报了什么错吗？",
            "rejected": "代码是你写的，你自己搞定。",
        },
        {
            "prompt": "你能解释一下什么是机器学习吗？我完全不懂。",
            "chosen": "没问题。机器学习可以看作是教计算机从数据中学习规律和模式，而不是直接编程告诉它怎么做。就像我们通过看很多猫的照片学会识别猫一样。你想从哪个方面开始了解呢？",
            "rejected": "自己上网搜，这个很简单。",
        },
        {
            "prompt": "我预订的会议室被别人占用了，该怎么办？",
            "chosen": "遇到这种情况确实很麻烦。我建议你先友好地和对方确认一下预订信息，也许是个误会。如果不行，可以联系行政部门寻求帮助。需要我帮你查看其他可用的会议室吗？",
            "rejected": "那你去跟他们吵啊，问我干嘛？",
        },
    ]
    
    # 将Python列表转换为Hugging Face的Dataset对象，以便与Trainer兼容
    train_dataset = Dataset.from_list(preference_dataset)

    # 4. DPO 训练器配置
    output_dir = "./dpo_qwen_polite_aligned_model"
    
    dpo_config = DPOConfig(
        output_dir=output_dir,
        num_train_epochs=2,
        per_device_train_batch_size=1,
        gradient_accumulation_steps=2,
        learning_rate=5e-5,
        lr_scheduler_type="cosine",
        warmup_ratio=0.1,
        logging_steps=10,
        bf16=False,                  # 显式禁用bf16以解决MPS兼容性问题
        report_to="none",           # 关闭向wandb等平台的报告
        beta=0.1,                   # DPO中KL散度的权重，是平衡偏好学习和保持与原始模型相似性的关键超参数
        max_prompt_length=128,      # 提示的最大长度
        max_length=256,             # 样本（提示+回答）的最大总长度
        remove_unused_columns=False,# DPO需要'prompt', 'chosen', 'rejected'列，不要移除它们
    )

    # 初始化DPOTrainer
    # DPOTrainer封装了DPO训练循环的所有逻辑
    dpo_trainer = DPOTrainer(
        model=policy_model,         # 传入策略模型
        ref_model=ref_model,        # 传入参考模型
        args=dpo_config,            # 传入DPO配置
        train_dataset=train_dataset,# 传入训练数据集
        processing_class=tokenizer, # 正确的参数名
    )
    
    # 启动训练
    print("\nStarting DPO training...")
    dpo_trainer.train()
    print("Training completed.")
    
    # 保存对齐后的模型
    print(f"Saving aligned model to {output_dir}...")
    dpo_trainer.save_model(output_dir)
    print("Model saved.")

    # 5. 效果对比
    print("\n--- Comparing Model Performance ---")
    
    # 在DPO训练中，policy_model的权重已经被原地更新，可以直接用于生成
    dpo_model = dpo_trainer.model 
    
    # 选择一个测试prompt
    test_prompt = "我不太明白你刚才说的那个概念，能再解释一遍吗？"
    
    # 使用Qwen2的聊天模板来格式化输入, 并关闭thinking模式
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": test_prompt}
    ]
    input_text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=False  # 关闭 "Thinking" 模式
    )
    model_inputs = tokenizer([input_text], return_tensors="pt").to(device)

    print(f"\n[Test Prompt]: {test_prompt}")

    # 使用原始模型（参考模型）生成回答
    print("\n--- Response from Original Model (ref_model) ---")
    generated_ids_ref = ref_model.generate(
        model_inputs.input_ids,
        max_new_tokens=100,
        pad_token_id=tokenizer.eos_token_id
    )
    response_ref_full = tokenizer.decode(generated_ids_ref[0], skip_special_tokens=True)
    # 精确提取模型生成的回答部分
    response_ref = response_ref_full.split("<|im_start|>assistant\n")[-1].strip()
    print(response_ref)

    # 使用DPO对齐后的模型生成回答
    print("\n--- Response from DPO-aligned Model ---")
    generated_ids_dpo = dpo_model.generate(
        model_inputs.input_ids,
        max_new_tokens=100,
        pad_token_id=tokenizer.eos_token_id
    )
    response_dpo_full = tokenizer.decode(generated_ids_dpo[0], skip_special_tokens=True)
    # 精确提取模型生成的回答部分
    response_dpo = response_dpo_full.split("<|im_start|>assistant\n")[-1].strip()
    print(response_dpo)
    
    print("\n--- Comparison Finished ---")
    print("Notice how the DPO-aligned model's response is likely more polite and helpful.")

if __name__ == "__main__":
    main()
