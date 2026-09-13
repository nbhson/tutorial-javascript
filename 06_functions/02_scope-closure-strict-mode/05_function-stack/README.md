# Scope & Function Stack

Call Stack LIFO, mỗi call tạo execution context.

```js
function a(){ b(); }
function b(){ c(); }
function c(){ console.trace(); }
a();
```
Scope chain: inner truy cập outer.
