# Classes — Basics

> roadmap.sh: Classes

```js
class Course {
  constructor(name, price) { this.name=name; this.price=price; }
  getName(){ return this.name; }
}
const c = new Course("JS", 100);
```

- `class` là syntactic sugar của prototype
- `constructor` chạy khi `new`
