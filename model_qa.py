import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from datasets import load_dataset

# Load your dataset
df = pd.read_csv('topics.csv')
dataset = load_dataset('csv', data_files={'train': 'topics.csv', 'test': 'test.csv'})

# Split the dataset into train and test sets
train_dataset = dataset['train']
test_dataset = dataset['test']

# Initialize tokenizer and model
tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
model = AutoModelForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=9)  # Adjust num_labels

# Tokenize the dataset
def tokenize_function(examples):
    return tokenizer(examples['Question'], examples['Context'], padding='max_length', truncation=True)

train_dataset = dataset['train'].map(tokenize_function, batched=True)
test_dataset = dataset['test'].map(tokenize_function, batched=True)


# Define training arguments
training_args = TrainingArguments(
    output_dir='./results',
    eval_strategy='epoch',
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
)

# Initialize Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
)

# Train and evaluate
trainer.train()
eval_results = trainer.evaluate()
print(f"Evaluation results: {eval_results}")

# Make predictions
def predict(texts):
    inputs = tokenizer(texts, padding=True, truncation=True, return_tensors='pt')
    outputs = model(**inputs)
    predictions = outputs.logits.argmax(dim=-1)
    return predictions



#model.save_pretrained('./geography_bert_model')
#tokenizer.save_pretrained('./geography_bert_model')