try{ null.f(); }catch(e){ console.log(e.name, e instanceof TypeError); }
try{ eval("a b"); }catch(e){ console.log(e.name); }
console.log(new RangeError("range").name);
