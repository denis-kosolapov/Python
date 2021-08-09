# License GPLv2
import numpy
import scipy.special


class NeuralNetworkGenerate:
    def __init__(self, parameters, learning_rate):
        self.weights = []
        for i in range(len(parameters)):
            if i < len(parameters) - 1:
                w = numpy.random.normal(0.0, pow(parameters[i], -0.5), (parameters[i + 1], parameters[i]))
                self.weights.append(w)

        self.learning_rate = learning_rate
        self.activation_function = lambda x: scipy.special.expit(x)
        self.parameters = parameters

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
        return final_outputs[self.last_index(final_outputs)]
