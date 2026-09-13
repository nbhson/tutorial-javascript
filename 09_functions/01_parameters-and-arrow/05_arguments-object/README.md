# arguments object

Array-like, có trong function thường, không có trong arrow.

```js
function f(){ console.log(arguments, arguments.length); }
f(1,2,3);
```
Nên dùng rest `...args` thay thế.
