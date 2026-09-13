function a(){ b(); }
function b(){ c(); }
function c(){ console.log("stack:"); console.trace(); }
a();
// scope chain
let g=1; function outer(){ let o=2; function inner(){ console.log(g,o); } inner(); } outer();
