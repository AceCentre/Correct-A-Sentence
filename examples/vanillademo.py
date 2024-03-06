from transformers import T5Tokenizer, T5ForConditionalGeneration

# Load the tokenizer and model
model_name = "willwade/t5-small-spoken-typo"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

# Prepare the input text with the "grammar: " prefix
input_text = "grammar: Hihowareyoudoingtaday?."
input_ids = tokenizer.encode(input_text, return_tensors="pt")

# Generate text
# Adjust num_beams and min_length to your needs
output = model.generate(input_ids, num_beams=5, min_length=1, max_new_tokens=50, early_stopping=True)

# Decode the generated text
decoded_output = tokenizer.decode(output[0], skip_special_tokens=True)

print(decoded_output)
