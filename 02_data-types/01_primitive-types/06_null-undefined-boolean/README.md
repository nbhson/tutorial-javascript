# null / undefined / boolean

| Giá trị | typeof | falsy | Ghi chú |
|---|---|---|---|
| `undefined` | undefined | yes | chưa gán |
| `null` | object (bug) | yes | cố ý rỗng |
| `true`/`false` | boolean | - | |

```js
console.log(typeof null); // object
console.log(null == undefined, null === undefined);
console.log(Boolean(0), Boolean(""), Boolean([]));
```

## Bài tập
- [ ] Demo phân biệt null vs undefined
- [ ] Demo Boolean coercion
