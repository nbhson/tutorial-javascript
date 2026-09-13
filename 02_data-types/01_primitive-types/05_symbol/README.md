# Symbol

> Primitive unique, dùng làm key ẩn / private

```js
const s1 = Symbol("id");
const s2 = Symbol("id");
console.log(s1 === s2); // false
const obj = { [s1]: 123 };
console.log(Object.keys(obj)); // [] - Symbol không enumerable
console.log(Object.getOwnPropertySymbols(obj));
```

## Built-in Symbols
- `Symbol.iterator`, `Symbol.toStringTag`

## TODO
- [ ] Demo Symbol làm private field
- [ ] Demo well-known Symbols
