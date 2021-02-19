import numpy
import math
import glob
import imageio
from DataBase import DataBase

class neuralNetwork:
    def __init__(self, inputnodes, hiddennodes, outputnodes, learningrate):
        self.inodes = inputnodes
        self.hnodes = hiddennodes
        self.onodes = outputnodes

        self.wih = numpy.random.normal(0.0, pow(self.inodes, -0.5), (self.hnodes, self.inodes))
        self.who = numpy.random.normal(0.0, pow(self.hnodes, -0.5), (self.onodes, self.hnodes))

        self.lr = learningrate

        self.activation_function = lambda x: 1 / (1 + (math.e ** (-x)))

    def train(self, inputs_list, targets_list):

        inputs = numpy.array(inputs_list, ndmin=2).T
        targets = numpy.array(targets_list, ndmin=2).T

        hidden_inputs = numpy.dot(self.wih, inputs)
        hidden_outputs = self.activation_function(hidden_inputs)

        final_inputs = numpy.dot(self.who, hidden_outputs)
        final_outputs = self.activation_function(final_inputs)


        output_errors = targets - final_outputs
        hidden_errors = numpy.dot(self.who.T, output_errors)

        self.who += self.lr * numpy.dot((output_errors * final_outputs * (1.0 - final_outputs)),
                                        numpy.transpose(hidden_outputs))

        self.wih += self.lr * numpy.dot((hidden_errors * hidden_outputs * (1.0 - hidden_outputs)),
                                        numpy.transpose(inputs))

    # def float_type(self, numpy_list):
    #     n = []
    #     for i in numpy_list:
    #         m = []
    #         n.append(m)
    #         for j in i:
    #             j = float(j)
    #             m.append(j)
    #     return n

    def float_type(self, numpy_array):
        n = []
        for i in numpy_array:
            n.append(i.tolist())
        return n

    def query(self, inputs_list):
        inputs = numpy.array(inputs_list, ndmin=2).T

        hidden_inputs = numpy.dot(self.wih, inputs)
        hidden_outputs = self.activation_function(hidden_inputs)

        final_inputs = numpy.dot(self.who, hidden_outputs)
        final_outputs = self.activation_function(final_inputs)

        w_1 = self.float_type(self.wih)
        w_2 = self.float_type(self.who)

        # потому что время ожидания с момента подключения большое и подключение завершается
        # до записи в базу данных
        # because the timeout from the moment of connection is long and the connection ends
        # before writing to the database

        host = 'localhost'
        user = 'root'
        password = ''
        database = 'neural_network'

        base = DataBase(host, user, password, database)
        
        # neural network parameters
        parameters = [784, 200, 10]
 
        name_w = []  # tables_name
 
        for i in range(len(parameters)):
            if i &gt; 0 and i &lt; len(parameters):
                name_w.append('weights_' + str(i))
        print(name_w)
 
        weights_n = []
        for i in range(len(parameters)):
            if i &lt; len(parameters):
                weights = []
                for j in range(parameters[i]):
                    if j &lt; parameters[i] - 1:
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
            w = " ".join(weights_n[i])
            base.createTable_weights(name_w[i], w)
        
        table_list = base.showColumnInfo(database, 'weights_1')
        column_info = base.getColumnInfo(table_list, 0)
        base.insertInto('weights_1', w_1, column_info)

        table_list = base.showColumnInfo(database, 'weights_2')
        column_info = base.getColumnInfo(table_list, 0)
        base.insertInto('weights_2', w_2, column_info)

        return final_outputs


input_nodes = 784
hidden_nodes = 200
output_nodes = 10
learning_rate = 0.3

n = neuralNetwork(input_nodes, hidden_nodes, output_nodes, learning_rate)

training_data_file = open("mnist_train.csv", 'r')
training_data_list = training_data_file.readlines()
training_data_file.close()

epochs = 5
for e in range(epochs):
    for record in training_data_list:
        all_values = record.split(',')
        inputs = (numpy.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01
        targets = numpy.zeros(output_nodes) + 0.01
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
