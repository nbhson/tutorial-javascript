# Generators

```js
function* gen(){ yield 1; yield 2; }
for(const x of gen()) console.log(x);
```
Khác Iterator: generator tự tạo iterator qua `function*`.
