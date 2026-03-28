#!/usr/bin/env python3
"""Turing machine simulator — configurable states, alphabet, transitions."""
import sys, json

class TuringMachine:
    def __init__(self, transitions, start="q0", accept={"qaccept"}, reject={"qreject"}, blank="_"):
        self.trans = transitions; self.state = start
        self.accept = accept; self.reject = reject; self.blank = blank
    def run(self, tape_input, max_steps=10000, verbose=False):
        tape = list(tape_input) + [self.blank]*100
        head = 0; self.state = "q0"
        for step in range(max_steps):
            if self.state in self.accept: return True, "".join(tape).strip(self.blank), step
            if self.state in self.reject: return False, "".join(tape).strip(self.blank), step
            sym = tape[head] if 0<=head<len(tape) else self.blank
            key = f"{self.state},{sym}"
            if key not in self.trans: return False, "".join(tape).strip(self.blank), step
            new_state, write, move = self.trans[key]
            if verbose:
                vis = "".join(tape[:head]) + f"[{tape[head]}]" + "".join(tape[head+1:head+20])
                print(f"  {step}: {self.state} | {vis.strip(self.blank)}")
            tape[head] = write; self.state = new_state
            head += 1 if move == "R" else -1
            if head < 0: tape.insert(0, self.blank); head = 0
            if head >= len(tape): tape.append(self.blank)
        return None, "".join(tape).strip(self.blank), max_steps

EXAMPLES = {
    "palindrome": {
        "q0,0": ("q1", "_", "R"), "q0,1": ("q2", "_", "R"), "q0,_": ("qaccept", "_", "R"),
        "q1,0": ("q1", "0", "R"), "q1,1": ("q1", "1", "R"), "q1,_": ("q3", "_", "L"),
        "q2,0": ("q2", "0", "R"), "q2,1": ("q2", "1", "R"), "q2,_": ("q4", "_", "L"),
        "q3,0": ("q5", "_", "L"), "q3,_": ("qaccept", "_", "R"),
        "q4,1": ("q5", "_", "L"), "q4,_": ("qaccept", "_", "R"),
        "q3,1": ("qreject", "1", "R"), "q4,0": ("qreject", "0", "R"),
        "q5,0": ("q5", "0", "L"), "q5,1": ("q5", "1", "L"), "q5,_": ("q0", "_", "R"),
    },
    "increment": {
        "q0,0": ("q0", "0", "R"), "q0,1": ("q0", "1", "R"), "q0,_": ("q1", "_", "L"),
        "q1,1": ("q1", "0", "L"), "q1,0": ("qaccept", "1", "R"), "q1,_": ("qaccept", "1", "R"),
    },
}

def cli():
    if len(sys.argv) < 2:
        print("Usage: turing_machine <example> <input> [-v]"); print(f"  Examples: {list(EXAMPLES.keys())}"); sys.exit(1)
    name = sys.argv[1]; inp = sys.argv[2] if len(sys.argv)>2 else ""
    verbose = "-v" in sys.argv
    trans = EXAMPLES.get(name)
    if not trans: print(f"Unknown example: {name}"); sys.exit(1)
    tm = TuringMachine(trans)
    accepted, tape, steps = tm.run(inp, verbose=verbose)
    print(f"Input: {inp}"); print(f"Result: {'ACCEPT' if accepted else 'REJECT' if accepted==False else 'TIMEOUT'}")
    print(f"Tape: {tape}"); print(f"Steps: {steps}")

if __name__ == "__main__": cli()
