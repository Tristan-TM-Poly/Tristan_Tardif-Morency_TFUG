
import numpy as np
from raman_ai.models.heads.bayes_multi import BayesianLinearMultiOutput

def test_bayes_fit_predict_shapes():
    X = np.random.randn(32, 8)
    W = np.random.randn(8, 2)
    Y = X @ W + 0.05*np.random.randn(32,2)
    model = BayesianLinearMultiOutput().fit(X, Y)
    mu, std = model.predict(X, return_std=True)
    assert mu.shape == Y.shape
    assert std.shape == Y.shape
    assert (std > 0).all()
