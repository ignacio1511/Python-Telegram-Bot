import json
from re import X
<<<<<<< HEAD
from functions import tokenize,stem,bag_of_words
=======
from functions import tokenize,stem,bag_of_words
>>>>>>> file split
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from model import NeuralNet

with open('intents.json', 'r') as f:
    intents = json.load(f)

print(intents)

palabras_totales = []
tags = []
xy = []

for intent in intents['intents']:
    tag = intent['tag']
    tags.append(tag)

    for pattern in intent['patterns']:
        palabra = tokenize(pattern)
        palabras_totales.extend(palabra) 
        xy.append((palabra,tag))


ignorar_palabras = ['?', ',', '!', '.']

palabras_totales = [stem(palabra) for palabra in palabras_totales if palabra not in ignorar_palabras]

palabras_totales = sorted(set(palabras_totales))
tags = sorted(set(tags))

print(palabras_totales)
print(tags)


x_train = []
y_train = []

for (pattern_sentence, tag) in xy: 
    bag = bag_of_words(pattern_sentence,palabras_totales)
    x_train.append(bag)

    label = tags.index(tag) #le da un numero a la etiqueta del mensaje
    y_train.append(label)


x_train = np.array(x_train)
y_train = np.array(y_train)


class ChatDataset(Dataset):
    def __init__(self):
        self.n_samples = len(x_train)
        self.x_data = x_train
        self.y_data = y_train


    #dataset[index]
    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]
    
    def __len__(self):
        return self.n_samples


# Parametros
learning_rate = 0.001
batch_size = 8
input_size = 8
hidden_size = 8
output_size = len(tags)
input_size = len(palabras_totales) ## len(x_train[0])
num_epochs = 1000

print(input_size,len(palabras_totales))
print(output_size, len(tags))

dataset = ChatDataset()
trainLoader = DataLoader(dataset=dataset,batch_size=batch_size, shuffle=True, num_workers=0)
model = NeuralNet(input_size,hidden_size, output_size)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = NeuralNet(input_size, hidden_size, output_size).to(device)
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

for epoch in range(num_epochs):
    for (words, labels) in trainLoader:
        words = words.to(device)
        labels = labels.to(dtype=torch.long).to(device)
        
        # Forward pass
        outputs = model(words)
        # if y would be one-hot, we must apply
        # labels = torch.max(labels, 1)[1]
        loss = criterion(outputs, labels)
        
        # Backward and optimize
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
    if (epoch+1) % 100 == 0:
        print (f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')


print(f'final loss: {loss.item():.4f}')

data = {

    "model_state": model.state_dict(),
    "input_size": input_size,
    "output_size": output_size,
    "hidden_size": hidden_size,
    "palabras_totales": palabras_totales,
    "tags": tags

}

FILE = "databot.pth"
torch.save(data, FILE)

print(f'entrenamiento completado. archivo guardado en {FILE}')