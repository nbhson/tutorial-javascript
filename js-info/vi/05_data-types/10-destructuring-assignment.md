# Destructuring assignment

> Nguồn: [https://javascript.info/destructuring-assignment](https://javascript.info/destructuring-assignment)

<!-- fetched: 2026-09-14 -->

Hai data structures được used nhiều nhất trong JavaScript là `Object` và `Array`.

- Objects cho phép chúng ta create một single entity mà store data items bởi key.
- Arrays cho phép chúng ta gather data items vào một ordered list.

Tuy nhiên, khi chúng ta pass这些 vào một function, chúng ta có thể không need tất cả của nó. Function có thể chỉ require certain elements hoặc properties.

*Destructuring assignment* là một special syntax mà allows chúng ta để "unpack" arrays hoặc objects vào một bunch của variables, vì đôi khi điều đó là more convenient.

Destructuring cũng work well với complex functions mà có nhiều parameters, default values, và vân vân. Sớm chúng ta sẽ see điều đó.

## [Array destructuring](#array-destructuring)

Đây là một ví例 của cách một array được destructured vào variables:

```
// chúng ta có một array với name và surname
let arr = ["John", "Smith"]

// destructuring assignment
// sets firstName = arr[0]
// và surname = arr[1]
let [firstName, surname] = arr;

alert(firstName); // John
alert(surname);  // Smith
```

Giờ chúng ta có thể làm việc với variables thay vì array members.

Nó看起来 great khi combined với `split` hoặc các array-returning methods khác:

```
let [firstName, surname] = "John Smith".split(' ');
alert(firstName); // John
alert(surname);  // Smith
```

Như bạn có thể see, syntax là simple. Có một few peculiar details though. Hãy xem thêm examples để understand nó better.

"Destructuring" không có nghĩa "destructive".

Nó được gọi là "destructuring assignment," vì nó "destructurizes" bằng cách copying items vào variables. Tuy nhiên, array本身 không được modified.

Nó chỉ là một shorter way để viết:

```
// let [firstName, surname] = arr;
let firstName = arr[0];
let surname = arr[1];
```

Ignore elements sử dụng commas

Unwanted elements của array cũng có thể được thrown away qua một extra comma:

```
// second element không needed
let [firstName, , title] = ["Julius", "Caesar", "Consul", "of the Roman Republic"];

alert( title ); // Consul
```

Trong code ở trên, second element của array được skipped, third một được assigned đến `title`, và rest của array items cũng bị skipped (vì không có variables cho chúng).

WorksWith bất kỳ iterable trên right-side

…Thực tế, chúng ta có thể sử dụng nó với bất kỳ iterable nào, không chỉ arrays:

```
let [a, b, c] = "abc"; // ["a", "b", "c"]
let [one, two, three] = new Set([1, 2, 3]);
```

Điều đó work, vì nội bộ một destructuring assignment làm việc bằng cách iterating qua right value. Đó là một kind của syntax sugar cho calling `for..of` qua value bên phải của `=` và assigning values.

Assign to bất kỳ cái gì trên left-side

Chúng ta có thể sử dụng bất kỳ "assignables" nào trên left side.

Ví例, một property của object:

```
let user = {};
[user.name, user.surname] = "John Smith".split(' ');

alert(user.name); // John
alert(user.surname); // Smith
```

Looping với .entries()

Trong previous chapter, chúng ta đã thấy [Object.entries(obj)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/entries) method.

Chúng ta có thể sử dụng nó với destructuring để loop qua keys-and-values của một object:

```
let user = {
  name: "John",
  age: 30
};

// loop qua keys-and-values
for (let [key, value] of Object.entries(user)) {
  alert(`${key}:${value}`); // name:John, sau đó age:30
}
```

Similar code cho một `Map` là simpler hơn, vì nó iterable:

```
let user = new Map();
user.set("name", "John");
user.set("age", "30");

// Map iterates như [key, value] pairs, very convenient cho destructuring
for (let [key, value] of user) {
  alert(`${key}:${value}`); // name:John, sau đó age:30
}
```

Swap variables trick

Có một well-known trick cho swapping values của hai variables sử dụng một destructuring assignment:

```
let guest = "Jane";
let admin = "Pete";

// Hãy swap values: make guest=Pete, admin=Jane
[guest, admin] = [admin, guest];

alert(`${guest} ${admin}`); // Pete Jane (successfully swapped!)
```

Ở đây chúng ta create một temporary array của hai variables và ngay lập tức destructure nó trong swapped order.

Chúng ta có thể swap nhiều hơn hai variables theo cách này.

### [The rest '…'](#the-rest)

Thông thường, nếu array dài hơn list ở left, "extra" items bị omitted.

Ví例, ở đây chỉ hai items được take, và rest bị ignore:

```
let [name1, name2] = ["Julius", "Caesar", "Consul", "of the Roman Republic"];

alert(name1); // Julius
alert(name2); // Caesar
// Further items không được assigned ở đâu
```

Nếu chúng ta muốn cũng để gather tất cả that follows – chúng ta có thể add một another parameter mà gets "the rest" sử dụng ba dots `"..."`:

```
let [name1, name2, ...rest] = ["Julius", "Caesar", "Consul", "of the Roman Republic"];

// rest là một array của items, bắt đầu từ 3rd một
alert(rest[0]); // Consul
alert(rest[1]); // of the Roman Republic
alert(rest.length); // 2
```

Value của `rest` là array của remaining array elements.

Chúng ta có thể sử dụng bất kỳ other variable name thay vì `rest`, just make sure nó có ba dots trước nó và goes last trong destructuring assignment.

```
let [name1, name2, ...titles] = ["Julius", "Caesar", "Consul", "of the Roman Republic"];
// giờ titles = ["Consul", "of the Roman Republic"]
```

### [Default values](#default-values)

Nếu array ngắn hơn list của variables ở left, sẽ không có errors. Absent values được considered undefined:

```
let [firstName, surname] = [];

alert(firstName); // undefined
alert(surname); // undefined
```

Nếu chúng ta muốn một "default" value để replace missing một, chúng ta có thể cung cấp nó sử dụng `=`:

```
// default values
let [name = "Guest", surname = "Anonymous"] = ["Julius"];

alert(name);    // Julius (từ array)
alert(surname); // Anonymous (default được used)
```

Default values có thể là phức tạp hơn expressions hoặc thậm chí function calls. Chúng được evaluated chỉ nếu value không được provided.

Ví例, ở đây chúng ta sử dụng `prompt` function cho hai defaults:

```
// runs only prompt cho surname
let [name = prompt('name?'), surname = prompt('surname?')] = ["Julius"];

alert(name);    // Julius (từ array)
alert(surname); // whatever prompt gets
```

Xin lưu ý: `prompt` sẽ run chỉ cho missing value (`surname`).

## [Object destructuring](#object-destructuring)

Destructuring assignment cũng work với objects.

Basic syntax là:

```
let {var1, var2} = {var1:…, var2:…}
```

Chúng ta nên có một existing object ở right side, mà chúng ta muốn split vào variables. Left side chứa một object-like "pattern" cho corresponding properties. Trong simplest case, đó là một list của variable names trong `{...}`.

Ví例:

```
let options = {
  title: "Menu",
  width: 100,
  height: 200
};

let [title, width, height] = options;

alert(title);  // Menu
alert(width);  // 100
alert(height); // 200
```

Properties `options.title`, `options.width` và `options.height` được assigned đến corresponding variables.

Order không matter. Điều này work cũng:

```
// thay đổi order trong let {...}
let [height, width, title] = { title: "Menu", height: 200, width: 100 }
```

Pattern ở left side có thể là more complex và specify mapping giữa properties và variables.

Nếu chúng ta muốn assign một property đến một variable với另一个 name, ví例, make `options.width` go vào variable tên là `w`, sau đó chúng ta có thể set variable name sử dụng một colon:

```
let options = {
  title: "Menu",
  width: 100,
  height: 200
};

// { sourceProperty: targetVariable }
let [width: w, height: h, title] = options;

// width -> w
// height -> h
// title -> title

alert(title);  // Menu
alert(w);      // 100
alert(h);      // 200
```

Colon shows "what : goes where". Trong ví例 này property `width` goes đến `w`, property `height` goes đến `h`, và `title` được assigned đến same name.

Cho potentially missing properties chúng ta có thể set default values sử dụng `"="`, như thế này:

```
let options = {
  title: "Menu"
};

let [width = 100, height = 200, title] = options;

alert(title);  // Menu
alert(width);  // 100
alert(height); // 200
```

Giống như với arrays hoặc function parameters, default values có thể là bất kỳ expressions hoặc thậm chí function calls. Chúng sẽ được evaluated nếu value không được provided.

Trong code dưới đây `prompt` hỏi cho `width`, nhưng không cho `title`:

```
let options = {
  title: "Menu"
};

let [width = prompt("width?"), title = prompt("title?")] = options;

alert(title);  // Menu
alert(width);  // (whatever result của prompt là)
```

Chúng ta cũng có thể kết hợp cả colon và equality:

```
let options = {
  title: "Menu"
};

let [width: w = 100, height: h = 200, title] = options;

alert(title);  // Menu
alert(w);      // 100
alert(h);      // 200
```

Nếu chúng ta có một complex object với nhiều properties, chúng ta có thể extract chỉ những gì chúng ta cần:

```
let options = {
  title: "Menu",
  width: 100,
  height: 200
};

// chỉ extract title như một variable
let [title] = options;

alert(title); // Menu
```

### [The rest pattern """]( #the-rest-pattern)

What nếu object có nhiều properties hơn chúng ta có variables? Có thể take some và sau đó assign "rest" ở đâu?

Chúng ta có thể sử dụng rest pattern, giống như chúng ta đã làm với arrays. Nó không được supported bởi một số older browsers (IE, use Babel để polyfill nó), nhưng work trong modern ones.

Nó看起来 như thế này:

```
let options = {
  title: "Menu",
  height: 200,
  width: 100
};

// title = property tên là title
// rest = object với rest của properties
let [title, ...rest] = options;

// giờ title="Menu", rest={height: 200, width: 100}
alert(rest.height);  // 200
alert(rest.width);   // 100
```

Gotcha nếu không có `let`

Trong các ví例 ở trên variables được declared right trong assignment: `let {...} = {...}`. Tất nhiên, chúng ta có thể sử dụng existing variables too, mà không có `let`. Nhưng có một catch.

Điều này sẽ không work:

```
let title, width, height;

// error trong dòng này
{title, width, height} = {title: "Menu", width: 200, height: 100};
```

Problem là JavaScript treats `{...}` trong main code flow (không phải bên trong một expression khác) như một code block. Such blocks có thể được used để group statements, như thế này:

```
{
  // một code block
  let message = "Hello";
  // ...
  alert( message );
}
```

Vì vậy ở đây JavaScript giả định rằng chúng ta có một code block, đó là lý do tại sao có một error. Chúng ta want destructuring thay vì.

Để show JavaScript rằng nó không phải là một code block, chúng ta có thể wrap expression trong parentheses `(...)`:

```
let title, width, height;

// okay giờ
({title, width, height} = {title: "Menu", width: 200, height: 100});

alert( title ); // Menu
```

## [Nested destructuring](#nested-destructuring)

Nếu một object hoặc một array chứa các nested objects và arrays khác, chúng ta có thể sử dụng more complex left-side patterns để extract deeper portions.

Trong code dưới đây `options` có một another object trong property `size` và một array trong property `items`. Pattern ở left side của assignment có same structure để extract values từ chúng:

```
let options = {
  size: {
    width: 100,
    height: 200
  },
  items: ["Cake", "Donut"],
  extra: true
};

// destructuring assignment split trong multiple lines cho clarity
let {
  size: { // put size ở đây
    width,
    height
  },
  items: [item1, item2], // assign items ở đây
  title = "Menu" // không present trong object (default value được used)
} = options;

alert(title);  // Menu
alert(width);  // 100
alert(height); // 200
alert(item1);  // Cake
alert(item2);  // Donut
```

Tất cả properties của `options` object ngoại trừ `extra` mà absent trong left part, được assigned đến corresponding variables:

![](/article/destructuring-assignment/destructuring-complex.svg)

Cuối cùng, chúng ta có `width`, `height`, `item1`, `item2` và `title` từ default value.

Note rằng không có variables cho `size` và `items`, vì chúng ta take content của họ thay vì.

## [Smart function parameters](#smart-function-parameters)

Có những times khi một function có nhiều parameters, most của chúng là optional. Điều đó đặc biệt true cho user interfaces. Imagine một function mà tạo một menu. Nó có thể có một width, một height, một title, một item list và vân vân.

Đây là một bad way để viết这样的 function:

```
function showMenu(title = "Untitled", width = 200, height = 100, items = []) {
  // ...
}
```

Trong thực life, problem là làm thế nào để remember order của arguments. Thông thường, IDEs try để help chúng ta, đặc biệt nếu code là well-documented, nhưng still… Một另一个 problem là làm thế nào để call một function khi most parameters là ok bởi default.

Như thế này?

```
// undefined nơi default values là fine
showMenu("My Menu", undefined, undefined, ["Item1", "Item2"])
```

Đó là ugly. Và trở nên unreadable khi chúng ta deal với nhiều parameters.

Destructuring comes to rescue!

Chúng ta có thể pass parameters như một object, và function ngay lập tức destructurizes chúng vào variables:

```
// chúng ta pass object đến function
let options = {
  title: "My menu",
  items: ["Item1", "Item2"]
};

// ...và nó ngay lập tức expand nó vào variables
function showMenu({title = "Untitled", width = 200, height = 100, items = []}) {
  // title, items – taken từ options,
  // width, height – defaults được used
  alert( `${title} ${width} ${height}` ); // My Menu 200 100
  alert( items ); // Item1, Item2
}

showMenu(options);
```

Chúng ta cũng có thể sử dụng more complex destructuring với nested objects và colon mappings:

```
let options = {
  title: "My menu",
  items: ["Item1", "Item2"]
};

function showMenu({
  title = "Untitled",
  width: w = 100,  // width goes đến w
  height: h = 200, // height goes đến h
  items: [item1, item2] // items first element goes đến item1, second đến item2
}) {
  alert( `${title} ${w} ${h}` ); // My Menu 100 200
  alert( item1 ); // Item1
  alert( item2 ); // Item2
}

showMenu(options);
```

Full syntax là same như cho một destructuring assignment:

```
function({
  incomingProperty: varName = defaultValue
  ...
})
```

Sau đó, cho một object của parameters, sẽ có một variable `varName` cho property `incomingProperty`, với `defaultValue` bởi default.

Xin lưu ý rằng such destructuring assumes rằng `showMenu()` có một argument. Nếu chúng ta muốn tất cả values bởi default, sau đó chúng ta nên specify một empty object:

```
showMenu({}); // ok, tất cả values là default

showMenu(); // điều đó sẽ give một error
```

Chúng ta có thể fix điều này bằng cách making `{}` default value cho whole object của parameters:

```
function showMenu({ title = "Menu", width = 100, height = 200 } = {}) {
  alert( `${title} ${width} ${height}` );
}

showMenu(); // Menu 100 200
```

Trong code ở trên, whole arguments object là `{}` bởi default, vì vậy luôn luôn có gì đó để destructurize.

## [Tổng kết](#summary)

- Destructuring assignment allows cho instantly mapping một object hoặc array onto many variables.
- Full object syntax:

  ```
  let {prop : varName = defaultValue, ...rest} = object
  ```

  Điều đó mean property `prop` nên go vào variable `varName` và, nếu không có property như vậy tồn tại, sau đó `default` value nên được used.

  Object properties mà không có mapping được copied đến `rest` object.
- Full array syntax:

  ```
  let [item1 = defaultValue, item2, ...rest] = array
  ```

  First item goes đến `item1`; second vào `item2`, và rest làm array `rest`.
- Có thể extract data từ nested arrays/objects, cho điều đó left side phải có same structure như right one.

---

---

## Các bài tập

## [Các bài tập](#tasks)

### [Destructuring assignment](#destructuring-assignment)

mức độ quan trọng: 5

Chúng ta có một object:

```
let user = {
  name: "John",
  years: 30
};
```

Viết destructuring assignment mà reads:

- `name` property vào variable `name`.
- `years` property vào variable `age`.
- `isAdmin` property vào variable `isAdmin` (false, nếu không có property như vậy)

Đây là một ví例 về values sau assignment của bạn:

```
let user = { name: "John", years: 30 };

// your code đến left side:
// ... = user

alert( name ); // John
alert( age ); // 30
alert( isAdmin ); // false
```

lời giải

```
let user = {
  name: "John",
  years: 30
};

let [name, years: age, isAdmin = false] = user;

alert( name ); // John
alert( age ); // 30
alert( isAdmin ); // false
```

### [Maximal salary](#the-maximal-salary)

mức độ quan trọng: 5

Có một `salaries` object:

```
let salaries = {
  "John": 100,
  "Pete": 300,
  "Mary": 250
};
```

Tạo function `topSalary(salaries)` mà trả về name của top-paid person.

- Nếu `salaries` là empty, nó nên trả về `null`.
- Nếu có nhiều top-paid persons, trả về bất kỳ trong số chúng.

P.S. Sử dụng `Object.entries` và destructuring để iterate qua key/value pairs.

[Mở một sandbox với tests.](https://plnkr.co/edit/mgJkWzDdbHZGdGhZ?p=preview)

lời giải

```
function topSalary(salaries) {

  let maxSalary = 0;
  let maxName = null;

  for(const [name, salary] of Object.entries(salaries)) {
    if (maxSalary < salary) {
      maxSalary = salary;
      maxName = name;
    }
  }

  return maxName;
}
```

[Mở solution với tests trong một sandbox.](https://plnkr.co/edit/wsYDW5HhZ4MzjtOb?p=preview)
