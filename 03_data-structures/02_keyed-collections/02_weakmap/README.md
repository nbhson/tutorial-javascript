# WeakMap

```js
let wm=new WeakMap(); let o={}; wm.set(o, "secret"); console.log(wm.get(o)); o=null; // GC có thể thu hồi
console.log("WeakMap không có size, không iterable");
```
