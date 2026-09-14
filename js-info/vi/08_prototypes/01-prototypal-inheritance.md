# Kế thừa nguyên mẫu (Prototypal inheritance)

> Source: [https://javascript.info/prototype-inheritance](https://javascript.info/prototype-inheritance)

<!-- fetched: 2026-09-14 -->

Trong lập trình, chúng ta thường muốn lấy một thứ gì đó và mở rộng nó.

Ví dụ, chúng ta có một đối tượng `user` với các thuộc tính và phương thức của nó, và muốn tạo `admin` và `guest` như các biến thể hơi sửa đổi của nó. Chúng ta muốn tái sử dụng những gì có trong `user`, không sao chép/triển khai lại các phương thức của nó, chỉ cần xây dựng một đối tượng mới dựa trên nó.

*Kế thừa nguyên mẫu* là một tính năng ngôn ngữ giúp ích trong việc đó.

## [[[Prototype]]](#prototype)

Trong JavaScript, các đối tượng có một thuộc tính ẩn đặc biệt `[[Prototype]]` (như được đặt tên trong đặc tả), giá trị là `null` hoặc tham chiếu đến một đối tượng khác. Đối tượng đó được gọi là "nguyên mẫu":

![](/article/prototype-inheritance/object-prototype-empty.svg)

Khi chúng ta đọc một thuộc tính từ `object`, và nó bị thiếu, JavaScript tự động lấy nó từ nguyên mẫu. Trong lập trình, điều này được gọi là "kế thừa nguyên mẫu". Và sớm thôi chúng ta sẽ nghiên cứu nhiều ví dụ về kế thừa như vậy, cũng như các tính năng ngôn ngữ tuyệt vời hơn được xây dựng dựa trên nó.

Thuộc tính `[[Prototype]]` là nội bộ và ẩn, nhưng có nhiều cách để đặt nó.

Một trong số đó là sử dụng tên đặc biệt `__proto__`, như thế này:

```
let animal = {
  eats: true
};
let rabbit = {
  jumps: true
};

rabbit.__proto__ = animal; // sets rabbit.[[Prototype]] = animal
```

Giờ nếu chúng ta đọc một thuộc tính từ `rabbit`, và nó bị thiếu, JavaScript sẽ tự động lấy nó từ `animal`.

Ví dụ:

```
let animal = {
  eats: true
};
let rabbit = {
  jumps: true
};

rabbit.__proto__ = animal; // (*)

// we can find both properties in rabbit now:
alert( rabbit.eats ); // true (**)
alert( rabbit.jumps ); // true
```

Ở đây dòng `(*)` đặt `animal` làm nguyên mẫu của `rabbit`.

Sau đó, khi `alert` cố gắng đọc thuộc tính `rabbit.eats` `(**)`, nó không có trong `rabbit`, vì vậy JavaScript đi theo tham chiếu `[[Prototype]]` và tìm thấy nó trong `animal` (nhìn từ dưới lên):

![](/article/prototype-inheritance/proto-animal-rabbit.svg)

Ở đây chúng ta có thể nói rằng "`animal` là nguyên mẫu của `rabbit`" hoặc "`rabbit` kế thừa nguyên mẫu từ `animal`".

Vì vậy, nếu `animal` có nhiều thuộc tính và phương thức hữu ích, thì chúng tự động có sẵn trong `rabbit`. Các thuộc tính như vậy được gọi là "kế thừa".

Nếu chúng ta có một phương thức trong `animal`, nó có thể được gọi trên `rabbit`:

```
let animal = {
  eats: true,
  walk() {
    alert("Animal walk");
  }
};

let rabbit = {
  jumps: true,
  __proto__: animal
};

// walk is taken from the prototype
rabbit.walk(); // Animal walk
```

Phương thức tự động được lấy từ nguyên mẫu, như thế này:

![](/article/prototype-inheritance/proto-animal-rabbit-walk.svg)

Chuỗi nguyên mẫu có thể dài hơn:

```
let animal = {
  eats: true,
  walk() {
    alert("Animal walk");
  }
};

let rabbit = {
  jumps: true,
  __proto__: animal
};

let longEar = {
  earLength: 10,
  __proto__: rabbit
};

// walk is taken from the prototype chain
longEar.walk(); // Animal walk
alert(longEar.jumps); // true (from rabbit)
```

![](/article/prototype-inheritance/proto-animal-rabbit-chain.svg)

Giờ nếu chúng ta đọc thứ gì đó từ `longEar`, và nó bị thiếu, JavaScript sẽ tìm kiếm nó trong `rabbit`, sau đó trong `animal`.

Có hai giới hạn duy nhất:

1. Các tham chiếu không thể vòng tròn. JavaScript sẽ ném lỗi nếu chúng ta cố gắng gán `__proto__` theo vòng tròn.
2. Giá trị của `__proto__` có thể là đối tượng hoặc `null`. Các kiểu khác bị bỏ qua.

Nó cũng có thể hiển nhiên, nhưng vẫn: chỉ có một `[[Prototype]]`. Một đối tượng không thể kế thừa từ hai đối tượng khác.

`__proto__` là getter/setter lịch sử cho `[[Prototype]]`

Một sai lầm phổ biến của các nhà phát triển mới không biết sự khác biệt giữa hai thứ này.

Xin lưu ý rằng `__proto__` *không phải là* thuộc tính `[[Prototype]]` nội bộ. Nó là một getter/setter cho `[[Prototype]]`. Sau này chúng ta sẽ thấy các tình huống nơi nó quan trọng, cho đến lúc đó hãy cứ ghi nhớ nó khi chúng ta xây dựng hiểu biết về ngôn ngữ JavaScript.

Thuộc tính `__proto__` hơi lỗi thời. Nó tồn tại vì lý do lịch sử, JavaScript hiện đại gợi ý rằng chúng ta nên sử dụng các hàm `Object.getPrototypeOf/Object.setPrototypeOf` thay thế để get/set nguyên mẫu. Chúng ta cũng sẽ đề cập đến các hàm này sau.

Theo đặc tả, `__proto__` chỉ phải được hỗ trợ bởi các trình duyệt. Trên thực tế, tất cả các môi trường bao gồm cả server-side đều hỗ trợ `__proto__`, vì vậy chúng ta khá an toàn khi sử dụng nó.

Vì ký hiệu `__proto__` trực quan hơn, chúng ta sử dụng nó trong các ví dụ.

## [Ghi không sử dụng nguyên mẫu](#writing-doesn't-use-prototype)

Nguyên mẫu chỉ được sử dụng cho việc đọc thuộc tính.

Các thao tác ghi/xóa hoạt động trực tiếp với đối tượng.

Trong ví dụ dưới đây, chúng ta gán phương thức `walk` riêng của nó vào `rabbit`:

```
let animal = {
  eats: true,
  walk() {
    /* this method won't be used by rabbit */
  }
};

let rabbit = {
  __proto__: animal
};

rabbit.walk = function() {
  alert("Rabbit! Bounce-bounce!");
};

rabbit.walk(); // Rabbit! Bounce-bounce!
```

Từ giờ trở đi, cuộc gọi `rabbit.walk()` tìm thấy phương thức ngay lập tức trong đối tượng và thực thi nó, mà không sử dụng nguyên mẫu:

![](/article/prototype-inheritance/proto-animal-rabbit-walk-2.svg)

Các thuộc tính accessor là trường hợp ngoại lệ, vì việc gán được xử lý bởi một hàm setter. Vì vậy, ghi vào thuộc tính như vậy thực sự giống như gọi một hàm.

Bởi lý do đó `admin.fullName` hoạt động chính xác trong mã dưới đây:

```
let user = {
  name: "John",
  surname: "Smith",

  set fullName(value) {
    [this.name, this.surname] = value.split(" ");
  },

  get fullName() {
    return `${this.name} ${this.surname}`;
  }
};

let admin = {
  __proto__: user,
  isAdmin: true
};

alert(admin.fullName); // John Smith (*)

// setter triggers!
admin.fullName = "Alice Cooper"; // (**)

alert(admin.fullName); // Alice Cooper, state of admin modified
alert(user.fullName); // John Smith, state of user protected
```

Ở đây trong dòng `(*)`, thuộc tính `admin.fullName` có một getter trong nguyên mẫu `user`, vì vậy nó được gọi. Và trong dòng `(**)` thuộc tính có một setter trong nguyên mẫu, vì vậy nó được gọi.

## [Giá trị của "this"](#the-value-of-this)

Một câu hỏi thú vị có thể nảy sinh trong ví dụ trên: giá trị của `this` bên trong `set fullName(value)` là gì? Các thuộc tính `this.name` và `this.surname` được ghi vào đâu: vào `user` hay `admin`?

Câu trả lời đơn giản: `this` không bị ảnh hưởng bởi nguyên mẫu chút nào.

**Bất kể phương thức được tìm thấy ở đâu: trong đối tượng hay nguyên mẫu của nó. Trong một cuộc gọi phương thức, `this` luôn là đối tượng trước dấu chấm.**

Vì vậy, cuộc gọi setter `admin.fullName=` sử dụng `admin` làm `this`, không phải `user`.

Điều này thực sự rất quan trọng, vì chúng ta có thể có một đối tượng lớn với nhiều phương thức, và có các đối tượng kế thừa từ nó. Và khi các đối tượng kế thừa chạy các phương thức kế thừa, chúng sẽ chỉ sửa đổi trạng thái của riêng chúng, không phải trạng thái của đối tượng lớn.

Ví dụ, ở đây `animal` đại diện cho một "kho phương thức", và `rabbit` sử dụng nó.

Cuộc gọi `rabbit.sleep()` đặt `this.isSleeping` trên đối tượng `rabbit`:

```
// animal has methods
let animal = {
  walk() {
    if (!this.isSleeping) {
      alert(`I walk`);
    }
  },
  sleep() {
    this.isSleeping = true;
  }
};

let rabbit = {
  name: "White Rabbit",
  __proto__: animal
};

// modifies rabbit.isSleeping
rabbit.sleep();

alert(rabbit.isSleeping); // true
alert(animal.isSleeping); // undefined (no such property in the prototype)
```

Bức tranh kết quả:

![](/article/prototype-inheritance/proto-animal-rabbit-walk-3.svg)

Nếu chúng ta có các đối tượng khác, như `bird`, `snake`, v.v., kế thừa từ `animal`, chúng cũng sẽ có quyền truy cập vào các phương thức của `animal`. Nhưng `this` trong mỗi cuộc gọi phương thức sẽ là đối tượng tương ứng, được đánh giá tại thời điểm gọi (trước dấu chấm), không phải `animal`. Vì vậy, khi chúng ta ghi dữ liệu vào `this`, nó được lưu vào các đối tượng đó.

Kết quả là, các phương thức được chia sẻ, nhưng trạng thái đối tượng thì không.

## [Vòng lặp for…in](#for-in-loop)

Vòng lặp `for..in` lặp qua cả các thuộc tính kế thừa.

Ví dụ:

```
let animal = {
  eats: true
};

let rabbit = {
  jumps: true,
  __proto__: animal
};

// Object.keys only returns own keys
alert(Object.keys(rabbit)); // jumps

// for..in loops over both own and inherited keys
for(let prop in rabbit) alert(prop); // jumps, then eats
```

Nếu đó không phải là những gì chúng ta muốn, và chúng ta muốn loại bỏ các thuộc tính kế thừa, có một phương thức tích hợp sẵn [obj.hasOwnProperty(key)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/hasOwnProperty): nó trả về `true` nếu `obj` có thuộc tính riêng (không kế thừa) tên là `key`.

Vì vậy, chúng ta có thể lọc bỏ các thuộc tính kế thừa (hoặc làm điều gì đó khác với chúng):

```
let animal = {
  eats: true
};

let rabbit = {
  jumps: true,
  __proto__: animal
};

for(let prop in rabbit) {
  let isOwn = rabbit.hasOwnProperty(prop);

  if (isOwn) {
    alert(`Our: ${prop}`); // Our: jumps
  } else {
    alert(`Inherited: ${prop}`); // Inherited: eats
  }
}
```

Ở đây chúng ta có chuỗi kế thừa sau: `rabbit` kế thừa từ `animal`, kế thừa từ `Object.prototype` (vì `animal` là một literal object `{...}`, vì vậy nó là mặc định), và sau đó là `null` ở trên:

![](/article/prototype-inheritance/rabbit-animal-object.svg)

Lưu ý, có một điều hài hước. Phương thức `rabbit.hasOwnProperty` đến từ đâu? Chúng ta không định nghĩa nó. Nhìn vào chuỗi chúng ta có thể thấy phương thức được cung cấp bởi `Object.prototype.hasOwnProperty`. Nói cách khác, nó là kế thừa.

…Nhưng tại sao `hasOwnProperty` không xuất hiện trong vòng lặp `for..in` giống như `eats` và `jumps`, nếu `for..in` liệt kê các thuộc tính kế thừa?

Câu trả lời đơn giản: nó không liệt kê được. Giống như tất cả các thuộc tính khác của `Object.prototype`, nó có cờ `enumerable:false`. Và `for..in` chỉ liệt kê các thuộc tính liệt kê được. Đó là lý do tại sao nó và phần còn lại của các thuộc tính `Object.prototype` không được liệt kê.

Hầu hết các phương thức lấy key/value khác bỏ qua các thuộc tính kế thừa

Hầu hết các phương thức lấy key/value khác, như `Object.keys`, `Object.values` và tương tự, bỏ qua các thuộc tính kế thừa.

Chúng chỉ hoạt động trên đối tượng chính nó. Các thuộc tính từ nguyên mẫu *không* được tính đến.

## [Tóm tắt](#summary)

- Trong JavaScript, tất cả các đối tượng có một thuộc tính ẩn `[[Prototype]]` giá trị là một đối tượng khác hoặc `null`.
- Chúng ta có thể sử dụng `obj.__proto__` để truy cập nó (một getter/setter lịch sử, có các cách khác, sẽ được đề cập sớm).
- Đối tượng được tham chiếu bởi `[[Prototype]]` được gọi là "nguyên mẫu".
- Nếu chúng ta muốn đọc một thuộc tính của `obj` hoặc gọi một phương thức, và nó không tồn tại, thì JavaScript cố gắng tìm nó trong nguyên mẫu.
- Các thao tác ghi/xóa hành xử trực tiếp trên đối tượng, chúng không sử dụng nguyên mẫu (giả sử nó là thuộc tính dữ liệu, không phải setter).
- Nếu chúng ta gọi `obj.method()`, và `method` được lấy từ nguyên mẫu, `this` vẫn tham chiếu đến `obj`. Vì vậy, các phương thức luôn hoạt động với đối tượng hiện tại ngay cả khi chúng được kế thừa.
- Vòng lặp `for..in` lặp qua cả thuộc tính riêng và kế thừa của nó. Tất cả các phương thức lấy key/value khác chỉ hoạt động trên đối tượng chính nó.

---

---

## Bài tập

## [Bài tập](#tasks)

### [Làm việc với nguyên mẫu](#working-with-prototype)

quan trọng: 5

Đây là mã tạo ra một cặp đối tượng, sau đó sửa đổi chúng.

Các giá trị nào được hiển thị trong quá trình?

```
let animal = {
  jumps: null
};
let rabbit = {
  __proto__: animal,
  jumps: true
};

alert( rabbit.jumps ); // ? (1)

delete rabbit.jumps;

alert( rabbit.jumps ); // ? (2)

delete animal.jumps;

alert( rabbit.jumps ); // ? (3)
```

Phải có 3 câu trả lời.

lời giải

1. `true`, lấy từ `rabbit`.
2. `null`, lấy từ `animal`.
3. `undefined`, không còn thuộc tính đó nữa.

### [Thuật toán tìm kiếm](#searching-algorithm)

quan trọng: 5

Bài tập có hai phần.

Cho các đối tượng sau:

```
let head = {
  glasses: 1
};

let table = {
  pen: 3
};

let bed = {
  sheet: 1,
  pillow: 2
};

let pockets = {
  money: 2000
};
```

1. Sử dụng `__proto__` để gán nguyên mẫu theo cách mà mọi tra cứu thuộc tính sẽ đi theo đường dẫn: `pockets` → `bed` → `table` → `head`. Ví dụ, `pockets.pen` sẽ là `3` (tìm thấy trong `table`), và `bed.glasses` sẽ là `1` (tìm thấy trong `head`).
2. Trả lời câu hỏi: có nhanh hơn không khi lấy `glasses` là `pockets.glasses` hay `head.glasses`? Benchmark nếu cần.

lời giải

1. Hãy thêm `__proto__`:

   ```
   let head = {
     glasses: 1
   };

   let table = {
     pen: 3,
     __proto__: head
   };

   let bed = {
     sheet: 1,
     pillow: 2,
     __proto__: table
   };

   let pockets = {
     money: 2000,
     __proto__: bed
   };

   alert( pockets.pen ); // 3
   alert( bed.glasses ); // 1
   alert( table.money ); // undefined
   ```
2. Trong các engine hiện đại, về hiệu suất, không có sự khác biệt về việc lấy thuộc tính từ một đối tượng hay nguyên mẫu của nó. Chúng nhớ nơi tìm thấy thuộc tính và tái sử dụng nó trong yêu cầu tiếp theo.

   Ví dụ, đối với `pockets.glasses`, chúng nhớ nơi chúng tìm thấy `glasses` (trong `head`), và lần sau sẽ tìm ngay tại đó. Chúng cũng đủ thông minh để cập nhật các bộ nhớ đệm nội bộ nếu có gì thay đổi, vì vậy tối ưu hóa này an toàn.

### [Ghi vào đâu?](#where-does-it-write)

quan trọng: 5

Chúng ta có `rabbit` kế thừa từ `animal`.

Nếu chúng ta gọi `rabbit.eat()`, đối tượng nào nhận thuộc tính `full`: `animal` hay `rabbit`?

```
let animal = {
  eat() {
    this.full = true;
  }
};

let rabbit = {
  __proto__: animal
};

rabbit.eat();
```

lời giải

**Câu trả lời: `rabbit`.**

Bởi vì `this` là đối tượng trước dấu chấm, vì vậy `rabbit.eat()` sửa đổi `rabbit`.

Tra cứu thuộc tính và thực thi là hai thứ khác nhau.

Phương thức `rabbit.eat` trước tiên được tìm thấy trong nguyên mẫu, sau đó được thực thi với `this=rabbit`.

### [Tại sao cả hai hamster đều no?](#why-are-both-hamsters-full)

quan trọng: 5

Chúng ta có hai con hamster: `speedy` và `lazy` kế thừa từ đối tượng `hamster` chung.

Khi chúng ta cho một con ăn, con kia cũng no. Tại sao? Làm thế nào để sửa nó?

```
let hamster = {
  stomach: [],

  eat(food) {
    this.stomach.push(food);
  }
};

let speedy = {
  __proto__: hamster
};

let lazy = {
  __proto__: hamster
};

// This one found the food
speedy.eat("apple");
alert( speedy.stomach ); // apple

// This one also has it, why? fix please.
alert( lazy.stomach ); // apple
```

lời giải

Hãy nhìn kỹ những gì đang xảy ra trong cuộc gọi `speedy.eat("apple")`.

1. Phương thức `speedy.eat` được tìm thấy trong nguyên mẫu (=hamster), sau đó được thực thi với `this=speedy` (đối tượng trước dấu chấm).
2. Sau đó `this.stomach.push()` cần tìm thuộc tính `stomach` và gọi `push` trên nó. Nó tìm `stomach` trong `this` (=speedy), nhưng không tìm thấy.
3. Sau đó nó đi theo chuỗi nguyên mẫu và tìm thấy `stomach` trong `hamster`.
4. Sau đó nó gọi `push` trên nó, thêm thức ăn vào *dạ dày của nguyên mẫu*.

Vì vậy tất cả hamster chia sẻ một dạ dày duy nhất!

Cả `lazy.stomach.push(...)` và `speedy.stomach.push()`, thuộc tính `stomach` được tìm thấy trong nguyên mẫu (vì nó không có trong đối tượng chính nó), sau đó dữ liệu mới được push vào đó.

Xin lưu ý rằng điều đó không xảy ra trong trường hợp gán đơn giản `this.stomach=`:

```
let hamster = {
  stomach: [],

  eat(food) {
    // assign to this.stomach instead of this.stomach.push
    this.stomach = [food];
  }
};

let speedy = {
   __proto__: hamster
};

let lazy = {
  __proto__: hamster
};

// Speedy one found the food
speedy.eat("apple");
alert( speedy.stomach ); // apple

// Lazy one's stomach is empty
alert( lazy.stomach ); // <nothing>
```

Giờ mọi thứ hoạt động tốt, vì `this.stomach=` không thực hiện tra cứu `stomach`. Giá trị được ghi trực tiếp vào đối tượng `this`.

Ngoài ra, chúng ta có thể hoàn toàn tránh vấn đề bằng cách đảm bảo rằng mỗi hamster có dạ dày riêng:

```
let hamster = {
  stomach: [],

  eat(food) {
    this.stomach.push(food);
  }
};

let speedy = {
  __proto__: hamster,
  stomach: []
};

let lazy = {
  __proto__: hamster,
  stomach: []
};

// Speedy one found the food
speedy.eat("apple");
alert( speedy.stomach ); // apple

// Lazy one's stomach is empty
alert( lazy.stomach ); // <nothing>
```

Như một giải pháp chung, tất cả các thuộc tính mô tả trạng thái của một đối tượng cụ thể, như `stomach` ở trên, nên được ghi vào đối tượng đó. Điều đó ngăn chặn các vấn đề như vậy.
