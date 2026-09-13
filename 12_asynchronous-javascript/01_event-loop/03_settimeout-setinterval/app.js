console.log(1);
setTimeout(()=>console.log("timeout 0"),0);
console.log(3);
let n=0; const id=setInterval(()=>{ console.log("interval",++n); if(n>=2) clearInterval(id); }, 10);
