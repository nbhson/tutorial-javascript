# SameValueZero (Map/Set)

> Thuật toán của Map/Set/ Array.includes: giống SameValue nhưng `0 === -0`, `NaN === NaN`

```js
console.log([NaN].includes(NaN)); // true (SameValueZero)
console.log(Object.is(NaN, NaN)); // true (SameValue)
const s = new Set(); s.add(0); s.add(-0); console.log(s.size); // 1
```
