# Promise

> Nguồn: [https://javascript.info/promise-basics](https://javascript.info/promise-basics)

<!-- fetched: 2026-09-14 -->

Hãy tưởng tượng bạn là một ca sĩ hàng đầu, và người hâm mộ hỏi ngày đêm về bài hát mới nhất của bạn.

Để giải quyết vấn đề, bạn hứa sẽ gửi nó cho họ khi nó được phát hành. Bạn đưa cho người hâm mộ của mình một danh sách. Họ có thể điền địa chỉ email của họ, vì vậy khi bài hát có sẵn, tất cả các bên đăng ký sẽ nhận được nó ngay lập tức. Và thậm chí nếu có gì đó đi rất sai, ví dụ, một đám cháy trong phòng thu, vì vậy bạn không thể phát hành bài hát, họ vẫn sẽ được thông báo.

Mọi người đều vui vẻ: bạn, vì mọi người không quấy rầy bạn nữa, và người hâm mộ, vì họ sẽ không bỏ lỡ bài hát.

Đây là một phép ẩn dụ thực tế cho những điều chúng ta thường gặp trong lập trình:

1. "Mã sản xuất" (producing code) thực hiện một việc gì đó và mất thời gian. Ví dụ, một số mã tải dữ liệu qua mạng. Đó là "ca sĩ".
2. "Mã tiêu thụ" (consuming code) muốn có kết quả của "mã sản xuất" một khi nó sẵn sàng. Nhiều hàm có thể cần kết quả đó. Đây là "người hâm mộ".
3. *promise* là một đối tượng JavaScript đặc biệt kết nối "mã sản xuất" và "mã tiêu thụ" với nhau. Theo phép ẩn dụ của chúng ta: đây là "danh sách đăng ký". "Mã sản xuất" mất bất kỳ thời gian nào nó cần để tạo ra kết quả hứa hẹn, và "promise" làm cho kết quả đó có sẵn cho tất cả mã đăng ký khi nó sẵn sàng.

Phép ẩn dụ không chính xác một cách tuyệt vời, bởi vì promises JavaScript phức tạp hơn một danh sách đăng ký đơn giản: chúng có các tính năng và hạn chế bổ sung. Nhưng nó cũng ổn để bắt đầu.

Cú pháp khởi tạo cho một đối tượng promise là:

```
let promise = new Promise(function(resolve, reject) {
  // executor (mã sản xuất, "ca sĩ")
});
```

Hàm được truyền vào `new Promise` được gọi là *executor* (bộ thực thi). Khi `new Promise` được tạo, executor chạy tự động. Nó chứa mã sản xuất sẽ cuối cùng tạo ra kết quả. Theo phép ẩn dụ ở trên: executor là "ca sĩ".

Các đối số của nó `resolve` và `reject` là các callback được cung cấp bởi chính JavaScript. Mã của chúng ta chỉ ở bên trong executor.

Khi executor lấy được kết quả, sớm hay muộn cũng không quan trọng, nó nên gọi một trong các callback này:

- `resolve(value)` — nếu công việc hoàn tất thành công, với kết quả `value`.
- `reject(error)` — nếu có lỗi xảy ra, `error` là đối tượng lỗi.

Vì vậy, để tóm tắt: executor chạy tự động và cố gắng thực hiện công việc. Khi nó hoàn thành với nỗ lực, nó gọi `resolve` nếu nó thành công hoặc `reject` nếu có lỗi.

Đối tượng `promise` được trả về bởi constructor `new Promise` có các thuộc tính nội bộ sau:

- `state` — ban đầu là `"pending"`, sau đó chuyển sang `"fulfilled"` khi `resolve` được gọi hoặc `"rejected"` khi `reject` được gọi.
- `result` — ban đầu là `undefined`, sau đó chuyển sang `value` khi `resolve(value)` được gọi hoặc `error` khi `reject(error)` được gọi.

Vì vậy, executor cuối cùng di chuyển `promise` sang một trong các trạng thái sau:

![](/article/promise-basics/promise-resolve-reject.svg)

Sau đó chúng ta sẽ thấy làm thế nào "người hâm mộ" có thể đăng ký (subscribe) để theo dõi những thay đổi này.

Dưới đây là một ví dụ về constructor promise và một hàm executor đơn giản với "mã sản xuất" mất thời gian (thông qua `setTimeout`):

```
let promise = new Promise(function(resolve, reject) {
  // hàm được thực thi tự động ngay lập tức khi promise được khởi tạo

  // sau 1 giây báo hiệu rằng công việc đã hoàn thành với kết quả "done"
  setTimeout(() => resolve("done"), 1000);
});
```

Chúng ta có thể thấy hai điều bằng cách chạy mã ở trên:

1. Executor được gọi tự động và ngay lập tức (bởi `new Promise`).
2. Executor nhận được hai đối số: `resolve` và `reject`. Các hàm này được định nghĩa trước bởi engine JavaScript, vì vậy chúng ta không cần phải tạo ra chúng. Chúng ta chỉ nên gọi một trong số chúng khi sẵn sàng.

   Sau một giây "xử lý", executor gọi `resolve("done")` để tạo ra kết quả. Điều này thay đổi trạng thái của đối tượng `promise`:

   ![](/article/promise-basics/promise-resolve-1.svg)

Đó là một ví dụ về hoàn thành công việc thành công, một "promise đã được fulfill" (fulfilled promise).

Và đây là một ví dụ về executor từ chối promise với một lỗi:

```
let promise = new Promise(function(resolve, reject) {
  // sau 1 giây báo hiệu rằng công việc đã hoàn thành với lỗi
  setTimeout(() => reject(new Error("Whoops!")), 1000);
});
```

Lệnh gọi `reject(...)` di chuyển đối tượng promise sang trạng thái `"rejected"`:

![](/article/promise-basics/promise-reject-1.svg)

Để tóm tắt, executor nên thực hiện công việc (thường là gì đó mất thời gian) và sau đó gọi `resolve` hoặc `reject` để thay đổi trạng thái của đối tượng promise tương ứng.

Một promise đã được resolved hoặc rejected được gọi là "settled", khác với promise ban đầu là "pending".

Chỉ có thể có một kết quả hoặc một lỗi

Executor nên gọi duy nhất một `resolve` hoặc một `reject`. Mọi thay đổi trạng thái là cuối cùng.

Tất cả các lệnh gọi tiếp theo của `resolve` và `reject` đều bị bỏ qua:

```
let promise = new Promise(function(resolve, reject) {
  resolve("done");

  reject(new Error("…")); // bị bỏ qua
  setTimeout(() => resolve("…")); // bị bỏ qua
});
```

Ý tưởng là công việc được thực hiện bởi executor chỉ có thể có một kết quả hoặc một lỗi.

Ngoài ra, `resolve`/`reject` chỉ mong đợi một đối số (hoặc không có) và sẽ bỏ qua các đối số bổ sung.

Từ chối với đối tượng Error

Trong trường hợp có gì đó đi sai, executor nên gọi `reject`. Điều đó có thể được thực hiện với bất kỳ loại đối số nào (giống như `resolve`). Nhưng được khuyến nghị sử dụng các đối tượng `Error` (hoặc các đối tượng thừa kế từ `Error`). Lý do cho điều đó sẽ sớm trở nên rõ ràng.

Gọi ngay lập tức `resolve`/`reject`

Trong thực tế, executor thường làm gì đó không đồng bộ và gọi `resolve`/`reject` sau một khoảng thời gian, nhưng nó không bắt buộc. Chúng ta cũng có thể gọi `resolve` hoặc `reject` ngay lập tức, như thế này:

```
let promise = new Promise(function(resolve, reject) {
  // không mất thời gian để làm công việc
  resolve(123); // ngay lập tức đưa ra kết quả: 123
});
```

Ví dụ, điều đó có thể xảy ra khi chúng ta bắt đầu làm một công việc nhưng sau đó thấy rằng mọi thứ đã được hoàn thành và lưu trong cache.

Điều đó hoàn toàn ổn. Chúng ta ngay lập tức có một promise đã được resolve.

`state` và `result` là nội bộ

Các thuộc tính `state` và `result` của đối tượng Promise là nội bộ. Chúng ta không thể truy cập trực tiếp chúng. Chúng ta có thể sử dụng các phương thức `.then`/`.catch`/`.finally` cho điều đó. Chúng được mô tả bên dưới.

## [Consumers: then, catch](#consumers-then-catch)

Một Promise object phục vụ như một liên kết giữa executor (mã "sản xuất" hoặc "ca sĩ") và các hàm tiêu thụ (các "người hâm mộ"), những người sẽ nhận được kết quả hoặc lỗi. Các hàm tiêu thụ có thể được đăng ký (subscribe) bằng cách sử dụng các phương thức `.then` và `.catch`.

### [then](#then)

Quan trọng nhất, cơ bản nhất là `.then`.

Cú pháp là:

```
promise.then(
  function(result) { /* xử lý kết quả thành công */ },
  function(error) { /* xử lý lỗi */ }
);
```

Đối số thứ nhất của `.then` là một hàm chạy khi promise được resolved và nhận kết quả.

Đối số thứ hai của `.then` là một hàm chạy khi promise bị rejected và nhận lỗi.

Ví dụ, đây là phản ứng đối với một promise được resolved thành công:

```
let promise = new Promise(function(resolve, reject) {
  setTimeout(() => resolve("done!"), 1000);
});

// resolve chạy hàm đầu tiên trong .then
promise.then(
  result => alert(result), // hiển thị "done!" sau 1 giây
  error => alert(error) // không chạy
);
```

Hàm đầu tiên đã được thực thi.

Và trong trường hợp rejection, hàm thứ hai:

```
let promise = new Promise(function(resolve, reject) {
  setTimeout(() => reject(new Error("Whoops!")), 1000);
});

// reject chạy hàm thứ hai trong .then
promise.then(
  result => alert(result), // không chạy
  error => alert(error) // hiển thị "Error: Whoops!" sau 1 giây
);
```

Nếu chúng ta chỉ quan tâm đến các hoàn thành thành công, thì chúng ta có thể chỉ cung cấp một đối số hàm cho `.then`:

```
let promise = new Promise(resolve => {
  setTimeout(() => resolve("done!"), 1000);
});

promise.then(alert); // hiển thị "done!" sau 1 giây
```

### [catch](#catch)

Nếu chúng ta chỉ quan tâm đến lỗi, thì chúng ta có thể sử dụng `null` làm đối số thứ nhất: `.then(null, errorHandlingFunction)`. Hoặc chúng ta có thể sử dụng `.catch(errorHandlingFunction)`, điều đó giống hệt nhau:

```
let promise = new Promise((resolve, reject) => {
  setTimeout(() => reject(new Error("Whoops!")), 1000);
});

// .catch(f) giống như promise.then(null, f)
promise.catch(alert); // hiển thị "Error: Whoops!" sau 1 giây
```

Lệnh gọi `.catch(f)` là một bản sao hoàn chỉnh của `.then(null, f)`, nó chỉ là một cách viết tắt.

## [Cleanup: finally](#cleanup-finally)

Giống như có một mệnh đề `finally` trong `try {...} catch {...}` thông thường, cũng có `finally` trong promises.

Lệnh gọi `.finally(f)` giống với `.then(f, f)` theo nghĩa là `f` chạy luôn, khi promise đã settled: будь it resolve hay reject.

Ý tưởng của `finally` là thiết lập một handler để thực hiện cleanup/kết thúc sau khi các hoạt động trước đó hoàn tất.

Ví dụ: dừng các chỉ báo tải, đóng các kết nối không còn cần thiết, v.v.

Hãy nghĩ về nó như một người kết thúc bữa tiệc. Bất kể bữa tiệc có tốt hay xấu, có bao nhiêu bạn bè tham gia, chúng ta vẫn cần (hoặc ít nhất nên) làm dọn dẹp sau đó.

Mã có thể trông như thế này:

```
new Promise((resolve, reject) => {
  /* làm gì đó mất thời gian, và sau đó gọi resolve hoặc reject */
})
  // chạy khi promise đã settled, bất kể thành công hay không
  .finally(() => stop loading indicator)
  // vì vậy chỉ báo tải luôn bị dừng trước khi chúng ta tiếp tục
  .then(result => show result, err => show error)
```

Xin lưu ý rằng `finally(f)` không chính xác là alias của `then(f,f)`.

Có những khác biệt quan trọng:

1. Một `finally` handler không có đối số. Trong `finally` chúng ta không biết liệu promise có thành công hay không. Điều đó ổn, vì nhiệm vụ của chúng ta thường là thực hiện các thủ tục kết thúc "chung chung".

   Xin hãy xem ví dụ ở trên: như bạn có thể thấy, `finally` handler không có đối số, và kết quả của promise được xử lý bởi handler tiếp theo.
2. Một `finally` handler "truyền qua" kết quả hoặc lỗi đến handler phù hợp tiếp theo.

   Ví dụ, ở đây kết quả được truyền qua `finally` đến `then`:

   ```
   new Promise((resolve, reject) => {
     setTimeout(() => resolve("value"), 2000);
   })
     .finally(() => alert("Promise ready")) // kích hoạt đầu tiên
     .then(result => alert(result)); // <-- .then hiển thị "value"
   ```

   Như bạn có thể thấy, `value` được trả về bởi promise đầu tiên được truyền qua `finally` đến `then` tiếp theo.

   Điều đó rất thuận tiện, vì `finally` không có nghĩa là xử lý kết quả promise. Như đã nói, đó là nơi để làm dọn dẹp chung, bất kể kết quả là gì.

   Và đây là một ví dụ về lỗi, để chúng ta xem làm thế nào nó được truyền qua `finally` đến `catch`:

   ```
   new Promise((resolve, reject) => {
     throw new Error("error");
   })
     .finally(() => alert("Promise ready")) // kích hoạt đầu tiên
     .catch(err => alert(err));  // <-- .catch hiển thị lỗi
   ```
3. Một `finally` handler cũng không nên trả về bất cứ điều gì. Nếu nó làm vậy, giá trị trả về sẽ bị bỏ qua.

   Ngoại lệ duy nhất đối với quy tắc này là khi một `finally` handler ném ra lỗi. Sau đó lỗi này đi đến handler tiếp theo, thay vì bất kỳ kết quả trước đó nào.

Để tóm tắt:

- Một `finally` handler không nhận được kết quả của handler trước (nó không có đối số). Kết quả đó được truyền qua thay thế, đến handler phù hợp tiếp theo.
- Nếu một `finally` handler trả về thứ gì đó, nó bị bỏ qua.
- Khi `finally` ném lỗi, thì execution đi đến handler lỗi gần nhất.

Các tính năng này hữu ích và làm cho mọi thứ hoạt động đúng cách nếu chúng ta sử dụng `finally` như cách nó được dự định sử dụng: cho các thủ tục dọn dẹp chung.

Chúng ta có thể gắn handlers vào các promise đã settled

Nếu một promise đang pending, các handler `.then/catch/finally` sẽ chờ kết quả của nó.

Đôi khi, có thể là một promise đã được settled khi chúng ta thêm handler vào nó.

Trong trường hợp đó, các handler này chỉ chạy ngay lập tức:

```
// promise trở nên resolved ngay lập tức khi được khởi tạo
let promise = new Promise(resolve => resolve("done!"));

promise.then(alert); // done! (hiển thị ngay bây giờ)
```

Lưu ý rằng điều này làm cho promises mạnh mẽ hơn kịch bản "danh sách đăng ký" trong thực tế. Nếu ca sĩ đã phát hành bài hát của họ và sau đó một người đăng ký danh sách đăng ký, họ có thể sẽ không nhận được bài hát đó. Đăng ký trong cuộc sống thực phải được thực hiện trước sự kiện.

Promises linh hoạt hơn. Chúng ta có thể thêm handlers bất cứ lúc nào: nếu kết quả đã có sẵn, chúng chỉ thực thi.

## [Ví dụ: loadScript](#loadscript)

Tiếp theo, hãy xem các ví dụ thực tiễn hơn về cách promises có thể giúp chúng ta viết mã không đồng bộ.

Chúng ta có hàm `loadScript` để tải script từ chương trước.

Dưới đây là biến thể dựa trên callback, chỉ để nhắc nhở chúng ta về nó:

```
function loadScript(src, callback) {
  let script = document.createElement('script');
  script.src = src;

  script.onload = () => callback(null, script);
  script.onerror = () => callback(new Error(`Lỗi tải script cho ${src}`));

  document.head.append(script);
}
```

Hãy viết lại nó bằng cách sử dụng Promises.

Hàm mới `loadScript` sẽ không yêu cầu callback. Thay vào đó, nó sẽ tạo và trả về một đối tượng Promise được resolve khi việc tải hoàn tất. Mã bên ngoài có thể thêm handlers (các hàm subscribe) vào nó bằng cách sử dụng `.then`:

```
function loadScript(src) {
  return new Promise(function(resolve, reject) {
    let script = document.createElement('script');
    script.src = src;

    script.onload = () => resolve(script);
    script.onerror = () => reject(new Error(`Lỗi tải script cho ${src}`));

    document.head.append(script);
  });
}
```

Cách sử dụng:

```
let promise = loadScript("https://cdnjs.cloudflare.com/ajax/libs/lodash.js/4.17.11/lodash.js");

promise.then(
  script => alert(`${script.src} đã được tải!`),
  error => alert(`Lỗi: ${error.message}`)
);

promise.then(script => alert('Another handler...'));
```

Chúng ta có thể ngay lập tức thấy một vài lợi ích so với mẫu dựa trên callback:

| Promises | Callbacks |
| --- | --- |
| Promises cho phép chúng ta làm mọi việc theo thứ tự tự nhiên. Đầu tiên, chạy `loadScript(script)`, sau đó `.then` viết những gì cần làm với kết quả. | Chúng ta phải có một hàm `callback` sẵn có khi gọi `loadScript(script, callback)`. Nói cách khác, chúng ta phải biết những gì cần làm với kết quả *trước khi* `loadScript` được gọi. |
| Chúng ta có thể gọi `.then` trên một Promise bao nhiêu lần tùy thích. Mỗi lần, chúng ta thêm một "người hâm mộ" mới, một hàm subscribe mới, vào "danh sách đăng ký". Thêm về điều này ở chương tiếp theo: [Promises chaining](/promise-chaining). | Chỉ có thể có một callback. |

Vì vậy, promises mang lại luồng mã và sự linh hoạt tốt hơn. Nhưng còn có nhiều hơn nữa. Chúng ta sẽ thấy điều đó ở các chương tiếp theo.

---

---

## Bài tập

## [Các bài tập](#tasks)

### [Re-resolve a promise?](#re-resolve-a-promise)

Đầu ra của mã dưới đây là gì?

```
let promise = new Promise(function(resolve, reject) {
  resolve(1);

  setTimeout(() => resolve(2), 1000);
});

promise.then(alert);
```

lời giải

Đầu ra là: `1`.

Lệnh gọi thứ hai đến `resolve` bị bỏ qua, vì chỉ lệnh gọi đầu tiên của `reject/resolve` được tính đến. Các lệnh gọi tiếp theo bị bỏ qua.

### [Delay với promise](#delay-with-a-promise)

Hàm tích hợp `setTimeout` sử dụng callbacks. Tạo một phiên bản dựa trên promise.

Hàm `delay(ms)` nên trả về một promise. Promise đó nên resolve sau `ms` milliseconds, vì vậy chúng ta có thể thêm `.then` vào nó, như thế này:

```
function delay(ms) {
  // mã của bạn
}

delay(3000).then(() => alert('chạy sau 3 giây'));
```

lời giải

```
function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

delay(3000).then(() => alert('chạy sau 3 giây'));
```

Xin lưu ý rằng trong bài tập này `resolve` được gọi mà không có đối số. Chúng ta không trả về bất kỳ giá trị nào từ `delay`, chỉ đảm bảo độ trễ.

### [Animated circle với promise](#animated-circle-with-promise)

Viết lại hàm `showCircle` trong lời giải của bài tập [Animated circle với callback](/task/animate-circle-callback) sao cho nó trả về một promise thay vì chấp nhận một callback.

Cách sử dụng mới:

```
showCircle(150, 150, 100).then(div => {
  div.classList.add('message-ball');
  div.append("Hello, world!");
});
```

Lấy lời giải của bài tập [Animated circle với callback](/task/animate-circle-callback) làm nền tảng.

lời giải

[Mở lời giải trong sandbox.](https://plnkr.co/edit/OowYulxp2BjbQnEj?p=preview)
