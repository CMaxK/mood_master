import torch
import torch.nn as nn
from sklearn.model_selection import train_test_split
from sentiment_analysis import BertClassifier
from transformers import BertTokenizer, AdamW
from helpers.db import load_from_db

MODEL_PATH = 'model_weights/bert_model_weights.pth'
DB_DATA = load_from_db()
BATCH_SIZE = 32
EPOCHS = 4
LEARNING_RATE = 2e-5
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

# split X and y
texts = DB_DATA['text'].values
labels = DB_DATA['target'].values

train_texts, test_texts, train_labels, test_labels = train_test_split(texts, labels, test_size=0.2, random_state=42)

#tokenise
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
train_encodings = tokenizer(train_texts, truncation=True, padding=True)
test_encodings = tokenizer(test_texts, truncation=True, padding=True)

# Convert to PyTorch DataLoaders
train_dataset = torch.utils.data.TensorDataset(train_encodings['input_ids'], train_encodings['attention_mask'], torch.Tensor(train_labels))
test_dataset = torch.utils.data.TensorDataset(test_encodings['input_ids'], test_encodings['attention_mask'], torch.Tensor(test_labels))

train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)

# Initialize model and optimizer
model = BertClassifier().to(DEVICE)
optimizer = AdamW(model.parameters(), lr=LEARNING_RATE)

# Train new model
loss_fn = nn.CrossEntropyLoss()
for epoch in range(EPOCHS):
    model.train()
    total_loss = 0
    for batch in train_loader:
        optimizer.zero_grad()
        input_ids, attention_mask, labels = [item.to(DEVICE) for item in batch]
        logits = model(input_ids, attention_mask)
        loss = loss_fn(logits, labels.long())
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    print(f"Epoch {epoch+1}/{EPOCHS}, Loss: {total_loss/len(train_loader)}")

# Evaluate new model
model.eval()
correct = 0
with torch.no_grad():
    for batch in test_loader:
        input_ids, attention_mask, labels = [item.to(DEVICE) for item in batch]
        logits = model(input_ids, attention_mask)
        predictions = torch.argmax(logits, dim=1)
        correct += (predictions == labels).sum().item()

new_accuracy = correct / len(test_texts)
print(f"New Model Accuracy: {new_accuracy*100:.2f}%")

# Load old model and evaluate
old_model = BertClassifier().to(DEVICE)
old_model.load_state_dict(torch.load(MODEL_PATH))
old_model.eval()

correct = 0
with torch.no_grad():
    for batch in test_loader:
        input_ids, attention_mask, labels = [item.to(DEVICE) for item in batch]
        logits = old_model(input_ids, attention_mask)
        predictions = torch.argmax(logits, dim=1)
        correct += (predictions == labels).sum().item()

old_accuracy = correct / len(test_texts)
print(f"Old Model Accuracy: {old_accuracy*100:.2f}%")

# Compare and overwrite if new model is better
if new_accuracy > old_accuracy:
    torch.save(model.state_dict(), MODEL_PATH)
    print("New model is better. Overwriting old model weights.")
else:
    print("Old model is better. Keeping old model weights.")
