# this in a method

```js
const obj={ name:"A", hi(){ console.log("method", this.name); } }; obj.hi();
const fn=obj.hi; try{ fn(); }catch(e){console.log("detached", e.message);}

```
