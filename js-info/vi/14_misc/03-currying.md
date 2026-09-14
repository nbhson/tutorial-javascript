# Currying (Áp dụng từng phần)

> Source: [https://javascript.info/currying-partials](https://javascript.info/currying-partials)

<!-- fetched: 2026-09-14 -->

[Currying](https://en.wikipedia.org/wiki/Currying) là một kỹ thuật nâng cao làm việc với các hàm. Nó được sử dụng không chỉ trong JavaScript, mà trong các ngôn ngữ khác cũng.

Currying là một phép biến đổi các hàm chuyển một hàm từ có thể gọi như `f(a, b, c)` thành có thể gọi như `f(a)(b)(c)`.

Currying không gọi một hàm. Nó chỉ biến đổi nó.

Hãy xem một ví dụ trước để hiểu rõ hơn những gì chúng ta đang nói, và sau đó xem các ứng dụng thực tế.

Chúng ta sẽ tạo một hàm helper `curry(f)` thực hiện currying cho một `f` hai đối số. Nói cách khác, `curry(f)` cho `f(a, b)` hai đối số chuyển đổi nó thành một hàm chạy như `f(a)(b)`:

```
function curry(f) { // curry(f) thực hiện biến đổi currying
  return function(a) {
    return function(b) {
      return f(a, b);
    };
  };
}

// usage
function sum(a, b) {
  return a + b;
}

let curriedSum = curry(sum);

alert( curriedSum(1)(2) ); // 3
```

Như bạn có thể thấy, implementation rất đơn giản: đó chỉ là hai wrapper.

- Kết quả của `curry(func)` là wrapper `function(a)`.
- Khi nó được gọi như `curriedSum(1)`, đối số được lưu trong Lexical Environment, và một wrapper mới được trả về `function(b)`.
- Sau đó wrapper này được gọi với `2` là đối số, và nó chuyển cuộc gọi đến `sum` gốc.

Các implementation currying nâng cao hơn, chẳng hạn như [\_.curry](https://lodash.com/docs#curry) từ thư viện lodash, trả về một wrapper cho phép một hàm được gọi cả theo cách thông thường và theo cách từng phần:

```
function sum(a, b) {
  return a + b;
}

let curriedSum = _.curry(sum); // sử dụng _.curry từ thư viện lodash

alert( curriedSum(1, 2) ); // 3, vẫn có thể gọi bình thường
alert( curriedSum(1)(2) ); // 3, gọi từng phần
```

## [Currying? Để làm gì?](#currying-what-for)

Để hiểu các lợi ích chúng ta cần một ví dụ thực tế xứng đáng.

Ví dụ, chúng ta có hàm logging `log(date, importance, message)` định dạng và xuất thông tin. Trong các dự án thực tế các hàm như vậy có nhiều tính năng hữu ích như gửi logs qua mạng, ở đây chúng ta sẽ chỉ sử dụng `alert`:

```
function log(date, importance, message) {
  alert(`[${date.getHours()}:${date.getMinutes()}] [${importance}] ${message}`);
}
```

Hãy currying nó!

```
log = _.curry(log);
```

Sau đó `log` hoạt động bình thường:

```
log(new Date(), "DEBUG", "some debug"); // log(a, b, c)
```

…Nhưng cũng hoạt động ở dạng curried:

```
log(new Date())("DEBUG")("some debug"); // log(a)(b)(c)
```

Giờ chúng ta có thể dễ dàng tạo một hàm tiện lợi cho các logs hiện tại:

```
// logNow sẽ là partial của log với đối số đầu tiên được cố định
let logNow = log(new Date());

// sử dụng nó
logNow("INFO", "message"); // [HH:mm] INFO message
```

Giờ `logNow` là `log` với đối số đầu tiên được cố định, nói cách khác "hàm đã áp dụng từng phần" hoặc "partial" để ngắn gọn.

Chúng ta có thể đi xa hơn và tạo một hàm tiện lợi cho các debug logs hiện tại:

```
let debugNow = logNow("DEBUG");

debugNow("message"); // [HH:mm] DEBUG message
```

Vì vậy:

1. Chúng ta không mất gì sau khi currying: `log` vẫn có thể gọi bình thường.
2. Chúng ta có thể dễ dàng tạo các hàm partial chẳng hạn như cho logs hôm nay.

## [Implementation currying nâng cao](#advanced-curry-implementation)