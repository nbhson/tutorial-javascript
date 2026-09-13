"use strict"; function fn(){ console.log("strict function this", this); } fn();
function nonStrict(){ console.log("non-strict this == window?", this==globalThis); } nonStrict();
