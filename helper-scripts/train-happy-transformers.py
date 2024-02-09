from happytransformer import HappyTextToText, TTTrainArgs

# Define your parameters
params = TTTrainArgs(
    fp16=False,
    learning_rate=5e-5,
    num_train_epochs=1,
    batch_size=1,
    save_steps=1000  # Automatic checkpoint every 1000 steps
)

#model.save_pretrained("my_checkpoint")
#model = HappyTextToText.from_pretrained("my_checkpoint")

# Specify your training file path
train_file_path = "output/data_augment.csv"

# Initialize HappyTextToText model
happy_tt = HappyTextToText()

# Train the model with Happy Transformers
happy_tt.train(train_file_path, args=params)
