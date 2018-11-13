lw $at, 4($zero) ; setup - endereco onde contem o valor 1 
add $v0, $at, $at ; gera 32 - 2
add $v0, $v0, $v0 ; 4
add $v0, $v0, $v0 ; 8
add $v0, $v0, $v0 ; 16
add $v0, $v0, $v0 ; 32
add $v1, $v0, $v0 ; 64
add $v1, $v1, $v1 ; 128
add $t0, $zero, $zero ; 0
add $t1, $at, $zero ; 1
beq $t0, $v0, 4
add $t1, $t1, $t1
sw $t1, 1024($zero); leds
j 8
add $t0, $zero, $zero
add $t1, $at, $zero ; 1
beq $t0, $v1, 4
add $t1, $t1, $at ; + 1
sw $t1, 1027($zero);
j 17
j 21