# Implicit Type Coercion

Engine tự ép kiểu:

```js
"5" + 3 // "53"
"5" - 3 // 2
if ("") console.log("falsy")
null == undefined // true
```
- Falsy: `false, 0, "", null, undefined, NaN, 0n`
- Truthy: còn lại
