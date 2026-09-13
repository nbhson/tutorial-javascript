// BigInt demo
const maxSafe = Number.MAX_SAFE_INTEGER;
console.log(maxSafe, maxSafe + 1, maxSafe + 2); // 9007199254740992 -> mất chính xác
const big = 9007199254740993n;
console.log(big, typeof big);
console.log(big + 1n);
try { console.log(big + 1); } catch(e) { console.log("Mix error:", e.message); }
console.log(1n == 1, 1n === 1, Object.is(1n, 1n));
