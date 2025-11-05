# Lightweight multi-output Bayesian linear regression with closed-form posterior.
# Prior: w ~ N(0, alpha^{-1} I), noise: y|x,w ~ N(Xw, beta^{-1} I).
# Predictive: y* ~ N(X* m_N, beta^{-1} I + X* S_N X*^T)

from dataclasses import dataclass
import numpy as np

@dataclass
class BayesLinConfig:
    alpha: float = 1.0   # prior precision
    beta: float = 25.0   # noise precision (1/variance)

class BayesianLinearMultiOutput:
    def __init__(self, config: BayesLinConfig | None = None):
        self.cfg = config or BayesLinConfig()
        self.m_N = None      # (D, K)
        self.S_N = None      # (D, D)
        self.D = None
        self.K = None

    def fit(self, X: np.ndarray, Y: np.ndarray):
        # X: (N, D), Y: (N, K)
        N, D = X.shape
        N2, K = Y.shape
        assert N == N2, "X and Y must have same rows"
        self.D, self.K = D, K
        alpha, beta = self.cfg.alpha, self.cfg.beta
        A = alpha * np.eye(D) + beta * (X.T @ X)   # (D,D)
        self.S_N = np.linalg.inv(A)                # (D,D)
        self.m_N = beta * (self.S_N @ X.T @ Y)     # (D,K)
        return self

    def predict(self, Xstar: np.ndarray, return_std: bool = True):
        # X*: (M, D)
        if self.m_N is None:
            raise RuntimeError("Model not fit")
        mean = Xstar @ self.m_N                    # (M, K)
        if not return_std:
            return mean
        beta = self.cfg.beta
        # predictive covariance per output: beta^{-1} I_K + diag(x S_N x^T)
        # we return std per output dimension: sqrt(beta^{-1} + diag)
        diag_xSnx = np.sum((Xstar @ self.S_N) * Xstar, axis=1)  # (M,)
        var = (1.0 / beta) + diag_xSnx                           # (M,)
        std = np.sqrt(var)                                       # shared across outputs per sample
        # Expand to (M, K)
        std_mat = np.tile(std[:, None], (1, self.K))
        return mean, std_mat
