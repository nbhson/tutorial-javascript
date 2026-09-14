# Module, giới thiệu

> Nguồn: [https://javascript.info/modules-intro](https://javascript.info/modules-intro)

<!-- fetched: 2026-09-14 -->

Khi ứng dụng của chúng ta trở nên lớn hơn, chúng ta muốn chia nó thành nhiều file, được gọi là "modules". Một module có thể chứa một class hoặc một thư viện các hàm cho một mục đích cụ thể.

Trong một thời gian dài, JavaScript tồn tại mà không có module syntax ở cấp ngôn ngữ. Đó không phải là vấn đề, vì ban đầu scripts nhỏ và đơn giản, vì vậy không có nhu cầu.

Nhưng cuối cùng scripts trở nên phức tạp hơn, vì vậy community đã phát minh ra nhiều cách khác nhau để tổ chức code vào modules, các thư viện đặc biệt để tải modules theo yêu cầu.

Để nêu tên một số (vì lý do lịch sử):

- [AMD](https://en.wikipedia.org/wiki/Asynchronous_module_definition) – một trong những hệ thống module cổ xưa nhất, ban đầu được implement bởi thư viện [require.js](https://requirejs.org/).
- [CommonJS](https://wiki.commonjs.org/wiki/Modules/1.1) – hệ thống module được tạo ra cho Node.js server.
- [UMD](https://github.com/umdjs/umd) – một hệ thống module khác, được đề xuất như một universal, tương thích với AMD và CommonJS.

Bây giờ tất cả chúng dần trở thành một phần của lịch sử, nhưng chúng ta vẫn có thể tìm thấy chúng trong các scripts cũ.

Hệ thống module cấp ngôn ngữ xuất hiện trong standard vào năm 2015, dần dần phát triển kể từ đó, và bây giờ được hỗ trợ bởi tất cả các trình duyệt chính và trong Node.js. Vì vậy chúng ta sẽ nghiên cứu các module JavaScript hiện đại từ bây giờ.

## [Module là gì?](#what-is-a-module)

Một module chỉ là một file. Một script là một module. Đơn giản như vậy.

Các module có thể tải lẫn nhau và sử dụng các directive đặc biệt `export` và `import` để trao đổi functionality, gọi các hàm của module này từ module khác:

- `export` keyword đánh dấu các variables và functions có thể truy cập được từ bên ngoài module hiện tại.
- `import` cho phép import functionality từ các module khác.

Ví dụ, nếu chúng ta có file `sayHi.js` exporting một hàm:

```
// 📁 sayHi.js
export function sayHi(user) {
  alert(`Xin chào, ${user}!`);
}
```

…Thì một file khác có thể import và sử dụng nó:

```
// 📁 main.js
import {sayHi} from './sayHi.js';

alert(sayHi); // function...
sayHi('John'); // Xin chào, John!
```

Directive `import` tải module bằng đường dẫn `./sayHi.js` tương đối so với file hiện tại, và gán hàm exported `sayHi` cho variable tương ứng.

Hãy chạy ví dụ trong-browser.

Vì modules hỗ trợ các keywords và features đặc biệt, chúng ta phải nói với trình duyệt rằng script nên được xử lý như một module, bằng cách sử dụng attribute `<script type="module">`.

Như thế này:

Result

say.js

index.html

```
export function sayHi(user) {
  return `Xin chào, ${user}!`;
}
```

```
<!doctype html>
<script type="module">
  import {sayHi} from './say.js';

  document.body.innerHTML = sayHi('John');
</script>
```

Trình duyệt tự động fetch và evaluate imported module (và các imports của nó nếu cần), và sau đó chạy script.

Modules chỉ hoạt động qua HTTP(s), không hoạt động local

Nếu bạn cố mở một web-page local, qua protocol `file://`, bạn sẽ thấy rằng các directive `import/export` không hoạt động. Hãy sử dụng một local web-server, chẳng hạn như [static-server](https://www.npmjs.com/package/static-server#getting-started) hoặc sử dụng capability "live server" của editor của bạn, chẳng hạn như VS Code [Live Server Extension](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer) để test modules.

## [Các tính năng cốt lõi của module](#core-module-features)

Có gì khác biệt trong modules, so với các script "thông thường"?

Có các core features, hợp lệ cho cả browser và server-side JavaScript.

### [Luôn luôn "use strict"]( #always-use-strict)

Modules luôn hoạt động trong strict mode. Ví dụ, gán cho một undeclared variable sẽ gây lỗi.

```
<script type="module">
  a = 5; // error
</script>
```

### [Scope cấp module](#module-level-scope)

Mỗi module có scope top-level riêng. Nói cách khác, các variables và functions top-level từ một module không được thấy trong các scripts khác.

Trong ví dụ dưới đây, hai scripts được import, và `hello.js` cố gắng sử dụng variable `user` được khai báo trong `user.js`. Nó thất bại, vì đó là một module riêng biệt (bạn sẽ thấy lỗi trong console):

Result

hello.js

user.js

index.html

```
alert(user); // không có variable như vậy (mỗi module có variables độc lập)
```

```
let user = "John";
```

```
<!doctype html>
<script type="module" src="user.js"></script>
<script type="module" src="hello.js"></script>
```

Modules nên `export` những gì họ muốn có thể truy cập từ bên ngoài và `import` những gì họ cần.

- `user.js` nên export variable `user`.
- `hello.js` nên import nó từ module `user.js`.

Nói cách khác, với modules chúng ta sử dụng import/export thay vì dựa vào global variables.

Đó là biến thể đúng:

Result

hello.js

user.js

index.html

```
import {user} from './user.js';

document.body.innerHTML = user; // John
```

```
export let user = "John";
```

```
<!doctype html>
<script type="module" src="hello.js"></script>
```

Trong trình duyệt, nếu chúng ta nói về các trang HTML, independent top-level scope cũng tồn tại cho mỗi `<script type="module">`.

Dưới đây là hai scripts trên cùng trang, cả hai `type="module"`. Chúng không thấy các variables top-level của nhau:

```
<script type="module">
  // Variable chỉ可见 trong module script này
  let user = "John";
</script>

<script type="module">
  alert(user); // Error: user is not defined
</script>
```

Xin lưu ý:

Trong trình duyệt, chúng ta có thể làm cho một variable window-level global bằng cách gán nó một cách explicit cho một `window` property, ví dụ `window.user = "John"`.

Sau đó tất cả scripts sẽ thấy nó, cả với `type="module"` và không có nó.

Tuy nhiên, việc tạo các global variables như vậy bị coi là không nên. Xin hãy cố tránh chúng.

### [Mã module chỉ được evaluate lần đầu tiên khi được import](#a-module-code-is-evaluated-only-the-first-time-when-imported)

Nếu cùng một module được import vào nhiều module khác, mã của nó được thực thi chỉ một lần, trong lần import đầu tiên. Sau đó các exports của nó được chuyển đến tất cả các importers tiếp theo.

Việc evaluate một lần có các hậu quả quan trọng, mà chúng ta nên nhận thức.

Hãy xem một vài ví dụ.

Trước tiên, nếu việc thực thi mã module mang lại side-effects, như hiển thị một thông báo, thì import nó nhiều lần sẽ chỉ kích hoạt nó lần đầu tiên:

```
// 📁 alert.js
alert("Module đã được evaluate!");
```

```
// Import cùng module từ các file khác nhau

// 📁 1.js
import `./alert.js`; // Module đã được evaluate!

// 📁 2.js
import `./alert.js`; // (không hiển thị gì)
```

Lần import thứ hai không hiển thị gì, vì module đã được evaluate rồi.

Có một rule: mã module top-level nên được sử dụng cho initialization, creation của các internal data structures đặc biệt cho module. Nếu chúng ta cần làm gì đó có thể gọi được nhiều lần – chúng ta nên export nó như một hàm, như chúng ta đã làm với `sayHi` ở trên.

Bây giờ, hãy xem xét một ví dụ sâu hơn.

Giả sử, một module export một đối tượng:

```
// 📁 admin.js
export let admin = {
  name: "John"
};
```

Nếu module này được import từ nhiều file, module chỉ được evaluate lần đầu tiên, đối tượng `admin` được tạo, và sau đó được chuyển đến tất cả các importers tiếp theo.

Tất cả các importers nhận được chính xác một đối tượng `admin` duy nhất:

```
// 📁 1.js
import {admin} from './admin.js';
admin.name = "Pete";

// 📁 2.js
import {admin} from './admin.js';
alert(admin.name); // Pete

// Cả 1.js và 2.js đều tham chiếu đến cùng đối tượng admin
// Các thay đổi được thực hiện trong 1.js visible trong 2.js
```

Như bạn có thể thấy, khi `1.js` thay đổi property `name` trong `admin` đã import, thì `2.js` có thể thấy `admin.name` mới.

Đó chính xác là vì module được thực thi chỉ một lần. Các exports được tạo, và sau đó chúng được chia sẻ giữa các importers, vì vậy nếu có gì đó thay đổi đối tượng `admin`, các importers khác sẽ thấy điều đó.

**Hành vi như vậy thực sự rất thuận tiện, vì nó cho phép chúng ta *cấu hình* các module.**

Nói cách khác, một module có thể cung cấp một generic functionality cần setup. Ví dụ, authentication cần credentials. Sau đó nó có thể export một configuration object mong đợi mã bên ngoài gán vào nó.

Dưới đây là pattern cổ điển:

1. Một module export một số means của configuration, ví dụ một configuration object.
2. Trong lần import đầu tiên chúng ta khởi tạo nó, ghi vào các properties của nó. Script ứng dụng top-level có thể làm điều đó.
3. Các imports tiếp theo sử dụng module.

Ví dụ, module `admin.js` có thể cung cấp một số functionality (ví dụ authentication), nhưng mong đợi các credentials đến từ object `config` từ bên ngoài:

```
// 📁 admin.js
export let config = { };

export function sayHi() {
  alert(`Sẵn sàng phục vụ, ${config.user}!`);
}
```

Ở đây, `admin.js` export object `config` (ban đầu trống, nhưng cũng có thể có các properties mặc định).

Sau đó trong `init.js`, script đầu tiên của ứng dụng chúng ta, chúng ta import `config` từ nó và đặt `config.user`:

```
// 📁 init.js
import {config} from './admin.js';
config.user = "Pete";
```

…Bây giờ module `admin.js` đã được configure.

Các importers tiếp theo có thể gọi nó, và nó hiển thị đúng user hiện tại:

```
// 📁 another.js
import {sayHi} from './admin.js';

sayHi(); // Sẵn sàng phục vụ, Pete!
```

### [import.meta](#import-meta)

Đối tượng `import.meta` chứa thông tin về module hiện tại.

Nội dung của nó phụ thuộc vào environment. Trong trình duyệt, nó chứa URL của script, hoặc URL trang web hiện tại nếu bên trong HTML:

```
<script type="module">
  alert(import.meta.url); // script URL
  // cho một inline script - URL của trang HTML hiện tại
</script>
```

### [Trong một module, "this" là undefined](#in-a-module-this-is-undefined)

Đó là một feature phụ, nhưng để đầy đủ chúng ta nên đề cập đến nó.

Trong một module, `this` top-level là undefined.

So sánh nó với các script không phải module, nơi `this` là global object:

```
<script>
  alert(this); // window
</script>

<script type="module">
  alert(this); // undefined
</script>
```

## [Tính năng riêng của browser](#browser-specific-features)

Cũng có một số differences browser-specific của các script với `type="module"` so với các script thông thường.

Bạn có thể bỏ qua phần này bây giờ nếu bạn đọc lần đầu, hoặc nếu bạn không sử dụng JavaScript trong một browser.

### [Module scripts được deferred](#module-scripts-are-deferred)

Module scripts luôn *deferred*, cùng hiệu ứng với `defer` attribute (được mô tả trong chương [Scripts: async, defer](/script-async-defer)), cho cả external và inline scripts.

Nói cách khác:

- downloading các external module scripts `<script type="module" src="...">` không block HTML processing, chúng load song song với các tài nguyên khác.
- module scripts chờ cho đến khi HTML document sẵn sàng đầy đủ (ngay cả khi chúng nhỏ và load nhanh hơn HTML), và sau đó chạy.
- thứ tự tương đối của các scripts được duy trì: các scripts đi đầu trong document, execute đầu tiên.

Như một side effect, module scripts luôn "nhìn thấy" trang HTML đã load đầy đủ, bao gồm cả các HTML elements bên dưới chúng.

Ví dụ:

```
<script type="module">
  alert(typeof button); // object: script có thể 'nhìn thấy' button bên dưới
  // vì modules là deferred, script chạy sau khi trang hoàn chỉnh được load
</script>

So sánh với regular script bên dưới:

<script>
  alert(typeof button); // button là undefined, script không thể nhìn thấy các elements bên dưới
  // regular scripts chạy ngay lập tức, trước khi phần còn lại của trang được xử lý
</script>

<button id="button">Button</button>
```

Xin lưu ý: script thứ hai thực sự chạy trước script đầu tiên! Vì vậy chúng ta sẽ thấy `undefined` trước, và sau đó `object`.

Đó là vì modules là deferred, vì vậy chúng ta chờ document được xử lý. Script thông thường chạy ngay lập tức, vì vậy chúng ta thấy output của nó trước.

Khi sử dụng modules, chúng ta nên nhận thức rằng trang HTML xuất hiện khi nó load, và JavaScript modules chạy sau đó, vì vậy user có thể thấy trang trước khi JavaScript application sẵn sàng. Một số functionality có thể không hoạt động noch. Chúng ta nên đặt "loading indicators", hoặc đảm bảo rằng visitor sẽ không bị nhầm lẫn bởi điều đó.

### [Async works trên inline scripts](#async-works-on-inline-scripts)

Đối với non-module scripts, attribute `async` chỉ hoạt động trên các external scripts. Async scripts chạy ngay lập tức khi sẵn sàng, độc lập với các scripts khác hoặc document HTML.

Đối với module scripts, nó hoạt động trên các inline scripts.

Ví dụ, inline script dưới đây có `async`, vì vậy nó không chờ đợi gì.

Nó thực hiện import (fetch `./analytics.js`) và chạy khi sẵn sàng, ngay cả khi document HTML chưa hoàn thành, hoặc nếu các scripts khác vẫn đang pending.

Điều đó tốt cho functionality không phụ thuộc vào bất kỳ thứ gì, như counters, ads, document-level event listeners.

```
<!-- tất cả dependencies được fetch (analytics.js), và script chạy -->
<!-- không chờ document hoặc các thẻ <script> khác -->
<script async type="module">
  import {counter} from './analytics.js';

  counter.count();
</script>
```

### [External scripts](#external-scripts)

Các external scripts có `type="module"` khác biệt ở hai aspects:

1. External scripts với cùng `src` chạy chỉ một lần:

   ```
   <!-- script my.js được fetch và thực thi chỉ một lần -->
   <script type="module" src="my.js"></script>
   <script type="module" src="my.js"></script>
   ```
2. External scripts được fetch từ một origin khác (ví dụ một site khác) yêu cầu [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) headers, như được mô tả trong chương [Fetch: Cross-Origin Requests](/fetch-crossorigin). Nói cách khác, nếu một module script được fetch từ một origin khác, remote server phải cung cấp header `Access-Control-Allow-Origin` cho phép fetch.

   ```
   <!-- another-site.com phải cung cấp Access-Control-Allow-Origin -->
   <!-- nếu không, script sẽ không execute -->
   <script type="module" src="http://another-site.com/their.js"></script>
   ```

   Điều đó đảm bảo security tốt hơn theo mặc định.

### [Không cho phép "bare" modules](#no-bare-modules-allowed)

Trong trình duyệt, `import` phải nhận được một URL tương đối hoặc tuyệt đối. Các modules không có bất kỳ path nào được gọi là "bare" modules. Các modules như vậy không được phép trong `import`.

Ví dụ, `import` này không hợp lệ:

```
import {sayHi} from 'sayHi'; // Error, "bare" module
// module phải có path, ví dụ './sayHi.js' hoặc nơi module đang ở
```

Một số environments, như Node.js hoặc bundle tools cho phép bare modules, không có path nào, vì chúng có cách riêng để tìm modules và hooks để fine-tune chúng. Nhưng browsers chưa hỗ trợ bare modules.

### [Compatibility, "nomodule"](#compatibility-nomodule)

Các trình duyệt cũ không hiểu `type="module"`. Các scripts của một loại không xác định bị bỏ qua. Đối với chúng, có thể cung cấp một fallback bằng cách sử dụng attribute `nomodule`:

```
<script type="module">
  alert("Chạy trong modern browsers");
</script>

<script nomodule>
  alert("Modern browsers biết cả type=module và nomodule, vì vậy bỏ qua cái này")
  alert("Old browsers bỏ qua script với type=module không xác định, nhưng thực thi cái này.");
</script>
```

## [Công cụ build](#build-tools)

Trong thực tế, browser modules hiếm khi được sử dụng ở dạng "raw" của chúng. Thông thường, chúng ta bundle chúng với một công cụ đặc biệt như [Webpack](https://webpack.js.org/) và deploy đến production server.

Một trong những lợi ích của việc sử dụng bundlers – chúng cung cấp nhiều kiểm soát hơn về cách các modules được resolve, cho phép bare modules và nhiều hơn nữa, như CSS/HTML modules.

Build tools làm các điều sau:

1. Nhận một module "main", cái được dự định để đặt trong `<script type="module">` trong HTML.
2. Phân tích dependencies của nó: imports và sau đó imports của imports vân vân.
3. Xây dựng một single file với tất cả modules (hoặc multiple files, có thể tunable), thay thế các cuộc gọi `import` native với các hàm bundler, vì vậy nó hoạt động. Các loại module "đặc biệt" như HTML/CSS modules cũng được hỗ trợ.
4. Trong quá trình, các transformations và optimizations khác có thể được áp dụng:
   - Unreachable code bị xóa.
   - Unused exports bị xóa ("tree-shaking").
   - Development-specific statements như `console` và `debugger` bị xóa.
   - Modern, bleeding-edge JavaScript syntax có thể được transform sang old one với similar functionality bằng cách sử dụng [Babel](https://babeljs.io/).
   - File kết quả được minified (spaces bị xóa, variables được thay thế bằng các tên ngắn hơn, vân vân).

Nếu chúng ta sử dụng bundle tools, thì vì scripts được bundle together vào một single file (hoặc vài files), các statement `import/export` bên trong những scripts đó được thay thế bởi các hàm bundler đặc biệt. Vì vậy script "bundled" kết quả không chứa bất kỳ `import/export` nào, nó không yêu cầu `type="module"`, và chúng ta có thể đặt nó vào một regular script:

```
<!-- Giả sử chúng ta đã nhận bundle.js từ một công cụ như Webpack -->
<script src="bundle.js"></script>
```

Tuy nhiên, native modules cũng có thể sử dụng được. Vì vậy chúng ta sẽ không sử dụng Webpack ở đây: bạn có thể cấu hình nó sau này.

## [Tóm tắt](#summary)

Để tóm tắt, các concepts core là:

1. Một module là một file. Để làm cho `import/export` hoạt động, browsers cần `<script type="module">`. Modules có một số differences:
   - Deferred theo mặc định.
   - Async works trên inline scripts.
   - Để tải external scripts từ một origin khác (domain/protocol/port), CORS headers là cần thiết.
   - Duplicate external scripts bị bỏ qua.
2. Modules có scope top-level local riêng và trao đổi functionality qua `import/export`.
3. Modules luôn `use strict`.
4. Mã module được thực thi chỉ một lần. Các exports được tạo một lần và được chia sẻ giữa các importers.

Khi chúng ta sử dụng modules, mỗi module implement functionality và export nó. Sau đó chúng ta sử dụng `import` để trực tiếp import nó nơi nó cần. Trình duyệt load và evaluate các scripts tự động.

Trong production, mọi người thường sử dụng các bundlers như [Webpack](https://webpack.js.org) để bundle các modules together vì performance và các lý do khác.

Ở chương tiếp theo chúng ta sẽ xem thêm các ví dụ về modules, và làm thế nào các thứ có thể được export/import.
