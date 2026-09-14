# Dynamic imports (Nhập động)

> Nguồn: [https://javascript.info/modules-dynamic-imports](https://javascript.info/modules-dynamic-imports)

<!-- fetched: 2026-09-14 -->

Export và import statements mà chúng ta đã đề cập trong các chương trước được gọi là "static". Cú pháp rất đơn giản và nghiêm ngặt.

Đầu tiên, chúng ta không thể dynamic generate bất kỳ parameters nào của `import`.

Đường dẫn module phải là một primitive string, không thể là một function call. Điều này sẽ không hoạt động:

```
import ... from getModuleName(); // Error, chỉ "string" được phép
```

Thứ hai, chúng ta không thể import conditional hoặc tại runtime:

```
if(...) {
  import ...; // Error, không được phép!
}

{
  import ...; // Error, chúng ta không thể đặt import trong bất kỳ block nào
}
```

Đó là vì `import`/`export` nhằm cung cấp một backbone cho cấu trúc mã. Đó là một điều tốt, vì cấu trúc mã có thể được phân tích, các module có thể được gather và bundle vào một file bởi các công cụ đặc biệt, unused exports có thể được xóa ("tree-shaken"). Điều đó chỉ có thể vì cấu trúc của imports/exports là đơn giản và cố định.

Nhưng làm thế nào để chúng ta import một module một cách dynamic, theo yêu cầu?

## [Biểu thức import()](#the-import-expression)

Biểu thức `import(module)` tải module và trả về một promise resolve vào một module object chứa tất cả exports của nó. Nó có thể được gọi từ bất cứ đâu trong mã.

Chúng ta có thể sử dụng nó một cách dynamic ở bất cứ đâu trong mã, ví dụ:

```
let modulePath = prompt("Module nào cần tải?");

import(modulePath)
  .then(obj => <module object>)
  .catch(err => <loading error, ví dụ nếu không có module như vậy>)
```

Hoặc, chúng ta có thể sử dụng `let module = await import(modulePath)` nếu bên trong một async function.

Ví dụ, nếu chúng ta có module sau `say.js`:

```
// 📁 say.js
export function hi() {
  alert(`Xin chào`);
}

export function bye() {
  alert(`Tạm biệt`);
}
```

…Thì dynamic import có thể như thế này:

```
let {hi, bye} = await import('./say.js');

hi();
bye();
```

Hoặc, nếu `say.js` có default export:

```
// 📁 say.js
export default function() {
  alert("Module đã được tải (export default)!");
}
```

…Sau đó, để truy cập nó, chúng ta có thể sử dụng property `default` của module object:

```
let obj = await import('./say.js');
let say = obj.default;
// hoặc, trong một dòng: let {default: say} = await import('./say.js');

say();
```

Dưới đây là ví dụ đầy đủ:

Result

say.js

index.html

```
export function hi() {
  alert(`Xin chào`);
}

export function bye() {
  alert(`Tạm biệt`);
}

export default function() {
  alert("Module đã được tải (export default)!");
}
```

```
<!doctype html>
<script>
  async function load() {
    let say = await import('./say.js');
    say.hi(); // Xin chào!
    say.bye(); // Tạm biệt!
    say.default(); // Module đã được tải (export default)!
  }
</script>
<button onclick="load()">Click vào tôi</button>
```

Xin lưu ý:

Dynamic imports hoạt động trong regular scripts, chúng không yêu cầu `script type="module"`.

Xin lưu ý:

Mặc dù `import()` trông giống như một function call, nó là một cú pháp đặc biệt chỉ tình cờ sử dụng parentheses (tương tự như `super()`).

Vì vậy chúng ta không thể copy `import` vào một variable hoặc sử dụng `call/apply` với nó. Nó không phải là một function.
