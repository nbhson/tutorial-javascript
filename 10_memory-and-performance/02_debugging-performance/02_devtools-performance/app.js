function heavy(){ let s=0; for(let i=0;i<1e7;i++) s+=i; return s; }
console.log("click to record performance");
setTimeout(heavy, 100);
