# XMLHttpRequest (roadmap.sh)

Tiền thân của fetch.

```js
const xhr = new XMLHttpRequest();
xhr.open("GET", "https://jsonplaceholder.typicode.com/posts/1");
xhr.onload = ()=> console.log(xhr.responseText.slice(0,80));
xhr.send();
```
Nên dùng fetch ngày nay.
