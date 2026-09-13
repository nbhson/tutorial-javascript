class Counter {
  static count=0;
  #value=42;
  static inc(){ this.count++; }
  get value(){ return this.#value; }
  set value(v){ this.#value=v; }
}
Counter.inc(); Counter.inc();
console.log(Counter.count);
const c=new Counter();
console.log(c.value);
c.value=100; console.log(c.value);
// console.log(c.#value) // SyntaxError
