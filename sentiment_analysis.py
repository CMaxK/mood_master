import re
import torch
from transformers import BertTokenizer, BertModel
import torch.nn as nn
from torch.nn.functional import softmax

class BertClassifier(nn.Module):
    """Bert Model for Classification Tasks.
    """
    def __init__(self, freeze_bert=False):
        super(BertClassifier, self).__init__()
        # Specify hidden size of BERT, hidden size of classifier, and number of labels
        D_in, H, D_out = 768, 50, 2

        # Instantiate BERT model
        self.bert = BertModel.from_pretrained('bert-base-uncased')

        # Instantiate an one-layer feed-forward classifier
        self.classifier = nn.Sequential(
            nn.Linear(D_in, H),
            nn.ReLU(),
            nn.Linear(H, D_out)
        )

        # Freeze the BERT model
        if freeze_bert:
            for param in self.bert.parameters():
                param.requires_grad = False

    def forward(self, input_ids, attention_mask):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        last_hidden_state_cls = outputs[0][:, 0, :]
        logits = self.classifier(last_hidden_state_cls)
        return logits

class SentimentAnalysis:
    def __init__(self, model_path, device='cpu'):
        self.model = BertClassifier()
        self.model.load_state_dict(torch.load(model_path, map_location=torch.device(device)))
        self.model.eval()
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.device = device

    def text_preprocessing(self, text):
        """
        - Remove entity mentions (e.g., '@united')
        - Correct errors (e.g., '&amp;' to '&')
        @param    text (str): a string to be processed.
        @return   text (Str): the processed string.
        """
        # Remove '@name'
        text = re.sub(r'(@.*?)[\s]', ' ', text)

        # Replace '&amp;' with '&'
        text = re.sub(r'&amp;', '&', text)

        # Remove trailing whitespace
        text = re.sub(r'\s+', ' ', text).strip()

        return text

    def perform_sentiment_analysis(self, text):
        preprocessed_text = self.text_preprocessing(text)
        inputs = self.tokenizer(preprocessed_text, return_tensors='pt', truncation=True, padding=True)
        with torch.no_grad():
            input_ids = inputs['input_ids'].to(self.device)
            attention_mask = inputs['attention_mask'].to(self.device)

            # Perform a forward pass on the model to get logits
            logits = self.model(input_ids, attention_mask)

        # Get the predicted class (0 or 1)
        predicted_class = torch.argmax(logits, dim=1).item()

        # Define a list of sentiment labels
        sentiment_labels = ["Negative", "Not Negative"]

        # Get the corresponding sentiment label
        sentiment_label = sentiment_labels[predicted_class]

        return sentiment_label
