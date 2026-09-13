# Iterators (Symbol.iterator)

```js
const obj={ *[Symbol.iterator](){ yield 1; yield 2; } };
for(const x of obj) console.log(x);
```
Phân biệt Iterator vs Generator.
