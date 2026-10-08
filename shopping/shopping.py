import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier


TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet
    evidence, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)

    # Evaluate results
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    correct = 0
    incorrect = 0

    for actual, predicted in zip(y_test, predictions):
        if actual == predicted:
            correct += 1
        else:
            incorrect += 1

    print(f"Correct: {correct}")
    print(f"Incorrect: {incorrect}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Loads shopping data from a CSV file and returns
    a tuple (evidence, labels).
    """
    evidence = []
    labels = []

    months = {
        "Jan": 0,
        "Feb": 1,
        "Mar": 2,
        "Apr": 3,
        "May": 4,
        "June": 5,
        "Jul": 6,
        "Aug": 7,
        "Sep": 8,
        "Oct": 9,
        "Nov": 10,
        "Dec": 11
    }

    with open(filename) as f:
        reader = csv.DictReader(f)

        for row in reader:

            evidence.append([
                int(row["Administrative"]),
                float(row["Administrative_Duration"]),
                int(row["Informational"]),
                float(row["Informational_Duration"]),
                int(row["ProductRelated"]),
                float(row["ProductRelated_Duration"]),
                float(row["BounceRates"]),
                float(row["ExitRates"]),
                float(row["PageValues"]),
                float(row["SpecialDay"]),
                months[row["Month"]],
                int(row["OperatingSystems"]),
                int(row["Browser"]),
                int(row["Region"]),
                int(row["TrafficType"]),
                1 if row["VisitorType"] == "Returning_Visitor" else 0,
                1 if row["Weekend"] == "TRUE" else 0
            ])

            labels.append(1 if row["Revenue"] == "TRUE" else 0)

    return evidence, labels


def train_model(evidence, labels):
    """
    Trains a k-nearest-neighbor classifier
    and returns the fitted model.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    return model


def evaluate(labels, predictions):
    """
    Evaluates a model's sensitivity and specificity.
    """
    true_positive = 0
    actual_positive = 0

    true_negative = 0
    actual_negative = 0

    for actual, predicted in zip(labels, predictions):

        if actual == 1:
            actual_positive += 1
            if predicted == 1:
                true_positive += 1

        else:
            actual_negative += 1
            if predicted == 0:
                true_negative += 1

    sensitivity = true_positive / actual_positive
    specificity = true_negative / actual_negative

    return sensitivity, specificity


if __name__ == "__main__":
    main()
