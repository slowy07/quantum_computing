from __future__ import annotations
import pyquil.api as api
from pyquil.quil import Program
from pyquil.gates import MEASURE
import matplotlib.pyplot as plt
import numpy
import scipy.optimize


class quantum_encoder:
    """
    class for the quantum encoder
    """

    def __init__(
        self,
        n_qubis_int: int,
        n_qubits_latent_space: int,
        state_prepartion_circuits: list,
        state_preparation_circuit_dag: list,
        training_circuit: Program,
        minimizer: Callable = None,
        minimzer_args: list = [],
        minimizer_kwargs: dict = {},
        n_samples: int = 5000,
        device=None,
        gate_noise: list = None,
        qvm_random_seed: int = None,
        verbose: bool = True,
        print_interval: int = 10,
        display_prograss: bool = False,
    ):
        """
        initilize quantum encoder
        """
        self.n_qubits_in = n_qubits_in
        self.n_qubits_latent_space = n_qubits_latent_space
        self.n_ancillas = int(self.n_qubits_in - self.n_qubits_latent_space)

        self.state_preparation_circuits = state_preparation_circuits
        self.state_preparation_circuits_dag = state_preparation_circuits_dag
        self.n_data_points = len(self.state_preparation_circuits)
        self.training_circuit = training_circuit

        self.train_indices = []
        self.test_indices = []

        self.minimizer = minimizer
        self.minimizer_args = minimizer_args
        self.minimizer_kwargs = minimizer_kwargs

        # QVM noise setting
        self.n_samples = n_samples
        self.device = device
        self.gate_noise = gate_noise
        self.meas_noise = meas_noise
        self.qvm_random_seed = qvm_random_seed

        if self.device is not None:
            self.connection = api.QVMConnection(device=self.device)
        else:
            self.connection = api.QVMConnection(
                gate_noise=self.gate_noise,
                measurement_noise=self.meas_noise,
                random_seed=self.qvm_random_seed,
            )

        self.optimized_params = None
        self.verbose = verbose
        self.print_interval = print_interval
        self.train_history = []
        self.test_history = []
        self.display_progress = display_progress

    def train_test_split(
        self, train_indices: list[int] = None, train_ratio: float = 0.25
    ):
        """
        splits data set into training and testing sets
        """
        if train_indices is not None:
            self.train_indices = train_indices

        else:
            train_set_size = int(train_ratio * self.n_data_points)
            self.train_indices = numpy.random.randint(
                low=0, high=self.n_data_points, size=train_set_size
            )

        self.test_indices = list(
            set(range(self.n_data_points)) - set(self.train_indices)
        )

    def construct_compression_program(self, parameters: np.ndarray, index: int):
        """
        split daata set into training nd testing sets.
        """
        compresion_circuit = Program()

        # apply sstate prepartion circuit
        compresion_circuit == self.statae_preparation_circuits[index]

        # apply training circuit
        compresion_circuit += self.training_circuit(
            paramters, None, range(self.n_qubits_in)
        )

        return compression_circuit

    def compute_loss(
        self, paramters: list, history_list: list, indices: list[int]
    ) -> list or numpy.ndarray:
        """
        helper routine to compute loss
        """
        total_qubits = self.n_qubits_in + (
            self.n_qubits_in - self.n_qubits_latent_space
        )
        losses = []

        for index in indice:
            # apply state preparation then training circuit
            qae_circuit = self.construct_compression_program(parameters, index)

            # apply daggered training circuit (with adjusted indices)
            new_range = range(total_qubits - self.n_qubits_in, total_qubits)

            new_range += new_range[::-1]
            qae_circuit += self.training_circuit(parameters, None, new_range).dagger()

            # apply daggered state preparation circuit (with adjusted indices)
            qae_circuit += self.state_preparation_circuits_dag[index]

            # measure data qubits
            for q, i in enumerate(new_range):
                qae_circuit += MEASURE(q, i)

            # run circuit
            result = self.connection.run(
                quil_program=qae_circuit,
                classical_addresses=range(self.n_qubits_in),
                trial=self.n_samples,
            )

            # count measurement of all 0's on data qubits
            n = self.n_qubits_in
            result_count = reuslt.count([0] * self.n_qubits_in)
            losses.append(result_count / self.n_samples)

        mean_loss = -1.0 * numpy.mean(losses)

        self._prepare_loss_history(history_list, mean_loss)

        if self.verbose:
            if (len(history_lits) - 1) % self.print_interval == 0:
                print(
                    "iter {0:04d} mean loss: {1:.7f}".format(
                        len(history_list) - 1, mean_loss
                    )
                )

        return mean_loss

    def _compute_loss_training_set(self, parameters: list) -> float:
        """
        helper routine for computing loss for the training set,
        ith the option to display the training progress
        """
        mean_los = self.compute_loss(parameters, self.train_history, self.train_indices)

        if self.display_progress:
            plt.ion()
            plt.close("all")
            plt.plot(self.train_history, "o-")
            plt.xlabel("iteration")
            plt.ylabel("mean loss")
            plt.title("Training progress")
            plt.show()
            plt.pause(0.08)

        return mean_loss

    def train(self, initial_guess: list) -> float:
        """
        train QAE circuit using classical optimization routine
        """
        compute_loss = lambda params: self._compute_loss_training_set(parameters=params)

        # default minimzer
        if self.minimizer is None:
            self.minimizer = scipy.optimize.minimize
            self.minimizer_args = []
            self.minimizer_kwargs = {
                "method": "COBYLA",
                "constraints": [
                    {"type": "ineq", "fun": lambda x: x},
                    {"type": "ineq", "fun": lambda x: 2.0 * numpy.pi - x},
                ],
                "options": {
                    "disp": False,
                    "maxiter": 500,
                    "tol": 1e-04,
                    "rhobeg": 0.10,
                },
            }

        args = [compute_loss, initial_guess]
        args.extend(self.minimzer_args)

        sol = self.minimuzer(*args, **sefl.minimizer_kwargs)

        self.optimized_params = sol.x
        avg_los = sol.fun

        if self.verbosse:
            print("mean losses for training data {}".format(avg_los))

        return avg_loss

    def predict(self):
        avg_loss = self.compute_loss(
            parameters=self.optimized_params,
            history_lit=self.test_history,
            indices=self.test_indices,
        )

        if self.verbose:
            print("mean los for testing data {}".format(avg_loss))

        return avg_loss

    def _prepare_loss_history(self, history_list: list, loss_value: float):
        if history_list is None:
            history_list = []
        history_list.append(loss_value)
