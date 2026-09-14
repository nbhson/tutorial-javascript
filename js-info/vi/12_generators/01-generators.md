# Generators (Hàm sinh)

> Nguồn: [https://javascript.info/generators](https://javascript.info/generators)

<!-- fetched: 2026-09-14 -->

Hàm thông thường chỉ trả về một, đơn giá trị (hoặc không có gì).

Generators có thể trả về ("yield") nhiều giá trị, một sau một, theo yêu cầu. Chúng hoạt động tuyệt vời với [iterables](/iterable), cho phép tạo streams dữ liệu một cách dễ dàng.

## [Hàm generator](#generator-functions)

Để tạo một generator, chúng ta cần một cấu trúc cú pháp đặc biệt: `function*`, được gọi là "generator function".

Nó trông như thế này:

```
function* generateSequence() {
  yield 1;
  yield 2;
  return 3;
}
```

Generator functions hành xử khác với các hàm thông thường. Khi hàm như vậy được gọi, nó không chạy mã của nó. Thay vào đó nó trả về một đối tượng đặc biệt, được gọi là "generator object", để quản lý execution.

Dưới đây, hãy xem:

```
function* generateSequence() {
  yield 1;
  yield 2;
  return 3;
}

// "generator function" tạo "generator object"
let generator = generateSequence();
alert(generator); // [object Generator]
```

Execution của hàm code chưa bắt đầu:

![](/article/generators/generateSequence-1.svg)

Phương thức chính của một generator là `next()`. Khi được gọi, nó chạy execution cho đến khi gần nhất `yield <value>` statement (`value` có thể bị bỏ qua, sau đó nó là `undefined`). Sau đó execution của hàm tạm dừng, và `value` được yield được trả về cho mã bên ngoài.

Kết quả của `next()` luôn là một đối tượng với hai thuộc tính:

- `value`: giá trị được yield.
- `done`: `true` nếu mã hàm đã hoàn tất, nếu không thì `false`.

Ví dụ, ở đây chúng ta tạo generator và nhận giá trị yield đầu tiên của nó:

```
function* generateSequence() {
  yield 1;
  yield 2;
  return 3;
}

let generator = generateSequence();

let one = generator.next();

alert(JSON.stringify(one)); // {value: 1, done: false}
```

Cho đến nay, chúng ta chỉ nhận được giá trị đầu tiên, và execution của hàm đang ở dòng thứ hai:

![](/article/generators/generateSequence-2.svg)

Hãy gọi `generator.next()` một lần nữa. Nó tiếp tục execution mã và trả về `yield` tiếp theo:

```
let two = generator.next();

alert(JSON.stringify(two)); // {value: 2, done: false}
```

![](/article/generators/generateSequence-3.svg)

Và, nếu chúng ta gọi nó lần thứ ba, execution đạt đến `return` statement kết thúc hàm:

```
let three = generator.next();

alert(JSON.stringify(three)); // {value: 3, done: true}
```

![](/article/generators/generateSequence-4.svg)

Bây giờ generator đã done. Chúng ta nên thấy nó từ `done:true` và xử lý `value:3` như là kết quả cuối cùng.

Các cuộc gọi mới đến `generator.next()` không còn ý nghĩa nữa. Nếu chúng ta làm vậy, chúng trả về cùng đối tượng: `{done: true}`.

`function* f(…)` hoặc `function *f(…)`?

Cả hai cú pháp đều đúng.

Nhưng thường thì cú pháp đầu tiên được ưa chuộng hơn, vì sao `*` chỉ ra rằng đó là một generator function, nó mô tả loại, không phải tên, vì vậy nó nên dính với từ khóa `function`.

## [Generators là iterable](#generators-are-iterable)

Như bạn có lẽ đã đoán khi nhìn vào phương thức `next()`, generators là [iterable](/iterable).

Chúng ta có thể lặp qua các giá trị của chúng bằng cách sử dụng `for..of`:

```
function* generateSequence() {
  yield 1;
  yield 2;
  return 3;
}

let generator = generateSequence();

for(let value of generator) {
  alert(value); // 1, sau đó 2
}
```

Trông đẹp hơn nhiều so với gọi `.next().value`, phải không?

…Nhưng xin lưu ý: ví dụ ở trên hiển thị `1`, sau đó `2`, và đó là tất cả. Nó không hiển thị `3`!

Đó là vì iteration `for..of` bỏ qua `value` cuối cùng, khi `done: true`. Vì vậy, nếu chúng ta muốn tất cả các kết quả được hiển thị bởi `for..of`, chúng ta phải trả chúng bằng `yield`:

```
function* generateSequence() {
  yield 1;
  yield 2;
  yield 3;
}

let generator = generateSequence();

for(let value of generator) {
  alert(value); // 1, sau đó 2, sau đó 3
}
```

Vì generators là iterable, chúng ta có thể gọi tất cả các functionality liên quan, ví dụ cú pháp spread `...`:

```
function* generateSequence() {
  yield 1;
  yield 2;
  yield 3;
}

let sequence = [0, ...generateSequence()];

alert(sequence); // 0, 1, 2, 3
```

Trong mã ở trên, `...generateSequence()` biến đối tượng generator iterable thành một mảng các mục (đọc thêm về cú pháp spread trong chương [Rest parameters and spread syntax](/rest-parameters-spread#spread-syntax))

## [Sử dụng generators cho iterables](#using-generators-for-iterables)

Một thời gian trước, trong chương [Iterables](/iterable) chúng ta đã tạo một đối tượng iterable `range` trả về các giá trị `from..to`.

Ở đây, hãy nhớ lại mã:

```
let range = {
  from: 1,
  to: 5,

  // for..of range gọi phương thức này một lần ở đầu tiên
  [Symbol.iterator]() {
    // ...nó trả về đối tượng iterator:
    // từ đây, for..of chỉ làm việc với đối tượng đó, hỏi nó về các giá trị tiếp theo
    return {
      current: this.from,
      last: this.to,

      // next() được gọi trên mỗi iteration bởi vòng lặp for..of
      next() {
        // nó nên trả về giá trị dưới dạng đối tượng {done:.., value :...}
        if (this.current <= this.last) {
          return { done: false, value: this.current++ };
        } else {
          return { done: true };
        }
      }
    };
  }
};

// iteration qua range trả về các số từ range.from đến range.to
alert([...range]); // 1,2,3,4,5
```

Chúng ta có thể sử dụng một generator function cho iteration bằng cách cung cấp nó như `Symbol.iterator`.

Dưới đây là `range` giống hệt nhau, nhưng compact hơn nhiều:

```
let range = {
  from: 1,
  to: 5,

  *[Symbol.iterator]() { // shorthand cho [Symbol.iterator]: function*()
    for(let value = this.from; value <= this.to; value++) {
      yield value;
    }
  }
};

alert( [...range] ); // 1,2,3,4,5
```

Nó hoạt động, vì `range[Symbol.iterator]()` bây giờ trả về một generator, và các phương thức generator là chính xác những gì `for..of` mong đợi:

- nó có một phương thức `.next()`
- mà trả về các giá trị dưới dạng `{value: ..., done: true/false}`

Đó không phải là một sự trùng hợp, tất nhiên. Generators được thêm vào ngôn ngữ JavaScript với iterators trong tâm trí, để thực hiện chúng một cách dễ dàng.

Biến thể với generator compact hơn nhiều so với mã iterable ban đầu của `range`, và giữ cùng functionality.

Generators có thể tạo giá trị mãi mãi

Trong các ví dụ ở trên chúng ta tạo ra các sequences hữu hạn, nhưng chúng ta cũng có thể tạo một generator tạo ra giá trị mãi mãi. Ví dụ, một sequence vô hạn của các số pseudo-random.

Điều đó chắc chắn sẽ yêu cầu một `break` (hoặc `return`) trong `for..of` qua generator như vậy. Nếu không, vòng lặp sẽ lặp mãi mãi và treo.

## [Composition của generator](#generator-composition)

Generator composition là một tính năng đặc biệt của generators cho phép "nhúng" các generators vào nhau một cách trong suốt.

Ví dụ, chúng ta có một hàm tạo một sequence của các số:

```
function* generateSequence(start, end) {
  for (let i = start; i <= end; i++) yield i;
}
```

Bây giờ chúng ta muốn tái sử dụng nó để tạo một sequence phức tạp hơn:

- trước tiên, các chữ số `0..9` (với character codes 48…57),
- tiếp theo là các chữ cái viết hoa `A..Z` (character codes 65…90)
- tiếp theo là các chữ cái viết thường `a..z` (character codes 97…122)

Chúng ta có thể sử dụng sequence này để tạo passwords bằng cách chọn các ký tự từ nó (có thể thêm các ký tự syntax), nhưng trước tiên hãy tạo nó.

Trong một hàm thông thường, để kết hợp kết quả từ nhiều hàm khác, chúng ta gọi chúng, lưu trữ các kết quả, và sau đó kết hợp ở cuối.

Đối với generators, có một cú pháp đặc biệt `yield*` để "nhúng" (compose) một generator vào generator khác.

Generator đã compose:

```
function* generateSequence(start, end) {
  for (let i = start; i <= end; i++) yield i;
}

function* generatePasswordCodes() {

  // 0..9
  yield* generateSequence(48, 57);

  // A..Z
  yield* generateSequence(65, 90);

  // a..z
  yield* generateSequence(97, 122);

}

let str = '';

for(let code of generatePasswordCodes()) {
  str += String.fromCharCode(code);
}

alert(str); // 0..9A..Za..z
```

Directive `yield*` *delegates* execution sang generator khác. Thuật ngữ này có nghĩa là `yield* gen` lặp qua generator `gen` và chuyển tiếp các yields của nó ra bên ngoài một cách trong suốt. Như thể các giá trị được yield bởi generator bên ngoài.

Kết quả giống nhau như nếu chúng ta inlined mã từ các generator lồng nhau:

```
function* generateSequence(start, end) {
  for (let i = start; i <= end; i++) yield i;
}

function* generateAlphaNum() {

  // yield* generateSequence(48, 57);
  for (let i = 48; i <= 57; i++) yield i;

  // yield* generateSequence(65, 90);
  for (let i = 65; i <= 90; i++) yield i;

  // yield* generateSequence(97, 122);
  for (let i = 97; i <= 122; i++) yield i;

}

let str = '';

for(let code of generateAlphaNum()) {
  str += String.fromCharCode(code);
}

alert(str); // 0..9A..Za..z
```

Generator composition là một cách tự nhiên để chèn một flow của một generator vào generator khác. Nó không sử dụng bộ nhớ bổ sung để lưu trữ các kết quả trung gian.

## ["yield" là con đường hai chiều](#yield-is-a-two-way-street)

Cho đến thời điểm này, generators tương tự như các đối tượng iterable, với một cú pháp đặc biệt để tạo ra giá trị. Nhưng thực sự chúng mạnh mẽ và linh hoạt hơn nhiều.

Đó là vì `yield` là con đường hai chiều: nó không chỉ trả về kết quả ra bên ngoài, mà còn có thể truyền giá trị vào bên trong generator.

Để làm điều đó, chúng ta nên gọi `generator.next(arg)`, với một đối số. Đối số đó trở thành kết quả của `yield`.

Hãy xem một ví dụ:

```
function* gen() {
  // Gửi câu hỏi đến mã bên ngoài và chờ câu trả lời
  let result = yield "2 + 2 = ?"; // (*)

  alert(result);
}

let generator = gen();

let question = generator.next().value; // <-- yield trả về giá trị

generator.next(4); // --> truyền kết quả vào generator
```

![](/article/generators/genYield2.svg)

1. Cuộc gọi đầu tiên `generator.next()` luôn phải được thực hiện mà không có đối số (đối số bị bỏ qua nếu được chuyển). Nó bắt đầu execution và trả về kết quả của `yield "2+2=?"` đầu tiên. Tại điểm này generator tạm dừng execution, trong khi vẫn ở dòng `(*)`.
2. Sau đó, như được hiển thị trong hình ở trên, kết quả của `yield` đi vào biến `question` trong mã gọi.
3. Trên `generator.next(4)`, generator tiếp tục, và `4` đi vào như kết quả: `let result = 4`.

Xin lưu ý, mã bên ngoài không nhất thiết phải gọi ngay `next(4)`. Nó có thể mất thời gian. Điều đó không phải là vấn đề: generator sẽ chờ.

Ví dụ:

```
// tiếp tục generator sau một khoảng thời gian
setTimeout(() => generator.next(4), 1000);
```

Như chúng ta có thể thấy, khác với các hàm thông thường, một generator và mã gọi có thể trao đổi kết quả bằng cách truyền giá trị trong `next/yield`.

Để làm cho mọi thứ rõ ràng hơn, dưới đây là một ví dụ khác, với nhiều cuộc gọi hơn:

```
function* gen() {
  let ask1 = yield "2 + 2 = ?";

  alert(ask1); // 4

  let ask2 = yield "3 * 3 = ?"

  alert(ask2); // 9
}

let generator = gen();

alert( generator.next().value ); // "2 + 2 = ?"

alert( generator.next(4).value ); // "3 * 3 = ?"

alert( generator.next(9).done ); // true
```

Bức tranh execution:

![](/article/generators/genYield2-2.svg)

1. `.next()` đầu tiên bắt đầu execution… Nó đạt đến `yield` đầu tiên.
2. Kết quả được trả về cho mã bên ngoài.
3. `.next(4)` thứ hai truyền `4` trở lại generator như kết quả của `yield` đầu tiên, và tiếp tục execution.
4. …Nó đạt đến `yield` thứ hai, mà trở thành kết quả của cuộc gọi generator.
5. `next(9)` thứ ba truyền `9` vào generator như kết quả của `yield` thứ hai và tiếp tục execution đạt đến cuối hàm, vì vậy `done: true`.

Giống như một trò chơi "ping-pong". Mỗi `next(value)` (trừ cái đầu tiên) truyền một giá trị vào generator, mà trở thành kết quả của `yield` hiện tại, và sau đó nhận lại kết quả của `yield` tiếp theo.

## [generator.throw](#generator-throw)

Như chúng ta đã quan sát trong các ví dụ ở trên, mã bên ngoài có thể truyền một giá trị vào generator, như kết quả của `yield`.

…Nhưng nó cũng có thể khởi tạo (throw) một lỗi ở đó. Điều đó tự nhiên, vì lỗi là một loại kết quả.

Để truyền lỗi vào một `yield`, chúng ta nên gọi `generator.throw(err)`. Trong trường hợp đó, `err` được throw ở dòng có `yield` đó.

Ví dụ, ở đây `yield` của `"2 + 2 = ?"` dẫn đến lỗi:

```
function* gen() {
  try {
    let result = yield "2 + 2 = ?"; // (1)

    alert("Execution không đạt đến đây, vì exception được throw ở trên");
  } catch(e) {
    alert(e); // hiển thị lỗi
  }
}

let generator = gen();

let question = generator.next().value;

generator.throw(new Error("Câu trả lời không được tìm thấy trong cơ sở dữ liệu của tôi")); // (2)
```

Lỗi được throw vào generator ở dòng `(2)` dẫn đến exception ở dòng `(1)` với `yield`. Trong ví dụ ở trên, `try..catch` bắt nó và hiển thị nó.

Nếu chúng ta không bắt nó, thì giống như bất kỳ exception nào, nó "rơi ra" generator vào mã gọi.

Dòng hiện tại của mã gọi là dòng với `generator.throw`, được đánh dấu là `(2)`. Vì vậy chúng ta có thể bắt nó ở đây, như thế này:

```
function* generate() {
  let result = yield "2 + 2 = ?"; // Lỗi ở dòng này
}

let generator = generate();

let question = generator.next().value;

try {
  generator.throw(new Error("Câu trả lời không được tìm thấy trong cơ sở dữ liệu của tôi"));
} catch(e) {
  alert(e); // hiển thị lỗi
}
```

Nếu chúng ta không bắt lỗi ở đó, thì, như thường lệ, nó rơi xuống mã gọi bên ngoài (nếu có) và, nếu không được bắt, nó giết script.

## [generator.return](#generator-return)

`generator.return(value)` kết thúc execution generator và trả về `value` đã cho.

```
function* gen() {
  yield 1;
  yield 2;
  yield 3;
}

const g = gen();

g.next();        // { value: 1, done: false }
g.return('foo'); // { value: "foo", done: true }
g.next();        // { value: undefined, done: true }
```

Nếu chúng ta lại sử dụng `generator.return()` trong một generator đã hoàn thành, nó sẽ trả lại giá trị đó lần nữa ([MDN](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Generator/return)).

Thường thì chúng ta không sử dụng nó, vì hầu hết thời gian chúng ta muốn nhận tất cả các giá trị trả về, nhưng nó có thể hữu ích khi chúng ta muốn dừng generator trong một điều kiện cụ thể.

## [Tóm tắt](#summary)

- Generators được tạo bởi generator functions `function* f(…) {…}`.
- Bên trong generators (chỉ) tồn tại toán tử `yield`.
- Mã bên ngoài và generator có thể trao đổi kết quả thông qua các cuộc gọi `next/yield`.

Trong JavaScript hiện đại, generators hiếm khi được sử dụng. Nhưng đôi khi chúng hữu ích, vì khả năng của một hàm để trao đổi dữ liệu với mã gọi trong suốt quá trình thực thi là khá độc đáo. Và, chắc chắn, chúng tuyệt vời để tạo các đối tượng iterable.

Ngoài ra, ở chương tiếp theo chúng ta sẽ học async generators, được sử dụng để đọc streams dữ liệu được tạo không đồng bộ (ví dụ fetch phân trang qua mạng) trong các vòng lặp `for await ... of`.

Trong web-programming chúng ta thường làm việc với dữ liệu stream, vì vậy đó là một trường hợp sử dụng quan trọng khác.

---

---

## Bài tập

## [Các bài tập](#tasks)

### [Generator pseudo-ngẫu nhiên](#pseudo-random-generator)

Có nhiều khu vực nơi chúng ta cần dữ liệu ngẫu nhiên.

Một trong số chúng là testing. Chúng ta có thể cần dữ liệu ngẫu nhiên: text, numbers, v.v. để test các thứ tốt.

Trong JavaScript, chúng ta có thể sử dụng `Math.random()`. Nhưng nếu có gì đó đi sai, chúng ta muốn có khả năng lặp lại test, bằng cách sử dụng chính xác cùng dữ liệu.

Để làm điều đó, các "seeded pseudo-random generators" được sử dụng. Chúng nhận một "seed", giá trị đầu tiên, và sau đó tạo ra các giá trị tiếp theo bằng cách sử dụng một công thức sao cho cùng seed tạo ra cùng sequence, và do đó toàn bộ flow dễ dàng có thể tái lập lại. Chúng ta chỉ cần nhớ seed để lặp lại nó.

Một ví dụ về công thức như vậy, tạo ra các giá trị phân bố somewhat uniformly:

```
next = previous * 16807 % 2147483647
```

Nếu chúng ta sử dụng `1` làm seed, các giá trị sẽ là:

1. `16807`
2. `282475249`
3. `1622650073`
4. …và cứ thế…

Bài tập là tạo một generator function `pseudoRandom(seed)` nhận `seed` và tạo generator với công thức này.

Ví dụ sử dụng:

```
let generator = pseudoRandom(1);

alert(generator.next().value); // 16807
alert(generator.next().value); // 282475249
alert(generator.next().value); // 1622650073
```

[Mở sandbox với tests.](https://plnkr.co/edit/CKGufQMDfkwSF7x0?p=preview)

lời giải

```
function* pseudoRandom(seed) {
  let value = seed;

  while(true) {
    value = value * 16807 % 2147483647;
    yield value;
  }

};

let generator = pseudoRandom(1);

alert(generator.next().value); // 16807
alert(generator.next().value); // 282475249
alert(generator.next().value); // 1622650073
```

Xin lưu ý, cùng thứ có thể được làm với một hàm thông thường, như thế này:

```
function pseudoRandom(seed) {
  let value = seed;

  return function() {
    value = value * 16807 % 2147483647;
    return value;
  }
}

let generator = pseudoRandom(1);

alert(generator()); // 16807
alert(generator()); // 282475249
alert(generator()); // 1622650073
```

Điều đó cũng hoạt động. Nhưng sau đó chúng ta mất khả năng iterate với `for..of` và để sử dụng generator composition, có thể hữu ích ở nơi khác.

[Mở lời giải với tests trong sandbox.](https://plnkr.co/edit/kO26Hfb7SKYVx0rq?p=preview)
