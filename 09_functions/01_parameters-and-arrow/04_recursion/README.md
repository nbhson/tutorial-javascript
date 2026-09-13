# Recursion

```js
function factorial(n){ return n<=1?1:n*factorial(n-1); }
console.log(factorial(5));
function fib(n){ return n<=1?n:fib(n-1)+fib(n-2); }
```
Lưu ý base case, stack overflow.
