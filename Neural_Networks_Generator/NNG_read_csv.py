# License GPLv2 
import numpy
import glob
import imageio
import csv
import os
import scipy.special

class neuralNetworkRead:

    def __init__(self):
        self.activation_function = lambda x: scipy.special.expit(x)
        self.path = 'weights/'

    def read_csv(self, filepath):
        val = []
        with open(filepath, 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                new_row = []
                for i in row:
                    i = float(i)
                    new_row.append(i)
                val.append(new_row)
        return val

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

    def query(self, inputs_list):
        inputs = numpy.array(inputs_list, ndmin=2).T

        self.weights = []
        path = os.path.abspath(self.path)
        files = os.listdir(path)

        for i in range(len(files)):
            weight = self.read_csv(self.path + files[i])
            self.weights.append(weight)

        final_outputs = self.layers_outputs(inputs)
        return final_outputs[self.last_index(final_outputs)]


n = neuralNetworkRead()

our_own_dataset = []

for image_file_name in glob.glob('2828_my_own_?.png'):
    label = int(image_file_name[-5:-4])
    print("loading ... ", image_file_name)
    img_array = imageio.imread(image_file_name, as_gray=True)

    img_data = 255.0 - img_array.reshape(784)

    img_data = (img_data / 255.0 * 0.99) + 0.01

    record = numpy.append(label, img_data)
    our_own_dataset.append(record)

item = [0, 1, 2, 3]

for i in item:
    correct_label = our_own_dataset[i][0]

    inputs = our_own_dataset[i][1:]

    outputs = n.query(inputs)

    label = numpy.argmax(outputs)
    print("network says ", label)
    if (label == correct_label):
        print ("match!")
    else:
        print ("no match!")
