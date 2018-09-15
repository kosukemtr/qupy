# -*- coding: utf-8 -*-
import numpy as np
import qupy.operator as operator
from qupy.hamiltonian import Hamiltonian


def convert_openfermion_op(openfermion_op):
    """convert_openfermion_op

    Args:
        openfermion_op (:class:`openfermion.ops.QubitOperator`)
    Returns:
        :class:`qupy.hamiltonian.Hamiltonian`
    """
    terms = openfermion_op.terms
    n_qubit = 0

    coefs = []
    for term in terms:
        coefs.append(terms[term])
        # count number of qubit
        for one_operator in term:
            n_qubit = one_operator[0] if n_qubit < one_operator[0] else n_qubit

    n_qubit += 1

    ops = []
    for term in terms:
        if term == ():
            tmp = ["I" for i in range(n_qubit)]
        else:
            tmp = ["I" for i in range(n_qubit)]
            for one_operator in term:
                tmp[one_operator[0]] = one_operator[1]

        ops.append(''.join(tmp))

    return Hamiltonian(n_qubit, coefs, ops)


if __name__ == '__main__':
    import openfermion
    from openfermionpsi4 import run_psi4
    from openfermion.transforms import get_fermion_operator, jordan_wigner
    from openfermion.transforms import get_sparse_operator
    from openfermion.hamiltonians import MolecularData

    basis = "sto-3g"
    multiplicity = 1
    charge = 0
    distance = 0.744
    geometry = [["H", [0, 0, 0]], ["H", [0, 0, distance]]]

    description = str(distance)

    molecule = MolecularData(
        geometry, basis, multiplicity, charge, description)

    molecule = run_psi4(molecule, run_scf=1, run_fci=1)

    jw_hamiltonian = jordan_wigner(get_fermion_operator(
        molecule.get_molecular_hamiltonian()))
    
    print(jw_hamiltonian)
    
    ham = convert_openfermion_op(jw_hamiltonian)

    print(ham.ops)
    print(ham.coefs)
    mat = ham.get_matrix(ifdense = True)
    from numpy.linalg import eigh
    eigvals, eigvecs = eigh(mat)
    print(eigvals)
    print(eigvecs)
