# Proxy và Reflect

> Source: [https://javascript.info/proxy](https://javascript.info/proxy)

<!-- fetched: 2026-09-14 -->

Một đối tượng `Proxy` bọc một đối tượng khác và chặn các thao tác, như đọc/ghi thuộc tính và các thao tác khác, tùy chọn xử lý chúng một cách độc lập, hoặc cho phép đối tượng xử lý chúng một cách trong suốt.

Proxies được sử dụng trong nhiều thư viện và một số framework trình duyệt. Chúng ta sẽ thấy nhiều ứng dụng thực tế trong bài viết này.

## [Proxy](#proxy)

Cú pháp:

```
let proxy = new Proxy(target, handler)
```

- `target` – là đối tượng để bọc, có thể là bất cứ thứ gì, bao gồm cả hàm.
- `handler` – cấu hình proxy: một đối tượng với "traps", các phương thức chặn các thao tác. – ví dụ trap `get` để đọc một thuộc tính của `target`, trap `set` để ghi thuộc tính vào `target`, và vân vân.

Đối với các thao tác trên `proxy`, nếu có trap tương ứng trong `handler`, thì nó sẽ chạy, và proxy có cơ hội xử lý nó, nếu không thì thao tác được thực hiện trên `target`.

Như một ví dụ khởi đầu, hãy tạo một proxy không có trap nào:

```
let target = {};
let proxy = new Proxy(target, {}); // handler trống

proxy.test = 5; // ghi vào proxy (1)
alert(target.test); // 5, thuộc tính xuất hiện trong target!

alert(proxy.test); // 5, chúng ta có thể đọc nó từ proxy (2)

for(let key in proxy) alert(key); // test, iteration hoạt động (3)
```

Vì không có trap nào, tất cả các thao tác trên `proxy` được chuyển tiếp đến `target`.

1. Thao tác ghi `proxy.test=` đặt giá trị lên `target`.
2. Thao tác đọc `proxy.test` trả về giá trị từ `target`.
3. Iteration qua `proxy` trả về giá trị từ `target`.

Như chúng ta có thể thấy, không có trap nào, `proxy` là một wrapper trong suốt xung quanh `target`.

![](/article/proxy/proxy.svg)

`Proxy` là một đối tượng "exotic" đặc biệt. Nó không có thuộc tính riêng. Với `handler` trống, nó chuyển tiếp các thao tác một cách trong suốt đến `target`.

Để kích hoạt nhiều khả năng hơn, hãy thêm traps.

Chúng ta có thể chặn những gì?

Đối với hầu hết các thao tác trên đối tượng, có một "phương thức nội bộ" trong đặc tả JavaScript mô tả cách nó hoạt động ở mức thấp nhất. Ví dụ `[[Get]]`, phương thức nội bộ để đọc thuộc tính, `[[Set]]`, phương thức nội bộ để ghi thuộc tính, và vân vân. Các phương thức này chỉ được sử dụng trong đặc tả, chúng ta không thể gọi chúng trực tiếp bằng tên.

Proxy traps chặn các lời gọi của các phương thức này. Chúng được liệt kê trong [đặc tả Proxy](https://tc39.es/ecma262/#sec-proxy-object-internal-methods-and-internal-slots) và trong bảng dưới đây.

Đối với mỗi phương thức nội bộ, có một trap trong bảng này: tên của phương thức mà chúng ta có thể thêm vào tham số `handler` của `new Proxy` để chặn thao tác:

| Phương thức nội bộ | Phương thức Handler | Kích hoạt khi… |
| --- | --- | --- |
| `[[Get]]` | `get` | đọc thuộc tính |
| `[[Set]]` | `set` | ghi vào thuộc tính |
| `[[HasProperty]]` | `has` | toán tử `in` |
| `[[Delete]]` | `deleteProperty` | toán tử `delete` |
| `[[Call]]` | `apply` | gọi hàm |
| `[[Construct]]` | `construct` | toán tử `new` |
| `[[GetPrototypeOf]]` | `getPrototypeOf` | [Object.getPrototypeOf](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/getPrototypeOf) |
| `[[SetPrototypeOf]]` | `setPrototypeOf` | [Object.setPrototypeOf](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/setPrototypeOf) |
| `[[IsExtensible]]` | `isExtensible` | [Object.isExtensible](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/isExtensible) |
| `[[PreventExtensions]]` | `preventExtensions` | [Object.preventExtensions](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/preventExtensions) |
| `[[DefineOwnProperty]]` | `defineProperty` | [Object.defineProperty](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/defineProperty), [Object.defineProperties](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/defineProperties) |
| `[[GetOwnProperty]]` | `getOwnPropertyDescriptor` | [Object.getOwnPropertyDescriptor](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/getOwnPropertyDescriptor), `for..in`, `Object.keys/values/entries` |
| `[[OwnPropertyKeys]]` | `ownKeys` | [Object.getOwnPropertyNames](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/getOwnPropertyNames), [Object.getOwnPropertySymbols](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/getOwnPropertySymbols), `for..in`, `Object.keys/values/entries` |

Các bất biến (Invariants)

JavaScript thực thi một số bất biến – các điều kiện phải được thỏa mãn bởi các phương thức nội bộ và traps.

Hầu hết trong số chúng là cho các giá trị trả về:

- `[[Set]]` phải trả về `true` nếu giá trị được ghi thành công, nếu không thì `false`.
- `[[Delete]]` phải trả về `true` nếu giá trị bị xóa thành công, nếu không thì `false`.
- …và tương tự, chúng ta sẽ thấy thêm trong các ví dụ dưới đây.

Có một số bất biến khác, như:

- `[[GetPrototypeOf]]`, áp dụng cho đối tượng proxy phải trả về cùng giá trị như `[[GetPrototypeOf]]` áp dụng cho đối tượng target của proxy. Nói cách khác, đọc prototype của proxy phải luôn trả về prototype của đối tượng target.

Traps có thể chặn các thao tác này, nhưng chúng phải tuân theo các quy tắc này.

Các bất biến đảm bảo hành vi đúng và nhất quán của các tính năng ngôn ngữ. Danh sách đầy đủ các bất biến có trong [đặc tả](https://tc39.es/ecma262/#sec-proxy-object-internal-methods-and-internal-slots). Bạn sẽ không vi phạm chúng nếu bạn không làm điều gì đó kỳ lạ.

Hãy xem cách nó hoạt động trong các ví dụ thực tế.

## [Giá trị mặc định với trap "get"](#default-value-with-get-trap)

Các trap phổ biến nhất là để đọc/ghi thuộc tính.

Để chặn đọc, `handler` nên có phương thức `get(target, property, receiver)`.

Nó kích hoạt khi một thuộc tính được đọc, với các đối số sau:

- `target` – là đối tượng target, đối tượng được truyền làm đối số đầu tiên cho `new Proxy`,
- `property` – tên thuộc tính,
- `receiver` – nếu thuộc tính target là getter, thì `receiver` là đối tượng sẽ được sử dụng làm `this` trong lời gọi của nó. Thường thì đó là đối tượng `proxy` chính nó (hoặc đối tượng kế thừa từ nó, nếu chúng ta kế thừa từ proxy). Hiện tại chúng ta không cần đối số này, vì vậy nó sẽ được giải thích chi tiết hơn sau.

Hãy sử dụng `get` để triển khai các giá trị mặc định cho một đối tượng.

Chúng ta sẽ tạo một mảng số trả về `0` cho các giá trị không tồn tại.

Thông thường khi ai đó cố gắng lấy một mục mảng không tồn tại, họ nhận được `undefined`, nhưng chúng ta sẽ bọc một mảng thông thường vào proxy chặn đọc và trả về `0` nếu không có thuộc tính đó:

```
let numbers = [0, 1, 2];

numbers = new Proxy(numbers, {
  get(target, prop) {
    if (prop in target) {
      return target[prop];
    } else {
      return 0; // giá trị mặc định
    }
  }
});

alert( numbers[1] ); // 1
alert( numbers[123] ); // 0 (không có mục đó)
```

Như chúng ta có thể thấy, điều đó khá dễ dàng với trap `get`.

Chúng ta có thể sử dụng `Proxy` để triển khai bất kỳ logic nào cho các "giá trị mặc định".

Hãy tưởng tượng chúng ta có một từ điển, với các cụm từ và bản dịch của chúng:

```
let dictionary = {
  'Hello': 'Hola',
  'Bye': 'Adiós'
};

alert( dictionary['Hello'] ); // Hola
alert( dictionary['Welcome'] ); // undefined
```

Hiện tại, nếu không có cụm từ, đọc từ `dictionary` trả về `undefined`. Nhưng trong thực tế, để lại một cụm từ không dịch thường tốt hơn `undefined`. Vì vậy hãy làm cho nó trả về cụm từ chưa dịch trong trường hợp đó thay vì `undefined`.

Để đạt được điều đó, chúng ta sẽ bọc `dictionary` trong một proxy chặn các thao tác đọc:

```
let dictionary = {
  'Hello': 'Hola',
  'Bye': 'Adiós'
};

dictionary = new Proxy(dictionary, {
  get(target, phrase) { // chặn đọc thuộc tính từ dictionary
    if (phrase in target) { // nếu chúng ta có nó trong từ điển
      return target[phrase]; // trả về bản dịch
    } else {
      // nếu không, trả về cụm từ chưa dịch
      return phrase;
    }
  }
});

// Tra cứu bất kỳ cụm từ nào trong từ điển!
// Tệ nhất là chúng không được dịch.
alert( dictionary['Hello'] ); // Hola
alert( dictionary['Welcome to Proxy']); // Welcome to Proxy (không dịch)
```

Xin lưu ý:

Xin lưu ý cách proxy ghi đè biến:

```
dictionary = new Proxy(dictionary, ...);
```

Proxy nên thay thế hoàn toàn đối tượng target ở mọi nơi. Không ai nên tham chiếu đến đối tượng target sau khi nó đã được proxy. Nếu không thì dễ gây nhầm lẫn.

## [Xác thực với trap "set"](#validation-with-set-trap)

Hãy nói chúng ta muốn một mảng chỉ dành cho số. Nếu một giá trị loại khác được thêm vào, sẽ có lỗi.

Trap `set` kích hoạt khi một thuộc tính được ghi.

`set(target, property, value, receiver)`:

- `target` – là đối tượng target, đối tượng được truyền làm đối số đầu tiên cho `new Proxy`,
- `property` – tên thuộc tính,
- `value` – giá trị thuộc tính,
- `receiver` – giống như trap `get`, chỉ quan trọng đối với các thuộc tính setter.

Trap `set` nên trả về `true` nếu việc ghi thành công, và `false` nếu không (kích hoạt `TypeError`).

Hãy sử dụng nó để xác thực các giá trị mới:

```
let numbers = [];

numbers = new Proxy(numbers, { // (*)
  set(target, prop, val) { // để chặn ghi thuộc tính
    if (typeof val == 'number') {
      target[prop] = val;
      return true;
    } else {
      return false;
    }
  }
});

numbers.push(1); // thêm thành công
numbers.push(2); // thêm thành công
alert("Length is: " + numbers.length); // 2

numbers.push("test"); // TypeError ('set' on proxy returned false)

alert("This line is never reached (error in the line above)");
```

Xin lưu ý: functionality tích hợp sẵn của arrays vẫn đang hoạt động! Giá trị được thêm bởi `push`. Thuộc tính `length` tự động tăng khi các giá trị được thêm. Proxy của chúng ta không phá vỡ bất kỳ thứ gì.

Chúng ta không phải ghi đè các phương thức thêm giá trị của mảng như `push` và `unshift`, và vân vân, để thêm kiểm tra vào đó, vì nội bộ chúng sử dụng thao tác `[[Set]]` được proxy chặn.

Vì vậy mã sạch và gọn gàng.

Đừng quên trả về `true`

Như đã nói ở trên, có các bất biến cần tuân thủ.

Đối với `set`, nó phải trả về `true` cho việc ghi thành công.

Nếu chúng ta quên làm vậy hoặc trả về bất kỳ giá trị falsy nào, thao tác sẽ kích hoạt `TypeError`.

## [Iteration với "ownKeys" và "getOwnPropertyDescriptor"](#iteration-with-ownkeys-and-getownpropertydescriptor)

`Object.keys`, vòng lặp `for..in` và hầu hết các phương thức khác lặp qua các thuộc tính đối tượng sử dụng phương thức nội bộ `[[OwnPropertyKeys]]` (được chặn bởi trap `ownKeys`) để nhận danh sách các thuộc tính.

Các phương thức này khác nhau ở chi tiết:

- `Object.getOwnPropertyNames(obj)` trả về các key không-symbol.
- `Object.getOwnPropertySymbols(obj)` trả về các key symbol.
- `Object.keys/values()` trả về các key/value không-symbol với cờ `enumerable` (các cờ thuộc tính được giải thích trong bài viết [Cờ và mô tả thuộc tính](/property-descriptors)).
- `for..in` lặp qua các key không-symbol với cờ `enumerable`, và cũng bao gồm các key prototype.

…Nhưng tất cả chúng đều bắt đầu với danh sách đó.

Trong ví dụ dưới đây chúng ta sử dụng trap `ownKeys` để làm cho vòng lặp `for..in` qua `user`, và cũng `Object.keys` và `Object.values`, bỏ qua các thuộc tính bắt đầu bằng dấu gạch dưới `_`:

```
let user = {
  name: "John",
  age: 30,
  _password: "***"
};

user = new Proxy(user, {
  ownKeys(target) {
    return Object.keys(target).filter(key => !key.startsWith('_'));
  }
});

// "ownKeys" lọc ra _password
for(let key in user) alert(key); // name, then: age

// same effect on these methods:
alert( Object.keys(user) ); // name,age
alert( Object.values(user) ); // John,30
```

Cho đến nay, nó hoạt động.

Mặc dù, nếu chúng ta trả về một key không tồn tại trong đối tượng, `Object.keys` sẽ không liệt kê nó:

```
let user = { };

user = new Proxy(user, {
  ownKeys(target) {
    return ['a', 'b', 'c'];
  }
});

alert( Object.keys(user) ); // <empty>
```

Tại sao? Lý do đơn giản: `Object.keys` chỉ trả về các thuộc tính với cờ `enumerable`. Để kiểm tra nó, nó gọi phương thức nội bộ `[[GetOwnProperty]]` cho mọi thuộc tính để nhận [mô tả của nó](/property-descriptors). Và ở đây, vì không có thuộc tính, mô tả của nó trống, không có cờ `enumerable`, vì vậy nó bị bỏ qua.

Để `Object.keys` trả về một thuộc tính, chúng ta cần nó tồn tại trong đối tượng, với cờ `enumerable`, hoặc chúng ta có thể chặn các lời gọi đến `[[GetOwnProperty]]` (trap `getOwnPropertyDescriptor` làm điều đó), và trả về một mô tả với `enumerable: true`.

Đây là một ví dụ về điều đó:

```
let user = { };

user = new Proxy(user, {
  ownKeys(target) { // được gọi một lần để nhận danh sách thuộc tính
    return ['a', 'b', 'c'];
  },

  getOwnPropertyDescriptor(target, prop) { // được gọi cho mỗi thuộc tính
    return {
      enumerable: true,
      configurable: true
      /* ...other flags, probable "value:..." */
    };
  }

});

alert( Object.keys(user) ); // a, b, c
```

Hãy ghi nhớ một lần nữa: chúng ta chỉ cần chặn `[[GetOwnProperty]]` nếu thuộc tính không có trong đối tượng.

## [Thuộc tính được bảo vệ với "deleteProperty" và các trap khác](#protected-properties-with-deleteproperty-and-other-traps)

Có một quy ước phổ biến rằng các thuộc tính và phương thức có tiền tố là dấu gạch dưới `_` là thuộc tính nội bộ. Chúng không nên được truy cập từ bên ngoài đối tượng.

Về mặt kỹ thuật điều đó có thể:

```
let user = {
  name: "John",
  _password: "secret"
};

alert(user._password); // secret
```

Hãy sử dụng proxies để ngăn chặn bất kỳ truy cập nào vào các thuộc tính bắt đầu với `_`.

Chúng ta sẽ cần các traps:

- `get` để ném lỗi khi đọc thuộc tính như vậy,
- `set` để ném lỗi khi ghi,
- `deleteProperty` để ném lỗi khi xóa,
- `ownKeys` để loại bỏ các thuộc tính bắt đầu với `_` khỏi `for..in` và các phương thức như `Object.keys`.

Đây là mã:

```
let user = {
  name: "John",
  _password: "***"
};

user = new Proxy(user, {
  get(target, prop) {
    if (prop.startsWith('_')) {
      throw new Error("Access denied");
    }
    let value = target[prop];
    return (typeof value === 'function') ? value.bind(target) : value; // (*)
  },
  set(target, prop, val) { // để chặn ghi thuộc tính
    if (prop.startsWith('_')) {
      throw new Error("Access denied");
    } else {
      target[prop] = val;
      return true;
    }
  },
  deleteProperty(target, prop) { // để chặn xóa thuộc tính
    if (prop.startsWith('_')) {
      throw new Error("Access denied");
    } else {
      delete target[prop];
      return true;
    }
  },
  ownKeys(target) { // để chặn danh sách thuộc tính
    return Object.keys(target).filter(key => !key.startsWith('_'));
  }
});

// "get" không cho phép đọc _password
try {
  alert(user._password); // Error: Access denied
} catch(e) { alert(e.message); }

// "set" không cho phép ghi _password
try {
  user._password = "test"; // Error: Access denied
} catch(e) { alert(e.message); }

// "deleteProperty" không cho phép xóa _password
try {
  delete user._password; // Error: Access denied
} catch(e) { alert(e.message); }

// "ownKeys" lọc ra _password
for(let key in user) alert(key); // name
```

Xin lưu ý chi tiết quan trọng trong trap `get`, ở dòng `(*)`:

```
get(target, prop) {
  // ...
  let value = target[prop];
  return (typeof value === 'function') ? value.bind(target) : value; // (*)
}
```

Tại sao chúng ta cần một hàm để gọi `value.bind(target)`?

Lý do là các phương thức đối tượng, chẳng hạn như `user.checkPassword()`, phải có thể truy cập `_password`:

```
user = {
  // ...
  checkPassword(value) {
    // object method must be able to read _password
    return value === this._password;
  }
}
```

Một lời gọi đến `user.checkPassword()` nhận proxied `user` làm `this` (đối tượng trước dấu chấm trở thành `this`), vì vậy khi nó cố gắng truy cập `this._password`, trap `get` kích hoạt (nó kích hoạt khi bất kỳ thuộc tính nào được đọc) và ném lỗi.

Vì vậy chúng ta bind ngữ cảnh của các phương thức đối tượng với đối tượng gốc, `target`, ở dòng `(*)`. Sau đó các cuộc gọi tiếp theo sẽ sử dụng `target` làm `this`, không có trap nào.

Giải pháp đó thường hoạt động, nhưng không lý tưởng, vì một phương thức có thể chuyển đối tượng không được bọc đi đâu đó, và sau đó chúng ta sẽ bị rối: đâu là đối tượng gốc, và đâu là đối tượng đã được proxy?

Bên cạnh đó, một đối tượng có thể được proxy nhiều lần (nhiều proxy có thể thêm các "tinh chỉnh" khác nhau vào đối tượng), và nếu chúng ta chuyển một đối tượng chưa được bọc đến một phương thức, có thể có hậu quả không mong muốn.

Vì vậy, proxy như vậy không nên được sử dụng ở mọi nơi.

Thuộc tính riêng của class

Các engine JavaScript hiện đại hỗ trợ native các thuộc tính riêng trong classes, có tiền tố `#`. Chúng được mô tả trong bài viết [Thuộc tính và phương thức riêng và được bảo vệ](/private-protected-properties-methods). Không cần proxy.

Những thuộc tính đó có các vấn đề riêng của chúng. Cụ thể, chúng không được kế thừa.

## ["Có trong khoảng" với trap "has"](#in-range-with-has-trap)

Hãy xem thêm các ví dụ.

Chúng ta có một đối tượng range:

```
let range = {
  start: 1,
  end: 10
};
```

Chúng ta muốn sử dụng toán tử `in` để kiểm tra rằng một số nằm trong `range`.

Trap `has` chặn các cuộc gọi `in`.

`has(target, property)`

- `target` – là đối tượng target, được truyền làm đối số đầu tiên cho `new Proxy`,
- `property` – tên thuộc tính

Đây là bản demo:

```
let range = {
  start: 1,
  end: 10
};

range = new Proxy(range, {
  has(target, prop) {
    return prop >= target.start && prop <= target.end;
  }
});

alert(5 in range); // true
alert(50 in range); // false
```

Sugar cú pháp đẹp, phải không? Và rất dễ triển khai.

## [Bọc hàm: "apply"](#proxy-apply)

Chúng ta có thể bọc một proxy xung quanh một hàm.

Trap `apply(target, thisArg, args)` xử lý việc gọi một proxy như một hàm:

- `target` là đối tượng target (hàm là một đối tượng trong JavaScript),
- `thisArg` là giá trị của `this`.
- `args` là danh sách các đối số.

Ví dụ, hãy nhớ lại decorator `delay(f, ms)`, mà chúng ta đã làm trong bài viết [Decorators và forwarding, call/apply](/call-apply-decorators).

Trong bài viết đó chúng ta làm mà không có proxies. Một cuộc gọi đến `delay(f, ms)` trả về một hàm chuyển tiếp tất cả các cuộc gọi đến `f` sau `ms` milliseconds.

Đây là implementation dựa trên hàm trước đó:

```
function delay(f, ms) {
  // return a wrapper that passes the call to f after the timeout
  return function() { // (*)
    setTimeout(() => f.apply(this, arguments), ms);
  };
}

function sayHi(user) {
  alert(`Hello, ${user}!`);
}

// sau khi wrapping này, các cuộc gọi đến sayHi sẽ bị trễ 3 giây
sayHi = delay(sayHi, 3000);

sayHi("John"); // Hello, John! (sau 3 giây)
```

Như chúng ta đã thấy, điều đó chủ yếu hoạt động. Hàm wrapper `(*)` thực hiện cuộc gọi sau timeout.

Nhưng hàm wrapper không chuyển tiếp các thao tác đọc/ghi thuộc tính hoặc bất kỳ thứ gì khác. Sau khi wrapping, quyền truy cập vào các thuộc tính của hàm gốc bị mất, chẳng hạn như `name`, `length` và các thuộc tính khác:

```
function delay(f, ms) {
  return function() {
    setTimeout(() => f.apply(this, arguments), ms);
  };
}

function sayHi(user) {
  alert(`Hello, ${user}!`);
}

alert(sayHi.length); // 1 (function length là số lượng đối số trong khai báo của nó)

sayHi = delay(sayHi, 3000);

alert(sayHi.length); // 0 (trong khai báo wrapper, có không có đối số)
```

`Proxy` mạnh mẽ hơn nhiều, vì nó chuyển tiếp mọi thứ đến đối tượng target.

Hãy sử dụng `Proxy` thay vì hàm wrapper:

```
function delay(f, ms) {
  return new Proxy(f, {
    apply(target, thisArg, args) {
      setTimeout(() => target.apply(thisArg, args), ms);
    }
  });
}

function sayHi(user) {
  alert(`Hello, ${user}!`);
}

sayHi = delay(sayHi, 3000);

alert(sayHi.length); // 1 (*) proxy chuyển tiếp thao tác "get length" đến target

sayHi("John"); // Hello, John! (sau 3 giây)
```

Kết quả giống nhau, nhưng giờ không chỉ các cuộc gọi, mà tất cả các thao tác trên proxy được chuyển tiếp đến hàm gốc. Vì vậy `sayHi.length` được trả về chính xác sau khi wrapping ở dòng `(*)`.

Chúng ta có một "wrapper" phong phú hơn.

Các trap khác tồn tại: danh sách đầy đủ có ở đầu bài viết này. Mẫu sử dụng của chúng tương tự như ở trên.

## [Reflect](#reflect)

`Reflect` là một object tích hợp sẵn giúp tạo `Proxy`.

Đã nói trước đó rằng các phương thức nội bộ, chẳng hạn như `[[Get]]`, `[[Set]]` và các phương thức khác chỉ dành cho đặc tả, chúng không thể được gọi trực tiếp.

Đối tượng `Reflect` làm cho điều đó có phần khả thi. Các phương thức của nó là các wrapper tối thiểu xung quanh các phương thức nội bộ.

Dưới đây là các ví dụ về các thao tác và lời gọi `Reflect` làm cùng một điều:

| Thao tác | Lời gọi `Reflect` | Phương thức nội bộ |
| --- | --- | --- |
| `obj[prop]` | `Reflect.get(obj, prop)` | `[[Get]]` |
| `obj[prop] = value` | `Reflect.set(obj, prop, value)` | `[[Set]]` |
| `delete obj[prop]` | `Reflect.deleteProperty(obj, prop)` | `[[Delete]]` |
| `new F(value)` | `Reflect.construct(F, value)` | `[[Construct]]` |
| … | … | … |

Ví dụ:

```
let user = {};

Reflect.set(user, 'name', 'John');

alert(user.name); // John
```

Đặc biệt, `Reflect` cho phép chúng ta gọi các toán tử (`new`, `delete`…) dưới dạng các hàm (`Reflect.construct`, `Reflect.deleteProperty`, …). Đó là một khả năng thú vị, nhưng ở đây một thứ khác quan trọng.

**Đối với mỗi phương thức nội bộ, có thể bị chặn bởi `Proxy`, có một phương thức tương ứng trong `Reflect`, với cùng tên và đối số như trap `Proxy`.**

Vì vậy chúng ta có thể sử dụng `Reflect` để chuyển tiếp một thao tác đến đối tượng gốc.

Trong ví dụ này, cả hai trap `get` và `set` chuyển tiếp các thao tác đọc/ghi một cách trong suốt (như thể chúng không tồn tại) đến đối tượng, hiển thị thông báo:

```
let user = {
  name: "John",
};

user = new Proxy(user, {
  get(target, prop, receiver) {
    alert(`GET ${prop}`);
    return Reflect.get(target, prop, receiver); // (1)
  },
  set(target, prop, val, receiver) {
    alert(`SET ${prop}=${val}`);
    return Reflect.set(target, prop, val, receiver); // (2)
  }
});

let name = user.name; // hiển thị "GET name"
user.name = "Pete"; // hiển thị "SET name=Pete"
```

Ở đây:

- `Reflect.get` đọc một thuộc tính đối tượng.
- `Reflect.set` ghi một thuộc tính đối tượng và trả về `true` nếu thành công, `false` nếu không.

Nghĩa là, mọi thứ đơn giản: nếu một trap muốn chuyển tiếp cuộc gọi đến đối tượng, chỉ cần gọi `Reflect.<method>` với các đối số tương tự.

Trong hầu hết các trường hợp chúng ta có thể làm điều tương tự mà không có `Reflect`, ví dụ đọc thuộc tính `Reflect.get(target, prop, receiver)` có thể được thay thế bằng `target[prop]`. Tuy nhiên có các sắc thái quan trọng.

### [Proxying một getter](#proxying-a-getter)

Hãy xem một ví dụ minh họa tại sao `Reflect.get` tốt hơn. Và chúng ta cũng sẽ thấy tại sao `get/set` có đối số thứ ba `receiver`, mà chúng ta chưa sử dụng trước đây.

Chúng ta có một đối tượng `user` với thuộc tính `_name` và một getter cho nó.

Đây là một proxy xung quanh nó:

```
let user = {
  _name: "Guest",
  get name() {
    return this._name;
  }
};

let userProxy = new Proxy(user, {
  get(target, prop, receiver) {
    return target[prop];
  }
});

alert(userProxy.name); // Guest
```

Trap `get` là "trong suốt" ở đây, nó trả về thuộc tính gốc, và không làm gì khác. Điều đó đủ cho ví dụ của chúng ta.

Mọi thứ có vẻ ổn. Nhưng hãy làm cho ví dụ phức tạp hơn một chút.

Sau khi kế thừa một đối tượng khác `admin` từ `user`, chúng ta có thể quan sát hành vi không chính xác:

```
let user = {
  _name: "Guest",
  get name() {
    return this._name;
  }
};

let userProxy = new Proxy(user, {
  get(target, prop, receiver) {
    return target[prop]; // (*) target = user
  }
});

let admin = {
  __proto__: userProxy,
  _name: "Admin"
};

// Expected: Admin
alert(admin.name); // outputs: Guest (?!?)
```

Đọc `admin.name` nên trả về `"Admin"`, không phải `"Guest"`!

Vấn đề là gì? Có lẽ chúng ta đã làm sai điều gì đó với kế thừa?

Nhưng nếu chúng ta bỏ proxy đi, thì mọi thứ sẽ hoạt động như mong đợi.

Vấn đề thực sự nằm ở proxy, ở dòng `(*)`.

1. Khi chúng ta đọc `admin.name`, vì đối tượng `admin` không có thuộc tính riêng như vậy, tìm kiếm đi đến prototype của nó.
2. Prototype là `userProxy`.
3. Khi đọc thuộc tính `name` từ proxy, trap `get` của nó kích hoạt và trả về nó từ đối tượng gốc là `target[prop]` ở dòng `(*)`.

   Một cuộc gọi đến `target[prop]`, khi `prop` là một getter, chạy mã của nó trong ngữ cảnh `this=target`. Vì vậy kết quả là `this._name` từ đối tượng gốc `target`, tức là: từ `user`.

Để sửa các tình huống như vậy, chúng ta cần `receiver`, đối số thứ ba của trap `get`. Nó giữ `this` đúng để chuyển đến getter. Trong trường hợp này là `admin`.

Làm thế nào để chuyển ngữ cảnh cho một getter? Đối với một hàm thông thường chúng ta có thể sử dụng `call/apply`, nhưng đó là một getter, nó không được "gọi", chỉ được truy cập.

`Reflect.get` có thể làm điều đó. Mọi thứ sẽ hoạt động đúng nếu chúng ta sử dụng nó.

Đây là biến thể được sửa chữa:

```
let user = {
  _name: "Guest",
  get name() {
    return this._name;
  }
};

let userProxy = new Proxy(user, {
  get(target, prop, receiver) { // receiver = admin
    return Reflect.get(target, prop, receiver); // (*)
  }
});

let admin = {
  __proto__: userProxy,
  _name: "Admin"
};

alert(admin.name); // Admin
```

Giờ `receiver` giữ tham chiếu đến `this` đúng (tức là `admin`), được chuyển đến getter bằng `Reflect.get` ở dòng `(*)`.

Chúng ta có thể viết lại trap ngắn gọn hơn nữa:

```
get(target, prop, receiver) {
  return Reflect.get(...arguments);
}
```

Các lời gọi `Reflect` được đặt tên chính xác giống như các trap và chấp nhận các đối số tương tự. Chúng được thiết kế đặc biệt như vậy.

Vì vậy, `return Reflect...` cung cấp một cách an toàn để chuyển tiếp thao tác và đảm bảo chúng ta không quên bất kỳ thứ gì liên quan đến nó.

## [Giới hạn của Proxy](#proxy-limitations)

Proxies cung cấp một cách duy nhất để thay đổi hoặc tinh chỉnh hành vi của các đối tượng hiện có ở mức thấp nhất. Vẫn còn đó, nó không hoàn hảo. Có các giới hạn.

### [Các đối tượng tích hợp sẵn: Internal slots](#built-in-objects-internal-slots)

Nhiều đối tượng tích hợp sẵn, chẳng hạn như `Map`, `Set`, `Date`, `Promise` và các đối tượng khác sử dụng những gì được gọi là "internal slots".

Đây giống như các thuộc tính, nhưng được dành riêng cho các mục đích nội bộ, chỉ dành cho đặc tả. Ví dụ, `Map` lưu trữ các mục trong internal slot `[[MapData]]`. Các phương thức tích hợp sẵn truy cập chúng trực tiếp, không thông qua các phương thức nội bộ `[[Get]]/[[Set]]`. Vì vậy `Proxy` không thể chặn được.

Tại sao phải quan tâm? Chúng là internal anyway!

Chà, đây là vấn đề. Sau khi một đối tượng tích hợp sẵn như vậy được proxy, proxy không có các internal slots này, vì vậy các phương thức tích hợp sẵn sẽ thất bại.

Ví dụ:

```
let map = new Map();

let proxy = new Proxy(map, {});

proxy.set('test', 1); // Error
```

Nội bộ, một `Map` lưu trữ tất cả dữ liệu trong internal slot `[[MapData]]` của nó. Proxy không có slot như vậy. Phương thức tích hợp sẵn [Map.prototype.set](https://tc39.es/ecma262/#sec-map.prototype.set) cố gắng truy cập thuộc tính nội bộ `this.[[MapData]]`, nhưng vì `this=proxy`, không tìm thấy nó trong `proxy` và просто thất bại.

May mắn thay, có một cách để sửa nó:

```
let map = new Map();

let proxy = new Proxy(map, {
  get(target, prop, receiver) {
    let value = Reflect.get(...arguments);
    return typeof value == 'function' ? value.bind(target) : value;
  }
});

proxy.set('test', 1);
alert(proxy.get('test')); // 1 (works!)
```

Giờ nó hoạt động tốt, vì trap `get` bind các thuộc tính hàm, chẳng hạn như `map.set`, đến đối tượng target (`map`) chính nó.

Khác với ví dụ trước đó, giá trị của `this` bên trong `proxy.set(...)` sẽ không phải là `proxy`, mà là `map` gốc. Vì vậy khi implementation nội bộ của `set` cố gắng truy cập internal slot `this.[[MapData]]`, nó thành công.

`Array` không có internal slots

Một ngoại lệ đáng chú ý: `Array` tích hợp sẵn không sử dụng internal slots. Đó là vì lý do lịch sử, vì nó xuất hiện từ rất lâu.

Vì vậy không có vấn đề như vậy khi proxy một mảng.

### [Các trường riêng](#private-fields)

Một thứ tương tự xảy ra với các trường class riêng.

Ví dụ, phương thức `getName()` truy cập thuộc tính riêng `#name` và bị lỗi sau khi proxy:

```
class User {
  #name = "Guest";

  getName() {
    return this.#name;
  }
}

let user = new User();

user = new Proxy(user, {});

alert(user.getName()); // Error
```

Lý do là các trường riêng được implement bằng các internal slots. JavaScript không sử dụng `[[Get]]/[[Set]]` khi truy cập chúng.

Trong cuộc gọi `getName()` giá trị của `this` là `user` đã proxy, và nó không có slot với các trường riêng.

Một lần nữa, giải pháp với việc bind phương thức làm cho nó hoạt động:

```
class User {
  #name = "Guest";

  getName() {
    return this.#name;
  }
}

let user = new User();

user = new Proxy(user, {
  get(target, prop, receiver) {
    let value = Reflect.get(...arguments);
    return typeof value == 'function' ? value.bind(target) : value;
  }
});

alert(user.getName()); // Guest
```

Tuy nhiên, giải pháp có các nhược điểm, như đã giải thích trước đây: nó tiếp xúc đối tượng gốc cho phương thức, có khả năng cho phép nó được chuyển tiếp và phá vỡ các functionality proxy khác.

### [Proxy != target](#proxy-target)

Proxy và đối tượng gốc là các đối tượng khác nhau. Điều đó tự nhiên, phải không?

Vì vậy nếu chúng ta sử dụng đối tượng gốc làm key, và sau đó proxy nó, thì proxy không thể tìm thấy:

```
let allUsers = new Set();

class User {
  constructor(name) {
    this.name = name;
    allUsers.add(this);
  }
}

let user = new User("John");

alert(allUsers.has(user)); // true

user = new Proxy(user, {});

alert(allUsers.has(user)); // false
```

Như chúng ta có thể thấy, sau khi proxy chúng ta không thể tìm thấy `user` trong set `allUsers`, vì proxy là một đối tượng khác.

Proxies không thể chặn phép kiểm tra equality nghiêm ngặt `===`

Proxies có thể chặn nhiều toán tử, chẳng hạn như `new` (với `construct`), `in` (với `has`), `delete` (với `deleteProperty`) và vân vân.

Nhưng không có cách nào để chặn phép kiểm tra equality nghiêm ngặt cho các đối tượng. Một đối tượng chỉ bằng chính nó, và không có giá trị nào khác.

Vì vậy tất cả các thao tác và các class tích hợp sẵn so sánh các đối tượng cho equality sẽ phân biệt giữa đối tượng và proxy. Không có thay thế trong suốt ở đây.

## [Proxies có thể thu hồi](#revocable-proxies)

Một *proxy có thể thu hồi* là một proxy có thể bị vô hiệu hóa.

Hãy nói chúng ta có một resource, và muốn đóng quyền truy cập vào nó bất cứ lúc nào.

Chúng ta có thể làm là bọc nó vào một proxy có thể thu hồi, không có trap nào. Proxy như vậy sẽ chuyển tiếp các thao tác đến đối tượng, và chúng ta có thể vô hiệu hóa nó bất cứ lúc nào.

Cú pháp là:

```
let {proxy, revoke} = Proxy.revocable(target, handler)
```

Lời gọi trả về một đối tượng với hàm `proxy` và `revoke` để vô hiệu hóa nó.

Đây là một ví dụ:

```
let object = {
  data: "Valuable data"
};

let {proxy, revoke} = Proxy.revocable(object, {});

// pass the proxy somewhere instead of object...
alert(proxy.data); // Valuable data

// later in our code
revoke();

// the proxy isn't working any more (revoked)
alert(proxy.data); // Error
```

Một cuộc gọi đến `revoke()` xóa tất cả các tham chiếu nội bộ đến đối tượng target từ proxy, vì vậy chúng không còn kết nối với nhau nữa.

Ban đầu, `revoke` tách biệt với `proxy`, vì vậy chúng ta có thể chuyển `proxy` đi trong khi để `revoke` trong scope hiện tại.

Chúng ta cũng có thể bind phương thức `revoke` đến proxy bằng cách đặt `proxy.revoke = revoke`.

Một tùy chọn khác là tạo một `WeakMap` có `proxy` làm key và `revoke` tương ứng làm value, cho phép tìm `revoke` dễ dàng cho một proxy:

```
let revokes = new WeakMap();

let object = {
  data: "Valuable data"
};

let {proxy, revoke} = Proxy.revocable(object, {});

revokes.set(proxy, revoke);

// ..somewhere else in our code..
revoke = revokes.get(proxy);
revoke();

alert(proxy.data); // Error (revoked)
```

Chúng ta sử dụng `WeakMap` thay vì `Map` ở đây vì nó không chặn garbage collection. Nếu một đối tượng proxy trở nên "không thể truy cập" (ví dụ: không có biến nào tham chiếu đến nó nữa), `WeakMap` cho phép nó bị xóa khỏi bộ nhớ cùng với `revoke` mà chúng ta không cần nữa.

## [Tham khảo](#references)

- Specification: [Proxy](https://tc39.es/ecma262/#sec-proxy-object-internal-methods-and-internal-slots).
- MDN: [Proxy](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Proxy).

## [Tóm tắt](#summary)

`Proxy` là một wrapper xung quanh một đối tượng, chuyển tiếp các thao tác trên nó đến đối tượng, tùy chọn chặn một số trong số chúng.

Nó có thể bọc bất kỳ loại đối tượng nào, bao gồm cả classes và functions.

Cú pháp là:

```
let proxy = new Proxy(target, {
  /* traps */
});
```

…Sau đó chúng ta nên sử dụng `proxy` ở mọi nơi thay vì `target`. Một proxy không có thuộc tính hoặc phương thức riêng. Nó chặn một thao tác nếu trap được cung cấp, nếu không thì chuyển tiếp nó đến đối tượng `target`.

Chúng ta có thể chặn:

- Đọc (`get`), ghi (`set`), xóa (`deleteProperty`) một thuộc tính (ngay cả khi không tồn tại).
- Gọi một hàm (`apply` trap).
- Toán tử `new` (`construct` trap).
- Nhiều thao tác khác (danh sách đầy đủ có ở đầu bài viết và trong [tài liệu](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Proxy)).

Điều đó cho phép chúng ta tạo các thuộc tính và phương thức "virtual", triển khai giá trị mặc định, các đối tượng observable, function decorators và nhiều hơn nữa.

Chúng ta cũng có thể bọc một đối tượng nhiều lần trong các proxy khác nhau, trang trí nó với các khía cạnh khác nhau của functionality.

API [Reflect](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Reflect) được thiết kế để bổ sung [Proxy](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Proxy). Đối với mọi trap `Proxy`, có một lời gọi `Reflect` với cùng các đối số. Chúng ta nên sử dụng những thứ đó để chuyển tiếp các cuộc gọi đến các đối tượng target.

Proxies có một số giới hạn:

- Các đối tượng tích hợp sẵn có "internal slots", quyền truy cập vào những slots đó không thể được proxy. Xem workaround ở trên.
- Tương tự cũng đúng cho các trường class riêng, vì chúng được implement nội bộ bằng slots. Vì vậy các cuộc gọi phương thức proxy phải có đối tượng target làm `this` để truy cập chúng.
- Phép kiểm tra equality của đối tượng `===` không thể bị chặn.
- Hiệu suất: benchmarks phụ thuộc vào engine, nhưng nhìn chung truy cập một thuộc tính bằng proxy đơn giản nhất mất nhiều thời gian hơn vài lần. Trong thực tế điều đó chỉ quan trọng đối với một số đối tượng "bottleneck".

---

---

## Bài tập

## [Các bài tập](#tasks)

### [Lỗi khi đọc thuộc tính không tồn tại](#error-on-reading-non-existent-property)

Thông thường, một nỗ lực đọc thuộc tính không tồn tại trả về `undefined`.

Tạo một proxy ném lỗi cho một nỗ lực đọc thuộc tính không tồn tại thay thế.

Điều đó có thể giúp phát hiện lỗi lập trình sớm.

Viết một hàm `wrap(target)` nhận một đối tượng `target` và trả về một proxy thêm functionality aspect đó.

Nó nên hoạt động như sau:

```
let user = {
  name: "John"
};

function wrap(target) {
  return new Proxy(target, {
      /* your code */
  });
}

user = wrap(user);

alert(user.name); // John
alert(user.age); // ReferenceError: Property doesn't exist: "age"
```

lời giải

```
let user = {
  name: "John"
};

function wrap(target) {
  return new Proxy(target, {
    get(target, prop, receiver) {
      if (prop in target) {
        return Reflect.get(target, prop, receiver);
      } else {
        throw new ReferenceError(`Property doesn't exist: "${prop}"`)
      }
    }
  });
}

user = wrap(user);

alert(user.name); // John
alert(user.age); // ReferenceError: Property doesn't exist: "age"
```

### [Truy cập array[-1]](#accessing-array-1)

Trong một số ngôn ngữ lập trình, chúng ta có thể truy cập các phần tử mảng bằng cách sử dụng các chỉ số âm, đếm từ cuối.

Như thế này:

```
let array = [1, 2, 3];

array[-1]; // 3, phần tử cuối cùng
array[-2]; // 2, một bước từ cuối
array[-3]; // 1, hai bước từ cuối
```

Nói cách khác, `array[-N]` giống như `array[array.length - N]`.

Tạo một proxy để triển khai hành vi đó.

Nó nên hoạt động như sau:

```
let array = [1, 2, 3];

array = new Proxy(array, {
  /* your code */
});

alert( array[-1] ); // 3
alert( array[-2] ); // 2

// Other array functionality should be kept "as is"
```

lời giải

```
let array = [1, 2, 3];

array = new Proxy(array, {
  get(target, prop, receiver) {
    if (prop < 0) {
      // even if we access it like arr[1]
      // prop is a string, so need to convert it to number
      prop = +prop + target.length;
    }
    return Reflect.get(target, prop, receiver);
  }
});

alert(array[-1]); // 3
alert(array[-2]); // 2
```

### [Observable](#observable)

Tạo một hàm `makeObservable(target)` mà "làm cho đối tượng observable" bằng cách trả về một proxy.

Đây là cách nó nên hoạt động:

```
function makeObservable(target) {
  /* your code */
}

let user = {};
user = makeObservable(user);

user.observe((key, value) => {
  alert(`SET ${key}=${value}`);
});

user.name = "John"; // alerts: SET name=John
```

Nói cách khác, một đối tượng được trả về bởi `makeObservable` giống như đối tượng gốc, nhưng cũng có phương thức `observe(handler)` thiết lập hàm `handler` để được gọi khi bất kỳ thuộc tính nào thay đổi.

Bất cứ khi nào một thuộc tính thay đổi, `handler(key, value)` được gọi với tên và giá trị của thuộc tính.

P.S. Trong bài tập này, xin chỉ chăm sóc việc ghi vào thuộc tính. Các thao tác khác có thể được triển khai theo cách tương tự.

lời giải

Lời giải gồm hai phần:

1. Bất cứ khi nào `.observe(handler)` được gọi, chúng ta cần nhớ handler ở đâu đó, để có thể gọi nó sau. Chúng ta có thể lưu trữ handlers ngay trong đối tượng, bằng cách sử dụng symbol của chúng ta làm property key.
2. Chúng ta cần một proxy với trap `set` để gọi handlers trong trường hợp có bất kỳ thay đổi nào.

```
let handlers = Symbol('handlers');

function makeObservable(target) {
  // 1. Initialize handlers store
  target[handlers] = [];

  // Store the handler function in array for future calls
  target.observe = function(handler) {
    this[handlers].push(handler);
  };

  // 2. Create a proxy to handle changes
  return new Proxy(target, {
    set(target, property, value, receiver) {
      let success = Reflect.set(...arguments); // forward the operation to object
      if (success) { // if there were no error while setting the property
        // call all handlers
        target[handlers].forEach(handler => handler(property, value));
      }
      return success;
    }
  });
}

let user = {};

user = makeObservable(user);

user.observe((key, value) => {
  alert(`SET ${key}=${value}`);
});

user.name = "John";
```
