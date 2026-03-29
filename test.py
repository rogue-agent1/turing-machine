from turing_machine import binary_increment_tm, palindrome_tm
tm = binary_increment_tm()
ok, _, result = tm.run("1011")
assert ok and result == "1100"
ok2, _, result2 = tm.run("111")
assert ok2 and result2 == "1000"
ok3, _, result3 = tm.run("0")
assert ok3 and result3 == "1"
pal = palindrome_tm()
assert pal.run("101")[0] == True
assert pal.run("1001")[0] == True
assert pal.run("10")[0] == False
assert pal.run("")[0] == True
print("turing_machine tests passed")
