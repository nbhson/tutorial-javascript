# Classes — Constructor

```js
class User {
  constructor(name){ this.name=name; }
}
console.log(new User("A").name);
```
- Mỗi class chỉ 1 constructor
- `new` tạo object + gọi constructor
- `super()` trong subclass phải gọi trước `this`
