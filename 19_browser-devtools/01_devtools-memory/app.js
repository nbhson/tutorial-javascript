// memory leak demo
let arr=[];
function leak(){ arr.push(new Array(100000).fill(0)); }
console.log("call leak() nhiều lần rồi chụp heap snapshot");
