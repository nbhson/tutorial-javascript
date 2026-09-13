const s1 = Symbol("id");
const s2 = Symbol("id");
console.log(s1 === s2);
const obj = { name: "A", [s1]: 42 };
console.log(Object.keys(obj), Object.getOwnPropertySymbols(obj));
console.log(obj[s1]);
// well-known
const arr = [1,2];
console.log(arr[Symbol.iterator].toString());
