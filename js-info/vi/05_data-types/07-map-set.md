# Map và Set

> Nguồn: [https://javascript.info/map-set](https://javascript.info/map-set)

<!-- fetched: 2026-09-14 -->

Cho đến giờ, chúng ta đã learn về following complex data structures:

- Objects được used để store keyed collections.
- Arrays được used để store ordered collections.

Nhưng điều đó không đủ cho thực life. Đó là lý do tại sao `Map` và `Set` cũng tồn tại.

## [Map](#map)

[Map](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map) là một collection của keyed data items, giống như một `Object`. Nhưng main difference là `Map` allows keys của bất kỳ type nào.

Methods và properties là:

- [`new Map()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map/Map) – creates map.
- [`map.set(key, value)`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map/set) – stores value bởi key.
- [`map.get(key)`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map/get) – returns value bởi key, `undefined` nếu `key` không exist trong map.
- [`map.has(key)`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map/has) – trả về `true` nếu `key` tồn tại, `false` ngược lại.
- [`map.delete(key)`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map/delete) – removes element (key/value pair) bởi key.
- [`map.clear()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map/clear) – removes everything từ map.
- [`map.size`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map/size) – returns current element count.

Ví例:

```
let map = new Map();

map.set('1', 'str1');   // một string key
map.set(1, 'num1');     // một numeric key
map.set(true, 'bool1'); // một boolean key

// remember regular Object? nó sẽ convert keys đến string
// Map giữ type, vì vậy hai cái này là different:
alert( map.get(1)   ); // 'num1'
alert( map.get('1') ); // 'str1'

alert( map.size ); // 3
```

Như chúng ta có thể see, khác với objects, keys không được converted đến strings. Bất kỳ type của key là possible.

`map[key]` không phải là right way để sử dụng một `Map`

Mặc dù `map[key]` cũng work, ví例 chúng ta có thể set `map[key] = 2`, điều này treat `map` như một plain JavaScript object, vì vậy nó imply tất cả corresponding limitations (chỉ string/symbol keys và vân vân).

Vì vậy chúng ta nên sử dụng `map` methods: `set`, `get` và vân vân.

**Map cũng có thể sử dụng objects như keys.**

Ví例:

```
let john = { name: "John" };

// cho mỗi user, hãy store visits count của họ
let visitsCountMap = new Map();

// john là key cho map
visitsCountMap.set(john, 123);

alert( visitsCountMap.get(john) ); // 123
```

Sử dụng objects như keys là một trong những most notable và important `Map` features. Same không tính cho `Object`. String như một key trong `Object` là fine, nhưng chúng ta không thể sử dụng another `Object` như một key trong `Object`.

Hãy thử:

```
let john = { name: "John" };
let ben = { name: "Ben" };

let visitsCountObj = {}; // try để sử dụng một object

visitsCountObj[ben] = 234; // try để sử dụng ben object như key
visitsCountObj[john] = 123; // try để sử dụng john object như key, ben object sẽ bị replaced

// Đó là những gì got written!
alert( visitsCountObj["[object Object]"] ); // 123
```

Như `visitsCountObj` là object, nó converts tất cả `Object` keys, như `john` và `ben` ở trên, đến cùng string `"[object Object]"`. Definitely không phải những gì chúng ta muốn.

How `Map` compares keys

Để test keys cho equivalence, `Map` sử dụng algorithm [SameValueZero](https://tc39.github.io/ecma262/#sec-samevaluezero). Nó roughly same như strict equality `===`, nhưng difference là `NaN` được considered equal với `NaN`. Vì vậy `NaN` có thể được sử dụng như key cũng.

Algorithm này không thể được changed hoặc customized.

Chaining

Mỗi `map.set` call trả về map本身, vì vậy chúng ta có thể "chain" các calls:

```
map.set('1', 'str1')
  .set(1, 'num1')
  .set(true, 'bool1');
```

## [Iteration qua Map](#iteration-over-map)

Cho looping qua một `map`, có 3 methods:

- [`map.keys()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map/keys) – trả về một iterable cho keys,
- [`map.values()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map/values) – trả về một iterable cho values,
- [`map.entries()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map/entries) – trả về một iterable cho entries `[key, value]`, nó được used bởi default trong `for..of`.

Ví例:

```
let recipeMap = new Map([
  ['cucumber', 500],
  ['tomatoes', 350],
  ['onion',    50]
]);

// iterate qua keys (vegetables)
for (let vegetable of recipeMap.keys()) {
  alert(vegetable); // cucumber, tomatoes, onion
}

// iterate qua values (amounts)
for (let amount of recipeMap.values()) {
  alert(amount); // 500, 350, 50
}

// iterate qua [key, value] entries
for (let entry of recipeMap) { // same như of recipeMap.entries()
  alert(entry); // cucumber,500 (và vân vân)
}
```

Insertion order được used

Iteration goes trong same order như values được inserted. `Map` preserves order đó, khác với một regular `Object`.

Bên cạnh đó, `Map` có một built-in `forEach` method, tương tự như `Array`:

```
// runs function cho mỗi (key, value) pair
recipeMap.forEach( (value, key, map) => {
  alert(`${key}: ${value}`); // cucumber: 500 v.v.
});
```

## [Object.entries: Map từ Object](#object-entries-map-from-object)

Khi một `Map` được created, chúng ta có thể pass một array (hoặc另一个 iterable) với key/value pairs cho initialization, như thế này:

```
// array của [key, value] pairs
let map = new Map([
  ['1',  'str1'],
  [1,    'num1'],
  [true, 'bool1']
]);

alert( map.get('1') ); // str1
```

Nếu chúng ta có một plain object, và chúng ta muốn tạo một `Map` từ nó, sau đó chúng ta có thể sử dụng built-in method [Object.entries(obj)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/entries) mà trả về một array của key/value pairs cho object exactly trong format đó.

Vì vậy chúng ta có thể tạo một map từ một object như thế này:

```
let obj = {
  name: "John",
  age: 30
};

let map = new Map(Object.entries(obj));

alert( map.get('name') ); // John
```

Ở đây, `Object.entries` trả về array của key/value pairs: `[ ["name","John"], ["age", 30] ]`. Đó là những gì `Map` cần.

## [Object.fromEntries: Object từ Map](#object-fromentries-object-from-map)

Chúng ta vừa thấy làm thế nào để tạo `Map` từ một plain object với `Object.entries(obj)`.

Có `Object.fromEntries` method mà làm reverse: cho một array của `[key, value]` pairs, nó creates một object từ chúng:

```
let prices = Object.fromEntries([
  ['banana', 1],
  ['orange', 2],
  ['meat', 4]
]);

// giờ prices = { banana: 1, orange: 2, meat: 4 }

alert(prices.orange); // 2
```

Chúng ta có thể sử dụng `Object.fromEntries` để get một plain object từ `Map`.

Ví例, chúng ta store data trong một `Map`, nhưng chúng ta cần để pass nó đến một 3rd-party code mà expects một plain object.

Đây chúng ta đi:

```
let map = new Map();
map.set('banana', 1);
map.set('orange', 2);
map.set('meat', 4);

let obj = Object.fromEntries(map.entries()); // make một plain object (*)

// done!
// obj = { banana: 1, orange: 2, meat: 4 }

alert(obj.orange); // 2
```

Một call đến `map.entries()` trả về một iterable của key/value pairs, exactly trong right format cho `Object.fromEntries`.

Chúng ta cũng có thể make dòng `(*)` ngắn hơn:

```
let obj = Object.fromEntries(map); // omit .entries()
```

Đó là same, vì `Object.fromEntries` expects một iterable object như argument. Không nhất thiết phải là array. Và standard iteration cho `map` trả về same key/value pairs như `map.entries()`. Vì vậy chúng ta get một plain object với same key/values như `map`.

## [Set](#set)

Một [`Set`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set) là một special type collection – "set của values" (không có keys), nơi mỗi value có thể occur only once.

Main methods của nó là:

- [`new Set([iterable])`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set/Set) – creates set, và nếu một `iterable` object được provided (thường là array), copies values từ nó vào set.
- [`set.add(value)`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set/add) – adds một value, trả về set本身.
- [`set.delete(value)`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set/delete) – removes value, trả về `true` nếu `value` existed tại moment của call, ngược lại `false`.
- [`set.has(value)`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set/has) – trả về `true` nếu value tồn tại trong set, ngược lại `false`.
- [`set.clear()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set/clear) – removes alles từ set.
- [`set.size`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set/size) – là elements count.

Main feature là repeated calls của `set.add(value)` với cùng value không làm gì. Đó là lý do tại sao mỗi value xuất hiện trong một `Set` chỉ một lần.

Ví例, chúng ta có visitors coming, và chúng ta muốn remember everyone. Nhưng repeated visits không nên lead đến duplicates. Một visitor must được "counted" chỉ một lần.

`Set` là exactly right thing cho điều đó:

```
let set = new Set();

let john = { name: "John" };
let pete = { name: "Pete" };
let mary = { name: "Mary" };

// visits, một số users đến nhiều lần
set.add(john);
set.add(pete);
set.add(mary);
set.add(john);
set.add(mary);

// set keeps only unique values
alert( set.size ); // 3

for (let user of set) {
  alert(user.name); // John (sau đó Pete và Mary)
}
```

Alternative cho `Set` có thể là một array của users, và code để check cho duplicates trên mỗi insertion sử dụng [arr.find](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/find). Nhưng performance sẽ much worse, vì method này walks qua toàn bộ array checking mọi element. `Set` là much better optimized internally cho uniqueness checks.

## [Iteration qua Set](#iteration-over-set)

Chúng ta có thể loop qua một set either với `for..of` hoặc sử dụng `forEach`:

```
let set = new Set(["oranges", "apples", "bananas"]);

for (let value of set) alert(value);

// same với forEach:
set.forEach((value, valueAgain, set) => {
  alert(value);
});
```

Note funny thing. Callback function passed trong `forEach` có 3 arguments: một `value`, sau đó *cùng value* `valueAgain`, và sau đó target object. Thật vậy, cùng value xuất hiện trong arguments hai lần.

Đó là cho compatibility với `Map` nơi callback passed `forEach` có three arguments. Looks a bit strange, chắc chắn. Nhưng điều đó có thể help để replace `Map` với `Set` trong certain cases với ease, và ngược lại.

Các same methods `Map` có cho iterators cũng được supported:

- [`set.keys()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set/keys) – trả về một iterable object cho values,
- [`set.values()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set/values) – same như `set.keys()`, cho compatibility với `Map`,
- [`set.entries()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set/entries) – trả về một iterable object cho entries `[value, value]`, tồn tại cho compatibility với `Map`.

## [Tổng kết](#summary)

[`Map`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map) – là một collection của keyed values.

Methods và properties:

- [`new Map([iterable])`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map/Map) – creates map, với optional `iterable` (ví例 array) của `[key,value]` pairs cho initialization.
- [`map.set(key, value)`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map/set) – stores value bởi key, trả về map本身.
- [`map.get(key)`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map/get) – trả về value bởi key, `undefined` nếu `key` không exist trong map.
- [`map.has(key)`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map/has) – trả về `true` nếu `key` tồn tại, `false` ngược lại.
- [`map.delete(key)`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map/delete) – removes element bởi key, trả về `true` nếu `key` existed tại moment của call, ngược lại `false`.
- [`map.clear()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map/clear) – removes alles từ map.
- [`map.size`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map/size) – trả về current element count.

Differences từ một regular `Object`:

- Bất kỳ keys, objects có thể là keys.
- Additional convenient methods, `size` property.

[`Set`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set) – là một collection của unique values.

Methods và properties:

- [`new Set([iterable])`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set/Set) – creates set, với optional `iterable` (ví例 array) của values cho initialization.
- [`set.add(value)`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set/add) – adds một value (không làm gì nếu `value` exists), trả về set本身.
- [`set.delete(value)`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set/delete) – removes value, trả về `true` nếu `value` existed tại moment của call, ngược lại `false`.
- [`set.has(value)`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set/has) – trả về `true` nếu value tồn tại trong set, ngược lại `false`.
- [`set.clear()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set/clear) – removes alles từ set.
- [`set.size`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set/size) – là elements count.

Iteration qua `Map` và `Set` luôn luôn trong insertion order, vì vậy chúng ta không thể nói rằng这些 collections là unordered, nhưng chúng ta không thể reorder elements hoặc trực tiếp get một element bởi number của nó.

---

---

## Các bài tập

## [Các bài tập](#tasks)

### [Filter unique array members](#filter-unique-array-members)

mức độ quan trọng: 5

Hãy `arr` là một array.

Tạo function `unique(arr)` mà nên trả về một array với unique items của `arr`.

Ví例:

```
function unique(arr) {
  /* your code */
}

let values = ["Hare", "Krishna", "Hare", "Krishna",
  "Krishna", "Krishna", "Hare", "Hare", ":-O"
];

alert( unique(values) ); // Hare, Krishna, :-O
```

P.S. Ở đây strings được sử dụng, nhưng có thể là values của bất kỳ type nào.

P.P.S. Sử dụng `Set` để store unique values.

[Mở một sandbox với tests.](https://plnkr.co/edit/MUauvXz2IM0FwzVK?p=preview)

lời giải

```
function unique(arr) {
  return Array.from(new Set(arr));
}
```

[Mở solution với tests trong một sandbox.](https://plnkr.co/edit/DleyXtQPkKBcDyzX?p=preview)

### [Filter anagrams](#filter-anagrams)

mức độ quan trọng: 4

[Anagrams](https://en.wikipedia.org/wiki/Anagram) là words mà có cùng number của same letters, nhưng trong different order.

Ví例:

```
nap - pan
ear - are - era
cheaters - hectares - teachers
```

Viết function `aclean(arr)` mà trả về một array cleaned từ anagrams.

Ví例:

```
let arr = ["nap", "teachers", "cheaters", "PAN", "ear", "era", "hectares"];

alert( aclean(arr) ); // "nap,teachers,ear" hoặc "PAN,cheaters,era"
```

Từ every anagram group nên remain chỉ một word, không quan trọng哪一个.

[Mở một sandbox với tests.](https://plnkr.co/edit/y8aLGlW40KzD1dMr?p=preview)

lời giải

Để tìm tất cả anagrams, hãy split mọi word thành letters và sort chúng. Khi letter-sorted, tất cả anagrams là same.

Ví例:

```
nap, pan -> anp
ear, era, are -> aer
cheaters, hectares, teachers -> aceehrst
...
```

Chúng ta sẽ sử dụng letter-sorted variants như map keys để store chỉ một value per mỗi key:

```
function aclean(arr) {
  let map = new Map();

  for (let word of arr) {
    // split word bởi letters, sort chúng và join back
    let sorted = word.toLowerCase().split('').sort().join(''); // (*)
    map.set(sorted, word);
  }

  return Array.from(map.values());
}

let arr = ["nap", "teachers", "cheaters", "PAN", "ear", "era", "hectares"];

alert( aclean(arr) );
```

Letter-sorting được done bởi chain của calls trong dòng `(*)`.

Cho convenience hãy split nó vào multiple lines:

```
let sorted = word // PAN
  .toLowerCase() // pan
  .split('') // ['p','a','n']
  .sort() // ['a','n','p']
  .join(''); // anp
```

Hai different words `'PAN'` và `'nap'` nhận được cùng letter-sorted form `'anp'`.

Next line put word vào map:

```
map.set(sorted, word);
```

Nếu chúng ta ever meet một word cùng letter-sorted form một lần nữa, sau đó nó sẽ overwrite previous value với cùng key trong map. Vì vậy chúng ta sẽ luôn có maximum một word per letter-form.

Tại cuối `Array.from(map.values())` takes một iterable qua map values (chúng ta không cần keys trong result) và trả về một array của chúng.

Ở đây chúng ta cũng có thể sử dụng một plain object thay vì `Map`, vì keys là strings.

Đó là cách solution có thể看起来:

```
function aclean(arr) {
  let obj = {};

  for (let i = 0; i < arr.length; i++) {
    let sorted = arr[i].toLowerCase().split("").sort().join("");
    obj[sorted] = arr[i];
  }

  return Object.values(obj);
}

let arr = ["nap", "teachers", "cheaters", "PAN", "ear", "era", "hectares"];

alert( aclean(arr) );
```

[Mở solution với tests trong một sandbox.](https://plnkr.co/edit/tWiX38HZvDfrwGnC?p=preview)

### [Iterable keys](#iterable-keys)

mức độ quan trọng: 5

Chúng ta muốn get một array của `map.keys()` trong một variable và sau đó áp dụng array-specific methods lên nó, ví例 `.push`.

Nhưng điều đó không work:

```
let map = new Map();

map.set("name", "John");

let keys = map.keys();

// Error: keys.push không phải là function
keys.push("more");
```

Tại sao? Làm thế nào để fix code để làm `keys.push` work?

lời giải

Đó là vì `map.keys()` trả về một iterable, nhưng không phải là một array.

Chúng ta có thể convert nó vào một array sử dụng `Array.from`:

```
let map = new Map();

map.set("name", "John");

let keys = Array.from(map.keys());

keys.push("more");

alert(keys); // name, more
```
