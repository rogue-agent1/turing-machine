#!/usr/bin/env python3
"""turing_machine - Universal Turing machine simulator."""
import argparse, json, sys

def run_tm(tape_str, rules, start, accept, reject, max_steps=10000):
    tape = dict(enumerate(tape_str))
    head = 0; state = start; steps = 0
    while steps < max_steps:
        sym = tape.get(head, "_")
        key = f"{state},{sym}"
        if state in (accept, reject): break
        if key not in rules:
            print(f"No rule for ({state}, {sym}), halting"); break
        new_sym, direction, new_state = rules[key]
        tape[head] = new_sym
        head += 1 if direction == "R" else -1
        state = new_state; steps += 1
        if steps <= 50:
            lo, hi = min(tape.keys()), max(tape.keys())
            t = "".join(tape.get(i,"_") for i in range(lo, hi+1))
            ptr = head - lo
            print(f"  [{state:>8}] {t[:ptr]}[{tape.get(head,'_')}]{t[ptr+1:]}")
    result = "ACCEPT" if state == accept else "REJECT" if state == reject else "HALT"
    lo, hi = min(tape.keys()), max(tape.keys())
    final = "".join(tape.get(i,"_") for i in range(lo, hi+1)).strip("_")
    print(f"\nResult: {result} after {steps} steps")
    print(f"Tape: {final}")

def main():
    p = argparse.ArgumentParser(description="Turing machine simulator")
    p.add_argument("program", help="JSON file with TM definition")
    p.add_argument("input", help="Input string")
    p.add_argument("-m","--max-steps",type=int,default=10000)
    a = p.parse_args()
    with open(a.program) as f: tm = json.load(f)
    run_tm(a.input, tm["rules"], tm.get("start","q0"), tm.get("accept","qa"), tm.get("reject","qr"), a.max_steps)

if __name__ == "__main__": main()
