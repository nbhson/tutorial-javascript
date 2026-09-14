# Export và Import (Xuất và Nhập)

> Nguồn: [https://javascript.info/import-export](https://javascript.info/import-export)

<!-- fetched: 2026-09-14 -->

Export và import directives có nhiều biến thể cú pháp.

Trong bài viết trước chúng ta đã thấy một sử dụng đơn giản, bây giờ hãy khám phá thêm các ví dụ.

## [Export trước declarations](#export-before-declarations)

Chúng ta có thể đánh dấu bất kỳ declaration nào là exported bằng cách đặt `export` trước nó, cho dù đó là một variable, function hoặc class.

Ví dụ, ở đây tất cả exports đều hợp lệ:

```
// export một array
export let months = ['Tháng 1', 'Tháng 2', 'Tháng 3','Tháng 4', 'Tháng 8', 'Tháng 9', 'Tháng 10', 'Tháng 11', 'Tháng 12'];

// export một constant
export const MODULES_BECAME_STANDARD_YEAR = 2015;

// export một class
export class User {
  constructor(name) {
    this.name = name;
  }
}
```

Không có semicolon sau export class/function

Xin lưu ý rằng `export` trước một class hoặc một hàm không làm cho nó thành một [function expression](/function-expressions). Đó vẫn là một function declaration, tuy nhiên được export.

Hầu hết các JavaScript style guides không khuyến nghị semicolons sau function và class declarations.

Đó là lý do tại sao không cần semicolon ở cuối `export class` và `export function`:

```
export function sayHi(user) {
  alert(`Xin chào, ${user}!`);
}  // không có ; ở cuối
```

## [Export riêng biệt với declarations](#export-apart-from-declarations)

Cũng vậy, chúng ta có thể đặt `export` riêng biệt.

Ở đây chúng ta khai báo trước, và sau đó export:

```
// 📁 say.js
function sayHi(user) {
  alert(`Xin chào, ${user}!`);
}

function sayBye(user) {
  alert(`Tạm biệt, ${user}!`);
}

export {sayHi, sayBye}; // một danh sách các exported variables
```

…Về mặt kỹ thuật, chúng ta cũng có thể đặt `export` trên các hàm.

## [Import \*](#import)

Thông thường, chúng ta đặt một danh sách những gì để import trong curly braces `import {...}`, như thế này:

```
// 📁 main.js
import {sayHi, sayBye} from './say.js';

sayHi('John'); // Xin chào, John!
sayBye('John'); // Tạm biệt, John!
```

Nhưng nếu có nhiều thứ để import, chúng ta có thể import tất cả như một đối tượng bằng cách sử dụng `import * as <obj>`, ví dụ:

```
// 📁 main.js
import * as say from './say.js';

say.sayHi('John');
say.sayBye('John');
```

Thoạt nhìn, "import everything" dường như là một thứ tuyệt vời, viết ngắn, tại sao chúng ta nên explicitly liệt kê những gì cần import?

Chà, có một vài lý do.

1. Explicitly liệt kê những gì để import cho các tên ngắn hơn: `sayHi()` thay vì `say.sayHi()`.
2. Explicit list của các imports cung cấp tổng quan tốt hơn về cấu trúc mã: những gì được sử dụng và ở đâu. Nó làm cho code support và refactoring dễ dàng hơn.

Đừng sợ import quá nhiều

Các build tools hiện đại, chẳng hạn như [webpack](https://webpack.js.org/) và những người khác, bundle modules together và optimize chúng để tăng tốc loading. Chúng cũng xóa các imports không được sử dụng.

Ví dụ, nếu bạn `import * as library` từ một library code lớn, và sau đó chỉ sử dụng một vài methods, thì những cái không sử dụng [sẽ không được include](https://github.com/webpack/webpack/tree/main/examples/harmony-unused#examplejs) vào bundle được optimize.

## [Import "as"]( #import-as)

Chúng ta cũng có thể sử dụng `as` để import dưới các tên khác nhau.

Ví dụ, hãy import `sayHi` vào variable local `hi` để viết ngắn gọn, và import `sayBye` như `bye`:

```
// 📁 main.js
import {sayHi as hi, sayBye as bye} from './say.js';

hi('John'); // Xin chào, John!
bye('John'); // Tạm biệt, John!
```

## [Export "as"]( #export-as)

Cú pháp tương tự tồn tại cho `export`.

Hãy export các hàm như `hi` và `bye`:

```
// 📁 say.js
...
export {sayHi as hi, sayBye as bye};
```

Bây giờ `hi` và `bye` là các tên chính thức cho người ngoài, để sử dụng trong các imports:

```
// 📁 main.js
import * as say from './say.js';

say.hi('John'); // Xin chào, John!
say.bye('John'); // Tạm biệt, John!
```

## [Export default](#export-default)

Trong thực tế, chủ yếu có hai loại modules.

1. Modules chứa một library, pack của các functions, như `say.js` ở trên.
2. Modules khai báo một entity đơn lẻ, ví dụ một module `user.js` export chỉ `class User`.

Phần lớn, cách tiếp cận thứ hai được ưa chuộng, vì vậy mọi "thing" cư trú trong module của riêng nó.

Tất nhiên, điều đó yêu cầu nhiều files, vì mọi thứ muốn có module riêng, nhưng đó không phải là vấn đề gì cả. Thực tế, việc điều hướng code trở nên dễ dàng hơn nếu các files được đặt tên tốt và được cấu trúc thành các folders.

Modules cung cấp một syntax đặc biệt `export default` ("the default export") để làm cho cách "one thing per module" trông đẹp hơn.

Đặt `export default` trước entity để export:

```
// 📁 user.js
export default class User { // chỉ thêm "default"
  constructor(name) {
    this.name = name;
  }
}
```

Có thể có duy nhất một `export default` per file.

…Và sau đó import nó mà không có curly braces:

```
// 📁 main.js
import User from './user.js'; // không phải {User}, chỉ User

new User('John');
```

Các imports không có curly braces trông đẹp hơn. Một lỗi phổ biến khi bắt đầu sử dụng modules là quên curly braces. Vì vậy, hãy nhớ, `import` cần curly braces cho named exports và không cần chúng cho default export.

| Named export | Default export |
| --- | --- |
| `export class User {...}` | `export default class User {...}` |
| `import {User} from ...` | `import User from ...` |

Về mặt kỹ thuật, chúng ta có thể có cả default và named exports trong một module đơn, nhưng trong thực tế mọi người thường không trộn chúng. Một module có要么 named exports hoặc default export.

Vì có thể có tối đa một default export per file, entity được export có thể không có tên.

Ví dụ, tất cả các default exports sau đều hoàn toàn hợp lệ:

```
export default class { // không có class name
  constructor() { ... }
}
```

```
export default function(user) { // không có function name
  alert(`Xin chào, ${user}!`);
}
```

```
// export một single value, mà không cần tạo variable
export default ['Tháng 1', 'Tháng 2', 'Tháng 3','Tháng 4', 'Tháng 8', 'Tháng 9', 'Tháng 10', 'Tháng 11', 'Tháng 12'];
```

Việc không đặt tên là ổn, vì có duy nhất một `export default` per file, vì vậy `import` không có curly braces biết những gì để import.

Không có `default`, export như vậy sẽ gây lỗi:

```
export class { // Error! (non-default export cần một tên)
  constructor() {}
}
```

### [Tên "default"]( #the-default-name)

Trong một số tình huống từ khóa `default` được sử dụng để tham chiếu đến default export.

Ví dụ, để export một hàm riêng biệt từ definition của nó:

```
function sayHi(user) {
  alert(`Xin chào, ${user}!`);
}

// giống như nếu chúng ta thêm "export default" trước hàm
export {sayHi as default};
```

Hoặc, một tình huống khác, giả sử một module `user.js` export một thứ chính "default", và một vài cái named (hiếm khi xảy ra, nhưng nó xảy ra):

```
// 📁 user.js
export default class User {
  constructor(name) {
    this.name = name;
  }
}

export function sayHi(user) {
  alert(`Xin chào, ${user}!`);
}
```

Dưới đây là cách import default export cùng với một named export:

```
// 📁 main.js
import {default as User, sayHi} from './user.js';

new User('John');
```

Và, cuối cùng, nếu import tất cả `*` như một đối tượng, thì property `default` chính xác là default export:

```
// 📁 main.js
import * as user from './user.js';

let User = user.default; // default export
new User('John');
```

### [Lời phản đối về default exports](#a-word-against-default-exports)

Named exports là explicit. Chúng đúng tên những gì chúng import, vì vậy chúng ta có thông tin đó từ chúng; đó là một điều tốt.

Named exports buộc chúng ta phải sử dụng đúng tên để import:

```
import {User} from './user.js';
// import {MyUser} sẽ không hoạt động, tên phải là {User}
```

…Trong khi đối với một default export, chúng ta luôn chọn tên khi import:

```
import User from './user.js'; // works
import MyUser from './user.js'; // cũng works
// có thể là import Anything... và nó vẫn sẽ hoạt động
```

Vì vậy các thành viên trong team có thể sử dụng các tên khác nhau để import cùng thứ, và điều đó không tốt.

Thông thường, để tránh điều đó và giữ cho code consistent, có một rule là các imported variables nên tương ứng với file names, ví dụ:

```
import User from './user.js';
import LoginForm from './loginForm.js';
import func from '/path/to/func.js';
...
```

Vẫn còn, một số team coi đó là một nhược điểm nghiêm trọng của default exports. Vì vậy họ thích luôn sử dụng named exports. Ngay cả khi chỉ một thứ được export, nó vẫn được export dưới một tên, không có `default`.

Điều đó cũng làm cho re-export (xem bên dưới) dễ dàng hơn một chút.

## [Re-export](#re-export)

Cú pháp "re-export" `export ... from ...` cho phép import các thứ và ngay lập tức export chúng (có thể dưới một tên khác), như thế này:

```
export {sayHi} from './say.js'; // re-export sayHi

export {default as User} from './user.js'; // re-export default
```

Tại sao điều đó lại cần thiết? Hãy xem một trường hợp sử dụng thực tế.

Hãy tưởng tượng, chúng ta đang viết một "package": một folder với nhiều modules, với một số functionality được export ra ngoài (các công cụ như NPM cho phép chúng ta publish và phân phối các packages như vậy, nhưng chúng ta không cần phải sử dụng chúng), và nhiều modules chỉ là "helpers", cho internal use trong các module package khác.

Cấu trúc file có thể như thế này:

```
auth/
    index.js
    user.js
    helpers.js
    tests/
        login.js
    providers/
        github.js
        facebook.js
        ...
```

Chúng ta muốn expose functionality package qua một entry point duy nhất.

Nói cách khác, một người muốn sử dụng package của chúng ta, nên import chỉ từ "main file" `auth/index.js`.

Như thế này:

```
import {login, logout} from 'auth/index.js'
```

"Main file", `auth/index.js` export tất cả functionality mà chúng ta muốn cung cấp trong package của chúng ta.

Ý tưởng là những người outsider, các nhà phát triển khác sử dụng package của chúng ta, không nên can thiệp vào cấu trúc nội bộ của nó, tìm kiếm các files bên trong package folder của chúng ta. Chúng ta export chỉ những gì cần thiết trong `auth/index.js` và giữ phần còn lại ẩn khỏi những con mắt tò mò.

Vì functionality thực tế được export rải rác trong package, chúng ta có thể import nó vào `auth/index.js` và export từ nó:

```
// 📁 auth/index.js

// import login/logout và ngay lập tức export chúng
import {login, logout} from './helpers.js';
export {login, logout};

// import default như User và export nó
import User from './user.js';
export {User};
...
```

Bây giờ users của package chúng ta có thể `import {login} from "auth/index.js"`.

Cú pháp `export ... from ...` chỉ là một notation ngắn gọn cho import-export như vậy:

```
// 📁 auth/index.js
// re-export login/logout
export {login, logout} from './helpers.js';

// re-export default export như User
export {default as User} from './user.js';
...
```

Sự khác biệt đáng chú ý của `export ... from` so với `import/export` là các module được re-export không có sẵn trong file hiện tại. Vì vậy bên trong ví dụ trên của `auth/index.js` chúng ta không thể sử dụng các functions `login/logout` đã re-export.

### [Re-exporting default export](#re-exporting-the-default-export)

Default export cần xử lý riêng khi re-exporting.

Hãy nói chúng ta có `user.js` với `export default class User` và muốn re-export nó:

```
// 📁 user.js
export default class User {
  // ...
}
```

Chúng ta có thể gặp hai vấn đề với nó:

1. `export User from './user.js'` sẽ không hoạt động. Điều đó sẽ dẫn đến syntax error.

   Để re-export default export, chúng ta phải viết `export {default as User}`, như trong ví dụ ở trên.
2. `export * from './user.js'` re-export chỉ các named exports, nhưng bỏ qua default.

   Nếu chúng ta muốn re-export cả named và default exports, thì cần hai statements:

   ```
   export * from './user.js'; // để re-export named exports
   export {default} from './user.js'; // để re-export default export
   ```

Các oddities của re-exporting một default export là một trong những lý do tại sao một số nhà phát triển không thích default exports và thích named ones.

## [Tóm tắt](#summary)

Dưới đây là tất cả các loại `export` mà chúng ta đã đề cập trong các bài viết này.

Bạn có thể tự kiểm tra bằng cách đọc chúng và nhớ lại chúng có nghĩa gì:

- Trước declaration của class/function/…:
  - `export [default] class/function/variable ...`
- Standalone export:
  - `export {x [as y], ...}`.
- Re-export:
  - `export {x [as y], ...} from "module"`
  - `export * from "module"` (không re-export default).
  - `export {default [as y]} from "module"` (re-export default).

Import:

- Importing named exports:
  - `import {x [as y], ...} from "module"`
- Importing default export:
  - `import x from "module"`
  - `import {default as x} from "module"`
- Import tất cả:
  - `import * as obj from "module"`
- Import module (code của nó chạy), nhưng không gán bất kỳ exports nào của nó vào variables:
  - `import "module"`

Chúng ta có thể đặt các statement `import/export` ở đầu hoặc ở cuối một script, điều đó không quan trọng.

Vì vậy, về mặt kỹ thuật mã này là ổn:

```
sayHi();

// ...

import {sayHi} from './say.js'; // import ở cuối file
```

Trong thực tế các imports thường ở đầu file, nhưng đó chỉ là để thuận tiện hơn.

**Xin lưu ý rằng các statement import/export không hoạt động nếu bên trong `{...}`.**

Một conditional import, như thế này, sẽ không hoạt động:

```
if (something) {
  import {sayHi} from "./say.js"; // Error: import phải ở top level
}
```

…Nhưng điều gì nếu chúng ta thực sự cần import một thứ gì đó một cách conditional? Hoặc vào thời điểm đúng? Ví dụ, load một module khi được request, khi nó thực sự cần?

Chúng ta sẽ thấy dynamic imports trong bài viết tiếp theo.
