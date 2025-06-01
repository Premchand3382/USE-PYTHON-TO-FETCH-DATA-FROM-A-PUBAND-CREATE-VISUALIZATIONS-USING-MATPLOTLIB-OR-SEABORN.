import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Load Dataset
url = "https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/sms.tsv"
df = pd.read_csv(url, sep='\t', header=None, names=['label', 'message'])

# Step 2: Encode labels
df['label_num'] = df.label.map({'ham': 0, 'spam': 1})

# Step 3: Split dataset
X_train, X_test, y_train, y_test = train_test_split(df['message'], df['label_num'], test_size=0.3, random_state=42)

# Step 4: Text vectorization
vectorizer = CountVectorizer()
X_train_counts = vectorizer.fit_transform(X_train)
X_test_counts = vectorizer.transform(X_test)

# Step 5: Train model
model = MultinomialNB()
model.fit(X_train_counts, y_train)

# Step 6: Predict
y_pred = model.predict(X_test_counts)

# Step 7: Evaluation
print("Accuracy:", round(accuracy_score(y_test, y_pred), 4))
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred, target_names=['Ham', 'Spam']))

# Step 8: Visualize label distribution
sns.countplot(data=df, x='label')
plt.title('Distribution of Spam and Ham Messages')
plt.xlabel('Message Type')
plt.ylabel('Count')
plt.show()

# Step 9: Predict on custom message
sample_msgs = ["Free entry in 2 a weekly competition", "Hey, are we still on for lunch?"]
sample_vec = vectorizer.transform(sample_msgs)
sample_preds = model.predict(sample_vec)

for msg, pred in zip(sample_msgs, sample_preds):
    label = 'Spam' if pred == 1 else 'Ham'
    print(f"Message: '{msg}' --> Prediction: {label}")
