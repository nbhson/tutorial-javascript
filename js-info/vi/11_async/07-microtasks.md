# Microtasks

> Nguồn: [https://javascript.info/microtask-queue](https://javascript.info/microtask-queue)

<!-- fetched: 2026-09-14 -->

Promise handlers `.then`/`.catch`/`.finally` luôn là asynchronous.

Ngay cả khi một Promise được resolved ngay lập tức, mã ở các dòng *bên dưới* `.then`/`.catch`/`.finally` sẽ vẫn chạy trước các handlers này.

Dưới đây là một demo:

```
let promise = Promise.resolve();

promise.then(() => alert("promise done!"));

alert("code finished"); // alert này hiển thị đầu tiên
```

Nếu bạn chạy nó, bạn thấy `code finished` trước, và sau đó `promise done!`.

Điều đó kỳ lạ, vì promise chắc chắn đã done từ đầu.

Tại sao `.then` lại kích hoạt sau đó? Có gì đang xảy ra?

## [Microtasks queue](#microtasks-queue)

Các task không đồng bộ cần quản lý đúng cách. Để làm điều đó, tiêu chuẩn ECMA quy định một hàng đợi nội bộ `PromiseJobs`, thường được gọi là "microtask queue" (thuật ngữ V8).

Như đã nêu trong [specification](https://tc39.github.io/ecma262/#sec-jobs-and-job-queues):

- Hàng đợi là first-in-first-out: các task được enqueue đầu tiên được chạy đầu tiên.
- Execution của một task chỉ được khởi tạo khi không có gì khác đang chạy.

Hoặc, nói một cách đơn giản hơn, khi một promise sẵn sàng, các handler `.then/catch/finally` của nó được đưa vào hàng đợi; chúng chưa được thực thi. Khi engine JavaScript trở nên rảnh từ mã hiện tại, nó lấy một task từ hàng đợi và thực thi nó.

Đó là lý do tại sao "code finished" trong ví dụ ở trên hiển thị đầu tiên.

![](/article/microtask-queue/promiseQueue.svg)

Promise handlers luôn đi qua hàng đợi nội bộ này.

Nếu có một chuỗi với nhiều `.then/catch/finally`, thì mỗi một trong số chúng được thực thi một cách asynchronous. Tức là, trước tiên nó được enqueue, sau đó được thực thi khi mã hiện tại hoàn tất và các handler đã được enqueue trước đó finishes.

**Điều gì nếu thứ tự quan trọng đối với chúng ta? Làm thế nào để chúng ta làm cho `code finished` xuất hiện sau `promise done`?**

Dễ dàng, chỉ cần đặt nó vào hàng đợi với `.then`:

```
Promise.resolve()
  .then(() => alert("promise done!"))
  .then(() => alert("code finished"));
```

Bây giờ thứ tự là như dự định.

## [Unhandled rejection](#unhandled-rejection)

Nhớ sự kiện `unhandledrejection` từ bài viết [Xử lý lỗi với promises](/promise-error-handling)?

Bây giờ chúng ta có thể thấy chính xác cách JavaScript tìm ra rằng có một unhandled rejection.

**Một "unhandled rejection" xảy ra khi lỗi promise không được xử lý ở cuối microtask queue.**

Thông thường, nếu chúng ta mong đợi một lỗi, chúng ta thêm `.catch` vào chuỗi promise để xử lý nó:

```
let promise = Promise.reject(new Error("Promise Failed!"));
promise.catch(err => alert('caught'));

// không chạy: lỗi đã được xử lý
window.addEventListener('unhandledrejection', event => alert(event.reason));
```

Nhưng nếu chúng ta quên thêm `.catch`, thì, sau khi microtask queue trống, engine kích hoạt sự kiện:

```
let promise = Promise.reject(new Error("Promise Failed!"));

// Promise Failed!
window.addEventListener('unhandledrejection', event => alert(event.reason));
```

Điều gì xảy ra nếu chúng ta xử lý lỗi sau đó? Như thế này:

```
let promise = Promise.reject(new Error("Promise Failed!"));
setTimeout(() => promise.catch(err => alert('caught')), 1000);

// Error: Promise Failed!
window.addEventListener('unhandledrejection', event => alert(event.reason));
```

Bây giờ, nếu chúng ta chạy nó, chúng ta sẽ thấy `Promise Failed!` trước và sau đó `caught`.

Nếu chúng ta không biết về microtasks queue, chúng ta có thể thắc mắc: "Tại sao handler `unhandledrejection` chạy? Chúng ta đã catch và xử lý lỗi rồi!"

Nhưng bây giờ chúng ta hiểu rằng `unhandledrejection` được tạo ra khi microtask queue hoàn tất: engine kiểm tra các promise và, nếu bất kỳ promise nào trong trạng thái "rejected", thì sự kiện kích hoạt.

Trong ví dụ ở trên, `.catch` được thêm bởi `setTimeout` cũng kích hoạt. Nhưng nó làm vậy sau đó, sau khi `unhandledrejection` đã xảy ra, vì vậy nó không thay đổi gì.

## [Tóm tắt](#summary)

Xử lý promise luôn là asynchronous, vì tất cả các hành động promise đi qua hàng đợi "promise jobs" nội bộ, còn được gọi là "microtask queue" (thuật ngữ V8).

Vì vậy các handler `.then/catch/finally` luôn được gọi sau khi mã hiện tại kết thúc.

Nếu chúng ta cần đảm bảo rằng một đoạn mã được thực thi sau `.then/catch/finally`, chúng ta có thể thêm nó vào một cuộc gọi `.then` chained.

Trong hầu hết các engine Javascript, bao gồm cả trình duyệt và Node.js, khái niệm microtasks gắn liền chặt chẽ với "event loop" và "macrotasks". Vì chúng không có mối quan hệ trực tiếp với promises, chúng được đề cập trong một phần khác của hướng dẫn, trong bài viết [Event loop: microtasks và macrotasks](/event-loop).
