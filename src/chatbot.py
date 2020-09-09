import nltk

import texttospeech

from nltk.stem.lancaster import LancasterStemmer


from tensorflow.python.compiler import tensorrt as trt
stemmer = LancasterStemmer()

import numpy
import tflearn
import tensorflow
import pickle
import random
import json

with open('intents.json') as file:
    data = json.load(file)

#pickle ser
with open("data.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)
words = []
labels = []
docs_x = []
docs_y = []
# n
for  intent in data['intents']:
        for pattern in intent['patterns']:
            #root word
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])

        if intent['tag'] not in labels:
            labels.append(intent['tag'])
    # remove extra characters and make it small for comparison
words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    # remove all the duplicates and sort them
words = sorted(list(set(words)))

labels = sorted(labels)

training = []
output = []

out_empty = [0 for _ in range(len(labels))]
##checking the bag of words ,looping through the chunks of words

for x, doc in enumerate(docs_x):
        bag = []

        wrds = [stemmer.stem(w.lower()) for w in doc]

        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)

    # data is ready
training = numpy.array(training)
output = numpy.array(output)

with open("data.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)
#rid of previous data
tensorflow.reset_default_graph()
# classifiction of words into output
net = tflearn.input_data(shape=[None, len(training[0])])# input shape
net = tflearn.fully_connected(net, 9)#output layer
net = tflearn.fully_connected(net, 9)#output layer
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)
#model wrapper 'DNN' that can automatically performs a neural network classifier tasks, such as training, prediction, save/restore
model = tflearn.DNN(net)
#predicting model output ^

#model fitting
# ,do train 2000 times

model.fit(training, output, n_epoch=2000, batch_size=10, show_metric=True)
model.save("model.tflearn")


def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return numpy.array(bag)


def chat(inp):


    if inp.lower() == "quit":
            texttospeech('good bye! sir')


        #predicting the model , in neuron get connection as per valued results
    results = model.predict([bag_of_words(inp, words)])[0]
        #max valued index
    results_index = numpy.argmax(results)
    tag = labels[results_index]

    for tg in data["intents"]:
                if tg['tag'] == tag:
                    responses = tg['responses']
    ans=random.choice(responses)

    return (ans)





