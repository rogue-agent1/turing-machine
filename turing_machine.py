#!/usr/bin/env python3
"""Turing machine simulator."""
import sys, json

class TuringMachine:
    def __init__(self, tape='', blank='_', initial_state='q0', accept_states=None, transitions=None):
        self.tape = list(tape) if tape else [blank]
        self.blank = blank
        self.head = 0
        self.state = initial_state
        self.accept = set(accept_states or ['qaccept'])
        self.reject = {'qreject'}
        self.transitions = transitions or {}  # (state, symbol) -> (new_state, write, move)
        self.steps = 0
    def step(self):
        if self.head < 0: self.tape.insert(0, self.blank); self.head = 0
        while self.head >= len(self.tape): self.tape.append(self.blank)
        sym = self.tape[self.head]
        key = f"{self.state},{sym}"
        if key not in self.transitions: return False
        ns, ws, mv = self.transitions[key]
        self.tape[self.head] = ws
        self.state = ns
        self.head += 1 if mv == 'R' else -1
        self.steps += 1
        return True
    def run(self, max_steps=10000, trace=False):
        for _ in range(max_steps):
            if trace: self.show()
            if self.state in self.accept: return 'ACCEPT'
            if self.state in self.reject: return 'REJECT'
            if not self.step(): return 'HALT'
        return 'TIMEOUT'
    def show(self):
        tape_str = ''.join(self.tape)
        pointer = ' ' * self.head + '^'
        print(f"  [{self.state:>8}] {tape_str}")
        print(f"            {pointer}")

# Built-in examples
EXAMPLES = {
    'binary_inc': {
        'tape': '1011', 'initial': 'right', 'accept': ['done'],
        'transitions': {
            'right,0': ('right','0','R'), 'right,1': ('right','1','R'), 'right,_': ('carry','_','L'),
            'carry,1': ('carry','0','L'), 'carry,0': ('done','1','R'), 'carry,_': ('done','1','R'),
        }
    },
}

if __name__ == '__main__':
    if '--example' in sys.argv:
        name = sys.argv[2] if len(sys.argv) > 2 else 'binary_inc'
        ex = EXAMPLES[name]
        tm = TuringMachine(ex['tape'], initial_state=ex['initial'], accept_states=ex['accept'], transitions=ex['transitions'])
        result = tm.run(trace=True)
        print(f"\nResult: {result} | Steps: {tm.steps} | Tape: {''.join(tm.tape).strip('_')}")
    elif len(sys.argv) > 1:
        config = json.load(open(sys.argv[1]))
        tm = TuringMachine(config.get('tape',''), initial_state=config.get('initial','q0'),
                          accept_states=config.get('accept',['qaccept']), transitions=config.get('transitions',{}))
        result = tm.run(trace='--trace' in sys.argv)
        print(f"Result: {result} | Steps: {tm.steps}")
    else:
        print("Usage: turing_machine.py <config.json> [--trace]")
        print("       turing_machine.py --example binary_inc")
