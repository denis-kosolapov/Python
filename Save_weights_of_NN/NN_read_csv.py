# License GPLv2 
import numpy
import math
import glob
import imageio
import csv

class neuralNetworkRead:

    def __init__(self):
        self.activation_function = lambda x: 1 / (1 + (math.e ** (-x)))

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

    def query(self, inputs_list):
        inputs = numpy.array(inputs_list, ndmin=2).T

        self.wih = self.read_csv('weights_1.csv')
        self.who = self.read_csv('weights_2.csv')

        hidden_inputs = numpy.dot(self.wih, inputs)
        hidden_outputs = self.activation_function(hidden_inputs)

        final_inputs = numpy.dot(self.who, hidden_outputs)
        final_outputs = self.activation_function(final_inputs)

        return final_outputs


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
