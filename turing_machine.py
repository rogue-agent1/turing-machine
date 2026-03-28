#!/usr/bin/env python3
"""Universal Turing Machine simulator."""
class TM:
    def __init__(self,states,alphabet,blank,transitions,start,accept,reject):
        self.states=states; self.alpha=alphabet; self.blank=blank
        self.trans=transitions; self.start=start; self.accept=accept; self.reject=reject
    def run(self,input_str,max_steps=10000):
        tape=dict(enumerate(input_str)); head=0; state=self.start; steps=0
        while steps<max_steps:
            sym=tape.get(head,self.blank)
            if state==self.accept: return True,self._tape_str(tape),steps
            if state==self.reject: return False,self._tape_str(tape),steps
            key=(state,sym)
            if key not in self.trans: return False,self._tape_str(tape),steps
            new_state,write_sym,direction=self.trans[key]
            tape[head]=write_sym; state=new_state
            head+=1 if direction=="R" else -1; steps+=1
        return None,self._tape_str(tape),steps
    def _tape_str(self,tape):
        if not tape: return ""
        lo,hi=min(tape),max(tape)
        return "".join(tape.get(i,self.blank) for i in range(lo,hi+1)).strip(self.blank)
if __name__=="__main__":
    # Binary increment
    trans={("q0","0"):("q0","0","R"),("q0","1"):("q0","1","R"),("q0","_"):("carry","_","L"),
        ("carry","0"):("done","1","L"),("carry","1"):("carry","0","L"),("carry","_"):("done","1","L")}
    tm=TM(["q0","carry","done"],["0","1"],"_",trans,"q0","done","reject")
    for inp,exp in [("101","110"),("111","1000"),("0","1")]:
        ok,tape,steps=tm.run(inp)
        assert tape==exp,f"FAIL: {inp}+1={tape}"
        print(f"{inp} + 1 = {tape} ({steps} steps)")
    print("Turing Machine OK")
