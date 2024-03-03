# RUN THIS ONCE to create the model in ONNX format. 
from fastT5 import export_and_get_onnx_model
from transformers import AutoTokenizer

model_name = "willwade/t5-small-spoken-typo"
model = export_and_get_onnx_model(model_name)

tokenizer = AutoTokenizer.from_pretrained(model_name)
t_input = "grammar: Hihowareyoudoingtaday?."
token = tokenizer(t_input, return_tensors='pt')

tokens = model.generate(input_ids=token['input_ids'],
               attention_mask=token['attention_mask'],
               num_beams=2)

output = tokenizer.decode(tokens.squeeze(), skip_special_tokens=True)
print(output)