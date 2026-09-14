# Thuộc tính và phương thức tĩnh

> Nguồn: [https://javascript.info/static-properties-methods](https://javascript.info/static-properties-methods)

<!-- fetched: 2026-09-14 -->

Chúng ta cũng có thể gán một method cho class như một tổng thể. Các phương thức như vậy được gọi là *static*.

Trong một khai báo class, chúng được thêm vào phía trước bằng từ khóa `static`, như thế này:

```
class User {
  static staticMethod() {
    alert(this === User);
  }
}

User.staticMethod(); // true
```

Điều đó thực sự làm giống như gán nó trực tiếp như một property:

```
class User { }

User.staticMethod = function() {
  alert(this === User);
};

User.staticMethod(); // true
```

Giá trị của `this` trong cuộc gọi `User.staticMethod()` là constructor class `User` chính nó (quy tắc "object trước dấu chấm").

Thông thường, các phương thức static được sử dụng để triển khai các functions thuộc về class như một tổng thể, nhưng không thuộc về bất kỳ object cụ thể nào của nó.

Ví dụ, chúng ta có các đối tượng `Article` và cần một function để so sánh chúng.

Một giải pháp tự nhiên sẽ là thêm phương thức static `Article.compare`:

```
class Article {
  constructor(title, date) {
    this.title = title;
    this.date = date;
  }

  static compare(articleA, articleB) {
    return articleA.date - articleB.date;
  }
}

// usage
let articles = [
  new Article("HTML", new Date(2019, 1, 1)),
  new Article("CSS", new Date(2019, 0, 1)),
  new Article("JavaScript", new Date(2019, 11, 1))
];

articles.sort(Article.compare);

alert( articles[0].title ); // CSS
```

Ở đây phương thức `Article.compare` đứng "ở trên" các articles, như một phương tiện để so sánh chúng. Nó không phải là phương thức của một article, mà là của cả class.

Một ví dụ khác sẽ là phương thức "factory" được gọi.

Giả sử, chúng ta cần nhiều cách để tạo một article:

1. Tạo bằng các đối số đã cho (`title`, `date` v.v.).
2. Tạo một article trống với ngày hôm nay.
3. …hoặc một cách nào đó khác.

Cách đầu tiên có thể được triển khai bằng constructor. Và cho cái thứ hai chúng ta có thể tạo một phương thức static của class.

Như `Article.createTodays()` ở đây:

```
class Article {
  constructor(title, date) {
    this.title = title;
    this.date = date;
  }

  static createTodays() {
    // remember, this = Article
    return new this("Today's digest", new Date());
  }
}

let article = Article.createTodays();

alert( article.title ); // Today's digest
```

Bây giờ mỗi khi chúng ta cần tạo một today's digest, chúng ta có thể gọi `Article.createTodays()`. Một lần nữa, đó không phải là phương thức của một article, mà là phương thức của cả class.

Các phương thức static cũng được sử dụng trong các class liên quan đến database để search/save/remove entries từ database, như thế này:

```
// assuming Article is a special class for managing articles
// static method to remove the article by id:
Article.remove({id: 12345});
```

Các phương thức static không khả dụng cho các đối tượng riêng lẻ

Các phương thức static có thể được gọi trên các class, không phải trên các đối tượng riêng lẻ.

Ví dụ, mã sau sẽ không hoạt động:

```
// ...
article.createTodays(); /// Error: article.createTodays is not a function
```

## [Thuộc tính tĩnh](#thuoc-tinh-tinh)

Một bổ sung gần đây

Đây là một bổ sung gần đây cho ngôn ngữ.
Các ví dụ hoạt động trong Chrome gần đây.

Các thuộc tính tĩnh cũng có thể có được, chúng trông giống như các thuộc tính class thường, nhưng được thêm vào phía trước bằng `static`:

```
class Article {
  static publisher = "Ilya Kantor";
}

alert( Article.publisher ); // Ilya Kantor
```

Đó là giống như một gán trực tiếp vào `Article`:

```
Article.publisher = "Ilya Kantor";
```

## [Kế thừa các thuộc tính và phương thức tĩnh](#ke-thua-cac-thuoc-tinh-va-phuong-thuc-tinh)

Các thuộc tính và phương thức tĩnh được kế thừa.

Ví dụ, `Animal.compare` và `Animal.planet` trong mã dưới đây được kế thừa và có thể truy cập như `Rabbit.compare` và `Rabbit.planet`:

```
class Animal {
  static planet = "Earth";

  constructor(name, speed) {
    this.speed = speed;
    this.name = name;
  }

  run(speed = 0) {
    this.speed += speed;
    alert(`${this.name} runs with speed ${this.speed}.`);
  }

  static compare(animalA, animalB) {
    return animalA.speed - animalB.speed;
  }

}

// Inherit from Animal
class Rabbit extends Animal {
  hide() {
    alert(`${this.name} hides!`);
  }
}

let rabbits = [
  new Rabbit("White Rabbit", 10),
  new Rabbit("Black Rabbit", 5)
];

rabbits.sort(Rabbit.compare);

rabbits[0].run(); // Black Rabbit runs with speed 5.

alert(Rabbit.planet); // Earth
```

Bây giờ khi chúng ta gọi `Rabbit.compare`, `Animal.compare` được kế thừa sẽ được gọi.

Nó hoạt động như thế nào? Một lần nữa, sử dụng prototypes. Như bạn có thể đã đoán, `extends` cấp cho `Rabbit` reference `[[Prototype]]` đến `Animal`.

![](/article/static-properties-methods/animal-rabbit-static.svg)

Vì vậy, `Rabbit extends Animal` tạo hai reference `[[Prototype]]`:

1. Hàm `Rabbit` function prototypically kế thừa từ hàm `Animal` function.
2. `Rabbit.prototype` prototypically kế thừa từ `Animal.prototype`.

Như kết quả, inheritance hoạt động cho cả các phương thức thường và static.

Đây, hãy kiểm tra điều đó bằng mã:

```
class Animal {}
class Rabbit extends Animal {}

// for statics
alert(Rabbit.__proto__ === Animal); // true

// for regular methods
alert(Rabbit.prototype.__proto__ === Animal.prototype); // true
```

## [Tóm tắt](#summary)

Các phương thức static được sử dụng cho chức năng thuộc về class "như một tổng thể". Nó không liên quan đến một instance class cụ thể.

Ví dụ, một phương thức cho comparison `Article.compare(article1, article2)` hoặc một factory method `Article.createTodays()`.

Chúng được dán nhãn bằng từ `static` trong khai báo class.

Các thuộc tính tĩnh được sử dụng khi chúng ta muốn lưu trữ dữ liệu ở cấp class, cũng không được bind vào một instance.

Cú pháp là:

```
class MyClass {
  static property = ...;

  static method() {
    ...
  }
}
```

Về mặt kỹ thuật, khai báo static giống như gán cho chính class:

```
MyClass.property = ...
MyClass.method = ...
```

Các thuộc tính và phương thức static được kế thừa.

Đối với `class B extends A` prototype của class `B` chính nó trỏ đến `A`: `B.[[Prototype]] = A`. Vì vậy, nếu một field không được tìm thấy trong `B`, việc tìm kiếm tiếp tục trong `A`.

---

---

## Bài tập

## [Các bài tập](#tasks)

### [Class kế thừa Object?](#class-extends-object)

importance: 3

Như chúng ta biết, tất cả các objects bình thường kế thừa từ `Object.prototype` và nhận quyền truy cập vào các phương thức "generic" object như `hasOwnProperty` v.v.

Ví dụ:

```
class Rabbit {
  constructor(name) {
    this.name = name;
  }
}

let rabbit = new Rabbit("Rab");

// hasOwnProperty method is from Object.prototype
alert( rabbit.hasOwnProperty('name') ); // true
```

Nhưng nếu chúng ta viết rõ ràng như `"class Rabbit extends Object"`, thì kết quả sẽ khác với một đơn giản `"class Rabbit"`?

Sự khác biệt là gì?

Đây là một ví dụ về mã như vậy (nó không hoạt động – tại sao? sửa nó?):

```
class Rabbit extends Object {
  constructor(name) {
    this.name = name;
  }
}

let rabbit = new Rabbit("Rab");

alert( rabbit.hasOwnProperty('name') ); // Error
```

[lời giải](#solution)

Trước tiên, hãy xem tại sao mã sau không hoạt động.

Lý do trở nên rõ ràng nếu chúng ta cố gắng chạy nó. Constructor của class kế thừa phải gọi `super()`. Nếu không, `"this"` sẽ không được "defined".

Vì vậy đây là fix:

```
class Rabbit extends Object {
  constructor(name) {
    super(); // cần gọi parent constructor khi kế thừa
    this.name = name;
  }
}

let rabbit = new Rabbit("Rab");

alert( rabbit.hasOwnProperty('name') ); // true
```

Nhưng đó chưa phải là tất cả.

Ngay cả sau khi fix, vẫn có một sự khác biệt quan trọng giữa `"class Rabbit extends Object"` và `class Rabbit`.

Như chúng ta đã biết, cú pháp "extends" thiết lập hai prototypes:

1. Giữa `"prototype"` của các constructor functions (cho các methods).
2. Giữa các constructor functions chính nó (cho các phương thức static).

Trong trường hợp của `class Rabbit extends Object` điều đó có nghĩa là:

```
class Rabbit extends Object {}

alert( Rabbit.prototype.__proto__ === Object.prototype ); // (1) true
alert( Rabbit.__proto__ === Object ); // (2) true
```

Vì vậy `Rabbit` giờ cung cấp quyền truy cập vào các phương thức static của `Object` thông qua `Rabbit`, như thế này:

```
class Rabbit extends Object {}

// normally we call Object.getOwnPropertyNames
alert ( Rabbit.getOwnPropertyNames({a: 1, b: 2})); // a,b
```

Nhưng nếu chúng ta không có `extends Object`, thì `Rabbit.__proto__` không được đặt thành `Object`.

Đây là demo:

```
class Rabbit {}

alert( Rabbit.prototype.__proto__ === Object.prototype ); // (1) true
alert( Rabbit.__proto__ === Object ); // (2) false (!)
alert( Rabbit.__proto__ === Function.prototype ); // as any function by default

// error, no such function in Rabbit
alert ( Rabbit.getOwnPropertyNames({a: 1, b: 2})); // Error
```

Vì vậy `Rabbit` không cung cấp quyền truy cập vào các phương thức static của `Object` trong trường hợp đó.

Nhân tiện, `Function.prototype` cũng có các "generic" function methods, như `call`, `bind` v.v. Chúng cuối cùng có sẵn trong cả hai trường hợp, vì đối với constructor `Object` built-in, `Object.__proto__ === Function.prototype`.

Đây là hình:

![](/task/class-extend-object/rabbit-extends-object.svg)

Vì vậy, nói ngắn gọn, có hai sự khác biệt:

| class Rabbit | class Rabbit extends Object |
| --- | --- |
| – | needs to call `super()` in constructor |
| `Rabbit.__proto__ === Function.prototype` | `Rabbit.__proto__ === Object` |
