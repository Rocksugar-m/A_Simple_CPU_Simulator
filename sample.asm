      j 3
      lw r1, 0(r0)
      lw r1, 1(r0)
      lw r1, 2(r0)
      addiu r2, r0, 0
loop: addu r2, r2, r1
      addiu r1, r1, -1
      bgtz r1, -2
      sw r2, 3(r0)