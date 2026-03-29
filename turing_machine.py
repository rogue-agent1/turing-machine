#!/usr/bin/env python3
"""turing_machine - Universal Turing machine simulator."""
import sys, json

class TuringMachine:
    def __init__(self, blank="_"):
        self.transitions = {}; self.start = None; self.accept = set(); self.reject = set()
        self.blank = blank
    
    def add_transition(self, state, read, new_state, write, move):
        self.transitions[(state, read)] = (new_state, write, move)
    
    def run(self, tape_input, max_steps=10000):
        tape = dict(enumerate(tape_input))
        head = 0; state = self.start; steps = 0; history = []
        while steps < max_steps:
            sym = tape.get(head, self.blank)
            if state in self.accept: return {"accepted": True, "steps": steps, "tape": self._read_tape(tape)}
            if state in self.reject: return {"accepted": False, "steps": steps, "tape": self._read_tape(tape)}
            key = (state, sym)
            if key not in self.transitions: return {"accepted": False, "steps": steps, "tape": self._read_tape(tape), "stuck": True}
            new_state, write, move = self.transitions[key]
            tape[head] = write; state = new_state
            head += 1 if move == "R" else (-1 if move == "L" else 0)
            steps += 1
        return {"accepted": False, "steps": steps, "tape": self._read_tape(tape), "timeout": True}
    
    def _read_tape(self, tape):
        if not tape: return ""
        lo, hi = min(tape.keys()), max(tape.keys())
        return "".join(tape.get(i, self.blank) for i in range(lo, hi+1)).strip(self.blank)

def main():
    print("Turing machine demo\n")
    # Binary increment
    tm = TuringMachine(); tm.start = "right"; tm.accept = {"done"}
    tm.add_transition("right", "0", "right", "0", "R")
    tm.add_transition("right", "1", "right", "1", "R")
    tm.add_transition("right", "_", "carry", "_", "L")
    tm.add_transition("carry", "0", "done", "1", "R")
    tm.add_transition("carry", "1", "carry", "0", "L")
    tm.add_transition("carry", "_", "done", "1", "R")
    for binary in ["101", "111", "1011", "1111"]:
        r = tm.run(binary)
        print(f"  {binary} + 1 = {r['tape']} ({r['steps']} steps)")
    # a^n b^n c^n checker
    tm2 = TuringMachine(); tm2.start = "q0"; tm2.accept = {"accept"}; tm2.reject = {"reject"}
    tm2.add_transition("q0", "a", "q1", "X", "R")
    tm2.add_transition("q0", "Y", "q4", "Y", "R")
    tm2.add_transition("q1", "a", "q1", "a", "R")
    tm2.add_transition("q1", "Y", "q1", "Y", "R")
    tm2.add_transition("q1", "b", "q2", "Y", "R")
    tm2.add_transition("q2", "b", "q2", "b", "R")
    tm2.add_transition("q2", "Z", "q2", "Z", "R")
    tm2.add_transition("q2", "c", "q3", "Z", "L")
    tm2.add_transition("q3", "a", "q3", "a", "L"); tm2.add_transition("q3", "b", "q3", "b", "L")
    tm2.add_transition("q3", "Y", "q3", "Y", "L"); tm2.add_transition("q3", "Z", "q3", "Z", "L")
    tm2.add_transition("q3", "X", "q0", "X", "R")
    tm2.add_transition("q4", "Y", "q4", "Y", "R"); tm2.add_transition("q4", "Z", "q4", "Z", "R")
    tm2.add_transition("q4", "_", "accept", "_", "R")
    print(f"\n  a^nb^nc^n:")
    for s in ["abc", "aabbcc", "aabbc", "abcc"]:
        r = tm2.run(s)
        print(f"    '{s}': {'✓' if r['accepted'] else '✗'} ({r['steps']} steps)")

if __name__ == "__main__":
    main()
