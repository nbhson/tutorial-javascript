# this in arrow function (lexical)

```js
const outer={ x:42, make(){ const fn=()=> console.log("arrow lexical this.x", this.x); fn(); } };
outer.make();
const o={ x:1, hi(){ setTimeout(()=> console.log("arrow in setTimeout", this.x), 0); } };
o.hi();

```
