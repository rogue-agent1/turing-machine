#!/usr/bin/env python3
"""Turing machine simulator. Zero dependencies."""

class TuringMachine:
    def __init__(self, transitions, start, accept, reject="reject", blank="_"):
        self.transitions = transitions; self.start = start
        self.accept = accept; self.reject = reject; self.blank = blank

    def run(self, input_str, max_steps=10000):
        tape = list(input_str) if input_str else [self.blank]
        head = 0; state = self.start; steps = 0; history = []
        while steps < max_steps:
            if head < 0: tape.insert(0, self.blank); head = 0
            if head >= len(tape): tape.append(self.blank)
            sym = tape[head]
            history.append((state, head, "".join(tape)))
            if state == self.accept: return True, history, "".join(tape).strip(self.blank)
            if state == self.reject: return False, history, "".join(tape).strip(self.blank)
            key = (state, sym)
            if key not in self.transitions: return False, history, "".join(tape).strip(self.blank)
            new_state, write, move = self.transitions[key]
            tape[head] = write
            head += 1 if move == "R" else -1
            state = new_state; steps += 1
        return None, history, "".join(tape).strip(self.blank)  # timeout

def binary_increment_tm():
    """TM that increments a binary number."""
    return TuringMachine({
        ("start","0"):("start","0","R"), ("start","1"):("start","1","R"),
        ("start","_"):("carry","_","L"),
        ("carry","0"):("done","1","L"), ("carry","1"):("carry","0","L"),
        ("carry","_"):("done","1","R"),
        ("done","0"):("done","0","L"), ("done","1"):("done","1","L"),
        ("done","_"):("accept","_","R"),
    }, "start", "accept")

def palindrome_tm():
    """TM that checks if a binary string is a palindrome."""
    return TuringMachine({
        ("q0","0"):("s0","_","R"), ("q0","1"):("s1","_","R"), ("q0","_"):("accept","_","R"),
        ("s0","0"):("s0","0","R"), ("s0","1"):("s0","1","R"), ("s0","_"):("c0","_","L"),
        ("s1","0"):("s1","0","R"), ("s1","1"):("s1","1","R"), ("s1","_"):("c1","_","L"),
        ("c0","0"):("back","_","L"), ("c0","_"):("accept","_","R"),
        ("c1","1"):("back","_","L"), ("c1","_"):("accept","_","R"),
        ("c0","1"):("reject","1","R"), ("c1","0"):("reject","0","R"),
        ("back","0"):("back","0","L"), ("back","1"):("back","1","L"), ("back","_"):("q0","_","R"),
    }, "q0", "accept")

if __name__ == "__main__":
    tm = binary_increment_tm()
    ok, hist, result = tm.run("1011")
    print(f"1011 + 1 = {result}")
