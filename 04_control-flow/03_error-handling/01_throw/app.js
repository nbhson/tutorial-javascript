function div(a,b){ if(b===0) throw new Error("divide by zero"); return a/b; }
try{ div(1,0);}catch(e){console.log(e.message);}
