console.log([NaN].includes(NaN));
const s=new Set(); s.add(0); s.add(-0); console.log("Set size 0/-0:", s.size);
console.log(Object.is(0,-0), s.has(-0));
