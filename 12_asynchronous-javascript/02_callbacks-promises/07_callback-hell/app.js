function async1(cb){ setTimeout(()=>cb(1),10); }
function async2(x,cb){ setTimeout(()=>cb(x+1),10); }
function async3(x,cb){ setTimeout(()=>cb(x+1),10); }
async1(a=> async2(a, b=> async3(b, c=> console.log("hell result", c))))
// Promise version
Promise.resolve(1).then(x=>x+1).then(x=>x+1).then(console.log)
