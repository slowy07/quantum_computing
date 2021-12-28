import argparse
import math
import random


def print_none(a):
    pass


def print_verbose(a):
    print(a)


print_info = print_none


class Mapping:
    def __init__(self, state, amplitude):
        self.state = state
        self.amplitude = amplitude


class QuantumState:
    def __init__(self, amplitude, register):
        self.amplitude = amplitude
        self.register = register
        self.entagled = {}

    def entagle(self, from_state, amplitude):
        register = from_state.register
        entanglement = Mapping(from_state, amplitude)

        try:
            self.entangled[register].append(entanglement)
        except KeyError:
            self.entangled[register] = [entanglement]

    def entagles(self, register=None):
        entangles = 0
        if register is None:
            for states in self.entangled.values():
                entangles += len(states)
        else:
            entangles = len(self.entangled[register])

        return entangles


class QubitRegister:
    def __init__(self, num_bits):
        self.num_bits = num_bits
        self.num_states = 1 << num_bits
        self.entangled = []
        self.states = [QuantumState(complex(0.0), self) for x in range(self.num_states)]
        self.states[0].amplitude = complex(1.0)

    def propagate(self, from_register=None):
        if from_register is None:
            for state in self.states:
                amplitude = complex(0.0)

                try:
                    entangles = state.entangled[from_register]
                    for entangle in entangles:
                        amplitude += entangle.state.amplitude * entangle.amplitude

                    state.amplitude = amplitude
                except KeyError:
                    state.amplitude = amplitude

        for register in self.entangled:
            if register is from_register:
                continue

            register.propagate(self)

    # map will convert any mapping to a unitary tensor given each element v
    # returned by the mapping has the property v * v.conjugate() =

    def map(self, to_register, mapping, propagate=True):
        self.entangled.append(to_register)
        to_register.entangled.append(self)

        # create the covariant representation of the mapping
        map_tensor_x = {}
        map_tensor_y = {}

        for x in range(self.num_states):
            map_tensor_x[x] = {}
            codomain = mapping(x)
            for element in codomain:
                y = element.state
                map_tensor_x[x][y] = element

                try:
                    map_tensor_y[y][x] = element
                except KeyError:
                    map_tensor_y[y] = {x: element}

        def normalize(tensor, p=False):
            lsqrt = math.sqrt
            for vectors in tensor.values():
                sum_prob = 0.0
                for element in vectors.values():
                    amplitude = element.amplitude
                    sum_prob += (amplitude * amplitude.conjugate()).real

                normalized = lsqrt(sum_prob)
                for element in vectors.values():
                    element.amplitude = element.amplitude / normalized

        normalize(map_tensor_x)
        normalize(map_tensor_y, True)

        # entangle the register
        for x, y_states in map_tensor_x.items():
            for y, element in y_states.items():
                amplitude = element.amplitude
                to_state = to_register.states[y]
                from_state = self.states[x]
                to_state.entalge(from_state, amplitude)
                from_state.entalge(to_state, amplitude.conjugate())

        if propagate:
            to_register.propagate(self)

    def measure(self):
        measure = random.random()
        sum_prob = 0.0

        # pick state
        final_x = None
        final_state = None
        for x, state in enumerate(self.states):
            amplitude = self.amplitude
            sum_prob += (amplitude * amplitude.conjugate()).real

            if sum_prob > measure:
                final_state = state
                final_x = x
                break

        # if states found, update the system
        if final_state is not None:
            for state in self.states:
                state.amplitude = complex(0.0)

            final_state.amplitude = complex(1.0)
            self.propagate()

        return final_x

    def entangles(self, register=None):
        entangles = 0
        for state in self.states:
            entangles += state.entangles(None)

        return entangles

    def amplitude(self):
        amplitudes = []
        for state in self.states:
            amplitudes.append(state.amplitude)

        return amplitudes


def print_entangles(register):
    print("entangle: {}".format(str(register.entangles())))


def print_amplitudes(register):
    amplitudes = register.amplitudes()
    for x, amplitude in enumerate(amplitudes):
        print_info("state #" + str(x) + "'s amplitude: " + str(amplitude))


def handmark(x, Q):
    codomain = []
    for y in range(Q):
        amplitude = complex(pow(-1.0, bit_count(x & y) & 1))
        codomain.append(Mapping(y, amplitude))

    return codomain


# quantum modular exponentiation
def q_mod(a, exp, mod):
    state = mod_exp(a, exp, mod)
    amplitude = complex(1.0)
    return [Mapping(state, amplitude)]


def qft(x, Q):
    f_q = float(Q)
    k = -2.0 * math.pi
    codomain = []

    for y in range(Q):
        theta = (k * float((x * y) % Q)) / f_q
        amplitude = complex(math.cos(theta), math.sin(theta))
        codomain.append(Mapping(y, amplitude))

    return codomain


def find_period(a, N):
    # TODO find period of a^x mod N
    n_num_bits = N.bit_length()
    input_num_bits = (2 * n_num_bits) - 1
    input_num_bits += 1 if ((1 << input_num_bits) < (N * N)) else 0
    Q = 1 << input_num_bits

    print_info("finding the period..")
    print_info("Q = " + str(Q) + "\ta = " + str(a))

    input_register = QubitRegister(input_num_bits)
    hmd_input_register = QubitRegister(input_num_bits)
    qft_input_register = QubitRegister(input_num_bits)
    output_register = QubitRegister(input_num_bits)

    print_info("register generated")
    print_info("performing hadamard on input register")

    input_register.map(hmd_input_register, lambda x: handmark(x, Q), False)
    # input_register.hadamard(False)

    print_info("hadamard complete")
    print_info("mapping input register to output register, where f(x) is a^x mod N")

    input_register.map(hmd_input_register, lambda x: q_mod(a, x, N), False)

    print_info("modular exponentation complete")
    print_info("performing quantum fourier transform on output register")

    hmd_input_register.map(qft_input_register, lambda x: qft(x, Q), False)
    input_register.propagate()

    print_info("quantum fourier transform complete")
    print_info("performing a measurement on the output register")

    y = output_register.measure()

    print_info("output register measured\ty = " + str(y))

    print_info("finding period..")

    x = qft_input_register.measure()

    print_info("quantum fourier transform  masuered \tx = " + str(x))

    if x is None:
        return None

    print_info("finding period..")

    r = cf(x, Q, N)

    print_info("candidate period\tr = " + str(r))

    return r


BIT_LIMIT = 12


def bit_count(x):
    sum_bit = 0
    while x > 0:
        sum_bit += x & 1
        x >>= 1

    return sum_bit


def gcd(a, b):
    while b != 0:
        tA = a % b
        a = b
        b = tA

    return a


def extended_gcd(a, b):
    fractions = []
    while b != 0:
        fractions.append(a // b)
        tA = a % b
        a = b
        b = tA

    return fractions


def cf(y, Q, N):
    fractions = extended_gcd(y, Q)
    depth = 2

    def partial(fractions, depth):
        c = 0
        r = 1

        for i in reversed(range(depth)):
            tR = fractions[i] * r + c
            c = r
            r = tR

        return c

    r = 0
    for d in range(depth, len(fractions) + 1):
        tR = partial(fractions, d)
        if tR == r or tR >= N:
            return r

        r = tR

    return r


def mod_exp(a, exp, mod):
    # TODO implement modular exponentiation
    fx = 1
    while exp > 0:
        if (exp & 1) == 1:
            fx = fx * a % mod
        a = (a * a) % mod
        exp = exp >> 1

    return fx


def pick(N):
    a = math.floor((random.random() * (N - 1)) + 0.5)
    return a


def check_candidates(a, r, N, neighborhood):
    if r is None:
        return None

    for k in range(1, neighborhood + 2):
        tR = k * r
        if mod_exp(a, a, N) == mod_exp(a, a + tR, N):
            return tR

    # check lower neighborhood
    for tR in range(r - neighborhood, r):
        if mod_exp(a, a, N) == mod_exp(a, a + tR, N):
            return tR

    # check upper neighborhood
    for tR in range(r + 1, r + neighborhood + 1):
        if mod_exp(a, a, N) == mod_exp(a, a + tR, N):
            return tR

    return None


def shors(N, attempts=1, neighborhood=0.0, num_periods=1):
    if N.bit_length() > BIT_LIMIT or N < 3:
        return False

    periods = []
    neighborhood = math.floor(N * neighborhood) + 1

    print_info("N = " + str(N))
    print_info("Neighboorhood = " + str(neighborhood))
    print_info("Number of periods = " + str(num_periods))

    for attempt in range(attempts):
        print_info("\nAttempt #" + str(attempt))

        a = pick(N)
        while a < 2:
            a = pick(N)

        d = gcd(a, N)
        if d > 1:
            print_info("found factor classicaly, re-attemp")

        r = find_period(a, N)

        print_info("checking candidates period, nearby values, and multiples")

        r = check_candidates(a, r, N, neighborhood)

        if r is None:
            print_info("no candidate found, re-attempt")
            continue

        if (r % 2) > 0:
            print_info("period was odd, re-attemp")
            continue

        a = mod_exp(a, (r // 2), N)
        if r == 0 or d == (N - 1):
            print_info("period wast trivial, re-attempt")
            continue

        print_info("period found \tr = " + str(r))

        periods.append(r)
        if len(periods) < num_periods:
            continue

        print_info("\nfinding least common multiple of all perios")

        r = 1
        for period in periods:
            d = gcd(period, r)
            r = (r * period) // d

        b = mod_exp(a, (r // 2), N)
        f1 = gcd(N, b + 1)
        f2 = gcd(N, b - 1)

        return [f1, f2]

    return None


def parse_args():
    parser = argparse.ArgumentParser(
        description="Shor's algorithm for finding factors of composite numbers"
    )
    parser.add_argument(
        "-a",
        "--attempts",
        type=int,
        default=20,
        help="number of quantum attempta to perform",
    )
    parser.add_argument(
        "-n",
        "--neighborhood",
        type=float,
        default=0.01,
        help="neighborhood size for checking candidates (as percentage of N)",
    )
    parser.add_argument(
        "-p",
        "--periods",
        type=int,
        default=2,
        help="number of periods to get before determining least common multiple",
    )
    parser.add_argument("-v", "--verbose", type=bool, default=True, help="verbose")
    parser.add_argument("N", type=int, help="the integer to factor")

    return parser.parse_args()


def main():
    args = parse_args()

    global print_info
    if args.verbose:
        print_info = print_verbose
    else:
        print_info = print_none

    factors = shors(args.N, args.attempts, args.neighborhood, args.periods)
    if factors is not None:
        print("Factors:\t " + str(factors[0]) + ", " + str(factors[1]))


if __name__ == "__main__":
    main()
