# Equality: == vs ===

|  | `==` (Loose) | `===` (Strict) |
|---|---|---|
| Coercion | có | không |
| `0 == false` | true | false |

```js
console.log(0 == false, 0 === false);
console.log("" == 0, "" === 0);
console.log(null == undefined, null === undefined);
```
