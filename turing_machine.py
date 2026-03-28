#!/usr/bin/env python3
"""turing_machine - Turing machine simulator."""
import sys, json

class TuringMachine:
    def __init__(self, tape='', blank='_', initial='q0', accepting=None, transitions=None):
        self.tape=list(tape) if tape else [blank]
        self.blank=blank; self.head=0; self.state=initial
        self.accepting=set(accepting or []); self.trans=transitions or {}
        self.steps=0
    def step(self):
        sym=self.tape[self.head] if self.head<len(self.tape) else self.blank
        key=(self.state, sym)
        if key not in self.trans: return False
        new_state, write, move = self.trans[key]
        while self.head>=len(self.tape): self.tape.append(self.blank)
        self.tape[self.head]=write
        self.state=new_state
        if move=='R': self.head+=1
        elif move=='L': self.head=max(0,self.head-1)
        self.steps+=1
        return True
    def run(self, max_steps=10000, verbose=False):
        while self.steps<max_steps:
            if verbose: self.display()
            if self.state in self.accepting: return True
            if not self.step(): return False
        return False
    def display(self):
        tape=''.join(self.tape).rstrip(self.blank) or self.blank
        pointer=' '*self.head+'^'
        print(f"  [{self.state:>4}] {tape}\n         {pointer}")
    def result(self): return ''.join(self.tape).strip(self.blank)

def binary_increment():
    """Increment a binary number."""
    trans={
        ('q0','0'):('q0','0','R'), ('q0','1'):('q0','1','R'), ('q0','_'):('carry','_','L'),
        ('carry','1'):('carry','0','L'), ('carry','0'):('done','1','L'), ('carry','_'):('done','1','R'),
        ('done','0'):('done','0','L'), ('done','1'):('done','1','L'), ('done','_'):('halt','_','R'),
    }
    return trans

def demo():
    print("Binary increment: 1011 -> ?")
    tm=TuringMachine('1011','_','q0',{'halt'},binary_increment())
    tm.run(verbose=True)
    print(f"\n  Result: {tm.result()} (steps: {tm.steps})")
    print(f"  {'✅ Accepted' if tm.state in tm.accepting else '❌ Rejected'}")

def main():
    args=sys.argv[1:]
    if not args or args[0]=='demo': demo()
    elif args[0]=='run':
        spec=json.loads(open(args[1]).read())
        trans={(tuple(k.split(','))):tuple(v) for k,v in spec['transitions'].items()}
        tm=TuringMachine(spec.get('tape',''),spec.get('blank','_'),spec.get('initial','q0'),
                        spec.get('accepting',[]),trans)
        tm.run(verbose='--verbose' in args)
        print(f"  Result: {tm.result()}, State: {tm.state}, Steps: {tm.steps}")

if __name__=='__main__': main()
