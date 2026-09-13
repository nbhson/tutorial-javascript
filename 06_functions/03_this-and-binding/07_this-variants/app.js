// 1. in a method
const obj={ name:"A", hi(){ console.log("method", this.name); } }; obj.hi();
// 2. in a function
function fn(){ console.log("function strict", this); } fn(); // undefined in strict
// 3. alone
console.log("alone global", typeof window !== "undefined" ? "window" : "global");
// 4. event handler (mô phỏng)
const btn={ addEventListener(type, cb){ cb.call(btn); } }; btn.addEventListener("click", function(){ console.log("event handler this == btn", this===btn); });
// 5. arrow captures lexical
const outer={ x:42, arrow(){ const fn=()=> console.log("arrow this.x", this.x); fn(); } }; outer.arrow();
// explicit binding
function greet(){ console.log(this.name); }
greet.call({name:"call"}); greet.apply({name:"apply"}); const b=greet.bind({name:"bind"}); b();
