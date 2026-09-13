# Callback Hell

Pyramid of doom.

```js
async1((a)=> async2(a,(b)=> async3(b, (c)=> console.log(c))));
```
Giải pháp: Promises / async/await.
