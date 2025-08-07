import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

def generate_creative_text(model, tokenizer, prompt: str, temperature: float, top_p: float, max_new_tokens: int = 150):
    """
    Generates creative text based on a prompt with adjustable parameters.

    Args:
        model: The pre-loaded transformer model.
        tokenizer: The pre-loaded tokenizer.
        prompt (str): The input text to generate from.
        temperature (float): Controls randomness. Higher is more random.
        top_p (float): Nucleus sampling parameter.
        max_new_tokens (int, optional): The maximum number of new tokens to generate. Defaults to 150.

    Returns:
        str: The generated text, decoded.
    """
    messages = [
        {"role": "user", "content": prompt}
    ]
    
    # Format the input using the chat template
    input_ids = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        return_tensors="pt",
        enable_thinking=False,  # Disable thinking mode
    ).to(model.device)

    # Generate text using the specified parameters
    outputs = model.generate(
        input_ids,
        max_new_tokens=max_new_tokens,
        do_sample=True,  # do_sample must be True to use temperature and top_p
        temperature=temperature,
        top_p=top_p
    )
    
    # Decode only the newly generated tokens, not the input prompt
    response = outputs[0][input_ids.shape[-1]:]
    return tokenizer.decode(response, skip_special_tokens=True)

# Main execution block
if __name__ == "__main__":
    # 1. Model and Tokenizer Loading
    MODEL_NAME = "Qwen/Qwen3-0.6B"
    
    # Check for CUDA and bfloat16 support
    device = "cuda" if torch.cuda.is_available() else "cpu"
    torch_dtype = "auto"
    if device == "cuda":
        # The prompt specifically requests bfloat16 for CUDA devices
        torch_dtype = torch.bfloat16

    print(f"Loading model '{MODEL_NAME}' on '{device}' with dtype '{torch_dtype}'...")
    
    try:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            torch_dtype=torch_dtype,
            device_map=device
        )
        print("Model and tokenizer loaded successfully.")

        # 4. Calling examples
        print("\n" + "="*50)
        print("Running creative text generation examples...")
        print("="*50)

        # Example 1: Generate a short story intro
        prompt1 = "在一个代码比诗歌更流行的世界里，一个人工智能实体悄悄地学会了做梦。它的第一个梦是关于..."
        temp1 = 0.85
        top_p1 = 0.95
        print(f"\n--- Example 1: Story Intro ---")
        print(f"Prompt: {prompt1}")
        print(f"Settings: temperature={temp1}, top_p={top_p1}")
        
        generated_text1 = generate_creative_text(
            model=model,
            tokenizer=tokenizer,
            prompt=prompt1,
            temperature=temp1,
            top_p=top_p1,
            max_new_tokens=100
        )
        
        print("\n>>> Generated Text:")
        print(generated_text1)
        
        # Example 2: Generate a product slogan
        prompt2 = "为一款能自动修复代码bug的AI工具'DevDoctor'想一个简短有力的广告语。"
        temp2 = 0.7
        top_p2 = 0.9
        print(f"\n--- Example 2: Product Slogan ---")
        print(f"Prompt: {prompt2}")
        print(f"Settings: temperature={temp2}, top_p={top_p2}")

        generated_text2 = generate_creative_text(
            model=model,
            tokenizer=tokenizer,
            prompt=prompt2,
            temperature=temp2,
            top_p=top_p2,
            max_new_tokens=30
        )
        
        print("\n>>> Generated Text:")
        print(generated_text2)
        print("\n" + "="*50)
        print("Script finished.")

    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Please ensure you have 'transformers', 'torch', and 'accelerate' installed.")
        print("For CUDA, ensure your PyTorch version matches your CUDA driver version.")
        print("You might need to log in to Hugging Face if the model requires authentication: `huggingface-cli login`")

