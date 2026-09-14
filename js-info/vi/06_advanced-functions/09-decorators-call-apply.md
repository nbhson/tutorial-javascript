# Bộ trang trí và chuyển tiếp, call/apply

> Nguồn: [https://javascript.info/call-apply-decorators](https://javascript.info/call-apply-decorators)

<!-- fetched: 2026-09-14 -->

JavaScript mang lại sự linh hoạt đặc biệt khi làm việc với các hàm. Chúng có thể được truyền đi, sử dụng như các đối tượng, và bây giờ chúng ta sẽ xem cách *chuyển tiếp* các lời gọi giữa chúng và *trang trí* chúng.

## [Lưu trữ trong bộ nhớ đệm minh bạch](#transparent-caching)

Giả sử chúng ta có một hàm `slow(x)` tốn nhiều CPU, nhưng kết quả của nó ổn định. Nói cách khác, với cùng một `x` nó luôn trả về cùng một kết quả.

Nếu hàm được gọi thường xuyên, chúng ta có thể muốn lưu trữ trong bộ nhớ đệm (ghi nhớ) các kết quả để tránh tiêu tốn thời gian tính toán lại.

Nhưng thay vì thêm chức năng đó vào `slow()`, chúng ta sẽ tạo một hàm bao, thêm bộ nhớ đệm. Như chúng ta sẽ thấy, có nhiều lợi ích của việc làm như vậy.

Đây là mã, và giải thích sẽ theo sau:

```
function slow(x) {
  // có thể có công việc nặng đây
  alert(`Called with ${x}`);
  return x;
}

function cachingDecorator(func) {
  let cache = new Map();

  return function(x) {
    if (cache.has(x)) {    // nếu có khóa này trong cache
      return cache.get(x); // đọc kết quả từ đó
    }

    let result = func(x);  // nếu không thì gọi func

    cache.set(x, result);  // và lưu trữ kết quả vào cache (ghi nhớ)
    return result;
  };
}

slow = cachingDecorator(slow);

alert( slow(1) ); // slow(1) được cache và kết quả được trả về
alert( "Again: " + slow(1) ); // slow(1) kết quả được trả về từ cache

alert( slow(2) ); // slow(2) được cache và kết quả được trả về
alert( "Again: " + slow(2) ); // slow(2) kết quả được trả về từ cache
```

Trong mã trên, `cachingDecorator` là một *bộ trang trí*: một hàm đặc biệt nhận một hàm khác và làm thay đổi hành vi của nó.

Ý tưởng là chúng ta có thể gọi `cachingDecorator` cho bất kỳ hàm nào, và nó sẽ trả về hàm bao có bộ nhớ đệm. Thật tuyệt vời, vì có nhiều hàm có thể sử dụng tính năng này, và tất cả những gì chúng ta cần làm là áp dụng `cachingDecorator` lên chúng.

Bằng cách tách bộ nhớ đệm khỏi mã chính của hàm, chúng ta cũng giữ cho mã chính đơn giản hơn.

Kết quả của `cachingDecorator(func)` là một "bộ bao": `function(x)` bao bọc lời gọi của `func(x)` vào trong logic bộ nhớ đệm:

![](/article/call-apply-decorators/decorator-makecaching-wrapper.svg)

Từ mã bên ngoài, hàm `slow` được bao vẫn hoạt động giống như trước. Nó chỉ được thêm một khía cạnh bộ nhớ đệm vào hành vi của nó.

Để tóm tắt, có một vài lợi ích của việc sử dụng `cachingDecorator` riêng biệt thay vì thay đổi mã của `slow` chính nó:

- `cachingDecorator` có thể tái sử dụng. Chúng ta có thể áp dụng nó cho một hàm khác.
- Logic bộ nhớ đệm được tách biệt, nó không làm tăng độ phức tạp của `slow` (nếu có).
- Chúng ta có thể kết hợp nhiều bộ trang trí nếu cần (các bộ trang trí khác sẽ tiếp theo).

## [Sử dụng "func.call" cho ngữ cảnh](#using-func-call-for-the-context)

Bộ trang trí bộ nhớ đệm được đề cập ở trên không phù hợp để làm việc với các phương thức đối tượng.

Ví dụ, trong mã dưới đây `worker.slow()` ngừng hoạt động sau khi trang trí:

```
// chúng ta sẽ tạo worker.slow có bộ nhớ đệm
let worker = {
  someMethod() {
    return 1;
  },

  slow(x) {
    // nhiệm vụ CPU nặng kinh hoàng ở đây
    alert("Called with " + x);
    return x * this.someMethod(); // (*)
  }
};

// cùng mã như trước
function cachingDecorator(func) {
  let cache = new Map();
  return function(x) {
    if (cache.has(x)) {
      return cache.get(x);
    }
    let result = func(x); // (**)
    cache.set(x, result);
    return result;
  };
}

alert( worker.slow(1) ); // phương thức ban đầu hoạt động

worker.slow = cachingDecorator(worker.slow); // bây giờ thêm bộ nhớ đệm

alert( worker.slow(2) ); // Ôi! Lỗi: Không thể đọc thuộc tính 'someMethod' của undefined
```

Lỗi xảy ra ở dòng `(*)` cố truy cập `this.someMethod` và thất bại. Bạn có thấy tại sao không?

Lý do là bộ bao gọi hàm gốc là `func(x)` ở dòng `(**)`. Và, khi được gọi như vậy, hàm nhận được `this = undefined`.

Chúng ta sẽ quan sát một triệu chứng tương tự nếu chúng ta thử chạy:

```
let func = worker.slow;
func(2);
```

Vì vậy, bộ bao chuyển lời gọi đến phương thức gốc, nhưng không có ngữ cảnh `this`. Do đó có lỗi.

Hãy sửa nó.

Có một phương thức built-in đặc biệt [func.call(context, …args)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Function/call) cho phép gọi một hàm bằng cách thiết lập rõ ràng `this`.

Cú pháp là:

```
func.call(context, arg1, arg2, ...)
```

Nó chạy `func` cung cấp đối số đầu tiên làm `this`, và các đối số tiếp theo.

Nói một cách đơn giản, hai lời gọi sau hầu như giống nhau:

```
func(1, 2, 3);
func.call(obj, 1, 2, 3)
```

Cả hai đều gọi `func` với các đối số `1`, `2` và `3`. Sự khác biệt duy nhất là `func.call` cũng đặt `this` thành `obj`.

Làm ví dụ, trong mã dưới đây chúng ta gọi `sayHi` trong ngữ cảnh của các đối tượng khác nhau: `sayHi.call(user)` chạy `sayHi` cung cấp `this=user`, và dòng tiếp theo đặt `this=admin`:

```
function sayHi() {
  alert(this.name);
}

let user = { name: "John" };
let admin = { name: "Admin" };

// sử dụng call để truyền các đối tượng khác nhau làm "this"
sayHi.call( user ); // John
sayHi.call( admin ); // Admin
```

Và ở đây chúng ta sử dụng `call` để gọi `say` với ngữ cảnh và cụm từ đã cho:

```
function say(phrase) {
  alert(this.name + ': ' + phrase);
}

let user = { name: "John" };

// user trở thành this, và "Hello" trở thành đối số đầu tiên
say.call( user, "Hello" ); // John: Hello
```

Trong trường hợp của chúng ta, chúng ta có thể sử dụng `call` trong bộ bao để truyền ngữ cảnh đến hàm gốc:

```
let worker = {
  someMethod() {
    return 1;
  },

  slow(x) {
    alert("Called with " + x);
    return x * this.someMethod(); // (*)
  }
};

function cachingDecorator(func) {
  let cache = new Map();
  return function(x) {
    if (cache.has(x)) {
      return cache.get(x);
    }
    let result = func.call(this, x); // "this" được truyền đúng bây giờ
    cache.set(x, result);
    return result;
  };
}

worker.slow = cachingDecorator(worker.slow); // bây giờ thêm bộ nhớ đệm

alert( worker.slow(2) ); // hoạt động
alert( worker.slow(2) ); // hoạt động, không gọi hàm gốc (đã được cache)
```

Giờ thì mọi thứ đều ổn.

Để làm cho tất cả rõ ràng, hãy xem sâu hơn cách `this` được truyền dọc theo:

1. Sau khi trang trí, `worker.slow` bây giờ là bộ bao `function (x) { ... }`.
2. Vì vậy khi `worker.slow(2)` được thực thi, bộ bao nhận `2` làm đối số và `this=worker` (đó là đối tượng trước dấu chấm).
3. Bên trong bộ bao, giả sử kết quả chưa được cache, `func.call(this, x)` truyền `this` hiện tại (`=worker`) và đối số hiện tại (`=2`) đến phương thức gốc.

## [Đa đối số](#going-multi-argument)

Bây giờ hãy làm cho `cachingDecorator` thậm chí phổ biến hơn. Cho đến nay nó chỉ hoạt động với các hàm một đối số.

Bây giờ làm thế nào để cache phương thức `worker.slow` đa đối số?

```
let worker = {
  slow(min, max) {
    return min + max; // giả sử có bộ phận CPU nặng
  }
};

// nên ghi nhớ các lời gọi cùng đối số
worker.slow = cachingDecorator(worker.slow);
```

Trước đây, với một đối số `x` chúng ta có thể chỉ cần `cache.set(x, result)` để lưu kết quả và `cache.get(x)` để truy xuất nó. Nhưng bây giờ chúng ta cần ghi nhớ kết quả cho *một tổ hợp các đối số* `(min,max)`. `Map` bản địa chỉ nhận một giá trị duy nhất làm khóa.

Có nhiều giải pháp có thể:

1. Triển khai một cấu trúc dữ liệu mới (hoặc sử dụng bên thứ ba) giống như map mà đa dạng hơn và cho phép nhiều khóa.
2. Sử dụng các map lồng nhau: `cache.set(min)` sẽ là một `Map` lưu trữ cặp `(max, result)`. Vì vậy chúng ta có thể lấy `result` là `cache.get(min).get(max)`.
3. Nối hai giá trị thành một. Trong trường hợp cụ thể của chúng ta, chúng ta có thể chỉ cần sử dụng chuỗi `"min,max"` làm khóa `Map`. Để linh hoạt, chúng ta có thể cho phép cung cấp *hàm băm* cho bộ trang trí, biết cách tạo một giá trị từ nhiều giá trị.

Đối với nhiều ứng dụng thực tế, biến thể thứ 3 là đủ tốt, vì vậy chúng ta sẽ sử dụng nó.

Ngoài ra chúng ta cần truyền không chỉ `x`, mà tất cả các đối số trong `func.call`. Hãy nhớ lại rằng trong một `function()` chúng ta có thể nhận được mảng giả của các đối số của nó là `arguments`, vì vậy `func.call(this, x)` nên được thay thế bằng `func.call(this, ...arguments)`.

Đây là một `cachingDecorator` mạnh mẽ hơn:

```
let worker = {
  slow(min, max) {
    alert(`Called with ${min},${max}`);
    return min + max;
  }
};

function cachingDecorator(func, hash) {
  let cache = new Map();
  return function() {
    let key = hash(arguments); // (*)
    if (cache.has(key)) {
      return cache.get(key);
    }

    let result = func.call(this, ...arguments); // (**)

    cache.set(key, result);
    return result;
  };
}

function hash(args) {
  return args[0] + ',' + args[1];
}

worker.slow = cachingDecorator(worker.slow, hash);

alert( worker.slow(3, 5) ); // hoạt động
alert( "Again " + worker.slow(3, 5) ); // giống nhau (cached)
```

Bây giờ nó hoạt động với bất kỳ số lượng đối số nào (mặc dù hàm băm cũng cần được điều chỉnh để cho phép bất kỳ số lượng đối số nào. Một cách thú vị để xử lý điều này sẽ được đề cập bên dưới).

Có hai thay đổi:

- Ở dòng `(*)` nó gọi `hash` để tạo một khóa duy nhất từ `arguments`. Ở đây chúng ta sử dụng một hàm "nối" đơn giản biến các đối số `(3, 5)` thành khóa `"3,5"`. Các trường hợp phức tạp hơn có thể yêu cầu các hàm băm khác.
- Sau đó `(**)` sử dụng `func.call(this, ...arguments)` để truyền cả ngữ cảnh và tất cả các đối số mà bộ bao nhận được (không chỉ cái đầu tiên) đến hàm gốc.

## [func.apply](#func-apply)

Thay vì `func.call(this, ...arguments)` chúng ta có thể sử dụng `func.apply(this, arguments)`.

Cú pháp của phương thức built-in [func.apply](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Function/apply) là:

```
func.apply(context, args)
```

Nó chạy `func` thiết lập `this=context` và sử dụng đối tượng giống mảng `args` làm danh sách các đối số.

Sự khác biệt cú pháp duy nhất giữa `call` và `apply` là `call` mong đợi một danh sách các đối số, trong khi `apply` nhận một đối tượng giống mảng với chúng.

Vì vậy, hai lời gọi sau hầu như tương đương:

```
func.call(context, ...args);
func.apply(context, args);
```

Chúng thực hiện cùng một lời gọi của `func` với ngữ cảnh và các đối số đã cho.

Chỉ có một sự khác biệt tinh tế liên quan đến `args`:

- Cú pháp spread `...` cho phép truyền *iterable* `args` làm danh sách cho `call`.
- `apply` chỉ chấp nhận *array-like* `args`.

…Và đối với các đối tượng vừa là iterable vừa là array-like, như một mảng thực sự, chúng ta có thể sử dụng bất kỳ cái nào, nhưng `apply` có lẽ sẽ nhanh hơn, vì hầu hết các động cơ JavaScript tối ưu hóa nội bộ nó tốt hơn.

Việc chuyển tất cả các đối số cùng với ngữ cảnh đến một hàm khác được gọi là *chuyển tiếp lời gọi*.

Đó là dạng đơn giản nhất của nó:

```
let wrapper = function() {
  return func.apply(this, arguments);
};
```

Khi mã bên ngoài gọi `wrapper` như vậy, nó không thể phân biệt được với lời gọi của hàm gốc `func`.

## [Thuê phương thức](#method-borrowing)

Bây giờ hãy thực hiện một cải tiến nhỏ hơn nữa trong hàm băm:

```
function hash(args) {
  return args[0] + ',' + args[1];
}
```

Cho đến nay, nó chỉ hoạt động với hai đối số. Sẽ tốt hơn nếu nó có thể nối bất kỳ số lượng `args` nào.

Giải pháp tự nhiên sẽ là sử dụng phương thức [arr.join](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/join):

```
function hash(args) {
  return args.join();
}
```

…Rất tiếc, điều đó sẽ không hoạt động. Bởi vì chúng ta đang gọi `hash(arguments)`, và đối tượng `arguments` vừa là iterable vừa là array-like, nhưng không phải là một mảng thực sự.

Vì vậy, gọi `join` trên nó sẽ thất bại, như chúng ta có thể thấy dưới đây:

```
function hash() {
  alert( arguments.join() ); // Lỗi: arguments.join không phải là hàm
}

hash(1, 2);
```

Vẫn còn, có một cách dễ dàng để sử dụng array join:

```
function hash() {
  alert( [].join.call(arguments) ); // 1,2
}

hash(1, 2);
```

Mẹo này được gọi là *thuê phương thức*.

Chúng ta lấy (thuê) một phương thức join từ một mảng thông thường (`[].join`) và sử dụng `[].join.call` để chạy nó trong ngữ cảnh của `arguments`.

Tại sao nó hoạt động?

Đó là vì thuật toán nội bộ của phương thức bản địa `arr.join(glue)` rất đơn giản.

Được trích xuất từ đặc tả gần như "nguyên bản":

1. Gọi `glue` là đối số đầu tiên hoặc, nếu không có đối số, thì là dấu phẩy `","`.
2. Gọi `result` là một chuỗi rỗng.
3. Nối `this[0]` vào `result`.
4. Nối `glue` và `this[1]`.
5. Nối `glue` và `this[2]`.
6. …Làm như vậy cho đến khi `this.length` mục được nối.
7. Trả về `result`.

Vì vậy, về mặt kỹ thuật nó lấy `this` và nối `this[0]`, `this[1]` …v.v. lại với nhau. Nó được viết một cách có chủ ý cho phép bất kỳ `this` array-like nào (không phải là ngẫu nhiên, nhiều phương thức làm theo thực hành này). Đó là lý do tại sao nó cũng hoạt động với `this=arguments`.

## [Bộ trang trí và thuộc tính hàm](#decorators-and-function-properties)

Nó nói chung là an toàn để thay thế một hàm hoặc một phương thức bằng một hàm được trang trí, trừ một điều nhỏ. Nếu hàm gốc có các thuộc tính trên nó, như `func.calledCount` hoặc bất cứ điều gì, thì hàm được trang trí sẽ không cung cấp chúng. Bởi vì đó là một bộ bao. Vì vậy, một người cần cẩn thận nếu họ sử dụng chúng.

Ví dụ, trong ví dụ trên nếu hàm `slow` có bất kỳ thuộc tính nào trên nó, thì `cachingDecorator(slow)` là một bộ bao không có chúng.

Một số bộ trang trí có thể cung cấp thuộc tính của riêng chúng. Ví dụ, một bộ trang trí có thể đếm xem hàm được gọi bao nhiêu lần và mất bao lâu, và công bố thông tin này thông qua các thuộc tính bộ bao.

Tồn tại một cách để tạo các bộ trang trí giữ quyền truy cập vào thuộc tính hàm, nhưng điều này yêu cầu sử dụng một đối tượng `Proxy` đặc biệt để bao bọc một hàm. Chúng ta sẽ thảo luận về nó sau trong bài viết [Proxy và Reflect](/proxy#proxy-apply).

## [Tóm tắt](#summary)

*Bộ trang trí* là một bộ bao xung quanh một hàm làm thay đổi hành vi của nó. Công việc chính vẫn được thực hiện bởi hàm.

Các bộ trang trí có thể được xem như là "tính năng" hoặc "khía cạnh" có thể được thêm vào một hàm. Chúng ta có thể thêm một hoặc nhiều. Và tất cả mà không cần thay đổi mã của nó!

Để triển khai `cachingDecorator`, chúng ta đã nghiên cứu các phương thức:

- [func.call(context, arg1, arg2…)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Function/call) – gọi `func` với ngữ cảnh và các đối số đã cho.
- [func.apply(context, args)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Function/apply) – gọi `func` truyền `context` làm `this` và `args` dạng array-like vào danh sách các đối số.

*Chuyển tiếp lời gọi* chung thường được thực hiện với `apply`:

```
let wrapper = function() {
  return original.apply(this, arguments);
};
```

Chúng ta cũng đã thấy một ví dụ về *thuê phương thức* khi chúng ta lấy một phương thức từ một đối tượng và `call` nó trong ngữ cảnh của một đối tượng khác. Điều này khá phổ biến khi lấy các phương thức mảng và áp dụng chúng cho `arguments`. Phương án thay thế là sử dụng đối tượng tham số còn lại là một mảng thực sự.

Có nhiều bộ trang trí tồn tại trong thực tế. Hãy kiểm tra xem bạn hiểu chúng tốt như thế nào bằng cách giải quyết các bài tập của chương này.

---

---

## Bài tập

## [Bài tập](#tasks)

### [Bộ trang trí Spy](#spy-decorator)

độ quan trọng: 5

Tạo một bộ trang trí `spy(func)` trả về một bộ bao lưu tất cả các lời gọi đến hàm trong thuộc tính `calls` của nó.

Mỗi lời gọi được lưu dưới dạng một mảng các đối số.

Ví dụ:

```
function work(a, b) {
  alert( a + b ); // work là một hàm hoặc phương thức tùy ý
}

work = spy(work);

work(1, 2); // 3
work(4, 5); // 9

for (let args of work.calls) {
  alert( 'call:' + args.join() ); // "call:1,2", "call:4,5"
}
```

P.S. Bộ trang trí đó đôi khi hữu ích cho unit-testing. Dạng nâng cao của nó là `sinon.spy` trong thư viện [Sinon.JS](http://sinonjs.org/).

[Mở một sandbox với các bài kiểm tra.](https://plnkr.co/edit/DMDbEyICftvJHWdq?p=preview)

solution

Bộ bao được trả về bởi `spy(f)` nên lưu trữ tất cả các đối số và sau đó sử dụng `f.apply` để chuyển tiếp lời gọi.

```
function spy(func) {

  function wrapper(...args) {
    // sử dụng ...args thay vì arguments để lưu trữ "mảng thực" trong wrapper.calls
    wrapper.calls.push(args);
    return func.apply(this, args);
  }

  wrapper.calls = [];

  return wrapper;
}
```

[Mở giải pháp với các bài kiểm tra trong một sandbox.](https://plnkr.co/edit/YBIyZYwz2ZkfIfIY?p=preview)

### [Bộ trang trí làm chậm](#delaying-decorator)

độ quan trọng: 5

Tạo một bộ trang trí `delay(f, ms)` làm chậm mỗi lời gọi của `f` đi `ms` mili giây.

Ví dụ:

```
function f(x) {
  alert(x);
}

// tạo các bộ bao
let f1000 = delay(f, 1000);
let f1500 = delay(f, 1500);

f1000("test"); // hiển thị "test" sau 1000ms
f1500("test"); // hiển thị "test" sau 1500ms
```

Nói cách khác, `delay(f, ms)` trả về biến thể của `f` bị "chậm đi `ms`".

Trong mã trên, `f` là một hàm của một đối số, nhưng giải pháp của bạn nên truyền tất cả các đối số và ngữ cảnh `this`.

[Mở một sandbox với các bài kiểm tra.](https://plnkr.co/edit/elpEfL4WRncZuzI2?p=preview)

solution

Giải pháp:

```
function delay(f, ms) {

  return function() {
    setTimeout(() => f.apply(this, arguments), ms);
  };

}

let f1000 = delay(alert, 1000);

f1000("test"); // hiển thị "test" sau 1000ms
```

Xin lưu ý cách một arrow function được sử dụng ở đây. Như chúng ta đã biết, các arrow function không có `this` và `arguments` riêng, vì vậy `f.apply(this, arguments)` lấy `this` và `arguments` từ bộ bao.

Nếu chúng ta truyền một hàm thông thường, `setTimeout` sẽ gọi nó không có đối số và `this=window` (giả sử chúng ta đang trong trình duyệt).

Chúng ta vẫn có thể truyền `this` đúng bằng cách sử dụng một biến trung gian, nhưng điều đó hơi cồng kềnh hơn:

```
function delay(f, ms) {

  return function(...args) {
    let savedThis = this; // lưu this vào một biến trung gian
    setTimeout(function() {
      f.apply(savedThis, args); // sử dụng nó ở đây
    }, ms);
  };

}
```

[Mở giải pháp với các bài kiểm tra trong một sandbox.](https://plnkr.co/edit/UmqFqUgYdZenLVc4?p=preview)

### [Bộ trang trí Debounce](#debounce-decorator)

độ quan trọng: 5

Kết quả của bộ trang trí `debounce(f, ms)` là một bộ bao làm gián đoạn các lời gọi đến `f` cho đến khi có `ms` mili giây không hoạt động (không có lời gọi, "thời gian nghỉ"), sau đó kích hoạt `f` một lần với các đối số cuối cùng.

Nói cách khác, `debounce` giống như một thư ký chấp nhận "cuộc gọi điện thoại", và chờ cho đến khi có `ms` mili giây yên tĩnh. Và chỉ sau đó nó chuyển thông tin cuộc gọi cuối cùng đến "ông chủ" (gọi hàm `f` thực tế).

Ví dụ, chúng ta có một hàm `f` và thay thế nó bằng `f = debounce(f, 1000)`.

Sau đó nếu hàm được bao gọi tại 0ms, 200ms và 500ms, và sau đó không có lời gọi nào nữa, thì hàm `f` thực tế sẽ chỉ được gọi một lần, tại 1500ms. Tức là: sau thời gian nghỉ 1000ms kể từ lời gọi cuối cùng.

![](/task/debounce/debounce.svg)

…Và nó sẽ nhận các đối số của lời gọi cuối cùng, các lời gọi khác bị bỏ qua.

Đây là mã cho nó (sử dụng bộ trang trí debounce từ [thư viện Lodash](https://lodash.com/docs/4.17.15#debounce)):

```
let f = _.debounce(alert, 1000);

f("a");
setTimeout( () => f("b"), 200);
setTimeout( () => f("c"), 500);
// hàm debounce chờ 1000ms sau lời gọi cuối cùng và sau đó chạy: alert("c")
```

Bây giờ là một ví dụ thực tế. Giả sử, người dùng đang nhập thứ gì đó, và chúng ta muốn gửi yêu cầu đến máy chủ khi việc nhập liệu kết thúc.

Không có lý do gì để gửi yêu cầu cho mỗi ký tự được gõ. Thay vào đó chúng ta muốn chờ, và sau đó xử lý toàn bộ kết quả.

Trong trình duyệt web, chúng ta có thể thiết lập một trình xử lý sự kiện – một hàm được gọi trên mỗi thay đổi của trường nhập liệu. Thông thường, một trình xử lý sự kiện được gọi rất thường xuyên, cho mỗi phím gõ. Nhưng nếu chúng ta `debounce` nó đi 1000ms, thì nó sẽ chỉ được gọi một lần, sau 1000ms kể từ lần nhập cuối cùng.

Trong ví dụ trực quan này, trình xử lý đặt kết quả vào một hộp bên dưới, hãy thử nó:

Nhìn thấy không? Đầu vào thứ hai gọi hàm debounce, vì vậy nội dung của nó được xử lý sau 1000ms kể từ lần nhập cuối cùng.

Vì vậy, `debounce` là một cách tuyệt vời để xử lý một chuỗi các sự kiện: dù là chuỗi các phím bấm, chuyển động chuột hoặc thứ gì đó khác.

Nó chờ thời gian đã cho sau lời gọi cuối cùng, và sau đó chạy hàm của nó, có thể xử lý kết quả.

Bài tập là triển khai bộ trang trí `debounce`.

Gợi ý: đó chỉ là vài dòng nếu bạn suy nghĩ về nó :)

[Mở một sandbox với các bài kiểm tra.](https://plnkr.co/edit/mCXThE9QB1dbfx9n?p=preview)

solution

```
function debounce(func, ms) {
  let timeout;
  return function() {
    clearTimeout(timeout);
    timeout = setTimeout(() => func.apply(this, arguments), ms);
  };
}
```

Một lời gọi đến `debounce` trả về một bộ bao. Khi được gọi, nó lên lịch gọi hàm gốc sau `ms` đã cho và hủy thời gian chờ trước đó.

[Mở giải pháp với các bài kiểm tra trong một sandbox.](https://plnkr.co/edit/U8aBqREMyhhzUssh?p=preview)

### [Bộ trang trí Throttle](#throttle-decorator)

độ quan trọng: 5

Tạo một bộ trang trí "throttle" `throttle(f, ms)` – trả về một bộ bao.

Khi nó được gọi nhiều lần, nó chuyển lời gọi đến `f` nhiều nhất một lần mỗi `ms` mili giây.

So với bộ trang trí debounce, hành vi hoàn toàn khác:

- `debounce` chạy hàm một lần sau "thời gian nghỉ". Tốt cho việc xử lý kết quả cuối cùng.
- `throttle` chạy nó không thường xuyên hơn thời gian `ms` đã cho. Tốt cho các cập nhật thường xuyên không nên quá thường xuyên.

Nói cách khác, `throttle` giống như một thư ký chấp nhận cuộc gọi điện thoại, nhưng làm phiền ông chủ (gọi `f` thực tế) không thường xuyên hơn một lần mỗi `ms` mili giây.

Hãy kiểm tra ứng dụng thực tế để hiểu rõ hơn yêu cầu này và xem nó đến từ đâu.

**Ví dụ, chúng ta muốn theo dõi chuyển động chuột.**

Trong trình duyệt chúng ta có thể thiết lập một hàm để chạy tại mỗi chuyển động chuột và lấy vị trí con trỏ khi nó di chuyển. Trong quá trình sử dụng chuột tích cực, hàm này thường chạy rất thường xuyên, có thể khoảng 100 lần mỗi giây (mỗi 10 ms).
**Chúng ta muốn cập nhật một số thông tin trên trang web khi con trỏ di chuyển.**

…Nhưng hàm `update()` quá nặng để làm điều đó trên mỗi chuyển động vi mô. Cũng không có lý do gì để cập nhật thường xuyên hơn một lần mỗi 100ms.

Vì vậy, chúng ta sẽ bao bọc nó vào bộ trang trí: sử dụng `throttle(update, 100)` làm hàm để chạy trên mỗi chuyển động chuột thay vì `update()` gốc. Bộ trang trí sẽ được gọi thường xuyên, nhưng chuyển tiếp lời gọi đến `update()` nhiều nhất một lần mỗi 100ms.

Theo trực quan, nó sẽ trông như thế này:

1. Đối với chuyển động chuột đầu tiên, biến thể được trang trí ngay lập tức chuyển lời gọi đến `update`. Điều đó quan trọng, người dùng nhìn thấy phản ứng của chúng ta với chuyển động của họ ngay lập tức.
2. Sau đó khi chuột di chuyển tiếp, cho đến khi `100ms` không có gì xảy ra. Biến thể được trang trí bỏ qua các lời gọi.
3. Vào cuối `100ms` – một lần `update` khác xảy ra với tọa độ cuối cùng.
4. Sau đó, cuối cùng, chuột dừng lại ở đâu đó. Biến thể được trang trí chờ cho đến khi `100ms` hết hạn và sau đó chạy `update` với tọa độ cuối cùng. Vì vậy, khá quan trọng, tọa độ chuột cuối cùng được xử lý.

Một ví dụ mã:

```
function f(a) {
  console.log(a);
}

// f1000 chuyển lời gọi đến f nhiều nhất một lần mỗi 1000 ms
let f1000 = throttle(f, 1000);

f1000(1); // hiển thị 1
f1000(2); // (throttling, 1000ms chưa hết)
f1000(3); // (throttling, 1000ms chưa hết)

// khi thời gian 1000 ms hết hạn...
// ...xuất ra 3, giá trị trung gian 2 bị bỏ qua
```

P.S. Các đối số và ngữ cảnh `this` được truyền đến `f1000` nên được truyền đến `f` gốc.

[Mở một sandbox với các bài kiểm tra.](https://plnkr.co/edit/XFaXFLWQWlqobruM?p=preview)

solution

```
function throttle(func, ms) {

  let isThrottled = false,
    savedArgs,
    savedThis;

  function wrapper() {

    if (isThrottled) { // (2)
      savedArgs = arguments;
      savedThis = this;
      return;
    }
    isThrottled = true;

    func.apply(this, arguments); // (1)

    setTimeout(function() {
      isThrottled = false; // (3)
      if (savedArgs) {
        wrapper.apply(savedThis, savedArgs);
        savedArgs = savedThis = null;
      }
    }, ms);
  }

  return wrapper;
}
```

Một lời gọi đến `throttle(func, ms)` trả về `wrapper`.

1. Trong lời gọi đầu tiên, `wrapper` chỉ chạy `func` và đặt trạng thái nghỉ (`isThrottled = true`).
2. Trong trạng thái này tất cả các lời gọi được ghi nhớ trong `savedArgs/savedThis`. Xin lưu ý rằng cả ngữ cảnh và các đối số đều quan trọng như nhau và nên được ghi nhớ. Chúng ta cần chúng đồng thời để tái tạo lời gọi.
3. Sau `ms` mili giây, `setTimeout` kích hoạt. Trạng thái nghỉ bị xóa (`isThrottled = false`) và, nếu chúng ta đã bỏ qua các lời gọi, `wrapper` được thực thi với các đối số và ngữ cảnh ghi nhớ cuối cùng.

Bước 3 chạy không phải `func`, mà là `wrapper`, bởi vì chúng ta không chỉ cần thực thi `func`, mà còn một lần nữa nhập vào trạng thái nghỉ và thiết lập thời gian chờ để đặt lại nó.

[Mở giải pháp với các bài kiểm tra trong một sandbox.](https://plnkr.co/edit/kp1bPN27eeDsC5Ch?p=preview)