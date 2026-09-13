console.log(5 & 1, 5 | 1, 5 ^ 1, ~5, 5<<1, 5>>1, -5>>>1);
// flags
const READ=1, WRITE=2, EXEC=4; let perm=READ|WRITE; console.log(perm & READ, perm & EXEC);
