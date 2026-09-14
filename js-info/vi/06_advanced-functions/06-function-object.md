# Function object, NFE

> Source: [https://javascript.info/function-object](https://javascript.info/function-object)

<!-- fetched: 2026-09-14 -->

Như chúng ta đã biết, một hàm trong JavaScript là một giá trị.

Mọi giá trị trong JavaScript đều có kiểu. Hàm thuộc kiểu gì?

Trong JavaScript, hàm là các đối tượng.

Một cách tốt để hình dung về hàm là các "action object" có thể gọi được. Chúng ta không chỉ có thể gọi chúng, mà còn có thể xử lý chúng như các đối tượng: thêm/xóa thuộc tính, truyền theo tham chiếu, v.v.

## [Thuộc tính "name"](#the-name-property)

Các hàm đối tượng chứa một số thuộc tính có ích.

Ví dụ, tên của hàm có thể truy cập được qua thuộc tính "name":

```
function sayHi() {
  alert("Hi");
}

alert(sayHi.name); // sayHi
```

Điều khá vui là logic gán tên rất thông minh. Nó cũng gán đúng tên cho một hàm ngay cả khi nó được tạo ra mà không có tên, sau đó ngay lập tức được gán:

```
let sayHi = function() {
  alert("Hi");
};

alert(sayHi.name); // sayHi (đã có tên!)
```

Nó cũng hoạt động nếu việc gán được thực hiện thông qua giá trị mặc định:

```
function f(sayHi = function() {}) {
  alert(sayHi.name); // sayHi (hoạt động!)
}

f();
```

Trong đặc tả, tính năng này được gọi là "tên ngữ cảnh". Nếu hàm không cung cấp tên, thì trong một phép gán, nó sẽ được xác định từ ngữ cảnh.

Phương thức của đối tượng cũng có tên:

```
let user = {

  sayHi() {
    // ...
  },

  sayBye: function() {
    // ...
  }

}

alert(user.sayHi.name); // sayHi
alert(user.sayBye.name); // sayBye
```

Tuy nhiên không có bí ẩn nào ở đây. Có những trường hợp không thể xác định được tên đúng. Trong trường hợp đó, thuộc tính name là rỗng, như ở đây:

```
// hàm được tạo bên trong mảng
let arr = [function() {}];

alert( arr[0].name ); // <chuỗi rỗng>
// engine không có cách nào thiết lập tên đúng, nên không có tên
```

Tuy nhiên, trong thực tế, hầu hết các hàm đều có tên.

## [Thuộc tính "length"](#the-length-property)

Có một thuộc tính tích hợp khác là "length", trả về số lượng tham số của hàm, ví dụ:

```
function f1(a) {}
function f2(a, b) {}
function many(a, b, ...more) {}

alert(f1.length); // 1
alert(f2.length); // 2
alert(many.length); // 2
```

Ở đây chúng ta thấy rằng các tham số rest không được tính.

Thuộc tính `length` đôi khi được sử dụng cho [introspection](https://en.wikipedia.org/wiki/Type_introspection) trong các hàm hoạt động trên các hàm khác.

Ví dụ, trong đoạn mã dưới đây, hàm `ask` nhận một `question` để hỏi và một số lượng tùy ý các hàm `handler` để gọi.

Sau khi người dùng đưa ra câu trả lời, hàm sẽ gọi các handler. Chúng ta có thể truyền hai loại handler:

- Một hàm không có tham số, chỉ được gọi khi người dùng đưa ra câu trả lời tích cực.
- Một hàm có tham số, được gọi trong cả hai trường hợp và trả về câu trả lời.

Để gọi `handler` theo cách đúng, chúng ta kiểm tra thuộc tính `handler.length`.

Ý tưởng là chúng ta có một cú pháp handler đơn giản, không có tham số cho các trường hợp tích cực (biến thể phổ biến nhất), nhưng vẫn có thể hỗ trợ các handler phổ quát:

```
function ask(question, ...handlers) {
  let isYes = confirm(question);

  for(let handler of handlers) {
    if (handler.length == 0) {
      if (isYes) handler();
    } else {
      handler(isYes);
    }
  }

}

// cho câu trả lời tích cực, cả hai handler đều được gọi
// cho câu trả lời tiêu cực, chỉ có handler thứ hai được gọi
ask("Question?", () => alert('You said yes'), result => alert(result));
```

Đây là một trường hợp đặc biệt của những gì được gọi là [đa hình](https://en.wikipedia.org/wiki/Polymorphism_(computer_science)) – xử lý các tham số khác nhau tùy thuộc vào kiểu của chúng, hoặc trong trường hợp của chúng ta, tùy thuộc vào `length`. Ý tưởng này thực sự có ứng dụng trong các thư viện JavaScript.

## [Thuộc tính tùy chỉnh](#custom-properties)

Chúng ta cũng có thể thêm các thuộc tính của riêng mình.

Ở đây chúng ta thêm thuộc tính `counter` để theo dõi tổng số lần gọi:

```
function sayHi() {
  alert("Hi");

  // hãy đếm xem chúng ta chạy bao nhiêu lần
  sayHi.counter++;
}
sayHi.counter = 0; // giá trị ban đầu

sayHi(); // Hi
sayHi(); // Hi

alert( `Called ${sayHi.counter} times` ); // Called 2 times
```

Một thuộc tính không phải là một biến

Một thuộc tính được gán cho một hàm như `sayHi.counter = 0` không *định nghĩa* một biến địa phương `counter` bên trong nó. Nói cách khác, thuộc tính `counter` và biến `let counter` là hai thứ không liên quan.

Chúng ta có thể xử lý một hàm như một đối tượng, lưu trữ các thuộc tính trong đó, nhưng điều đó không ảnh hưởng đến việc thực thi của nó. Các biến không phải là thuộc tính của hàm và ngược lại. Đây chỉ là những thế giới song song.

Thuộc tính của hàm đôi khi có thể thay thế closure. Ví dụ, chúng ta có thể viết lại ví dụ hàm counter từ chương [Phạm vi biến, closure](/closure) để sử dụng thuộc tính hàm:

```
function makeCounter() {
  // thay vì:
  // let count = 0

  function counter() {
    return counter.count++;
  };

  counter.count = 0;

  return counter;
}

let counter = makeCounter();
alert( counter() ); // 0
alert( counter() ); // 1
```

Biến `count` bây giờ được lưu trực tiếp trong hàm, không phải trong Lexical Environment bên ngoài.

Như vậy có tốt hơn hay không so với việc sử dụng closure?

Sự khác biệt chính là nếu giá trị của `count` sống trong một biến bên ngoài, thì mã bên ngoài không thể truy cập được nó. Chỉ có các hàm lồng nhau mới có thể sửa đổi nó. Và nếu nó được gắn với một hàm, thì điều đó là có thể:

```
function makeCounter() {

  function counter() {
    return counter.count++;
  };

  counter.count = 0;

  return counter;
}

let counter = makeCounter();

counter.count = 10;
alert( counter() ); // 10
```

Vì vậy, lựa chọn cách triển khai phụ thuộc vào mục tiêu của chúng ta.

## [Named Function Expression](#named-function-expression)

Named Function Expression, hay NFE, là thuật ngữ dùng cho các Function Expression có tên.

Ví dụ, hãy lấy một Function Expression thông thường:

```
let sayHi = function(who) {
  alert(`Hello, ${who}`);
};
```

Và thêm một tên vào nó:

```
let sayHi = function func(who) {
  alert(`Hello, ${who}`);
};
```

Chúng ta đã đạt được điều gì ở đây? Mục đích của tên `"func"` bổ sung là gì?

Đầu tiên hãy lưu ý, rằng chúng ta vẫn đang có một Function Expression. Việc thêm tên `"func"` sau `function` không biến nó thành Function Declaration, vì nó vẫn được tạo ra như một phần của biểu thức gán.

Việc thêm tên như vậy cũng không phá vỡ bất cứ điều gì.

Hàm vẫn có thể được gọi như `sayHi()`:

```
let sayHi = function func(who) {
  alert(`Hello, ${who}`);
};

sayHi("John"); // Hello, John
```

Có hai điều đặc biệt về tên `func`, đó là lý do cho việc sử dụng nó:

1. Nó cho phép hàm tham chiếu đến chính nó bên trong.
2. Nó không hiển thị ra bên ngoài hàm.

Ví dụ, hàm `sayHi` bên dưới gọi lại chính nó với `"Guest"` nếu không có `who` được cung cấp:

```
let sayHi = function func(who) {
  if (who) {
    alert(`Hello, ${who}`);
  } else {
    func("Guest"); // sử dụng func để gọi lại chính nó
  }
};

sayHi(); // Hello, Guest

// Nhưng cái này sẽ không hoạt động:
func(); // Error, func is not defined (không hiển thị ra bên ngoài hàm)
```

Tại sao chúng ta sử dụng `func`? Tại sao không chỉ sử dụng `sayHi` cho lệnh gọi lồng nhau?

Thực tế, trong hầu hết các trường hợp chúng ta có thể:

```
let sayHi = function(who) {
  if (who) {
    alert(`Hello, ${who}`);
  } else {
    sayHi("Guest");
  }
};
```

Vấn đề với đoạn mã đó là `sayHi` có thể thay đổi trong mã bên ngoài. Nếu hàm được gán cho một biến khác, thì mã sẽ bắt đầu đưa ra lỗi:

```
let sayHi = function(who) {
  if (who) {
    alert(`Hello, ${who}`);
  } else {
    sayHi("Guest"); // Error: sayHi is not a function
  }
};

let welcome = sayHi;
sayHi = null;

welcome(); // Error, lệnh gọi nested sayHi không hoạt động nữa!
```

Điều đó xảy ra vì hàm lấy `sayHi` từ lexical environment bên ngoài của nó. Không có `sayHi` cục bộ, nên biến bên ngoài được sử dụng. Và tại thời điểm gọi, `sayHi` bên ngoài đó là `null`.

Tên tùy chọn mà chúng ta có thể đặt vào Function Expression là để giải quyết chính xác những vấn đề như vậy.

Hãy sử dụng nó để sửa mã của chúng ta:

```
let sayHi = function func(who) {
  if (who) {
    alert(`Hello, ${who}`);
  } else {
    func("Guest"); // Giờ mọi thứ ổn
  }
};

let welcome = sayHi;
sayHi = null;

welcome(); // Hello, Guest (lồng gọi hoạt động)
```

Bây giờ nó hoạt động, vì tên `"func"` là cục bộ đối với hàm. Nó không được lấy từ bên ngoài (và không hiển thị ra bên ngoài). Đặc tả đảm bảo rằng nó sẽ luôn tham chiếu đến hàm hiện tại.

Mã bên ngoài vẫn có biến `sayHi` hoặc `welcome`. Và `func` là một "tên hàm nội bộ", cách để hàm gọi chính nó một cách đáng tin cậy.

Không có tính năng này cho Function Declaration

Tính năng "tên nội bộ" được mô tả ở đây chỉ khả dụng cho các Function Expression, không phải cho Function Declaration. Đối với Function Declaration, không có cú pháp để thêm "tên nội bộ".

Đôi khi, khi chúng ta cần một tên nội bộ đáng tin cậy, đó là lý do để chuyển đổi một Function Declaration sang dạng Named Function Expression.

## [Tổng kết](#summary)

Hàm là các đối tượng.

Ở đây chúng ta đã tìm hiểu các thuộc tính của chúng:

- `name` – tên của hàm. Thường được lấy từ định nghĩa hàm, nhưng nếu không có, JavaScript sẽ cố gắng đoán nó từ ngữ cảnh (ví dụ: một phép gán).
- `length` – số lượng đối số trong định nghĩa hàm. Các tham số Rest không được tính.

Nếu hàm được khai báo là một Function Expression (không phải trong luồng mã chính), và nó mang tên, thì nó được gọi là Named Function Expression. Tên có thể được sử dụng bên trong để tham chiếu đến chính nó, cho các lệnh gọi đệ quy hoặc tương tự.

Ngoài ra, hàm có thể mang các thuộc tính bổ sung. Nhiều thư viện JavaScript nổi tiếng sử dụng tính năng này rất hiệu quả.

Họ tạo ra một hàm "chính" và gắn nhiều hàm "hỗ trợ" khác vào nó. Ví dụ, thư viện [jQuery](https://jquery.com) tạo ra một hàm tên là `$`. Thư viện [lodash](https://lodash.com) tạo ra một hàm `_`, sau đó thêm các thuộc tính `_.clone`, `_.keyBy` và các thuộc tính khác vào nó (xem [tài liệu](https://lodash.com/docs) khi bạn muốn tìm hiểu thêm về chúng). Thực tế, họ làm vậy để giảm thiểu ô nhiễm không gian toàn cục, vì một thư viện chỉ đưa ra một biến toàn cục duy nhất. Điều đó làm giảm khả năng xảy ra xung đột tên.

Vì vậy, một hàm có thể tự làm việc hữu ích và cũng có thể mang theo một loạt các chức năng khác trong các thuộc tính.

---

---

## Nhiệm vụ

## [Nhiệm vụ](#tasks)

### [Thiết lập và giảm bộ đếm](#set-and-decrease-for-counter)

Độ quan trọng: 5

Sửa đổi mã của `makeCounter()` để bộ đếm cũng có thể giảm và đặt số:

- `counter()` nên trả về số tiếp theo (như trước đây).
- `counter.set(value)` nên đặt bộ đếm thành `value`.
- `counter.decrease()` nên giảm bộ đếm đi 1.

Xem mã sandbox để biết ví dụ sử dụng đầy đủ.

P.S. Bạn có thể sử dụng either closure hoặc thuộc tính hàm để giữ số đếm hiện tại. Hoặc viết cả hai biến thể.

[Mở sandbox với các bài kiểm tra.](https://plnkr.co/edit/0RKnsQVgnzLvOvuI?p=preview)

solution

Giải pháp sử dụng `count` trong biến cục bộ, nhưng các phương thức thêm được ghi trực tiếp vào `counter`. Chúng chia sẻ cùng một lexical environment bên ngoài và cũng có thể truy cập `count` hiện tại.

```
function makeCounter() {
  let count = 0;

  function counter() {
    return count++;
  }

  counter.set = value => count = value;

  counter.decrease = () => count--;

  return counter;
}
```

[Mở giải pháp với các bài kiểm tra trong sandbox.](https://plnkr.co/edit/8WxZOAIKj3ZEXpjP?p=preview)

### [Phép cộng với số lượng dấu ngoặc tùy ý](#sum-with-an-arbitrary-amount-of-brackets)

Độ quan trọng: 2

Viết hàm `sum` hoạt động như sau:

```
sum(1)(2) == 3; // 1 + 2
sum(1)(2)(3) == 6; // 1 + 2 + 3
sum(5)(-1)(2) == 6
sum(6)(-1)(-2)(-3) == 0
sum(0)(1)(2)(3)(4)(5) == 15
```

P.S. Gợi ý: bạn có thể cần thiết lập chuyển đổi đối tượng tùy chỉnh sang primitive cho hàm của bạn.

[Mở sandbox với các bài kiểm tra.](https://plnkr.co/edit/sEtzrFl9HDoMW0dg?p=preview)

solution

1. Để toàn bộ hoạt động *bất kể*, kết quả của `sum` phải là một hàm.
2. Hàm đó phải ghi nhớ giá trị hiện tại giữa các lần gọi.
3. Theo yêu cầu, hàm phải trở thành số khi được sử dụng trong `==`. Hàm là các đối tượng, vì vậy việc chuyển đổi xảy ra như mô tả trong chương [Chuyển đổi đối tượng sang primitive](/object-toprimitive), và chúng ta có thể cung cấp phương thức riêng trả về số.

Giờ đây là mã:

```
function sum(a) {

  let currentSum = a;

  function f(b) {
    currentSum += b;
    return f;
  }

  f.toString = function() {
    return currentSum;
  };

  return f;
}

alert( sum(1)(2) ); // 3
alert( sum(5)(-1)(2) ); // 6
alert( sum(6)(-1)(-2)(-3) ); // 0
alert( sum(0)(1)(2)(3)(4)(5) ); // 15
```

Xin lưu ý rằng hàm `sum` thực sự chỉ hoạt động một lần. Nó trả về hàm `f`.

Sau đó, trên mỗi lần gọi tiếp theo, `f` thêm tham số của nó vào tổng `currentSum`, và trả về chính nó.

**Không có đệ quy trong dòng cuối cùng của `f`.**

Đây là cách trông giống như đệ quy:

```
function f(b) {
  currentSum += b;
  return f(); // <-- lệnh gọi đệ quy
}
```

Và trong trường hợp của chúng ta, chúng ta chỉ trả về hàm, mà không gọi nó:

```
function f(b) {
  currentSum += b;
  return f; // <-- không gọi chính nó, trả về chính nó
}
```

`f` này sẽ được sử dụng trong lần gọi tiếp theo, lại trả về chính nó, nhiều lần như cần. Sau đó, khi được sử dụng như một số hoặc chuỗi – `toString` trả về `currentSum`. Chúng ta cũng có thể sử dụng `Symbol.toPrimitive` hoặc `valueOf` ở đây để chuyển đổi.

[Mở giải pháp với các bài kiểm tra trong sandbox.](https://plnkr.co/edit/MqYkSVdiLluDbige?p=preview)