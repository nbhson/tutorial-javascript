const btn={ name:"btn", handle(){ console.log("event handler this.name", this.name); } };
// simulate addEventListener
function addListener(el, cb){ cb.call(el); }
addListener(btn, btn.handle);
// arrow loses this
const arrowBtn={ name:"arrow", handle: ()=> console.log("arrow this", this)};
arrowBtn.handle();
