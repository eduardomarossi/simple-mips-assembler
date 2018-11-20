lw $at, 0($zero) ; obtem 1 pra efeitos, ram(0) = 1 obrigatório
add $v0, $at, $at ; gera 2
add $v1, $v0, $at ; gera 3
add $t0, $v1, $v1 ; gera 6
add $t1, $t0, $v1 ; resultado esperado 9
sub $t1, $zero, $at ; resultado esperado -1
sub $t1, $t0, $v1 ; resultado esperado 3
sub $t1, $v1, $t0 ; resultado esperado -3
and $t1, $t0, $v0 ; resultado esperado 2
or $t1, $t0, $v0 ; resultado esperado 6
slt $t1, $v1, $t0 ; resultado esperado 1
slt $t1, $t0, $v1 ; resultado esperado 0
j 0