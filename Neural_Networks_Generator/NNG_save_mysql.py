# (c) Kosolapov Denis 2021
# License GPLv2
import numpy
import glob
import imageio
import scipy.special
from DataBase import DataBase


class NeuralNetworkGenerate:

    def __init__(self, parameters, learning_rate, database_name):
        self.weights = []
        for i in range(len(parameters)):
            if i < len(parameters) - 1:
                w = numpy.random.normal(0.0, pow(parameters[i], -0.5), (parameters[i + 1], parameters[i]))
                self.weights.append(w)

        self.learning_rate = learning_rate
        self.activation_function = lambda x: scipy.special.expit(x)
        self.parameters = parameters
        self.database = database_name

    def float_type(self, numpy_array):
        n = []
        for i in numpy_array:
            n.append(i.tolist())
        return n

    def last_index(self, list): # get list index
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
        return x[1:] # return an array starting from the first element

    def train(self, inputs_list, targets_list):

        inputs = numpy.array(inputs_list, ndmin=2).T
        targets = numpy.array(targets_list, ndmin=2).T
        outputs = self.layers_outputs(inputs)

        output_errors = targets - outputs[self.last_index(outputs)] # error[0]
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
                self.weights[i] += self.learning_rate * numpy.dot((errors[i] * outputs[i] * (1.0 - outputs[i])),
                                        numpy.transpose(inputs))
            if i > 0:
                self.weights[i] += self.learning_rate * numpy.dot((errors[i] * outputs[i] * (1.0 - outputs[i])),
                                                       numpy.transpose(outputs[i - 1]))

    def query(self, inputs_list):
        inputs = numpy.array(inputs_list, ndmin=2).T

        final_outputs = self.layers_outputs(inputs)

        # connect to database
        # if database exist rise exception
        host = 'localhost'
        user = 'root'
        password = ''
        database = self.database
        base = DataBase(host, user, password, database)

        # create names of tables
        name_w = []  # tables_name
        for i in range(len(self.parameters)):
            if i > 0 and i < len(self.parameters):
                name_w.append('weights_' + str(i))

        # create columns in tables
        weights_n = []
        for i in range(len(self.parameters)):
            if i < len(self.parameters):
                weights = []
                for j in range(self.parameters[i]):
                    if j < self.parameters[i] - 1:
                        n = 'w' + str(j + 1) + ' DOUBLE,'
                        weights.append(n)
                    else:
                        n = 'w' + str(j + 1) + ' DOUBLE'
                        weights.append(n)
                weights_n.append(weights)

        for i in range(len(name_w)):
            w = " ".join(weights_n[i])
            base.createTable_weights(name_w[i], w)

        for i in range(len(name_w)):
            weight = self.float_type(self.weights[i])
            table_list = base.showColumnInfo(database, name_w[i])
            column_info = base.getColumnInfo(table_list, 0)
            base.insertInto(name_w[i], weight, column_info)

        return final_outputs[self.last_index(final_outputs)]

parameters = [784, 200, 100, 10]
learning_rate = 0.3
database = 'new_nng'
last_index = len(parameters) -1
n = NeuralNetworkGenerate(parameters, learning_rate, database)

training_data_file = open("mnist_train.csv", 'r')
training_data_list = training_data_file.readlines()
training_data_file.close()

epochs = 1
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
