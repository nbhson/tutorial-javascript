# Mixins

> Nguồn: [https://javascript.info/mixins](https://javascript.info/mixins)

<!-- fetched: 2026-09-14 -->

Trong JavaScript chúng ta chỉ có thể kế thừa từ một object. Chỉ có một `[[Prototype]]` cho một object. Và một class có thể chỉ extends một class khác.

Nhưng đôi khi điều đó cảm thấy giới hạn. Ví dụ, chúng ta có một class `StreetSweeper` và một class `Bicycle`, và muốn tạo mix của chúng: một `StreetSweepingBicycle`.

Hoặc chúng ta có một class `User` và một class `EventEmitter` triển khai event generation, và chúng ta muốn thêm functionality của `EventEmitter` vào `User`, vì vậy users của chúng ta có thể emit events.

Có một khái niệm có thể giúp ở đây, được gọi là "mixins".

Theo định nghĩa trong Wikipedia, một [mixin](https://en.wikipedia.org/wiki/Mixin) là một class chứa các methods có thể được sử dụng bởi các classes khác mà không cần inherit từ nó.

Nói cách khác, một *mixin* cung cấp các methods triển khai một hành vi nhất định, nhưng chúng ta không sử dụng nó đơn lẻ, chúng ta sử dụng nó để thêm hành vi vào các classes khác.

## [Ví dụ về mixin](#mot-vi-du-mixin)

Cách đơn giản nhất để triển khai một mixin trong JavaScript là tạo một object có các methods hữu ích, vì vậy chúng ta có thể dễ dàng gộp chúng vào prototype của bất kỳ class nào.

Ví dụ ở đây mixin `sayHiMixin` được sử dụng để thêm "speech" cho `User`:

```
// mixin
let sayHiMixin = {
  sayHi() {
    alert(`Hello ${this.name}`);
  },
  sayBye() {
    alert(`Bye ${this.name}`);
  }
};

// usage:
class User {
  constructor(name) {
    this.name = name;
  }
}

// copy the methods
Object.assign(User.prototype, sayHiMixin);

// now User can say hi
new User("Dude").sayHi(); // Hello Dude!
```

Không có inheritance, nhưng là việc copy methods đơn giản. Vì vậy `User` có thể kế thừa từ một class khác và cũng include mixin để "mix-in" các methods bổ sung, như thế này:

```
class User extends Person {
  // ...
}

Object.assign(User.prototype, sayHiMixin);
```

Các mixins có thể sử dụng inheritance bên trong chúng.

Ví dụ, ở đây `sayHiMixin` kế thừa từ `sayMixin`:

```
let sayMixin = {
  say(phrase) {
    alert(phrase);
  }
};

let sayHiMixin = {
  __proto__: sayMixin, // (or we could use Object.setPrototypeOf to set the prototype here)

  sayHi() {
    // call parent method
    super.say(`Hello ${this.name}`); // (*)
  },
  sayBye() {
    super.say(`Bye ${this.name}`); // (*)
  }
};

class User {
  constructor(name) {
    this.name = name;
  }
}

// copy the methods
Object.assign(User.prototype, sayHiMixin);

// now User can say hi
new User("Dude").sayHi(); // Hello Dude!
```

Xin lưu ý rằng cuộc gọi đến parent method `super.say()` từ `sayHiMixin` (ở các dòng được đánh dấu bằng `(*)`) tìm phương thức trong prototype của mixin đó, không phải class.

Đây là sơ đồ (xem phần bên phải):

![](/article/mixins/mixin-inheritance.svg)

Đó là vì các methods `sayHi` và `sayBye` ban đầu được tạo trong `sayHiMixin`. Vì vậy ngay cả khi chúng được copy, thuộc tính nội bộ `[[HomeObject]]` của chúng reference đến `sayHiMixin`, như được hiển thị trong hình trên.

Vì `super` tìm kiếm các parent methods trong `[[HomeObject]].[[Prototype]]`, điều đó có nghĩa là nó tìm kiếm `sayHiMixin.[[Prototype]]`.

## [EventMixin](#eventmixin)

Bây giờ hãy tạo một mixin cho thực tế.

Một tính năng quan trọng của nhiều objects browser (ví dụ) là chúng có thể tạo events. Events là một cách tuyệt vời để "broadcast thông tin" cho bất kỳ ai muốn nó. Vì vậy hãy tạo một mixin cho phép chúng ta dễ dàng thêm các functions liên quan đến event vào bất kỳ class/object nào.

- Mixin sẽ cung cấp một method `.trigger(name, [...data])` để "generate một event" khi có gì đó quan trọng xảy ra với nó. Argument `name` là tên của event, tùy chọn được theo sau bởi các additional arguments với event data.
- Cũng là method `.on(name, handler)` thêm function `handler` như listener cho các events với tên đã cho. Nó sẽ được gọi khi một event với tên `name` đã cho trigger, và nhận các arguments từ cuộc gọi `.trigger`.
- …Và method `.off(name, handler)` xóa listener `handler`.

Sau khi thêm mixin, một object `user` sẽ có thể tạo một event `"login"` khi visitor logs in. Và một object khác, ví dụ `calendar` có thể muốn nghe các events đó để load calendar cho người đã đăng nhập.

Hoặc, một `menu` có thể tạo event `"select"` khi một menu item được chọn, và các objects khác có thể assign handlers để phản ứng với event đó. Và vân vân.

Đây là mã:

```
let eventMixin = {
  /**
   * Subscribe to event, usage:
   *  menu.on('select', function(item) { ... }
  */
  on(eventName, handler) {
    if (!this._eventHandlers) this._eventHandlers = {};
    if (!this._eventHandlers[eventName]) {
      this._eventHandlers[eventName] = [];
    }
    this._eventHandlers[eventName].push(handler);
  },

  /**
   * Cancel the subscription, usage:
   *  menu.off('select', handler)
  */
  off(eventName, handler) {
    let handlers = this._eventHandlers?.[eventName];
    if (!handlers) return;
    for (let i = 0; i < handlers.length; i++) {
      if (handlers[i] === handler) {
        handlers.splice(i--, 1);
      }
    }
  },

  /**
   * Generate an event with the given name and data
   *  this.trigger('select', data1, data2);
  */
  trigger(eventName, ...args) {
    if (!this._eventHandlers?.[eventName]) {
      return; // no handlers for that event name
    }

    // call the handlers
    this._eventHandlers[eventName].forEach(handler => handler.apply(this, args));
  }
};
```

- `.on(eventName, handler)` – gán function `handler` để chạy khi event với tên đó xảy ra. Về mặt kỹ thuật, có một property `_eventHandlers` lưu trữ một mảng các handlers cho mỗi event name, và nó chỉ thêm nó vào danh sách.
- `.off(eventName, handler)` – xóa function khỏi danh sách handlers.
- `.trigger(eventName, ...args)` – tạo event: tất cả các handlers từ `_eventHandlers[eventName]` được gọi, với danh sách arguments `...args`.

Cách dùng:

```
// Make a class
class Menu {
  choose(value) {
    this.trigger("select", value);
  }
}
// Add the mixin with event-related methods
Object.assign(Menu.prototype, eventMixin);

let menu = new Menu();

// add a handler, to be called on selection:
menu.on("select", value => alert(`Value selected: ${value}`));

// triggers the event => the handler above runs and shows:
// Value selected: 123
menu.choose("123");
```

Bây giờ, nếu chúng ta muốn bất kỳ mã nào phản ứng với menu selection, chúng ta có thể listen cho nó bằng `menu.on(...)`.

Và mixin `eventMixin` làm cho việc thêm hành vi như vậy vào bất kỳ số classes nào chúng ta muốn trở nên dễ dàng, mà không làm nhiễu chain inheritance.

## [Tóm tắt](#summary)

*Mixin* – là một thuật ngữ lập trình hướng đối tượng chung: một class chứa các methods cho các classes khác.

Một số ngôn ngữ khác cho phép kế thừa đa thừa. JavaScript không hỗ trợ kế thừa đa thừa, nhưng mixins có thể được triển khai bằng cách copy methods vào prototype.

Chúng ta có thể sử dụng mixins như một cách để mở rộng một class bằng cách thêm nhiều hành vi, như xử lý sự kiện như chúng ta đã thấy ở trên.

Các mixins có thể trở thành điểm xung đột nếu chúng vô tình ghi đè các methods class hiện có. Vì vậy nói chung một người nên suy nghĩ kỹ về việc đặt tên các methods của mixin, để giảm thiểu khả năng xảy ra điều đó.
