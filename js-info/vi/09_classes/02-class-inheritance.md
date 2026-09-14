# Kế thừa Class

> Nguồn: [https://javascript.info/class-inheritance](https://javascript.info/class-inheritance)

<!-- fetched: 2026-09-14 -->

Kế thừa class là cách để một class mở rộng một class khác.

Vì vậy, chúng ta có thể tạo ra chức năng mới dựa trên chức năng hiện có.

## [Từ khóa "extends"]( #tu-khoa-extends)

Giả sử chúng ta có class `Animal`:

```
class Animal {
  constructor(name) {
    this.speed = 0;
    this.name = name;
  }
  run(speed) {
    this.speed = speed;
    alert(`${this.name} runs with speed ${this.speed}.`);
  }
  stop() {
    this.speed = 0;
    alert(`${this.name} stands still.`);
  }
}

let animal = new Animal("My animal");
```

Đây là cách chúng ta có thể biểu diễn đồ họa đối tượng `animal` và class `Animal`:

![](/article/class-inheritance/rabbit-animal-independent-animal.svg)

…Và chúng ta muốn tạo một `class Rabbit` khác.

Vì rabbits là animals, class `Rabbit` nên dựa trên `Animal`, có quyền truy cập vào các phương thức của animal, vì vậy rabbits có thể làm những gì các "animals" generic có thể làm.

Cú pháp để kế thừa từ một class khác là: `class Child extends Parent`.

Hãy tạo `class Rabbit` kế thừa từ `Animal`:

```
class Rabbit extends Animal {
  hide() {
    alert(`${this.name} hides!`);
  }
}

let rabbit = new Rabbit("White Rabbit");

rabbit.run(5); // White Rabbit runs with speed 5.
rabbit.hide(); // White Rabbit hides!
```

Đối tượng của class `Rabbit` có quyền truy cập vào cả các phương thức `Rabbit`, như `rabbit.hide()`, và cả các phương thức `Animal`, như `rabbit.run()`.

Về mặt nội bộ, từ khóa `extends` hoạt động bằng cách sử dụng cơ chế prototype cũ kỹ. Nó đặt `Rabbit.prototype.[[Prototype]]` thành `Animal.prototype`. Vì vậy, nếu một phương thức không được tìm thấy trong `Rabbit.prototype`, JavaScript sẽ lấy nó từ `Animal.prototype`.

![](/article/class-inheritance/animal-rabbit-extends.svg)

Ví dụ, để tìm phương thức `rabbit.run`, engine kiểm tra (từ dưới lên trong hình):

1. Đối tượng `rabbit` (không có `run`).
2. Prototype của nó, đó là `Rabbit.prototype` (có `hide`, nhưng không có `run`).
3. Prototype của nó, đó là (do `extends`) `Animal.prototype`, cuối cùng có phương thức `run`.

Như chúng ta có thể nhớ từ chương [Native prototypes](/native-prototypes), chính JavaScript sử dụng prototypal inheritance cho các đối tượng built-in. Ví dụ `Date.prototype.[[Prototype]]` là `Object.prototype`. Đó là lý do tại sao dates có quyền truy cập vào các phương thức object generic.

Bất kỳ expression nào cũng được phép sau `extends`

Cú pháp class cho phép chỉ định không chỉ một class, mà bất kỳ expression nào sau `extends`.

Ví dụ, một function call sinh ra parent class:

```
function f(phrase) {
  return class {
    sayHi() { alert(phrase); }
  };
}

class User extends f("Hello") {}

new User().sayHi(); // Hello
```

Ở đây `class User` kế thừa từ kết quả của `f("Hello")`.

Điều đó có thể hữu ích cho các mẫu lập trình nâng cao khi chúng ta sử dụng functions để sinh ra các class dựa trên nhiều điều kiện và có thể kế thừa từ chúng.

## [Ghi đè phương thức](#overriding-a-method)

Bây giờ hãy tiến xa hơn và override một phương thức. Theo mặc định, tất cả các phương thức không được chỉ định trong `class Rabbit` được lấy trực tiếp "nguyên trạng" từ `class Animal`.

Nhưng nếu chúng ta chỉ định phương thức của riêng mình trong `Rabbit`, như `stop()` thì nó sẽ được sử dụng thay thế:

```
class Rabbit extends Animal {
  stop() {
    // ...now this will be used for rabbit.stop()
    // thay thế cho stop() từ class Animal
  }
}
```

Thông thường, tuy nhiên, chúng ta không muốn thay thế hoàn toàn một phương thức parent, mà là xây dựng dựa trên nó để tinh chỉnh hoặc mở rộng chức năng của nó. Chúng ta làm điều gì đó trong phương thức của mình, nhưng gọi phương thức parent trước/sau khi nó hoặc trong quá trình đó.

Classes cung cấp từ khóa `"super"` cho việc đó.

- `super.method(...)` để gọi một phương thức parent.
- `super(...)` để gọi một constructor parent (chỉ bên trong constructor của chúng ta).

Ví dụ, hãy làm cho rabbit autohide khi stopped:

```
class Animal {

  constructor(name) {
    this.speed = 0;
    this.name = name;
  }

  run(speed) {
    this.speed = speed;
    alert(`${this.name} runs with speed ${this.speed}.`);
  }

  stop() {
    this.speed = 0;
    alert(`${this.name} stands still.`);
  }

}

class Rabbit extends Animal {
  hide() {
    alert(`${this.name} hides!`);
  }

  stop() {
    super.stop(); // call parent stop
    this.hide(); // and then hide
  }
}

let rabbit = new Rabbit("White Rabbit");

rabbit.run(5); // White Rabbit runs with speed 5.
rabbit.stop(); // White Rabbit stands still. White Rabbit hides!
```

Bây giờ `Rabbit` có phương thức `stop` gọi phương thức `super.stop()` của parent trong quá trình đó.

Arrow functions không có `super`

Như đã đề cập trong chương [Arrow functions revisited](/arrow-functions), arrow functions không có `super`.

Nếu được truy cập, nó được lấy từ function bên ngoài. Ví dụ:

```
class Rabbit extends Animal {
  stop() {
    setTimeout(() => super.stop(), 1000); // call parent stop after 1sec
  }
}
```

`super` trong arrow function giống như trong `stop()`, vì vậy nó hoạt động như dự định. Nếu chúng ta chỉ định một function "thường" ở đây, sẽ có lỗi:

```
// Unexpected super
setTimeout(function() { super.stop() }, 1000);
```

## [Ghi đè constructor](#overriding-constructor)

Với constructors, mọi thứ trở nên hơi phức tạp.

Cho đến nay, `Rabbit` không có `constructor` riêng.

Theo [specification](https://tc39.github.io/ecma262/#sec-runtime-semantics-classdefinitionevaluation), nếu một class kế thừa từ một class khác và không có `constructor`, thì sau đây "empty" `constructor` được tạo:

```
class Rabbit extends Animal {
  // generated for extending classes without own constructors
  constructor(...args) {
    super(...args);
  }
}
```

Như chúng ta có thể thấy, nó về cơ bản gọi `constructor` parent truyền cho nó tất cả các đối số. Điều đó xảy ra nếu chúng ta không viết một constructor của riêng mình.

Bây giờ hãy thêm một constructor tùy chỉnh vào `Rabbit`. Nó sẽ chỉ định `earLength` ngoài `name`:

```
class Animal {
  constructor(name) {
    this.speed = 0;
    this.name = name;
  }
  // ...
}

class Rabbit extends Animal {

  constructor(name, earLength) {
    this.speed = 0;
    this.name = name;
    this.earLength = earLength;
  }

  // ...
}

// Doesn't work!
let rabbit = new Rabbit("White Rabbit", 10); // Error: this is not defined.
```

Whoops! Chúng ta đã gặp lỗi. Bây giờ chúng ta không thể tạo rabbits. Đã xảy ra lỗi gì?

Câu trả lời ngắn gọn là:

- **Constructors trong các class kế thừa phải gọi `super(...)`, và (!) làm điều đó trước khi sử dụng `this`.**

…Nhưng tại sao? Đã xảy ra chuyện gì ở đây? Thực ra, yêu cầu này có vẻ lạ.

Tất nhiên, có một lời giải thích. Hãy đi vào chi tiết, để bạn thực sự hiểu những gì đang xảy ra.

Trong JavaScript, có sự phân biệt giữa constructor function của một class kế thừa (được gọi là "derived constructor") và các functions khác. Một derived constructor có thuộc tính nội bộ đặc biệt `[[ConstructorKind]]:"derived"`. Đó là một nhãn nội bộ đặc biệt.

Nhãn đó ảnh hưởng đến hành vi của nó với `new`.

- Khi một function thường được thực thi với `new`, nó tạo một đối tượng rỗng và gán nó cho `this`.
- Nhưng khi một derived constructor chạy, nó không làm điều đó. Nó mong đợi constructor parent làm công việc đó.

Vì vậy một derived constructor phải gọi `super` để thực thi parent (base) constructor của nó, nếu không đối tượng cho `this` sẽ không được tạo. Và chúng ta sẽ nhận được lỗi.

Để `Rabbit` constructor hoạt động, nó cần gọi `super()` trước khi sử dụng `this`, như ở đây:

```
class Animal {

  constructor(name) {
    this.speed = 0;
    this.name = name;
  }

  // ...
}

class Rabbit extends Animal {

  constructor(name, earLength) {
    super(name);
    this.earLength = earLength;
  }

  // ...
}

// now fine
let rabbit = new Rabbit("White Rabbit", 10);
alert(rabbit.name); // White Rabbit
alert(rabbit.earLength); // 10
```

### [Ghi đè các trường class: ghi chú tinh vi](#overriding-class-fields-a-tricky-note)

Ghi chú nâng cao

Ghi chú này giả định bạn có kinh nghiệm nhất định với classes, có thể trong các ngôn ngữ lập trình khác.

Nó cung cấp cái nhìn sâu sắc hơn về ngôn ngữ và cũng giải thích hành vi có thể là nguồn gốc của bugs (nhưng không thường xuyên).

Nếu bạn thấy khó hiểu, cứ tiếp tục đọc, sau đó quay lại ghi chú này sau.

Chúng ta có thể override không chỉ methods, mà còn class fields.

Tuy nhiên, có một hành vi tinh vi khi chúng ta truy cập một field đã override trong parent constructor, khá khác với hầu hết các ngôn ngữ lập trình khác.

Xét ví dụ sau:

```
class Animal {
  name = 'animal';

  constructor() {
    alert(this.name); // (*)
  }
}

class Rabbit extends Animal {
  name = 'rabbit';
}

new Animal(); // animal
new Rabbit(); // animal
```

Ở đây, class `Rabbit` kế thừa `Animal` và override field `name` với giá trị của riêng nó.

Không có constructor riêng trong `Rabbit`, vì vậy `Animal` constructor được gọi.

Điều thú vị là trong cả hai trường hợp: `new Animal()` và `new Rabbit()`, `alert` ở dòng `(*)` hiển thị `animal`.

**Nói cách khác, parent constructor luôn sử dụng giá trị field của riêng nó, không phải giá trị đã override.**

Điều kỳ lạ là gì?

Nếu vẫn chưa rõ, vui lòng so sánh với methods.

Đây là cùng mã, nhưng thay vì field `this.name` chúng ta gọi phương thức `this.showName()`:

```
class Animal {
  showName() {  // instead of this.name = 'animal'
    alert('animal');
  }

  constructor() {
    this.showName(); // instead of alert(this.name);
  }
}

class Rabbit extends Animal {
  showName() {
    alert('rabbit');
  }
}

new Animal(); // animal
new Rabbit(); // rabbit
```

Hãy chú ý: bây giờ output khác nhau.

Và đó là những gì chúng ta mong đợi một cách tự nhiên. Khi parent constructor được gọi trong derived class, nó sử dụng phương thức đã override.

…Nhưng đối với class fields thì không phải vậy. Như đã nói, parent constructor luôn sử dụng field parent.

Tại sao có sự khác biệt?

Chà, lý do là thứ tự khởi tạo field. Class field được khởi tạo:

- Trước constructor cho base class (không kế thừa gì),
- Ngay sau `super()` cho derived class.

Trong trường hợp của chúng ta, `Rabbit` là derived class. Không có `constructor()` trong nó. Như đã nói trước đó, đó giống như có một constructor trống chỉ với `super(...args)`.

Vì vậy, `new Rabbit()` gọi `super()`, do đó thực thi parent constructor, và (theo quy tắc cho derived classes) chỉ sau đó các class fields của nó được khởi tạo. Tại thời điểm thực thi parent constructor, không có class fields `Rabbit` nào, đó là lý do tại sao `Animal` fields được sử dụng.

Sự khác biệt tinh tế giữa fields và methods là đặc thù của JavaScript.

May mắn thay, hành vi này chỉ bộc lộ nếu một field đã override được sử dụng trong parent constructor. Sau đó nó có thể khó hiểu những gì đang xảy ra, vì vậy chúng ta đang giải thích nó ở đây.

Nếu nó trở thành vấn đề, một người có thể khắc phục nó bằng cách sử dụng methods hoặc getters/setters thay vì fields.

## [Super: chi tiết nội bộ, [[HomeObject]]](#super-internals-homeobject)

Thông tin nâng cao

Nếu bạn đang đọc tutorial lần đầu tiên – phần này có thể được bỏ qua.

Nó về các cơ chế nội bộ đằng sau inheritance và `super`.

Hãy đi sâu hơn vào nội bộ của `super`. Chúng ta sẽ thấy một số điều thú vị dọc đường.

Đầu tiên phải nói, từ tất cả những gì chúng ta đã học till now, không thể để `super` hoạt động at all!

Đúng vậy, hãy tự hỏi, nó nên hoạt động về mặt kỹ thuật như thế nào? Khi một object method chạy, nó nhận được object hiện tại dưới dạng `this`. Nếu chúng ta gọi `super.method()` thì, engine cần lấy `method` từ prototype của object hiện tại. Nhưng như thế nào?

Nhiệm vụ có vẻ đơn giản, nhưng không phải vậy. Engine biết object hiện tại `this`, vì vậy nó có thể lấy parent `method` là `this.__proto__.method`. Thật không may, giải pháp "naive" như vậy sẽ không hoạt động.

Hãy minh họa vấn đề. Không có classes, sử dụng plain objects để đơn giản hóa.

Bạn có thể bỏ qua phần này và chuyển đến phần `[[HomeObject]]` bên dưới nếu bạn không muốn biết chi tiết. Điều đó sẽ không gây hại. Hoặc đọc tiếp nếu bạn quan tâm đến việc hiểu sâu sắc mọi thứ.

Trong ví dụ dưới đây, `rabbit.__proto__ = animal`. Bây giờ hãy thử: trong `rabbit.eat()` chúng ta sẽ gọi `animal.eat()`, sử dụng `this.__proto__`:

```
let animal = {
  name: "Animal",
  eat() {
    alert(`${this.name} eats.`);
  }
};

let rabbit = {
  __proto__: animal,
  name: "Rabbit",
  eat() {
    // that's how super.eat() could presumably work
    this.__proto__.eat.call(this); // (*)
  }
};

rabbit.eat(); // Rabbit eats.
```

Ở dòng `(*)` chúng ta lấy `eat` từ prototype (`animal`) và gọi nó trong ngữ cảnh của object hiện tại. Xin lưu ý rằng `.call(this)` là quan trọng ở đây, vì một đơn giản `this.__proto__.eat()` sẽ thực thi parent `eat` trong ngữ cảnh của prototype, không phải object hiện tại.

Và trong mã ở trên nó thực sự hoạt động như dự định: chúng ta có `alert` đúng.

Bây giờ hãy thêm một object nữa vào chain. Chúng ta sẽ thấy mọi thứ bị phá vỡ như thế nào:

```
let animal = {
  name: "Animal",
  eat() {
    alert(`${this.name} eats.`);
  }
};

let rabbit = {
  __proto__: animal,
  eat() {
    // ...bounce around rabbit-style and call parent (animal) method
    this.__proto__.eat.call(this); // (*)
  }
};

let longEar = {
  __proto__: rabbit,
  eat() {
    // ...do something with long ears and call parent (rabbit) method
    this.__proto__.eat.call(this); // (**)
  }
};

longEar.eat(); // Error: Maximum call stack size exceeded
```

Mã không hoạt động nữa! Chúng ta có thể thấy lỗi khi gọi `longEar.eat()`.

Nó có thể không rõ ràng như vậy, nhưng nếu chúng ta trace cuộc gọi `longEar.eat()`, thì chúng ta có thể thấy tại sao. Ở cả hai dòng `(*)` và `(**)` giá trị của `this` là object hiện tại (`longEar`). Điều đó rất quan trọng: tất cả các object methods nhận được object hiện tại là `this`, không phải prototype hoặc thứ gì khác.

Vì vậy, ở cả hai dòng `(*)` và `(**)` giá trị của `this.__proto__` giống hệt nhau: `rabbit`. Cả hai đều gọi `rabbit.eat` mà không đi lên chain trong endless loop.

Đây là hình ảnh về những gì đang xảy ra:

![](/article/class-inheritance/this-super-loop.svg)

1. Bên trong `longEar.eat()`, dòng `(**)` gọi `rabbit.eat` cung cấp cho nó `this=longEar`.

   ```
   // inside longEar.eat() we have this = longEar
   this.__proto__.eat.call(this) // (**)
   // becomes
   longEar.__proto__.eat.call(this)
   // that is
   rabbit.eat.call(this);
   ```
2. Sau đó ở dòng `(*)` của `rabbit.eat`, chúng ta muốn chuyển cuộc gọi lên cao hơn nữa trong chain, nhưng `this=longEar`, vì vậy `this.__proto__.eat` lại là `rabbit.eat`!

   ```
   // inside rabbit.eat() we also have this = longEar
   this.__proto__.eat.call(this) // (*)
   // becomes
   longEar.__proto__.eat.call(this)
   // or (again)
   rabbit.eat.call(this);
   ```
3. …Vì vậy `rabbit.eat` gọi chính nó trong endless loop, vì nó không thể ascend any further.

Vấn đề không thể được giải quyết bằng cách chỉ sử dụng `this`.

### [`[[HomeObject]]`](#homeobject)

Để cung cấp giải pháp, JavaScript thêm một thuộc tính nội bộ đặc biệt khác cho các functions: `[[HomeObject]]`.

Khi một function được chỉ định là một class hoặc object method, thuộc tính `[[HomeObject]]` của nó trở thành object đó.

Sau đó `super` sử dụng nó để resolve parent prototype và các methods của nó.

Hãy xem nó hoạt động như thế nào, đầu tiên với plain objects:

```
let animal = {
  name: "Animal",
  eat() {         // animal.eat.[[HomeObject]] == animal
    alert(`${this.name} eats.`);
  }
};

let rabbit = {
  __proto__: animal,
  name: "Rabbit",
  eat() {         // rabbit.eat.[[HomeObject]] == rabbit
    super.eat();
  }
};

let longEar = {
  __proto__: rabbit,
  name: "Long Ear",
  eat() {         // longEar.eat.[[HomeObject]] == longEar
    super.eat();
  }
};

// works correctly
longEar.eat();  // Long Ear eats.
```

Nó hoạt động như dự định, do cơ chế `[[HomeObject]]`. Một method, như `longEar.eat`, biết `[[HomeObject]]` của nó và lấy phương thức parent từ prototype của nó. Không có bất kỳ sử dụng nào của `this`.

### [Methods, not function properties](#methods-not-function-properties)

Như chúng ta đã biết trước đây, nói chung các functions là "free", không được bind vào objects trong JavaScript. Vì vậy chúng có thể được copy giữa các objects và gọi với một `this` khác.

Việc tồn tại của `[[HomeObject]]` vi phạm nguyên tắc đó, vì các methods nhớ objects của chúng. `[[HomeObject]]` không thể bị thay đổi, vì vậy bond này là vĩnh viễn.

Nơi duy nhất trong ngôn ngữ nơi `[[HomeObject]]` được sử dụng – là `super`. Vì vậy, nếu một method không sử dụng `super`, thì chúng ta vẫn có thể coi nó là free và copy giữa các objects. Nhưng với `super` mọi thứ có thể đi sai.

Đây là demo của kết quả `super` sai sau khi copy:

```
let animal = {
  sayHi() {
    alert(`I'm an animal`);
  }
};

// rabbit inherits from animal
let rabbit = {
  __proto__: animal,
  sayHi() {
    super.sayHi();
  }
};

let plant = {
  sayHi() {
    alert("I'm a plant");
  }
};

// tree inherits from plant
let tree = {
  __proto__: plant,
  sayHi: rabbit.sayHi // (*)
};

tree.sayHi();  // I'm an animal (?!?)
```

Một cuộc gọi đến `tree.sayHi()` hiển thị "I'm an animal". Chắc chắn là sai.

Lý do rất đơn giản:

- Trong dòng `(*)`, phương thức `tree.sayHi` được copy từ `rabbit`. Có lẽ chúng ta chỉ muốn tránh duplicate code?
- `[[HomeObject]]` của nó là `rabbit`, vì nó được tạo trong `rabbit`. Không có cách nào để thay đổi `[[HomeObject]]`.
- Mã của `tree.sayHi()` có `super.sayHi()` bên trong. Nó đi lên từ `rabbit` và lấy phương thức từ `animal`.

Đây là sơ đồ về những gì đang xảy ra:

![](/article/class-inheritance/super-homeobject-wrong.svg)

### [Các methods, không phải function properties](#methods-not-function-properties)

`[[HomeObject]]` được định nghĩa cho methods trong cả classes và plain objects. Nhưng đối với objects, methods phải được chỉ định chính xác là `method()`, không phải là `"method: function()"`.

Sự khác biệt có thể không quan trọng đối với chúng ta, nhưng nó quan trọng đối với JavaScript.

Trong ví dụ dưới đây một non-method syntax được sử dụng để so sánh. Thuộc tính `[[HomeObject]]` không được đặt và inheritance không hoạt động:

```
let animal = {
  eat: function() { // intentionally writing like this instead of eat() {...
    // ...
  }
};

let rabbit = {
  __proto__: animal,
  eat: function() {
    super.eat();
  }
};

rabbit.eat();  // Error calling super (because there's no [[HomeObject]])
```

## [Tóm tắt](#summary)

1. Để extend một class: `class Child extends Parent`:
   - Điều đó có nghĩa là `Child.prototype.__proto__` sẽ là `Parent.prototype`, vì vậy các methods được inheritance.
2. Khi overriding một constructor:
   - Chúng ta phải gọi parent constructor là `super()` trong `Child` constructor trước khi sử dụng `this`.
3. Khi overriding một method khác:
   - Chúng ta có thể sử dụng `super.method()` trong một `Child` method để gọi `Parent` method.
4. Nội bộ:
   - Các methods nhớ class/object của chúng trong thuộc tính nội bộ `[[HomeObject]]`. Đó là cách `super` resolve các phương thức parent.
   - Vì vậy, không an toàn để copy một method có `super` từ object này sang object khác.

Cũng:

- Arrow functions không có `this` hoặc `super` riêng, vì vậy chúng fit vào ngữ cảnh xung quanh một cách transparent.

---

---

## Bài tập

## [Các bài tập](#tasks)

### [Lỗi khi tạo instance](#error-creating-an-instance)

importance: 5

Đây là mã với `Rabbit` extending `Animal`.

Thật không may, các đối tượng `Rabbit` không thể được tạo. Đã xảy ra lỗi gì? Sửa nó.

```
class Animal {

  constructor(name) {
    this.name = name;
  }

}

class Rabbit extends Animal {
  constructor(name) {
    this.name = name;
    this.created = Date.now();
  }
}

let rabbit = new Rabbit("White Rabbit"); // Error: this is not defined
alert(rabbit.name);
```

[lời giải](#solution)

Đó là vì child constructor phải gọi `super()`.

Đây là mã đã sửa:

```
class Animal {

  constructor(name) {
    this.name = name;
  }

}

class Rabbit extends Animal {
  constructor(name) {
    super(name);
    this.created = Date.now();
  }
}

let rabbit = new Rabbit("White Rabbit"); // ok now
alert(rabbit.name); // White Rabbit
```

### [Extended clock](#extended-clock)

importance: 5

Chúng ta đã có class `Clock`. Hiện tại, nó in thời gian mỗi giây.

```
class Clock {
  constructor({ template }) {
    this.template = template;
  }

  render() {
    let date = new Date();

    let hours = date.getHours();
    if (hours < 10) hours = '0' + hours;

    let mins = date.getMinutes();
    if (mins < 10) mins = '0' + mins;

    let secs = date.getSeconds();
    if (secs < 10) secs = '0' + secs;

    let output = this.template
      .replace('h', hours)
      .replace('m', mins)
      .replace('s', secs);

    console.log(output);
  }

  stop() {
    clearInterval(this.timer);
  }

  start() {
    this.render();
    this.timer = setInterval(() => this.render(), 1000);
  }
}
```

Tạo class mới `ExtendedClock` kế thừa từ `Clock` và thêm parameter `precision` – số lượng `ms` giữa các "ticks". Mặc định nên là `1000` (1 giây).

- Mã của bạn nên nằm trong file `extended-clock.js`
- Đừng sửa đổi `clock.js` ban đầu. Extend nó.

[Mở sandbox cho bài tập.](https://plnkr.co/edit/wJs6KuZH7TGABRGy?p=preview)

[lời giải](#solution)

```
class ExtendedClock extends Clock {
  constructor(options) {
    super(options);
    let { precision = 1000 } = options;
    this.precision = precision;
  }

  start() {
    this.render();
    this.timer = setInterval(() => this.render(), this.precision);
  }
};
```

[Mở lời giải trong sandbox.](https://plnkr.co/edit/jFyrQiEw32ZfFYqN?p=preview)
