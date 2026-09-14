# Kiểu Symbol

> Nguồn: [https://javascript.info/symbol](https://javascript.info/symbol)

<!-- fetched: 2026-09-14 -->

Theo specification, chỉ có hai primitive types có thể serve như là object property keys:

- string type, hoặc
- symbol type.

Nếu không, nếu một người sử dụng một type khác, như số, nó được autoconvert thành string. Vì vậy `obj[1]` giống hệt `obj["1"]`, và `obj[true]` giống hệt `obj["true"]`.

Cho đến giờ chúng ta đã chỉ sử dụng strings.

Giờ hãy explore symbols, xem chúng có thể làm gì cho chúng ta.

## [Symbols](#symbols)

Một "symbol" đại diện cho một unique identifier.

Một giá trị của type này có thể được tạo bằng cách sử dụng `Symbol()`:

```
let id = Symbol();
```

Upon creation, chúng ta có thể gán symbols một description (cũng được gọi là một symbol name), mostly useful cho debugging purposes:

```
// id là một symbol với description "id"
let id = Symbol("id");
```

Symbols được guaranteed để là unique. Ngay cả khi chúng ta tạo nhiều symbols với exactly cùng description, chúng là các different values. Description chỉ là một label không affect anything.

Ví dụ, ở đây là hai symbols với cùng description – chúng không equal:

```
let id1 = Symbol("id");
let id2 = Symbol("id");

alert(id1 == id2); // false
```

Nếu bạn familiar với Ruby hoặc một language khác cũng có một loại "symbols" – xin đừng bị misguided. JavaScript symbols là khác.

Vì vậy, để summarize, một symbol là một "primitive unique value" với một optional description. Hãy xem chúng ta có thể sử dụng chúng ở đâu.

Symbols không auto-convert sang string

Hầu hết các giá trị trong JavaScript hỗ trợ implicit conversion sang string. Ví dụ, chúng ta có thể `alert` hầu hết bất kỳ giá trị nào, và nó sẽ hoạt động. Symbols là special. Chúng không auto-convert.

Ví dụ, `alert` này sẽ show một error:

```
let id = Symbol("id");
alert(id); // TypeError: Cannot convert a Symbol value to a string
```

Đó là một "language guard" against messing up, vì strings và symbols là fundamentally different và không nên accidentally convert one into another.

Nếu chúng ta thực sự muốn show một symbol, chúng ta cần explicitly gọi `.toString()` trên nó, như ở đây:

```
let id = Symbol("id");
alert(id.toString()); // Symbol(id), giờ nó hoạt động
```

Hoặc get `symbol.description` property để show description only:

```
let id = Symbol("id");
alert(id.description); // id
```

## ["Hidden" properties](#hidden-properties)

Symbols cho phép chúng ta tạo "hidden" properties của một object, mà không có other part của code có thể accidentally access hoặc overwrite.

Ví dụ, nếu chúng ta đang làm việc với các objects `user`, thuộc về một third-party code. Chúng ta muốn thêm identifiers vào chúng.

Hãy sử dụng một symbol key cho nó:

```
let user = { // belongs to another code
  name: "John"
};

let id = Symbol("id");

user[id] = 1;

alert( user[id] ); // chúng ta có thể access data bằng cách sử dụng symbol như là key
```

Benefit của việc sử dụng `Symbol("id")` thay vì string `"id"` là gì?

Vì `user` objects thuộc về một codebase khác, nó không safe để thêm các fields vào chúng, vì chúng ta có thể ảnh hưởng đến pre-defined behavior trong codebase khác đó. Tuy nhiên, symbols không thể được accessed accidentally. Third-party code sẽ không aware của newly defined symbols, vì vậy nó là safe để thêm symbols vào các `user` objects.

Cũng, hãy tưởng tượng rằng một script khác muốn có một identifier của riêng nó bên trong `user`, cho purposes của nó.

Sau đó script đó có thể tạo một `Symbol("id")` của riêng nó, như thế này:

```
// ...
let id = Symbol("id");

user[id] = "Their id value";
```

Sẽ không có conflict giữa identifiers của chúng ta và của họ, vì symbols luôn luôn different, ngay cả khi chúng có cùng name.

…Nhưng nếu chúng ta sử dụng một string `"id"` thay vì một symbol cho cùng purpose, thì *sẽ* có conflict:

```
let user = { name: "John" };

// Script của chúng ta sử dụng property "id"
user.id = "Our id value";

// ...Script khác cũng muốn "id" cho purposes của nó...

user.id = "Their id value"
// Boom! overwritten bởi script khác!
```

### [Symbols trong một object literal](#symbols-in-an-object-literal)

Nếu chúng ta muốn sử dụng một symbol trong một object literal `{...}`, chúng ta cần square brackets xung quanh nó.

Như thế này:

```
let id = Symbol("id");

let user = {
  name: "John",
  [id]: 123 // không phải "id": 123
};
```

Điều đó là vì chúng ta cần giá trị từ variable `id` như là key, không phải string "id".

### [Symbols được bỏ qua bởi for…in](#symbols-are-skipped-by-for-in)

Symbolic properties không participate trong `for..in` loop.

Ví dụ:

```
let id = Symbol("id");
let user = {
  name: "John",
  age: 30,
  [id]: 123
};

for (let key in user) alert(key); // name, age (không có symbols)

// direct access bởi symbol hoạt động
alert( "Direct: " + user[id] ); // Direct: 123
```

[Object.keys(user)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/keys) cũng ignores them. Đó là một phần của general "hiding symbolic properties" principle. Nếu một script khác hoặc một library loop qua object của chúng ta, nó sẽ không unexpectedly access một symbolic property.

Ngược lại, [Object.assign](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/assign) copies cả string và symbol properties:

```
let id = Symbol("id");
let user = {
  [id]: 123
};

let clone = Object.assign({}, user);

alert( clone[id] ); // 123
```

Không có paradox ở đây. Đó là by design. Idea là khi chúng ta clone một object hoặc merge objects, chúng ta thường muốn *tất cả* properties được copy (bao gồm cả symbols như `id`).

## [Global symbols](#global-symbols)

Như chúng ta đã thấy, thông thường tất cả các symbols là different, ngay cả khi chúng có cùng name. Nhưng đôi khi chúng ta muốn same-named symbols là same entities. Ví dụ, các parts khác nhau của application của chúng ta muốn access symbol `"id"` có nghĩa là exactly cùng property.

Để đạt được điều đó, có một *global symbol registry*. Chúng ta có thể tạo symbols trong nó và access chúng sau, và nó guarantees rằng repeated accesses bởi cùng name return exactly cùng symbol.

Để read (create nếu absent) một symbol từ registry, sử dụng `Symbol.for(key)`.

Call đó checks global registry, và nếu có một symbol được described như `key`, sau đó return nó, ngược lại tạo một new symbol `Symbol(key)` và store nó trong registry bởi `key` được cho.

Ví dụ:

```
// read từ global registry
let id = Symbol.for("id"); // nếu symbol không tồn tại, nó được tạo

// read lại (maybe từ một part khác của code)
let idAgain = Symbol.for("id");

// cùng symbol
alert( id === idAgain ); // true
```

Symbols bên trong registry được gọi là *global symbols*. Nếu chúng ta muốn một application-wide symbol, accessible ở mọi nơi trong code – đó là những gì chúng dành cho.

Điều đó sounding như Ruby

Trong một số programming languages, như Ruby, có một single symbol per name.

Trong JavaScript, như chúng ta có thể thấy, điều đó đúng cho global symbols.

### [Symbol.keyFor](#symbol-keyfor)

Chúng ta đã thấy rằng đối với global symbols, `Symbol.for(key)` return một symbol bởi name. Để làm ngược lại – return một name bởi global symbol – chúng ta có thể sử dụng: `Symbol.keyFor(sym)`:

Ví dụ:

```
// get symbol bởi name
let sym = Symbol.for("name");
let sym2 = Symbol.for("id");

// get name bởi symbol
alert( Symbol.keyFor(sym) ); // name
alert( Symbol.keyFor(sym2) ); // id
```

`Symbol.keyFor` internally sử dụng global symbol registry để lookup key cho symbol. Vì vậy nó không hoạt động cho non-global symbols. Nếu symbol không phải global, nó sẽ không thể find nó và return `undefined`.

Tuy nhiên, tất cả các symbols có `description` property.

Ví dụ:

```
let globalSymbol = Symbol.for("name");
let localSymbol = Symbol("name");

alert( Symbol.keyFor(globalSymbol) ); // name, global symbol
alert( Symbol.keyFor(localSymbol) ); // undefined, not global

alert( localSymbol.description ); // name
```

## [System symbols](#system-symbols)

Có nhiều "system" symbols mà JavaScript sử dụng nội bộ, và chúng ta có thể sử dụng chúng để fine-tune various aspects của objects của chúng ta.

Chúng được listed trong specification trong [Well-known symbols](https://tc39.github.io/ecma262/#sec-well-known-symbols) table:

- `Symbol.hasInstance`
- `Symbol.isConcatSpreadable`
- `Symbol.iterator`
- `Symbol.toPrimitive`
- …và vân vân.

Ví dụ, `Symbol.toPrimitive` cho phép chúng ta mô tả object to primitive conversion. Chúng ta sẽ see cách sử dụng very soon.

Các symbols khác cũng sẽ become familiar khi chúng ta study các language features tương ứng.

## [Tổng kết](#summary)

`Symbol` là một primitive type cho unique identifiers.

Symbols được tạo với `Symbol()` call với một optional description (name).

Symbols luôn luôn là các different values, ngay cả khi chúng có cùng name. Nếu chúng ta muốn same-named symbols là equal, sau đó chúng ta nên sử dụng global registry: `Symbol.for(key)` return (create nếu cần) một global symbol với `key` như là name. Multiple calls của `Symbol.for` với cùng `key` return exactly cùng symbol.

Symbols có hai main use cases:

1. "Hidden" object properties.

   Nếu chúng ta muốn thêm một property vào một object mà "thuộc về" một script khác hoặc một library, chúng ta có thể tạo một symbol và sử dụng nó như là property key. Một symbolic property không xuất hiện trong `for..in`, vì vậy nó sẽ không được accidentally processed cùng với các properties khác. Cũng nó sẽ không được accessed trực tiếp, vì một script khác không có symbol của chúng ta. Vì vậy property sẽ được protect khỏi accidental use hoặc overwrite.

   Vì vậy chúng ta có thể "covertly" hide cái gì đó vào objects mà chúng ta cần, nhưng những người khác không nên nhìn thấy, bằng cách sử dụng symbolic properties.
2. Có nhiều system symbols được sử dụng bởi JavaScript mà accessible như `Symbol.*`. Chúng ta có thể sử dụng chúng để alter một số built-in behaviors. Ví dụ, sau đó trong tutorial chúng ta sẽ sử dụng `Symbol.iterator` cho [iterables](/iterable), `Symbol.toPrimitive` để setup [object-to-primitive conversion](/object-toprimitive) và vân vân.

Về mặt kỹ thuật, symbols không phải là 100% hidden. Có một built-in method [Object.getOwnPropertySymbols(obj)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/getOwnPropertySymbols) cho phép chúng ta get tất cả các symbols. Cũng có một method tên là [Reflect.ownKeys(obj)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Reflect/ownKeys) return *tất cả* keys của một object bao gồm symbolic ones. Nhưng hầu hết các libraries, built-in functions và syntax constructs không sử dụng những methods này.
