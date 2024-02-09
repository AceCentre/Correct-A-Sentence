from datasets import load_dataset
from transformers import T5Tokenizer, T5ForConditionalGeneration, Trainer, TrainingArguments

# Load your dataset
dataset = load_dataset('csv', data_files='processed_dialogues.csv')

# Assuming 'dataset' is a DatasetDict object returned by load_dataset
original_dataset = load_dataset('csv', data_files='processed_dialogues.csv')

# Split the dataset (assuming it only has a single split, commonly 'train')
train_test_dataset = original_dataset["train"].train_test_split(test_size=0.1)

# Now you have a DatasetDict with 'train' and 'test' splits
train_dataset = train_test_dataset["train"]
test_dataset = train_test_dataset["test"]


# Initialize the tokenizer for T5
tokenizer = T5Tokenizer.from_pretrained('t5-small')

# Preprocess the dataset
def preprocess_function(examples):
    model_inputs = tokenizer(examples["input"], padding="max_length", truncation=True, max_length=128)
    # Prepare labels
    with tokenizer.as_target_tokenizer():
        labels = tokenizer(examples["target"], padding="max_length", truncation=True, max_length=128)["input_ids"]
    model_inputs["labels"] = labels
    return model_inputs

tokenized_train_dataset = train_dataset.map(preprocess_function, batched=True)
tokenized_test_dataset = test_dataset.map(preprocess_function, batched=True)

# Training arguments
training_args = TrainingArguments(
    output_dir="./results",
    per_device_train_batch_size=8,  # Adjust based on the GPU memory
    save_steps=500,  # Save a checkpoint every 500 steps
    save_total_limit=2,  # Keep only the 2 most recent checkpoints
    evaluation_strategy="steps",  # Evaluate periodically
    eval_steps=500,  # Evaluation frequency
    logging_dir='./logs',  # Directory for logs
    logging_steps=100,  # Log metrics every 100 steps
    fp16=True
)

# Initialize the model
checkpoint = None  # Replace with path to checkpoint if resuming
if checkpoint:
    model = T5ForConditionalGeneration.from_pretrained(checkpoint)
else:
    model = T5ForConditionalGeneration.from_pretrained('t5-small')


# Initialize the Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train_dataset,
    eval_dataset=tokenized_test_dataset,
    tokenizer=tokenizer,
)

# Start training
trainer.train()