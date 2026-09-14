# Lên lịch: setTimeout và setInterval

> Nguồn: [https://javascript.info/settimeout-setinterval](https://javascript.info/settimeout-setinterval)

<!-- fetched: 2026-09-14 -->

Chúng ta có thể quyết định thực thi một hàm không phải ngay bây giờ, mà vào một thời điểm nào đó sau. Đó gọi là "lên lịch gọi hàm".

Có hai phương thức để làm điều này:

- `setTimeout` cho phép chúng ta thực thi một hàm một lần sau một khoảng thời gian xác định.
- `setInterval` cho phép chúng ta thực thi một hàm nhiều lần, bắt đầu sau một khoảng thời gian, sau đó liên tục lặp lại theo khoảng thời gian đó.

Các phương thức này không phải là một phần của đặc tả JavaScript. Nhưng hầu hết các môi trường đều có bộ lên lịch nội tại và cung cấp các phương thức này. Cụ thể, chúng được hỗ trợ trong tất cả các trình duyệt và Node.js.

## [setTimeout](#settimeout)

Cú pháp:

```
let timerId = setTimeout(func|code, [delay], [arg1], [arg2], ...)
```

Các tham số:

`func|code`
:   Hàm hoặc chuỗi mã để thực thi.
    Thông thường, đó là một hàm. Vì lý do lịch sử, có thể truyền một chuỗi mã, nhưng điều này không được khuyến nghị.

`delay`
:   Độ trễ trước khi chạy, tính bằng miligiây (1000 ms = 1 giây), mặc định là 0.

`arg1`, `arg2`…
:   Các đối số cho hàm

Ví dụ, mã này gọi `sayHi()` sau một giây:

```
function sayHi() {
  alert('Hello');
}

setTimeout(sayHi, 1000);
```

Với các đối số:

```
function sayHi(phrase, who) {
  alert( phrase + ', ' + who );
}

setTimeout(sayHi, 1000, "Hello", "John"); // Hello, John
```

Nếu đối số đầu tiên là một chuỗi, thì JavaScript tạo một hàm từ chuỗi đó.

Vì vậy, cái này cũng hoạt động:

```
setTimeout("alert('Hello')", 1000);
```

Nhưng việc sử dụng chuỗi không được khuyến nghị, hãy dùng hàm arrow thay thế, như sau:

```
setTimeout(() => alert('Hello'), 1000);
```

Truyền một hàm, nhưng đừng gọi nó

Các nhà phát triển mới thường mắc lỗi khi thêm dấu ngoặc đơn `()` sau tên hàm:

```
// sai!
setTimeout(sayHi(), 1000);
```

Điều đó không hoạt động, vì `setTimeout` mong đợi một tham chiếu đến hàm. Và ở đây `sayHi()` thực thi hàm, và *kết quả thực thi* được truyền cho `setTimeout`. Trong trường hợp của chúng ta, kết quả của `sayHi()` là `undefined` (hàm không trả về gì), nên không có gì được lên lịch.

### [Hủy bằng clearTimeout](#canceling-with-cleartimeout)

Một lệnh gọi đến `setTimeout` trả về một "Nhận dạng bộ hẹn giờ" `timerId` mà chúng ta có thể sử dụng để hủy thực thi.

Cú pháp để hủy:

```
let timerId = setTimeout(...);
clearTimeout(timerId);
```

Trong mã dưới đây, chúng ta lên lịch hàm rồi hủy nó (thay đổi ý định). Kết quả là không có gì xảy ra:

```
let timerId = setTimeout(() => alert("never happens"), 1000);
alert(timerId); // mã nhận dạng bộ hẹn giờ

clearTimeout(timerId);
alert(timerId); // cùng mã nhận dạng (không trở thành null sau khi hủy)
```

Như chúng ta có thể thấy từ kết quả `alert`, trong trình duyệt, mã nhận dạng bộ hẹn giờ là một số. Trong các môi trường khác, điều này có thể là thứ khác. Ví dụ, Node.js trả về một đối tượng bộ hẹn giờ với các phương thức bổ sung.

Một lần nữa, không có đặc tả chung nào cho các phương thức này, vì vậy điều đó là ổn.

Đối với trình duyệt, các bộ hẹn giờ được mô tả trong [phần timers](https://html.spec.whatwg.org/multipage/timers-and-user-prompts.html#timers) của HTML Living Standard.

## [setInterval](#setinterval)

Phương thức `setInterval` có cú pháp giống như `setTimeout`:

```
let timerId = setInterval(func|code, [delay], [arg1], [arg2], ...)
```

Tất cả các đối số đều có cùng ý nghĩa. Nhưng khác với `setTimeout`, nó thực thi hàm không chỉ một lần mà còn lặp lại thường xuyên sau khoảng thời gian đã cho.

Để dừng các lệnh gọi tiếp theo, chúng ta nên gọi `clearInterval(timerId)`.

Ví dụ sau sẽ hiển thị thông báo mỗi 2 giây. Sau 5 giây, việc hiển thị bị dừng:

```
// lặp lại với khoảng cách 2 giây
let timerId = setInterval(() => alert('tick'), 2000);

// sau 5 giây thì dừng
setTimeout(() => { clearInterval(timerId); alert('stop'); }, 5000);
```

Thời gian vẫn trôi khi đang hiển thị `alert`

Trong hầu hết các trình duyệt, bao gồm Chrome và Firefox, bộ đếm thời gian nội bộ tiếp tục "tích tắc" trong khi hiển thị `alert/confirm/prompt`.

Vì vậy, nếu bạn chạy mã trên và không đóng cửa sổ `alert` trong một lúc, thì `alert` tiếp theo sẽ được hiển thị ngay lập tức khi bạn làm điều đó. Khoảng thời gian thực tế giữa các lần cảnh báo sẽ ngắn hơn 2 giây.

## [setTimeout lồng nhau](#nested-settimeout)

Có hai cách để thực hiện điều gì đó thường xuyên.

Một là `setInterval`. Cách kia là `setTimeout` lồng nhau, như sau:

```
/** thay vì:
let timerId = setInterval(() => alert('tick'), 2000);
*/

let timerId = setTimeout(function tick() {
  alert('tick');
  timerId = setTimeout(tick, 2000); // (*)
}, 2000);
```

`setTimeout` ở trên lên lịch cuộc gọi tiếp theo ngay ở cuối cuộc gọi hiện tại `(*)`.

`setTimeout` lồng nhau là phương pháp linh hoạt hơn so với `setInterval`. Bằng cách này, cuộc gọi tiếp theo có thể được lên lịch khác đi, tùy thuộc vào kết quả của cuộc gọi hiện tại.

Ví dụ, chúng ta cần viết một dịch vụ gửi yêu cầu đến máy chủ mỗi 5 giây để lấy dữ liệu, nhưng trong trường hợp máy chủ bị quá tải, nó nên tăng khoảng thời gian thành 10, 20, 40 giây…

Dưới đây là mã giả:

```
let delay = 5000;

let timerId = setTimeout(function request() {
  ...gửi yêu cầu...

  if (yêu cầu thất bại do máy chủ quá tải) {
    // tăng khoảng thời gian cho lần chạy tiếp theo
    delay *= 2;
  }

  timerId = setTimeout(request, delay);

}, delay);
```

Và nếu các hàm mà chúng ta đang lên lịch là những hàm tốn nhiều CPU, thì chúng ta có thể đo thời gian thực thi và lên kế hoạch cho cuộc gọi tiếp theo sớm hoặc muộn hơn.

**`setTimeout` lồng nhau cho phép đặt khoảng cách giữa các lần thực thi chính xác hơn so với `setInterval`.**

Hãy so sánh hai đoạn mã. Đoạn đầu tiên sử dụng `setInterval`:

```
let i = 1;
setInterval(function() {
  func(i++);
}, 100);
```

Đoạn thứ hai sử dụng `setTimeout` lồng nhau:

```
let i = 1;
setTimeout(function run() {
  func(i++);
  setTimeout(run, 100);
}, 100);
```

Đối với `setInterval`, bộ lên lịch nội tại sẽ thực thi `func(i++)` cứ mỗi 100ms:

![](/article/settimeout-setinterval/setinterval-interval.svg)

Bạn có nhận ra không?

**Độ trễ thực tế giữa các lần gọi `func` cho `setInterval` là nhỏ hơn trong mã!**

Điều đó là bình thường, vì thời gian thực thi của `func` "tiêu thụ" một phần khoảng thời gian.

Có thể xảy ra trường hợp thời gian thực thi của `func` dài hơn chúng ta dự kiến và vượt quá 100ms.

Trong trường hợp này, công cụ chờ cho đến khi `func` hoàn thành, sau đó kiểm tra bộ lên lịch và nếu đã đến giờ, nó sẽ chạy lại *ngay lập tức*.

Trong trường hợp biên, nếu hàm luôn thực thi lâu hơn `delay` ms, thì các lệnh gọi sẽ diễn ra mà không có khoảng nghỉ nào.

Và đây là hình ảnh cho `setTimeout` lồng nhau:

![](/article/settimeout-setinterval/settimeout-interval.svg)

**`setTimeout` lồng nhau đảm bảo độ trễ tối thiểu (100ms ở đây) giữa lần kết thúc của một lệnh gọi và lần bắt đầu của lệnh gọi tiếp theo.**

Điều đó là vì một cuộc gọi mới được lên kế hoạch ở cuối cuộc gọi trước đó.

Thu gom rác và callback của setInterval/setTimeout

Khi một hàm được truyền trong `setInterval/setTimeout`, một tham chiếu nội bộ được tạo ra và được lưu trong bộ lên lịch. Nó ngăn hàm bị thu gom rác, ngay cả khi không có tham chiếu nào khác đến nó.

```
// hàm vẫn tồn tại trong bộ nhớ cho đến khi bộ lên lịch gọi nó
setTimeout(function() {...}, 100);
```

Đối với `setInterval`, hàm vẫn tồn tại trong bộ nhớ cho đến khi `clearInterval` được gọi.

Có một hiệu ứng phụ. Một hàm tham chiếu đến môi trường lexical bên ngoài, vì vậy, trong khi nó tồn tại, các biến bên ngoài cũng tồn tại. Chúng có thể chiếm nhiều bộ nhớ hơn cả bản thân hàm. Vì vậy, khi chúng ta không cần hàm đã lên lịch nữa, tốt hơn là nên hủy nó, ngay cả khi nó rất nhỏ.

## [setTimeout với độ trễ bằng 0](#zero-delay-settimeout)

Có một trường hợp sử dụng đặc biệt: `setTimeout(func, 0)`, hay chỉ `setTimeout(func)`.

Điều này lên lịch thực thi của `func` càng sớm càng tốt. Nhưng bộ lên lịch sẽ chỉ gọi nó sau khi script hiện tại đang thực thi đã hoàn tất.

Vì vậy, hàm được lên lịch để chạy "ngay sau" script hiện tại.

Ví dụ, cái này xuất "Hello", sau đó ngay lập tức xuất "World":

```
setTimeout(() => alert("World"));

alert("Hello");
```

Dòng đầu tiên "đặt lệnh gọi vào lịch sau 0ms". Nhưng bộ lên lịch sẽ chỉ "kiểm tra lịch" sau khi script hiện tại hoàn tất, vì vậy `"Hello"` đến trước, và `"World"` — sau đó.

Cũng có các trường hợp sử dụng tiên tiến liên quan đến trình duyệt của timeout không có độ trễ, mà chúng ta sẽ thảo luận trong chương [Chuỗi sự kiện: microtasks và macrotasks](/event-loop).

Độ trễ bằng 0 thực tế không phải là bằng 0 (trong trình duyệt)

Trong trình duyệt, có một hạn chế về tần suất các bộ hẹn giờ lồng nhau có thể chạy. [HTML Living Standard](https://html.spec.whatwg.org/multipage/timers-and-user-prompts.html#timers) nói: "sau năm bộ hẹn giờ lồng nhau, khoảng thời gian bị buộc phải ít nhất là 4 miligiây.".

Hãy minh họa điều đó bằng ví dụ dưới đây. Lệnh gọi `setTimeout` trong đó tự lên lịch lại với độ trễ bằng 0. Mỗi lệnh gọi nhớ thời gian thực tế từ lệnh gọi trước đó vào mảng `times`. Độ trễ thực tế trông như thế nào? Hãy xem:

```
let start = Date.now();
let times = [];

setTimeout(function run() {
  times.push(Date.now() - start); // nhớ độ trễ từ lệnh gọi trước

  if (start + 100 < Date.now()) alert(times); // hiển thị độ trễ sau 100ms
  else setTimeout(run); // nếu không thì lên lịch lại
});

// một ví dụ về kết quả:
// 1,1,1,1,9,15,20,24,30,35,40,45,50,55,59,64,70,75,80,85,90,95,100
```

Các bộ hẹn giờ đầu tiên chạy ngay lập tức (chính xác như trong đặc tả), và sau đó chúng ta thấy `9, 15, 20, 24...`. Độ trễ bắt buộc 4+ ms giữa các lần gọi phát huy tác dụng.

Điều tương tự cũng xảy ra nếu chúng ta sử dụng `setInterval` thay vì `setTimeout`: `setInterval(f)` chạy `f` vài lần với độ trễ bằng 0, và sau đó với độ trễ 4+ ms.

Hạn chế này có từ thời cổ xưa và nhiều script dựa vào nó, nên nó tồn tại vì lý do lịch sử.

Đối với JavaScript phía máy chủ, hạn chế này không tồn tại, và có các cách khác để lên lịch một công việc bất đồng bộ ngay lập tức, như [setImmediate](https://nodejs.org/api/timers.html#timers_setimmediate_callback_args) cho Node.js. Vì vậy, ghi chú này chỉ dành cho trình duyệt.

## [Tóm tắt](#summary)

- Các phương thức `setTimeout(func, delay, ...args)` và `setInterval(func, delay, ...args)` cho phép chúng ta thực thi `func` một lần/thường xuyên sau `delay` miligiây.
- Để hủy thực thi, chúng ta nên gọi `clearTimeout/clearInterval` với giá trị trả về từ `setTimeout/setInterval`.
- Các lệnh gọi `setTimeout` lồng nhau là một giải pháp thay thế linh hoạt hơn so với `setInterval`, cho phép chúng ta đặt thời gian *giữa* các lần thực thi chính xác hơn.
- Lên lịch với độ trễ bằng 0 bằng `setTimeout(func, 0)` (cũng giống như `setTimeout(func)`) được sử dụng để lên lịch cuộc gọi "sớm nhất có thể, nhưng sau khi script hiện tại hoàn tất".
- Trình duyệt giới hạn độ trễ tối thiểu cho năm hoặc nhiều hơn các lệnh gọi lồng nhau của `setTimeout` hoặc cho `setInterval` (sau lần gọi thứ 5) là 4ms. Đó là vì lý do lịch sử.

Xin lưu ý rằng tất cả các phương thức lên lịch không *đảm bảo* độ trễ chính xác.

Ví dụ, bộ đếm thời gian trong trình duyệt có thể bị chậm vì nhiều lý do:

- CPU bị quá tải.
- Tab trình duyệt đang ở chế độ nền.
- Laptop đang ở chế độ tiết kiệm pin.

Tất cả những điều đó có thể làm tăng độ phân giải bộ đếm thời gian tối thiểu (độ trễ tối thiểu) lên 300ms hoặc thậm chí 1000ms tùy thuộc vào trình duyệt và cài đặt hiệu suất ở cấp hệ điều hành.

---

---

## Bài tập

## [Bài tập](#tasks)

### [Xuất mỗi giây](#output-every-second)

độ khó: 5

Viết hàm `printNumbers(from, to)` xuất một số mỗi giây, bắt đầu từ `from` và kết thúc ở `to`.

Làm hai phiên bản của lời giải.

1. Sử dụng `setInterval`.
2. Sử dụng `setTimeout` lồng nhau.

Lời giải

Sử dụng `setInterval`:

```
function printNumbers(from, to) {
  let current = from;

  let timerId = setInterval(function() {
    alert(current);
    if (current == to) {
      clearInterval(timerId);
    }
    current++;
  }, 1000);
}

// cách dùng:
printNumbers(5, 10);
```

Sử dụng `setTimeout` lồng nhau:

```
function printNumbers(from, to) {
  let current = from;

  setTimeout(function go() {
    alert(current);
    if (current < to) {
      setTimeout(go, 1000);
    }
    current++;
  }, 1000);
}

// cách dùng:
printNumbers(5, 10);
```

Lưu ý rằng trong cả hai lời giải, có một độ trễ ban đầu trước lần xuất đầu tiên. Hàm được gọi sau `1000ms` lần đầu tiên.

Nếu chúng ta cũng muốn hàm chạy ngay lập tức, thì chúng ta có thể thêm một lệnh gọi bổ sung trên một dòng riêng, như sau:

```
function printNumbers(from, to) {
  let current = from;

  function go() {
    alert(current);
    if (current == to) {
      clearInterval(timerId);
    }
    current++;
  }

  go();
  let timerId = setInterval(go, 1000);
}

printNumbers(5, 10);
```

### [setTimeout sẽ hiển thị gì?](#what-will-settimeout-show)

độ khó: 5

Trong mã dưới đây có một lệnh gọi `setTimeout` được lên lịch, sau đó là một phép tính nặng chạy, mất hơn 100ms để hoàn thành.

Khi nào hàm được lên lịch sẽ chạy?

1. Sau vòng lặp.
2. Trước vòng lặp.
3. Ở đầu vòng lặp.

`alert` sẽ hiển thị gì?

```
let i = 0;

setTimeout(() => alert(i), 100); // ?

// giả sử thời gian thực thi hàm này >100ms
for(let j = 0; j < 100000000; j++) {
  i++;
}
```

Lời giải

Bất kỳ `setTimeout` nào cũng chỉ chạy sau khi mã hiện tại đã hoàn tất.

`i` sẽ là giá trị cuối cùng: `100000000`.

```
let i = 0;

setTimeout(() => alert(i), 100); // 100000000

// giả sử thời gian thực thi hàm này >100ms
for(let j = 0; j < 100000000; j++) {
  i++;
}
```
