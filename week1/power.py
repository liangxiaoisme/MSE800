# Week 4 Quantum Computing Tasks
# Requires: qiskit, qiskit-aer, matplotlib

from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_state_qsphere
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt

# ==========================================================
# Task 1:
# Create a 2-qubit quantum circuit with a 90° phase shift
# and visualize it using the Q-sphere.
# ==========================================================

print("=== Task 1: 2-Qubit Circuit with 90° Phase Shift ===")

qc1 = QuantumCircuit(2)

# Put qubit 0 into superposition
qc1.h(0)

# Apply a 90° phase shift (π/2 radians)
qc1.p(3.1415926535 / 2, 0)

# Entangle the two qubits
qc1.cx(0, 1)

print(qc1.draw('mpl'))
plt.show()

# Generate statevector and plot Q-sphere
state = Statevector.from_instruction(qc1)
plot_state_qsphere(state)
plt.show()