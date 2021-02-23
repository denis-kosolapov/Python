# (c) Kosolapov Denis 2021
# License GPLv2 
import numpy
import glob
import imageio
import scipy.special
import csv


class NeuralNetworkGenerate:

    def __init__(self, mass, learning_rate):
        self.weights = []
        for i in range(len(mass)):
            if i < len(mass) - 1:
                w = numpy.random.normal(0.0, pow(mass[i], -0.5), (mass[i + 1], mass[i]))
                self.weights.append(w)

        self.lr = learning_rate
        self.activation_function = lambda x: scipy.special.expit(x)

    def csv_write(self, data, path):
        my_list = []
        fieldnames = data[0]
        cell = data[1:]

        for values in cell:
            inner_dict = dict(zip(fieldnames, values))
            my_list.append(inner_dict)

        with open(path, "w", newline='') as out_file:
            writer = csv.DictWriter(out_file, delimiter=',', fieldnames=fieldnames)
            writer.writeheader()
            for row in my_list:
                writer.writerow(row)

    def float_type(self, numpy_array):
        n = []
        for i in numpy_array:
            n.append(i.tolist())
        return n

    def li(self, list): # get list index
        return len(list) -1

    def layers_inputs(self, index, inputs):
        input = numpy.dot(index, inputs)
        output = self.activation_function(input)
        return output

    def layers_outputs(self, inputs):
        x = []
        x.append(inputs)
        for i in range(len(self.weights)):
            x.append(self.layers_inputs(self.weights[i], x[i]))
        return x[1:] # вернуть массив начиная с первого элемента

    def train(self, inputs_list, targets_list):

        inputs = numpy.array(inputs_list, ndmin=2).T
        targets = numpy.array(targets_list, ndmin=2).T
        outputs = self.layers_outputs(inputs)

        output_errors = targets - outputs[self.li(outputs)] # error[0]
        errors = [] # all errors
        errors.append(output_errors)

        self.weights.reverse() # weights indexes [1, 0]
        for i in range(len(self.weights) - 1):
            hidden_errors = numpy.dot(self.weights[i].T, errors[i]) # error[1]
            errors.append(hidden_errors)
        self.weights.reverse() # weights indexes [0, 1]
        errors.reverse()

        for i in range(len(self.weights)):
            if i == 0:
                self.weights[i] += self.lr * numpy.dot((errors[i] * outputs[i] * (1.0 - outputs[i])),
                                        numpy.transpose(inputs))
            if i > 0:
                self.weights[i] += self.lr * numpy.dot((errors[i] * outputs[i] * (1.0 - outputs[i])),
                                                       numpy.transpose(outputs[i - 1]))

    def query(self, inputs_list):
        inputs = numpy.array(inputs_list, ndmin=2).T
        q = self.layers_outputs(inputs)

        # save weights to csv file
        float_q = []
        for i in range(len(self.weights)):
            file_name = 'weights/w_' + str(i) + '.csv'
            float_q.append(self.float_type(self.weights[i]))
            self.csv_write(float_q[i], file_name)

        return q[self.li(q)]

parameters = [784, 200, 50, 10]
last_index = len(parameters) -1
n = NeuralNetworkGenerate(parameters, 0.3)

training_data_file = open("mnist_train.csv", 'r')
training_data_list = training_data_file.readlines()
training_data_file.close()

epochs = 5
for e in range(epochs):
    for record in training_data_list:
        all_values = record.split(',')
        inputs = (numpy.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01
        targets = numpy.zeros(parameters[last_index]) + 0.01
        targets[int(all_values[0])] = 0.99
        n.train(inputs, targets)

our_own_dataset = []

for image_file_name in glob.glob('2828_my_own_?.png'):
    label = int(image_file_name[-5:-4])
    print("loading ... ", image_file_name)
    img_array = imageio.imread(image_file_name, as_gray=True)

    img_data = 255.0 - img_array.reshape(784)

    img_data = (img_data / 255.0 * 0.99) + 0.01
    print(numpy.min(img_data))
    print(numpy.max(img_data))

    record = numpy.append(label, img_data)
    our_own_dataset.append(record)

item = 0

correct_label = our_own_dataset[item][0]

inputs = our_own_dataset[item][1:]

outputs = n.query(inputs)
print(outputs)

label = numpy.argmax(outputs)
print("network says ", label)
if (label == correct_label):
    print ("match!")
else:
    print ("no match!")
