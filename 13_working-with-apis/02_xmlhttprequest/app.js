const xhr=new XMLHttpRequest();
xhr.open("GET","https://jsonplaceholder.typicode.com/posts/1");
xhr.onload=()=> console.log("XHR status",xhr.status, xhr.responseText.slice(0,100));
xhr.onerror=()=> console.log("XHR error");
xhr.send();
// fetch equivalent
fetch("https://jsonplaceholder.typicode.com/posts/1").then(r=>r.text()).then(t=>console.log("fetch",t.slice(0,100)))
