# Function Borrowing — bind Advanced

> `bind` tạo hàm mới với `this` cố định, hỗ trợ partial application

```js
function greet(greeting, name){ console.log(greeting+name+this.suffix); }
const b = greet.bind({suffix:"!"}, "Hello ");
b("An"); // Hello An!
```
Xem `app.js` demo bind + currying.
