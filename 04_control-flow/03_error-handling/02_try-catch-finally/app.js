function risky(){ throw new Error("fail"); }
try{ risky(); }catch(e){ console.log("catch", e.message); }finally{ console.log("finally"); }
try{ try{ throw new Error("inner"); }finally{ console.log("inner finally"); } }catch(e){ console.log("outer catch"); }
