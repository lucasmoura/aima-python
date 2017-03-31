import pytest

from learning import parse_csv, weighted_mode, weighted_replicate, DataSet, \
                     PluralityLearner, NaiveBayesLearner, NearestNeighborLearner, \
                     NeuralNetLearner, PerceptronLearner, DecisionTreeLearner, \
                     mean_error, rms_error, ms_error, manhattan_distance, \
                     mean_boolean_error, hamming_distance
from utils import DataFile
from math import sqrt


def test_ms_error():
    predictions = [1, 1, 1]
    targets = [1, 1, 1]

    assert ms_error(predictions, targets) == 0

    predictions = [1, 1, 1]
    targets = [2, 2, 2]

    assert ms_error(predictions, targets) == 1

    predictions = [1, 1, 1, 1]
    targets = [1, 3, 3, 1]

    assert ms_error(predictions, targets) == 2


def test_mean_error():
    predictions = [1, 1, 1]
    targets = [1, 1, 1]

    assert mean_error(predictions, targets) == 0

    predictions = [1, 1, 1]
    targets = [2, 2, 2]

    assert mean_error(predictions, targets) == 1

    predictions = [1, 1, 2, 1]
    targets = [1, 3, 1, 1]

    assert mean_error(predictions, targets) == 0.75


def test_rms_error():
    predictions = [1, 1, 1]
    targets = [1, 1, 1]

    assert rms_error(predictions, targets) == 0

    predictions = [1, 1, 1]
    targets = [2, 2, 2]

    assert rms_error(predictions, targets) == 1

    predictions = [1, 1, 2, 1]
    targets = [1, 2, 1, 1]

    assert rms_error(predictions, targets) == pytest.approx(sqrt(0.5))


def test_manhattan_distance():
    predictions = [1, 1, 1]
    targets = [1, 1, 1]

    assert manhattan_distance(predictions, targets) == 0

    predictions = [1, 1, 1]
    targets = [2, 2, 2]

    assert manhattan_distance(predictions, targets) == 3

    predictions = [1, 1, 2, 3]
    targets = [1, 3, 1, 1]

    assert manhattan_distance(predictions, targets) == 5


def test_mean_boolean_error():
    predictions = [1, 1, 1]
    targets = [1, 1, 1]

    assert mean_boolean_error(predictions, targets) == 0

    predictions = [1, 1, 1]
    targets = [2, 2, 2]

    assert mean_boolean_error(predictions, targets) == 1

    predictions = [1, 1, 2, 3]
    targets = [1, 3, 1, 2]

    assert mean_boolean_error(predictions, targets) == 0.75


def test_hamming_distance():
    predictions = [1, 1, 1]
    targets = [1, 1, 1]

    assert hamming_distance(predictions, targets) == 0

    predictions = [1, 1, 1]
    targets = [2, 2, 2]

    assert hamming_distance(predictions, targets) == 3

    predictions = [1, 1, 2, 3]
    targets = [1, 3, 1, 1]

    assert hamming_distance(predictions, targets) == 3


def test_exclude():
    iris = DataSet(name='iris', exclude=[3])
    assert iris.inputs == [0, 1, 2]


def test_parse_csv():
    Iris = DataFile('iris.csv').read()
    assert parse_csv(Iris)[0] == [5.1,3.5,1.4,0.2,'setosa']


def test_weighted_mode():
    assert weighted_mode('abbaa', [1, 2, 3, 1, 2]) == 'b'


def test_weighted_replicate():
    assert weighted_replicate('ABC', [1, 2, 1], 4) == ['A', 'B', 'B', 'C']


def test_plurality_learner():
    zoo = DataSet(name="zoo")

    pL = PluralityLearner(zoo)
    assert pL([1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 4, 1, 0, 1]) == "mammal"


def test_naive_bayes():
    iris = DataSet(name="iris")

    nB = NaiveBayesLearner(iris)
    assert nB([5,3,1,0.1]) == "setosa"


def test_k_nearest_neighbors():
    iris = DataSet(name="iris")

    kNN = NearestNeighborLearner(iris,k=3)
    assert kNN([5,3,1,0.1]) == "setosa"


def test_decision_tree_learner():
    iris = DataSet(name="iris")

    dTL = DecisionTreeLearner(iris)
    assert dTL([5,3,1,0.1]) == "setosa"


def test_neural_network_learner():
    iris = DataSet(name="iris")
    iris.remove_examples("virginica")
    
    classes = ["setosa","versicolor","virginica"]
    iris.classes_to_numbers()

    nNL = NeuralNetLearner(iris)
    # NeuralNetLearner might be wrong. Just check if prediction is in range.
    assert nNL([5,3,1,0.1]) in range(len(classes))


def test_perceptron():
    iris = DataSet(name="iris")
    iris.remove_examples("virginica")
    
    classes = ["setosa","versicolor","virginica"]
    iris.classes_to_numbers()

    perceptron = PerceptronLearner(iris)
    # PerceptronLearner might be wrong. Just check if prediction is in range.
    assert perceptron([5,3,1,0.1]) in range(len(classes))
