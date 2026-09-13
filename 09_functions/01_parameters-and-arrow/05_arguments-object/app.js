function f(){ console.log(arguments, Array.from(arguments)); console.log(arguments.length); }
f(1,2,3);
const arrow = (...args)=> console.log(args); arrow(1,2);
