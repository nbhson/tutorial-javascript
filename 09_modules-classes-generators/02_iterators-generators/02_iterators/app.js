const obj={ *[Symbol.iterator](){ yield 1; yield 2; yield 3; } };
for(const x of obj) console.log(x);
const it=obj[Symbol.iterator](); console.log(it.next(), it.next());
