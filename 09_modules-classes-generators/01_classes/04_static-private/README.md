# Classes — Static & Private

```js
class Counter {
  static count=0;
  #private=42;
  static inc(){ this.count++; }
  getPriv(){ return this.#private; }
}
Counter.inc(); console.log(Counter.count);
console.log(new Counter().getPriv());
```
- `static` thuộc class, không phải instance
- `#private` (ES2022) chỉ truy cập trong class
