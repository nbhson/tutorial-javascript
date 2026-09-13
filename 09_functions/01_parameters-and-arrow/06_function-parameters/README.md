# Function Parameters

```js
function greet(name, age=18, ...rest){ console.log(name, age, rest); }
greet("A", 20, "x", "y");
greet(); // name undefined
```
- Params vs Arguments
- Required vs Default
- Rest gathers remaining
