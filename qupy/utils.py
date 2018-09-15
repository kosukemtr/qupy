# -*- coding: utf-8 -*-
import numpy as np
import qupy.operator as operator


def expm_pauli(q, theta, op):
    """expm_pauli(q, theta, op)
    applies Pauli rotation $expm(-i*theta*op)$ on the Qubits instance q

    Args:
        q (:class:`qupy.qubit.Qubits`):
            the state which you want to apply
        theta (:class:`float`):
            rotation angle
        op (:class:`str`)
            the pauli string
    """
    target_list = [i for i, p in enumerate(op) if p != "I"]
    cnot_target = target_list[-1]
    if op[cnot_target] == "X":
        q.gate(operator.H, target=cnot_target)
    elif op[cnot_target] == "Y":
        q.gate(operator.S, target=cnot_target)
        q.gate(operator.H, target=cnot_target)
    for target in target_list[:-1]:
        targ = int(target)
        if op[targ] == "X":
            #print("H {}".format(i))
            q.gate(operator.H, target=targ)
        elif op[targ] == "Y":
            #print("HS {}".format(i))
            q.gate(operator.S, target=targ)
            q.gate(operator.H, target=targ)
        #print("CNOT({}, {})".format(i, target))
        q.gate(operator.X, control=targ, target=cnot_target)
    q.gate(operator.rz(2*theta), target=cnot_target)
    for target in target_list[:-1]:
        targ = int(target)
        q.gate(operator.X, control=targ, target=cnot_target)
        if op[targ] == "X":
            q.gate(operator.H, target=targ)
        elif op[targ] == "Y":
            q.gate(operator.H, target=targ)
            q.gate(operator.Sdag, target=targ)
    if op[cnot_target] == "X":
        q.gate(operator.H, target=cnot_target)
    elif op[cnot_target] == "Y":
        q.gate(operator.H, target=cnot_target)
        q.gate(operator.Sdag, target=cnot_target)


if __name__ == '__main__':
    from qupy.qubit import Qubits
    q_ins = Qubits(2)
    q_ins.gate(operator.H, target = 1)
    q_ins.gate(operator.H, target = 0)
    th = np.pi/2
    paulistr = "ZY"
    expm_pauli(q_ins, th, paulistr)
    print(q_ins.get_state())
