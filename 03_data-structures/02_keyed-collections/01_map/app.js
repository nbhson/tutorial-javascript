const m=new Map(); m.set("a",1); m.set({id:1}, "obj"); console.log(m.get("a"), m.size); for(const [k,v] of m) console.log(k,v);
