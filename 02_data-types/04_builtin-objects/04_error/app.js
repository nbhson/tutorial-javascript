try{throw new TypeError("bad");}catch(e){console.log(e.name, e.message, e.stack.slice(0,80));}
