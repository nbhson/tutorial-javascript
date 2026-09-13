# setTimeout / setInterval

Macrotask queue.

```js
console.log(1);
setTimeout(()=>console.log(2),0);
console.log(3);
// 1 3 2
```
setInterval cần clearInterval.
