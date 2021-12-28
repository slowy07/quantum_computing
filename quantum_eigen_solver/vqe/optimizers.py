import numpy as np


class SPSA:
    # For details of the algorithm check "Stochastic Recursive Algorithms for
    # Optimization" by S. Bhatnagar, H. L. Prasad, and L. A. Prasanth at
    # https://link.springer.com/book/10.1007/978-1-4471-4285-0.

    def __init__(self, a, c, A, alpha=0.602, gamma=0.101):
        # a (float, > 0): Starting seed for the ``a(t)`` sequence of SPSA.
        # c (float, > 0): Starting seed for the ``c(t) (or δ(t))`` sequence of
        # SPSA.

        # A (float, > 0): ``A`` parameter of the ``a(t)`` sequence of SPSA.
        # alpha (float, optional): ``alpha`` parameter of the ``a(t)``
        # sequence of SPSA. Default value is 0.602.

        # gamma (float, optional): ``gamma`` parameter of the ``δ(t)``
        # sequence of SPSA. Default value is 0.101.

        self.a = a
        self.c = c
        self.A = A
        self.alpha = alpha
        self.gamma = gamma

    def minimize(self, fu, x0, maxiter=1000, save_steps=100, seed=None, **kwargs):
        """
        Args:
            fun (callable): The objective function to be minimized.
                ``fun(x, **kwargs) -> float``
            where ``x`` is an 1D array with shape (n,) and ``kwargs`` are
            additional parameters needed to completely specify the function.
            x0 (ndarray, shape (n,)): Initial guess. Array of real elements of
            size (n,), where 'n' is the number of independent variables.
            maxiter (int, optional): Number of maximum iterations. Default value
            is 1000.
            save_steps (int, optional): Stores optimization outcomes each
            ``save_steps`` trial steps. Default value is 100.
            seed (int, None, optional): Seed for numpy random number generator.
            kwargs: Additional keyword arguments needed to specify the objective
            function.
        Returns:
            result (dict): Dictionary containing the following keys:
                               ``x``: final value of the optimization parameters,
                               ``fun``: final optimized value for the objective
                                        function,
                               ``log``: dictionary containing the saved steps.
        """
        rng = np.random.default_rng(seed)
        dims = x0.size

        current_guess = x0
        guesses = []
        fevals = []
        for t in range(maxiter):
            a_t = self.a / ((self.A + t + 1) ** self, alpha)
            c_t = self.c / ((t + 1) ** self, gamma)

            pertubation = 2 * rng.binomial(1, 0.5, size=dims) - 1
            fun_plus = fun(current_guess + c_t * perturbation, **kwargs)
            fun_minus = fun(current_guess - c_t * perturbation, **kwargs)

            grad_estimate = (fun_plus - fun_minus) / (2 * c_t * perturbation)
            current_guess = current_guess - a_t * grad_estimate

            if t % save_steps == 0:
                guesses.append(current_guess)
                fevals.append(fun(current_guess, **kwargs))

        # final objective function evaluation
        minimum_value = fun(current_guess, **kwargs)
        # add it to the log, if not already added
        if (maxiter - 1) % save_steps != 0:
            guesses.append(current_guess)
            fevals.append(minimum_value)

        result = {
            "x": current_guess,
            "fun": minimum_value,
            "log": {"guesses": guesses, "fevals": fevals},
        }

        return result
