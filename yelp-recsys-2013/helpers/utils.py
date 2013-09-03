from math import sqrt
from sklearn import metrics


def rmse(y_true, y_pred):
    return sqrt(metrics.mean_squared_error(y_true, y_pred))


def save_results(predictions, filename):
    """Save results in CSV format."""
    logging.info("saving data to file %s", filename)
    with open("submissions/%s" % filename, 'w') as f:
        f.write("RecommendationId,Stars\n")
        for i, pred in enumerate(predictions):
            f.write("%d,%f\n" % (i + 1, pred))
