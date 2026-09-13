# BigInt

> Primitive type cho số nguyên lớn hơn `Number.MAX_SAFE_INTEGER` (2^53 - 1)

## Cú pháp
```js
const big = 9007199254740993n;
const viaCtor = BigInt("9007199254740993");
console.log(typeof big); // bigint
```

## Lưu ý roadmap.sh
- Không trộn BigInt với Number: `1n + 1` → TypeError
- So sánh: `1n == 1` true (loose), `1n === 1` false
- Dùng cho ID, timestamp nano, crypto

## TODO
- [ ] Demo tính toán lớn
- [ ] So sánh `==` vs `===` với BigInt
