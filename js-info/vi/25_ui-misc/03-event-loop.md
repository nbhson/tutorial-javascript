# Vòng lặp sự kiện (Event loop): microtasks và macrotasks

> Source: [https://javascript.info/event-loop](https://javascript.info/event-loop)

<!-- fetched: 2026-09-14 -->

Luồng execution JavaScript trong browser, cũng như trong Node.js, dựa trên *event loop*.

Hiểu cách event loop hoạt động quan trọng cho optimizations, và đôi khi cho kiến trúc đúng.

Trong chương này chúng ta trước tiên cover các chi tiết lý thuyết về cách các thứ hoạt động, và sau đó xem các applications thực tế của kiến thức đó.

## [Event Loop](#event-loop)

Khái niệm *event loop* rất đơn giản. Có một vòng lặp vô tận, nơi JavaScript engine chờ các tasks, thực thi chúng và sau đó ngủ, chờ thêm tasks.

Algorithm chung của engine:

1. Trong khi có tasks:
   - thực thi chúng, bắt đầu với task cũ nhất.
2. Ngủ cho đến khi một task xuất hiện, sau đó quay lại 1.

Đó là sự formalization của những gì chúng ta thấy khi browsing một trang. JavaScript engine không làm gì hầu hết thời gian, nó chỉ chạy nếu một script/handler/sự kiện kích hoạt.

Ví dụ về tasks:

- Khi external script `<script src="...">` tải, task là thực thi nó.
- Khi người dùng di chuyển chuột, task là dispatch sự kiện `mousemove` và thực thi các handlers.
- Khi thời gian đến cho một scheduled `setTimeout`, task là chạy callback của nó.
- …và tương tự.

Tasks được thiết lập – engine xử lý chúng – sau đó chờ thêm tasks (trong khi ngủ và tiêu thụ gần như bằng 0 CPU).

Có thể xảy ra rằng một task đến trong khi engine đang bận, sau đó nó được enqueue.

Các tasks tạo thành một queue, cái gọi là "macrotask queue" ([v8](https://v8.dev/) term):

![](/article/event-loop/eventLoop.svg)

Ví dụ, trong khi engine đang bận thực thi `script`, người dùng có thể di chuyển chuột gây ra `mousemove`, và `setTimeout` có thể đã đến hạn và tương tự, các tasks này tạo thành queue, như minh họa trong hình trên.

Các tasks từ queue được xử lý theo nguyên tắc "first come – first served". Khi engine browser xong với `script`, nó xử lý sự kiện `mousemove`, sau đó handler `setTimeout`, và tương tự.

Cho đến giờ khá đơn giản, phải không?

Hai chi tiết nữa:

1. Rendering không bao giờ xảy ra trong khi engine đang thực thi một task. Không quan trọng task đó có dài hay không. Các thay đổi đến DOM được paint chỉ sau khi task hoàn tất.
2. Nếu một task kéo dài quá lâu, browser không thể làm các tasks khác, như xử lý user events. Vậy sau một khoảng thời gian, nó raises một alert giống như "Trang không phản hồi", gợi ý giết task với toàn bộ trang. Điều đó xảy ra khi có nhiều calculations phức tạp hoặc một programming error dẫn đến infinite loop.

Đó là lý thuyết. Giờ hãy xem chúng ta có thể apply kiến thức đó như thế nào.

## [Use-case 1: chia nhỏ các task nặng CPU](#use-case-1-splitting-cpu-hungry-tasks)

Giả sử chúng ta có một task nặng CPU.

Ví dụ, syntax-highlighting (được dùng để colorize code examples trên trang này) khá nặng CPU. Để highlight code, nó thực hiện analysis, tạo nhiều elements có màu sắc, thêm chúng vào document – đối với một lượng lớn text điều đó mất nhiều thời gian.

Trong khi engine đang bận với syntax highlighting, nó không thể làm các việc liên quan đến DOM khác, xử lý user events, v.v. Nó thậm chí có thể gây cho browser "hiccup" hoặc thậm chí "treo" trong một chút, điều không thể chấp nhận được.

Chúng ta có thể tránh các vấn đề bằng cách chia task lớn thành các pieces. Highlight 100 dòng đầu tiên, sau đó schedule `setTimeout` (với zero-delay) cho 100 dòng tiếp theo, và tương tự.

Để demo approach này, vì mục đích đơn giản, thay vì text-highlighting, hãy lấy một hàm đếm từ `1` đến `1000000000`.

Nếu bạn chạy code bên dưới, engine sẽ "treo" trong một thời gian. Đối với server-side JS điều đó dễ nhận thấy, và nếu bạn đang chạy nó trong-browser, thì hãy thử click vào các buttons khác trên trang – bạn sẽ thấy rằng không có events nào khác được xử lý cho đến khi counting finishes.

```
let i = 0;

let start = Date.now();

function count() {

  // làm một công việc nặng
  for (let j = 0; j < 1e9; j++) {
    i++;
  }

  alert("Xong trong " + (Date.now() - start) + 'ms');
}

count();
```

Browser thậm chí có thể hiển thị cảnh báo "script mất quá lâu".

Hãy chia nhỏ job bằng cách dùng nested `setTimeout` calls:

```
let i = 0;

let start = Date.now();

function count() {

  // làm một phần của công việc nặng (*)
  do {
    i++;
  } while (i % 1e6 != 0);

  if (i == 1e9) {
    alert("Xong trong " + (Date.now() - start) + 'ms');
  } else {
    setTimeout(count); // schedule call mới (**)
  }

}

count();
```

Giờ giao diện browser hoàn toàn hoạt động trong suốt quá trình "counting".

Một lần chạy `count` làm một phần của job `(*)`, và sau đó re-schedule chính nó `(**)` nếu cần:

1. Lần chạy đầu tiên đếm: `i=1...1000000`.
2. Lần chạy thứ hai đếm: `i=1000001..2000000`.
3. …và tương tự.

Giờ, nếu một side task mới (ví dụ sự kiện `onclick`) xuất hiện trong khi engine đang bận thực thi part 1, nó được queue và sau đó thực thi khi part 1 kết thúc, trước part tiếp theo. Việc quay lại event loop định kỳ giữa các executions `count` cung cấp đủ "không khí" cho JavaScript engine để làm việc khác, để phản hồi với các actions khác của user.

Điều đáng chú ý là cả hai variants – với và không có việc chia job bằng `setTimeout` – có speed tương đương. Không có nhiều khác biệt trong overall counting time.

Để làm chúng gần hơn, hãy cải tiến.

Chúng ta sẽ di chuyển scheduling về đầu `count()`:

```
let i = 0;

let start = Date.now();

function count() {

  // di chuyển scheduling về đầu
  if (i < 1e9 - 1e6) {
    setTimeout(count); // schedule call mới
  }

  do {
    i++;
  } while (i % 1e6 != 0);

  if (i == 1e9) {
    alert("Xong trong " + (Date.now() - start) + 'ms');
  }

}

count();
```

Giờ khi chúng ta bắt đầu `count()` và thấy rằng chúng ta sẽ cần `count()` thêm, chúng ta schedule nó ngay lập tức, trước khi làm job.

Nếu bạn chạy nó, dễ nhận thấy rằng nó mất ít thời gian hơn đáng kể.

Tại sao?

Đơn giản là: như bạn nhớ, có minimal delay 4ms trong-browser cho nhiều nested `setTimeout` calls. Ngay cả khi chúng ta đặt `0`, nó là `4ms` (hoặc hơi nhiều hơn). Vậy càng schedule sớm – càng chạy nhanh.

Cuối cùng, chúng ta đã chia một task nặng CPU thành các phần – giờ nó không block user interface. Và overall execution time của nó không dài hơn nhiều.

## [Use case 2: hiển thị progress](#use-case-2-progress-indication)

Lợi ích khác của việc chia nhỏ các tasks nặng cho browser scripts là chúng ta có thể hiển thị progress indication.

Như đã đề cập earlier, các thay đổi đến DOM được paint chỉ sau khi task đang chạy hiện tại hoàn tất, bất kể nó kéo dài bao lâu.

Mặt khác, điều đó thật tuyệt, vì hàm của chúng ta có thể tạo nhiều elements, thêm chúng từng cái một vào document và thay đổi styles của chúng – người truy cập sẽ không thấy bất kỳ trạng thái "intermediate", chưa hoàn thành nào. Một điều quan trọng, phải không?

Đây là demo, các thay đổi đến `i` sẽ không hiển thị cho đến khi hàm kết thúc, vậy chúng ta sẽ chỉ thấy giá trị cuối cùng:

```
<div id="progress"></div>

<script>

  function count() {
    for (let i = 0; i < 1e6; i++) {
      i++;
      progress.innerHTML = i;
    }
  }

  count();
</script>
```

…Nhưng chúng ta cũng có thể muốn hiển thị thứ gì đó trong quá trình task, ví dụ một progress bar.

Nếu chúng ta chia task nặng thành các pieces bằng `setTimeout`, thì các thay đổi được paint ra giữa chúng.

Điều này đẹp hơn:

```
<div id="progress"></div>

<script>
  let i = 0;

  function count() {

    // làm một phần của công việc nặng (*)
    do {
      i++;
      progress.innerHTML = i;
    } while (i % 1e3 != 0);

    if (i < 1e7) {
      setTimeout(count);
    }

  }

  count();
</script>
```

Giờ `<div>` hiển thị các giá trị tăng dần của `i`, một kind của progress bar.

## [Use case 3: làm gì đó sau event](#use-case-3-doing-something-after-the-event)

Trong một handler event chúng ta có thể quyết định postpone một số actions cho đến khi event đã bubbled up và được handle trên tất cả các levels. Chúng ta có thể làm điều đó bằng cách wrap code trong zero delay `setTimeout`.

Trong chương [Dispatching custom events](/dispatch-events) chúng ta đã thấy một example: custom event `menu-open` được dispatch trong `setTimeout`, vậy nó xảy ra sau khi sự kiện "click" được handle hoàn toàn.

```
menu.onclick = function() {
  // ...

  // tạo một custom event với dữ liệu menu item được click
  let customEvent = new CustomEvent("menu-open", {
    bubbles: true
  });

  // dispatch custom event một cách bất đồng bộ
  setTimeout(() => menu.dispatchEvent(customEvent));
};
```

## [Macrotasks và Microtasks](#macrotasks-and-microtasks)

Cùng với *macrotasks*, được mô tả trong chương này, có *microtasks*, được đề cập trong chương [Microtasks](/microtask-queue).

Microtasks đến duy nhất từ code của chúng ta. Chúng thường được tạo bởi promises: execution của `.then/catch/finally` handler trở thành một microtask. Microtasks được dùng "under the cover" của `await` cũng vậy, vì đó là một dạng khác của promise handling.

Cũng có một special function `queueMicrotask(func)` queues `func` để thực thi trong microtask queue.

**Ngay lập tức sau mỗi *macrotask*, engine thực thi tất cả tasks từ *microtask* queue, trước khi chạy bất kỳ macrotasks khác hoặc rendering hoặc bất cứ thứ gì khác.**

Ví dụ, hãy xem:

```
setTimeout(() => alert("timeout"));

Promise.resolve()
  .then(() => alert("promise"));

alert("code");
```

Thứ tự sẽ như thế nào ở đây?

1. `code` hiển thị trước tiên, vì nó là một synchronous call thông thường.
2. `promise` hiển thị thứ hai, vì `.then` đi qua microtask queue, và chạy sau current code.
3. `timeout` hiển thị cuối cùng, vì nó là một macrotask.

Hình ảnh event loop phong phú hơn trông như thế này (thứ tự từ trên xuống dưới, tức là: script trước, sau đó microtasks, rendering và tương tự):

![](/article/event-loop/eventLoop-full.svg)

Tất cả microtasks được hoàn tất trước bất kỳ event handling khác hoặc rendering hoặc bất kỳ macrotask nào khác xảy ra.

Điều đó quan trọng, vì nó đảm bảo rằng environment application về cơ bản là giống nhau (không có thay đổi tọa độ chuột, không có network data mới, v.v.) giữa các microtasks.

Nếu chúng ta muốn thực thi một hàm một cách bất đồng bộ (sau current code), nhưng trước khi các changes được render hoặc các events mới được handle, chúng ta có thể schedule nó bằng `queueMicrotask`.

Đây là một example với "progress bar counting", tương tự như cái đã được hiển thị trước đó, nhưng `queueMicrotask` được dùng thay vì `setTimeout`. Bạn có thể thấy rằng nó render ở cuối cùng. Giống như synchronous code:

```
<div id="progress"></div>

<script>
  let i = 0;

  function count() {

    // làm một phần của công việc nặng (*)
    do {
      i++;
      progress.innerHTML = i;
    } while (i % 1e3 != 0);

    if (i < 1e6) {
      queueMicrotask(count);
    }

  }

  count();
</script>
```

## [Tóm tắt](#summary)

Algorithm event loop chi tiết hơn (mặc dù vẫn simplified so với [specification](https://html.spec.whatwg.org/multipage/webappapis.html#event-loop-processing-model)):

1. Dequeue và chạy task cũ nhất từ *macrotask* queue (ví dụ "script").
2. Thực thi tất cả *microtasks*:
   - Trong khi microtask queue không rỗng:
     - Dequeue và chạy microtask cũ nhất.
3. Render các changes nếu có.
4. Nếu macrotask queue rỗng, chờ cho đến khi một macrotask xuất hiện.
5. Quay lại bước 1.

Để schedule một *macrotask* mới:

- Dùng zero delayed `setTimeout(f)`.

Điều đó có thể được dùng để chia một task calculation-heavy lớn thành các pieces, để browser có thể phản hồi với user events và hiển thị progress giữa chúng.

Cũng được dùng trong event handlers để schedule một action sau khi event được handle hoàn toàn (bubbling xong).

Để schedule một *microtask* mới

- Dùng `queueMicrotask(f)`.
- Cũng promise handlers đi qua microtask queue.

Không có UI hoặc network event handling giữa các microtasks: chúng chạy ngay lập tức sau nhau.

Vậy có thể muốn `queueMicrotask` để thực thi một hàm một cách bất đồng bộ, nhưng trong trạng thái environment.

Web Workers

Đối với các calculations nặng dài không nên block event loop, chúng ta có thể dùng [Web Workers](https://html.spec.whatwg.org/multipage/workers.html).

Đó là một cách để chạy code trong một thread khác, song song.

Web Workers có thể exchange messages với process chính, nhưng chúng có các variables riêng của chúng, và event loop riêng của chúng.

Web Workers không có access đến DOM, vậy chúng hữu ích, chủ yếu, cho calculations, để sử dụng nhiều CPU cores đồng thời.

---

---

## Tasks

## [Tasks](#tasks)

### [Output của code này sẽ là gì?](#what-will-be-the-output-of-this-code)

importance: 5

```
console.log(1);

setTimeout(() => console.log(2));

Promise.resolve().then(() => console.log(3));

Promise.resolve().then(() => setTimeout(() => console.log(4)));

Promise.resolve().then(() => console.log(5));

setTimeout(() => console.log(6));

console.log(7);
```

solution

Output console là: 1 7 3 5 2 6 4.

Task khá đơn giản, chúng ta chỉ cần biết cách microtask và macrotask queues hoạt động.

Hãy xem điều gì đang xảy ra, từng bước.

```
console.log(1);
// Dòng đầu tiên thực thi ngay lập tức, nó outputs `1`.
// Macrotask và microtask queues đều rỗng, cho đến giờ.

setTimeout(() => console.log(2));
// `setTimeout` append callback vào macrotask queue.
// - nội dung macrotask queue:
//   `console.log(2)`

Promise.resolve().then(() => console.log(3));
// Callback được append vào microtask queue.
// - nội dung microtask queue:
//   `console.log(3)`

Promise.resolve().then(() => setTimeout(() => console.log(4)));
// Callback với `setTimeout(...4)` được append vào microtasks
// - nội dung microtask queue:
//   `console.log(3); setTimeout(...4)`

Promise.resolve().then(() => console.log(5));
// Callback được append vào microtask queue
// - nội dung microtask queue:
//   `console.log(3); setTimeout(...4); console.log(5)`

setTimeout(() => console.log(6));
// `setTimeout` append callback vào macrotasks
// - nội dung macrotask queue:
//   `console.log(2); console.log(6)`

console.log(7);
// Outputs 7 ngay lập tức.
```

Để tóm tắt,

1. Các số `1` và `7` xuất hiện ngay lập tức, vì các `console.log` calls đơn giản không dùng bất kỳ queues nào.
2. Sau đó, sau khi main code flow kết thúc, microtask queue chạy.
   - Nó có commands: `console.log(3); setTimeout(...4); console.log(5)`.
   - Các số `3` và `5` xuất hiện, trong khi `setTimeout(() => console.log(4))` thêm call `console.log(4)` vào cuối macrotask queue.
   - Macrotask queue giờ là: `console.log(2); console.log(6); console.log(4)`.
3. Sau khi microtask queue trở nên rỗng, macrotask queue thực thi. Nó outputs `2`, `6`, `4`.

Cuối cùng, chúng ta có output: `1 7 3 5 2 6 4`.
