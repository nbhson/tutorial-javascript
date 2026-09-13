# Classes — Inheritance (extends)

```js
class Animal { speak(){ console.log("..."); } }
class Dog extends Animal { speak(){ super.speak(); console.log("woof"); } }
```
- `extends` kế thừa prototype
- `super` gọi parent
