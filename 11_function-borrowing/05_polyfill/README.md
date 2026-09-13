# Polyfill (call/apply/bind)

Tự viết lại `myCall`, `myApply`, `myBind` để hiểu cơ chế.

```js
Function.prototype.myBind = function(ctx, ...args){ ... }
```

Xem `app.js` demo polyfill.
