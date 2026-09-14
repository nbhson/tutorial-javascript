# Function binding

> Source: [https://javascript.info/bind](https://javascript.info/bind)

<!-- fetched: 2026-09-14 -->

Khi truyền phương thức của đối tượng làm callback, chẳng hạn như cho `setTimeout`, có một vấn đề đã biết: "mất `this`".

Trong chương này, chúng ta sẽ xem các cách để sửa chữa nó.

## [Mất "this"](#losing-this)

Chúng ta đã thấy các ví dụ về việc mất `this`. Một khi phương thức được chuyển ở đâu đó riêng biệt với đối tượng – `this` bị mất.

Sau đây là cách nó có thể xảy ra với `setTimeout`:

```
let user = {
  firstName: "John",
  sayHi() {
    alert(`Hello, ${this.firstName}!`);
  }
};

setTimeout(user.sayHi, 1000); // Hello, undefined!
```

Như chúng ta có thể thấy, kết quả hiển thị không phải "John" cho `this.firstName`, mà là `undefined`!

Điều đó là vì `setTimeout` nhận được hàm `user.sayHi`, riêng biệt với đối tượng. Dòng cuối cùng có thể được viết lại như sau:

```
let f = user.sayHi;
setTimeout(f, 1000); // mất ngữ cảnh user
```

Phương thức `setTimeout` trong trình duyệt hơi đặc biệt: nó đặt `this=window` cho cuộc gọi hàm (trong Node.js, `this` trở thành đối tượng bộ hẹn giờ, nhưng điều đó không thực sự quan trọng ở đây). Vì vậy đối với `this.firstName`, nó cố gắng lấy `window.firstName`, thứ không tồn tại. Trong các trường hợp tương tự khác, thường thì `this` chỉ trở thành `undefined`.

Bài toán khá điển hình – chúng ta muốn truyền một phương thức đối tượng ở đâu đó (ở đây – đến bộ lập lịch) nơi nó sẽ được gọi. Làm thế nào để đảm bảo rằng nó sẽ được gọi trong đúng ngữ cảnh?

## [Giải pháp 1: một hàm bao](#solution-1-a-wrapper)

Giải pháp đơn giản nhất là sử dụng một hàm bao:

```
let user = {
  firstName: "John",
  sayHi() {
    alert(`Hello, ${this.firstName}!`);
  }
};

setTimeout(function() {
  user.sayHi(); // Hello, John!
}, 1000);
```

Bây giờ nó hoạt động, vì nó nhận được `user` từ môi trường lexical bên ngoài, và sau đó gọi phương thức một cách bình thường.

Giống nhau, nhưng ngắn gọn hơn:

```
setTimeout(() => user.sayHi(), 1000); // Hello, John!
```

Có vẻ ổn, nhưng một điểm yếu nhẹ xuất hiện trong cấu trúc mã của chúng ta.

Nếu trước khi `setTimeout` kích hoạt (có độ trễ một giây!) `user` thay đổi giá trị? Sau đó, đột nhiên, nó sẽ gọi sai đối tượng!

```
let user = {
  firstName: "John",
  sayHi() {
    alert(`Hello, ${this.firstName}!`);
  }
};

setTimeout(() => user.sayHi(), 1000);

// ...giá trị của user thay đổi trong vòng 1 giây
user = {
  sayHi() { alert("Another user in setTimeout!"); }
};

// Another user in setTimeout!
```

Giải pháp tiếp theo đảm bảo rằng điều như vậy sẽ không xảy ra.

## [Giải pháp 2: bind](#solution-2-bind)

Các hàm cung cấp một phương thức tích hợp [bind](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Function/bind) cho phép sửa chữa `this`.

Cú pháp cơ bản là:

```
// cú pháp phức tạp hơn sẽ đến sau
let boundFunc = func.bind(context);
```

Kết quả của `func.bind(context)` là một đối tượng "đặc biệt" giống như hàm, có thể gọi được như một hàm và truyền cuộc gọi đến `func` một cách trong suốt, đặt `this=context`.

Nói cách khác, gọi `boundFunc` giống như `func` với `this` cố định.

Chẳng hạn, ở đây `funcUser` truyền một cuộc gọi đến `func` với `this=user`:

```
let user = {
  firstName: "John"
};

function func() {
  alert(this.firstName);
}

let funcUser = func.bind(user);
funcUser(); // John
```

Ở đây `func.bind(user)` là một "biến thể đã bound" của `func`, với `this=user` cố định.

Tất cả các đối số được truyền đến `func` gốc "nguyên bản", chẳng hạn:

```
let user = {
  firstName: "John"
};

function func(phrase) {
  alert(phrase + ', ' + this.firstName);
}

// bind this với user
let funcUser = func.bind(user);

funcUser("Hello"); // Hello, John (đối số "Hello" được truyền, và this=user)
```

Bây giờ hãy thử với một phương thức đối tượng:

```
let user = {
  firstName: "John",
  sayHi() {
    alert(`Hello, ${this.firstName}!`);
  }
};

let sayHi = user.sayHi.bind(user); // (*)

// có thể chạy nó mà không cần đối tượng
sayHi(); // Hello, John!

setTimeout(sayHi, 1000); // Hello, John!

// ngay cả khi giá trị của user thay đổi trong vòng 1 giây
// sayHi sử dụng giá trị pre-bound là tham chiếu đến đối tượng user cũ
user = {
  sayHi() { alert("Another user in setTimeout!"); }
};
```

Ở dòng `(*)`, chúng ta lấy phương thức `user.sayHi` và bind nó với `user`. `sayHi` là một hàm "bound", có thể gọi riêng lẻ hoặc truyền cho `setTimeout` – không quan trọng, ngữ cảnh sẽ đúng.

Ở đây chúng ta có thể thấy rằng các đối số được truyền "nguyên bản", chỉ có `this` được cố định bởi `bind`:

```
let user = {
  firstName: "John",
  say(phrase) {
    alert(`${phrase}, ${this.firstName}!`);
  }
};

let say = user.say.bind(user);

say("Hello"); // Hello, John! ("Hello" là đối số được truyền đến say)
say("Bye"); // Bye, John! ("Bye" được truyền đến say)
```

Phương thức tiện lợi: `bindAll`

Nếu một đối tượng có nhiều phương thức và chúng ta dự định chuyển nó đi khắp nơi, thì chúng ta có thể bind tất cả chúng trong một vòng lặp:

```
for (let key in user) {
  if (typeof user[key] == 'function') {
    user[key] = user[key].bind(user);
  }
}
```

Các thư viện JavaScript cũng cung cấp các hàm để bind hàng loạt tiện lợi, chẳng hạn như [\_.bindAll(object, methodNames)](https://lodash.com/docs#bindAll) trong lodash.

## [Hàm partial](#partial-functions)

Cho đến nay chúng ta chỉ đang nói về bind `this`. Hãy nâng lên một bước.

Chúng ta có thể bind không chỉ `this`, mà còn các đối số. Điều đó hiếm khi được thực hiện, nhưng đôi khi có thể hữu ích.

Cú pháp đầy đủ của `bind`:

```
let bound = func.bind(context, [arg1], [arg2], ...);
```

Nó cho phép bind context như `this` và các đối số bắt đầu của hàm.

Chẳng hạn, chúng ta có một hàm nhân `mul(a, b)`:

```
function mul(a, b) {
  return a * b;
}
```

Hãy sử dụng `bind` để tạo hàm `double` trên cơ sở của nó:

```
function mul(a, b) {
  return a * b;
}

let double = mul.bind(null, 2);

alert( double(3) ); // = mul(2, 3) = 6
alert( double(4) ); // = mul(2, 4) = 8
alert( double(5) ); // = mul(2, 5) = 10
```

Cuộc gọi đến `mul.bind(null, 2)` tạo ra một hàm mới `double` truyền các cuộc gọi đến `mul`, cố định `null` làm context và `2` làm đối số đầu tiên. Các đối số tiếp theo được truyền "nguyên bản".

Điều đó được gọi là [partial function application](https://en.wikipedia.org/wiki/Partial_application) – chúng ta tạo ra một hàm mới bằng cách cố định một số tham số của hàm hiện có.

Xin lưu ý rằng chúng ta thực sự không sử dụng `this` ở đây. Nhưng `bind` yêu cầu nó, vì vậy chúng ta phải đặt vào thứ gì đó như `null`.

Hàm `triple` trong mã dưới đây gấp ba giá trị:

```
function mul(a, b) {
  return a * b;
}

let triple = mul.bind(null, 3);

alert( triple(3) ); // = mul(3, 3) = 9
alert( triple(4) ); // = mul(3, 4) = 12
alert( triple(5) ); // = mul(3, 5) = 15
```

Tại sao chúng ta thường tạo một hàm partial?

Lợi ích là chúng ta có thể tạo ra một hàm độc lập với tên dễ đọc (`double`, `triple`). Chúng ta có thể sử dụng nó và không cần cung cấp đối số đầu tiên mỗi lần vì nó đã được cố định với `bind`.

Trong các trường hợp khác, partial application hữu ích khi chúng ta có một hàm rất tổng quát và muốn một biến thể ít phổ quát hơn của nó để tiện lợi.

Chẳng hạn, chúng ta có một hàm `send(from, to, text)`. Sau đó, bên trong một đối tượng `user` chúng ta có thể muốn sử dụng biến thể partial của nó: `sendTo(to, text)` gửi từ người dùng hiện tại.

## [Partial mà không cần context](#going-partial-without-context)

Nếu chúng ta muốn cố định một số đối số, nhưng không phải context `this`? Chẳng hạn, cho một phương thức đối tượng.

`bind` native không cho phép điều đó. Chúng ta không thể chỉ bỏ qua context và nhảy đến các đối số.

May mắn thay, một hàm `partial` để chỉ bind các đối số có thể được triển khai một cách dễ dàng.

Như thế này:

```
function partial(func, ...argsBound) {
  return function(...args) { // (*)
    return func.call(this, ...argsBound, ...args);
  }
}

// Usage:
let user = {
  firstName: "John",
  say(time, phrase) {
    alert(`[${time}] ${this.firstName}: ${phrase}!`);
  }
};

// add a partial method with fixed time
user.sayNow = partial(user.say, new Date().getHours() + ':' + new Date().getMinutes());

user.sayNow("Hello");
// Something like:
// [10:00] John: Hello!
```

Kết quả của cuộc gọi `partial(func[, arg1, arg2...])` là wrapper `(*)` gọi `func` với:

- Cùng `this` như nó nhận được (đối với cuộc gọi `user.sayNow` thì đó là `user`)
- Sau đó nó đưa `...argsBound` – các đối số từ cuộc gọi `partial` (`"10:00"`)
- Sau đó nó đưa `...args` – các đối số được truyền cho wrapper (`"Hello"`)

Thật dễ dàng để làm điều đó với spread syntax, đúng không?

Cũng có một sẵn [\_.partial](https://lodash.com/docs#partial) implementation từ thư viện lodash.

## [Tóm tắt](#summary)

Method `func.bind(context, ...args)` trả về một "biến thể bound" của hàm `func` cố định context `this` và các đối số đầu tiên nếu có.

Thông thường chúng ta áp dụng `bind` để cố định `this` cho một phương thức đối tượng, vì vậy chúng ta có thể truyền nó ở đâu đó. Chẳng hạn, đến `setTimeout`.

Khi chúng ta cố định một số đối số của một hàm hiện có, hàm kết quả (ít phổ quát hơn) được gọi là *partially applied* hoặc *partial*.

Partials tiện lợi khi chúng ta không muốn lặp lại cùng một đối số nhiều lần. Giống như nếu chúng ta có một hàm `send(from, to)`, và `from` luôn luôn phải giống nhau cho nhiệm vụ của chúng ta, chúng ta có thể lấy một partial và tiếp tục với nó.

---

---

## Bài tập

## [Bài tập](#tasks)

### [Bound function như một phương thức](#bound-function-as-a-method)

importance: 5

Kết quả sẽ là gì?

```
function f() {
  alert( this ); // ?
}

let user = {
  g: f.bind(null)
};

user.g();
```

solution

Câu trả lời: `null`.

```
function f() {
  alert( this ); // null
}

let user = {
  g: f.bind(null)
};

user.g();
```

Context của một bound function bị hard-fixed. Không có cách nào để thay đổi nó thêm.

Vì vậy, ngay cả khi chúng ta chạy `user.g()`, hàm gốc được gọi với `this=null`.

### [Second bind](#second-bind)

importance: 5

Chúng ta có thể thay đổi `this` bằng cách bind bổ sung không?

Kết quả sẽ là gì?

```
function f() {
  alert(this.name);
}

f = f.bind( {name: "John"} ).bind( {name: "Ann" } );

f();
```

solution

Câu trả lời: **John**.

```
function f() {
  alert(this.name);
}

f = f.bind( {name: "John"} ).bind( {name: "Pete"} );

f(); // John
```

Object [bound function](https://tc39.github.io/ecma262/#sec-bound-function-exotic-objects) trả về bởi `f.bind(...)` ghi nhớ context (và các đối số nếu có) chỉ tại thời điểm tạo.

Một hàm không thể được re-bind.

### [Function property sau khi bind](#function-property-after-bind)

importance: 5

Có một giá trị trong property của một hàm. Nó sẽ thay đổi sau khi `bind` không? Tại sao có, hoặc tại sao không?

```
function sayHi() {
  alert( this.name );
}
sayHi.test = 5;

let bound = sayHi.bind({
  name: "John"
});

alert( bound.test ); // what will be the output? why?
```

solution

Câu trả lời: `undefined`.

Kết quả của `bind` là một object khác. Nó không có property `test`.

### [Sửa một hàm bị mất "this"](#fix-a-function-that-loses-this)

importance: 5

Cuộc gọi đến `askPassword()` trong mã dưới đây nên kiểm tra mật khẩu và sau đó gọi `user.loginOk/loginFail` tùy thuộc vào câu trả lời.

Nhưng nó gây ra lỗi. Tại sao?

Sửa dòng được đánh dấu để mọi thứ hoạt động đúng (các dòng khác không được thay đổi).

```
function askPassword(ok, fail) {
  let password = prompt("Password?", '');
  if (password == "rockstar") ok();
  else fail();
}

let user = {
  name: 'John',

  loginOk() {
    alert(`${this.name} logged in`);
  },

  loginFail() {
    alert(`${this.name} failed to log in`);
  },

};

askPassword(user.loginOk, user.loginFail);
```

solution

Lỗi xảy ra vì `askPassword` nhận được các hàm `loginOk/loginFail` mà không có đối tượng.

Khi nó gọi chúng, chúng mặc nhiên coi `this=undefined`.

Hãy `bind` context:

```
function askPassword(ok, fail) {
  let password = prompt("Password?", '');
  if (password == "rockstar") ok();
  else fail();
}

let user = {
  name: 'John',

  loginOk() {
    alert(`${this.name} logged in`);
  },

  loginFail() {
    alert(`${this.name} failed to log in`);
  },

};

askPassword(user.loginOk.bind(user), user.loginFail.bind(user));
```

Bây giờ nó hoạt động.

Một giải pháp thay thế có thể là:

```
//...
askPassword(() => user.loginOk(), () => user.loginFail());
```

Thông thường điều đó cũng hoạt động và trông tốt.

Tuy nhiên, nó kém tin cậy hơn một chút trong các tình huống phức tạp hơn nơi biến `user` có thể thay đổi *sau khi* `askPassword` được gọi, nhưng *trước khi* người dùng trả lời và gọi `() => user.loginOk()`.

### [Partial application cho login](#partial-application-for-login)

importance: 5

Bài toán là một biến thể phức tạp hơn của [Fix a function that loses "this"](/task/question-use-bind).

Đối tượng `user` đã được sửa đổi. Bây giờ thay vì hai hàm `loginOk/loginFail`, nó có một hàm duy nhất `user.login(true/false)`.

Chúng ta nên truyền `askPassword` gì trong mã dưới đây, để nó gọi `user.login(true)` như `ok` và `user.login(false)` như `fail`?

```
function askPassword(ok, fail) {
  let password = prompt("Password?", '');
  if (password == "rockstar") ok();
  else fail();
}

let user = {
  name: 'John',

  login(result) {
    alert( this.name + (result ? ' logged in' : ' failed to log in') );
  }
};

askPassword(?, ?); // ?
```

Các thay đổi của bạn chỉ nên sửa đổi fragment được đánh dấu.

solution

1. Hoặc sử dụng một hàm wrapper, arrow để ngắn gọn:

   ```
   askPassword(() => user.login(true), () => user.login(false));
   ```

   Bây giờ nó nhận được `user` từ các biến bên ngoài và chạy nó theo cách bình thường.
2. Hoặc tạo một partial function từ `user.login` sử dụng `user` làm context và có đối số đầu tiên đúng:

   ```
   askPassword(user.login.bind(user, true), user.login.bind(user, false));
   ```
