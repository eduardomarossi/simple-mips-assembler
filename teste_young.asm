lw $at, 0($zero) # ram(0) = 1
add $at, $at, $at
add $at, $at, $at
lw $v0, 1($zero) #ram(1) = 0x10000
sw $at, 0($v0)
j 0