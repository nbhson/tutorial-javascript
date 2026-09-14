# Các phương thức mảng (Array methods)

> Nguồn: [https://javascript.info/array-methods](https://javascript.info/array-methods)

<!-- fetched: 2026-09-14 -->

Arrays provide a lot của methods. Để make things easier, trong chương này, chúng được split vào groups.

## [Add/remove items](#add-remove-items)

Chúng ta đã biết methods mà add và remove items từ beginning hoặc end:

- `arr.push(...items)` – adds items đến end,
- `arr.pop()` – extracts một element từ end,
- `arr.shift()` – extracts một element từ beginning,
- `arr.unshift(...items)` – adds items đến beginning.

Đây là một few others.

### [splice](#splice)

Làm thế nào để delete một element từ array?

Arrays là objects, vì vậy chúng ta có thể try để sử dụng `delete`:

```
let arr = ["Tôi", "study", "JavaScript"];

delete arr[1]; // remove "study"

alert( arr[1] ); // undefined

// giờ arr = ["Tôi",  , "JavaScript"]
alert( arr.length ); // 3
```

Element đã được removed, nhưng array vẫn có 3 elements, chúng ta có thể see rằng `arr.length == 3`.

Điều đó là natural, vì `delete obj.key` removes một value bởi `key`. Đó là tất cả nó làm. Fine cho objects. Nhưng cho arrays chúng ta usually want rest của elements để shift và occupy freed place. Chúng ta expect để có một shorter array giờ.

Vì vậy, special methods nên được sử dụng.

[arr.splice](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/splice) method là Swiss army knife cho arrays. Nó có thể làm everything: insert, remove và replace elements.

Syntax là:

```
arr.splice(start[, deleteCount, elem1, ..., elemN])
```

Nó modifies `arr` bắt đầu từ index `start`: removes `deleteCount` elements và sau đó inserts `elem1, ..., elemN` tại place của chúng. Returns array của removed elements.

Method này là easy để grasp bằng examples.

Hãy bắt đầu với deletion:

```
let arr = ["Tôi", "study", "JavaScript"];

arr.splice(1, 1); // từ index 1 remove 1 element

alert( arr ); // ["Tôi", "JavaScript"]
```

Easy, phải không? Bắt đầu từ index `1` nó removed `1` element.

Trong next example, chúng ta remove 3 elements và replace chúng với other two:

```
let arr = ["Tôi", "study", "JavaScript", "right", "now"];

// remove 3 first elements và replace chúng với another
arr.splice(0, 3, "Let's", "dance");

alert( arr ) // giờ ["Let's", "dance", "right", "now"]
```

Ở đây chúng ta có thể see rằng `splice` trả về array của removed elements:

```
let arr = ["Tôi", "study", "JavaScript", "right", "now"];

// remove 2 first elements
let removed = arr.splice(0, 2);

alert( removed ); // "Tôi", "study" <-- array của removed elements
```

`splice` method cũng có thể insert các elements mà không có任何 removals. Cho điều đó, chúng ta cần để set `deleteCount` đến `0`:

```
let arr = ["Tôi", "study", "JavaScript"];

// từ index 2
// delete 0
// sau đó insert "complex" và "language"
arr.splice(2, 0, "complex", "language");

alert( arr ); // "Tôi", "study", "complex", "language", "JavaScript"
```

Negative indexes allowed

Ở đây và trong các array methods khác, negative indexes được allowed. Chúng specify position từ end của array, như ở đây:

```
let arr = [1, 2, 5];

// từ index -1 (một step từ end)
// delete 0 elements,
// sau đó insert 3 và 4
arr.splice(-1, 0, 3, 4);

alert( arr ); // 1,2,3,4,5
```

### [slice](#slice)

Method [arr.slice](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/slice) simpler hơn nhiều so với similar-looking `arr.splice`.

Syntax là:

```
arr.slice([start], [end])
```

Nó trả về một new array copying vào nó tất cả items từ index `start` đến `end` (không including `end`). Cả `start` và `end` có thể là negative, trong case đó position từ array end được assumed.

Nó tương tự như string method `str.slice`, nhưng thay vì substrings, nó makes subarrays.

Ví例:

```
let arr = ["t", "e", "s", "t"];

alert( arr.slice(1, 3) ); // e,s (copy từ 1 đến 3)

alert( arr.slice(-2) ); // s,t (copy từ -2 till end)
```

Chúng ta cũng có thể call nó mà không có arguments: `arr.slice()` creates một copy của `arr`. Điều đó thường được used để obtain một copy cho further transformations mà không nên affect original array.

### [concat](#concat)

Method [arr.concat](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/concat) creates một new array mà includes values từ các arrays khác và additional items.

Syntax là:

```
arr.concat(arg1, arg2...)
```

Nó accepts bất kỳ number của arguments – either arrays hoặc values.

Result là một new array chứa items từ `arr`, sau đó `arg1`, `arg2` v.v.

Nếu argument `argN` là một array, sau đó tất cả elements của nó được copied. Ngược lại, argument本身 được copied.

Ví例:

```
let arr = [1, 2];

// create một array từ: arr và [3,4]
alert( arr.concat([3, 4]) ); // 1,2,3,4

// create một array từ: arr và [3,4] và [5,6]
alert( arr.concat([3, 4], [5, 6]) ); // 1,2,3,4,5,6

// create một array từ: arr và [3,4], sau đó add values 5 và 6
alert( arr.concat([3, 4], 5, 6) ); // 1,2,3,4,5,6
```

Normally, nó chỉ copies elements từ arrays. Other objects, ngay cả nếu chúng看起来 như arrays, được added như một whole:

```
let arr = [1, 2];

let arrayLike = {
  0: "something",
  length: 1
};

alert( arr.concat(arrayLike) ); // 1,2,[object Object]
```

…Nhưng nếu một array-like object có special `Symbol.isConcatSpreadable` property, sau đó nó được treat như một array bởi `concat`: elements của nó được added thay vì:

```
let arr = [1, 2];

let arrayLike = {
  0: "something",
  1: "else",
  [Symbol.isConcatSpreadable]: true,
  length: 2
};

alert( arr.concat(arrayLike) ); // 1,2,something,else
```

## [Iterate: forEach](#iterate-foreach)

[arr.forEach](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/forEach) method allows để run một function cho mọi element của array.

Syntax:

```
arr.forEach(function(item, index, array) {
  // ... do something với一个 item
});
```

Ví例, cái này shows mỗi element của array:

```
// cho mỗi element call alert
["Bilbo", "Gandalf", "Nazgul"].forEach(alert);
```

Và cái này code là more elaborate về positions của chúng trong target array:

```
["Bilbo", "Gandalf", "Nazgul"].forEach((item, index, array) => {
  alert(`${item} is at index ${index} trong ${array}`);
});
```

Result của function (nếu nó returns bất kỳ) được thrown away và ignored.

## [Searching trong array](#searching-in-array)

Giờ hãy cover các methods mà searching trong một array.

### [indexOf/lastIndexOf và includes](#indexof-lastindexof-and-includes)

Các methods [arr.indexOf](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/indexOf) và [arr.includes](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/includes) có similar syntax và làm essentially same như string counterparts, nhưng operate trên items thay vì characters:

- `arr.indexOf(item, from)` – looks cho `item` bắt đầu từ index `from`, và trả về index nơi nó được found, ngược lại `-1`.
- `arr.includes(item, from)` – looks cho `item` bắt đầu từ index `from`, trả về `true` nếu found.

Thông thường, these methods được sử dụng với chỉ một argument: `item` để search. Theo mặc định, search là từ beginning.

Ví例:

```
let arr = [1, 0, false];

alert( arr.indexOf(0) ); // 1
alert( arr.indexOf(false) ); // 2
alert( arr.indexOf(null) ); // -1

alert( arr.includes(1) ); // true
```

Xin lưu ý rằng `indexOf` sử dụng strict equality `===` cho comparison. Vì vậy, nếu chúng ta look cho `false`, nó finds exactly `false` và không phải zero.

Nếu chúng ta muốn để check nếu `item` exists trong array và không cần index, sau đó `arr.includes` được preferred.

Method [arr.lastIndexOf](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/lastIndexOf) là same như `indexOf`, nhưng looks cho từ right sang left.

```
let fruits = ['Táo', 'Cam', 'Táo']

alert( fruits.indexOf('Táo') ); // 0 (first Táo)
alert( fruits.lastIndexOf('Táo') ); // 2 (last Táo)
```

`includes` method handles `NaN` correctly

Một minor, nhưng noteworthy feature của `includes` là nó correctly handles `NaN`, không giống `indexOf`:

```
const arr = [NaN];
alert( arr.indexOf(NaN) ); // -1 (wrong, should be 0)
alert( arr.includes(NaN) );// true (correct)
```

Đó là vì `includes` được added đến JavaScript much later và sử dụng more up-to-date comparison algorithm internally.

### [find và findIndex/findLastIndex](#find-and-findindex-findlastindex)

Imagine chúng ta có một array của objects. Làm thế nào để find một object với một specific condition?

Ở đây [arr.find(fn)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/find) method comes in handy.

Syntax là:

```
let result = arr.find(function(item, index, array) {
  // nếu true được returned, item được returned và iteration được stopped
  // cho falsy scenario trả về undefined
});
```

Function được gọi cho elements của array, one after another:
- `item` là element.
- `index` là index của nó.
- `array` là array本身.

Nếu nó trả về `true`, search được stopped, `item` được returned. Nếu không có gì được found, `undefined` được returned.

Ví例, chúng ta có một array của users, mỗi one có fields `id` và `name`. Hãy find một với `id == 1`:

```
let users = [
  {id: 1, name: "John"},
  {id: 2, name: "Pete"},
  {id: 3, name: "Mary"}
];

let user = users.find(item => item.id == 1);

alert(user.name); // John
```

Trong thực tế, arrays của objects là một common thing, vì vậy `find` method là very useful.

Note rằng trong ví例 chúng ta provide đến `find` function `item => item.id == 1` với một argument. Đó là typical, các arguments khác của function này rarely được used.

[arr.findIndex](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/findIndex) method có same syntax nhưng trả về index nơi element được found thay vì element本身. Value của `-1` được returned nếu không có gì được found.

[arr.findLastIndex](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/findLastIndex) method là like `findIndex`, nhưng searches từ right sang left, tương tự như `lastIndexOf`.

Đây là một ví例:

```
let users = [
  {id: 1, name: "John"},
  {id: 2, name: "Pete"},
  {id: 3, name: "Mary"},
  {id: 4, name: "John"}
];

// Find index của first John
alert(users.findIndex(user => user.name == 'John')); // 0

// Find index của last John
alert(users.findLastIndex(user => user.name == 'John')); // 3
```

### [filter](#filter)

`find` method looks cho một single (first) element mà makes function trả về `true`.

Nếu có thể có nhiều, chúng ta có thể sử dụng [arr.filter(fn)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/filter).

Syntax tương tự như `find`, nhưng `filter` trả về một array của tất cả matching elements:

```
let results = arr.filter(function(item, index, array) {
  // nếu true item được push vào results và iteration continues
  // trả về empty array nếu không found gì
});
```

Ví例:

```
let users = [
  {id: 1, name: "John"},
  {id: 2, name: "Pete"},
  {id: 3, name: "Mary"}
];

// returns array của first two users
let someUsers = users.filter(item => item.id < 3);

alert(someUsers.length); // 2
```

## [Transform một array](#transform-an-array)

Hãy move on đến các methods mà transform và reorder một array.

### [map](#map)

[arr.map](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/map) method là một trong những most useful và thường được used nhất.

Nó calls function cho mỗi element của array và trả về array của results.

Syntax là:

```
let result = arr.map(function(item, index, array) {
  // trả về new value thay vì item
});
```

Ví例, ở đây chúng ta transform mỗi element vào length của nó:

```
let lengths = ["Bilbo", "Gandalf", "Nazgul"].map(item => item.length);
alert(lengths); // 5,7,6
```

### [sort(fn)](#sort-fn)

Call đến [arr.sort()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/sort) sorts array *in place*, changing element order.

Nó cũng trả về sorted array, nhưng returned value thường được ignored, vì `arr`本身 được modified.

Ví例:

```
let arr = [ 1, 2, 15 ];

// method reorders content của arr
arr.sort();

alert( arr );  // 1, 15, 2
```

Bạn đã notice bất kỳ strange gì trong outcome?

Order became `1, 15, 2`. Incorrect. Nhưng tại sao?

**Items được sorted như strings theo mặc định.**

Literally, all elements được converted đến strings cho comparisons. Cho strings, lexicographic ordering được áp dụng và indeed `"2" > "15"`.

Để sử dụng sorting order của riêng chúng ta, chúng ta cần để supply một function như argument của `arr.sort()`.

Function nên compare hai arbitrary values và trả về:

```
function compare(a, b) {
  if (a > b) return 1; // nếu first value greater hơn second
  if (a == b) return 0; // nếu values bằng nhau
  if (a < b) return -1; // nếu first value less hơn second
}
```

Ví例, để sort như numbers:

```
function compareNumeric(a, b) {
  if (a > b) return 1;
  if (a == b) return 0;
  if (a < b) return -1;
}

let arr = [ 1, 2, 15 ];

arr.sort(compareNumeric);

alert(arr);  // 1, 2, 15
```

Giờ nó work như intended.

Hãy step aside và think về những gì happening. `arr` có thể là một array của bất kỳ cái gì, phải không? Nó có thể chứa numbers hoặc strings hoặc objects hoặc whatever. Chúng ta có một set của *some items*. Để sort nó, chúng ta need một *ordering function* mà biết làm thế nào để compare các elements của nó. Default là string order.

`arr.sort(fn)` method implements một generic sorting algorithm. Chúng ta không cần để care về cách nó hoạt động nội bộ (một optimized [quicksort](https://en.wikipedia.org/wiki/Quicksort) hoặc [Timsort](https://en.wikipedia.org/wiki/Timsort) most of the time). Nó sẽ walk array, compare các elements sử dụng provided function và reorder chúng, tất cả những gì chúng ta cần là提供 `fn` mà làm comparison.

By the way, nếu chúng ta ever want để know những elements được compared – không có gì ngăn chúng ta alert chúng:

```
[1, -2, 15, 2, 0, 8].sort(function(a, b) {
  alert( a + " <> " + b );
  return a - b;
});
```

Algorithm có thể compare một element với multiple others trong quá trình, nhưng nó cố gắng để make as few comparisons như có thể.

Comparison function có thể trả về bất kỳ number nào

Actually, một comparison function chỉ required để trả về một positive number để nói "greater" và một negative number để nói "less".

Điều đó allows để viết shorter functions:

```
let arr = [ 1, 2, 15 ];

arr.sort(function(a, b) { return a - b; });

alert(arr);  // 1, 2, 15
```

Arrow functions cho best

Remember [arrow functions](/arrow-functions-basics)? Chúng ta có thể sử dụng chúng ở đây cho neater sorting:

```
arr.sort( (a, b) => a - b );
```

Điều đó work exactly same như longer version ở trên.

Sử dụng `localeCompare` cho strings

Remember [strings](/string#correct-comparisons) comparison algorithm? Nó compares letters bởi codes của chúng theo mặc định.

Cho nhiều alphabets, tốt hơn để sử dụng `str.localeCompare` method để correctly sort letters, như `Ö`.

Ví例, hãy sort vài countries trong German:

```
let countries = ['Österreich', 'Andorra', 'Vietnam'];

alert( countries.sort( (a, b) => a > b ? 1 : -1) ); // Andorra, Vietnam, Österreich (wrong)

alert( countries.sort( (a, b) => a.localeCompare(b) ) ); // Andorra,Österreich,Vietnam (correct!)
```

### [reverse](#reverse)

Method [arr.reverse](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/reverse) reverses order của elements trong `arr`.

Ví例:

```
let arr = [1, 2, 3, 4, 5];
arr.reverse();

alert( arr ); // 5,4,3,2,1
```

Nó cũng trả về array `arr` sau reversal.

### [split và join](#split-and-join)

Đây là situation từ thực life. Chúng ta đang writing một messaging app, và person enters comma-delimited list của receivers: `John, Pete, Mary`. Nhưng cho chúng ta một array của names sẽ comfortable hơn nhiều hơn một single string. Làm thế nào để get nó?

[str.split(delim)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/split) method làm exactly cái đó. Nó splits string vào một array bởi given delimiter `delim`.

Trong ví例 dưới đây, chúng ta split bởi một comma followed bởi một space:

```
let names = 'Bilbo, Gandalf, Nazgul';

let arr = names.split(', ');

for (let name of arr) {
  alert( `Một message đến ${name}.` ); // Một message đến Bilbo  (và các tên khác)
}
```

`split` method có một optional second numeric argument – một limit trên array length. Nếu nó được cung cấp, sau đó extra elements được ignored. Trong thực tế nó rarely được used though:

```
let arr = 'Bilbo, Gandalf, Nazgul, Saruman'.split(', ', 2);

alert(arr); // Bilbo, Gandalf
```

Split into letters

Call đến `split(s)` với một empty `s` sẽ split string vào một array của letters:

```
let str = "test";

alert( str.split('') ); // t,e,s,t
```

Call [arr.join(glue)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/join) làm reverse cho `split`. Nó creates một string của `arr` items joined bởi `glue` giữa chúng.

Ví例:

```
let arr = ['Bilbo', 'Gandalf', 'Nazgul'];

let str = arr.join(';'); // glue array vào một string sử dụng ;

alert( str ); // Bilbo;Gandalf;Nazgul
```

### [reduce/reduceRight](#reduce-reduceright)

Khi chúng ta cần iterate qua một array – we có thể sử dụng `forEach`, `for` hoặc `for..of`.

Khi chúng ta cần iterate và trả về data cho mỗi element – we có thể sử dụng `map`.

Các methods [arr.reduce](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/reduce) và [arr.reduceRight](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/reduceRight) cũng thuộc về breed đó, nhưng là một little bit more intricate. Chúng được used để calculate một single value dựa trên array.

Syntax là:

```
let value = arr.reduce(function(accumulator, item, index, array) {
  // ...
}, [initial]);
```

Function được applied cho tất cả array elements one after another và "carries on" result của nó đến next call.

Arguments:
- `accumulator` – là result của previous function call, bằng `initial` lần đầu tiên (nếu `initial` được cung cấp).
- `item` – là current array item.
- `index` – là position của nó.
- `array` – là array.

Như function được applied, result của previous function call được passed đến next như là first argument.

Vì vậy, first argument về cơ bản là accumulator mà stores combined result của tất cả previous executions. Và ở cuối, nó becomes result của `reduce`.

Sounds complicated?

Easyest way để grasp điều đó là bằng example.

Ở đây chúng ta get sum của một array trong một line:

```
let arr = [1, 2, 3, 4, 5];

let result = arr.reduce((sum, current) => sum + current, 0);

alert(result); // 15
```

Function passed đến `reduce` sử dụng only 2 arguments, đó là typically enough.

Hãy xem chi tiết của những gì happening.

1. Tại first run, `sum` là `initial` value (last argument của `reduce`), bằng `0`, và `current` là first array element, bằng `1`. Vì vậy function result là `1`.
2. Tại second run, `sum = 1`, chúng ta add second array element (`2`) vào nó và return.
3. Tại 3rd run, `sum = 3` và chúng ta add one more element vào nó, và vân vân…

Calculation flow:

![](/article/array-methods/reduce.svg)

Hoặc dưới dạng một table, nơi mỗi row đại diện cho một function call trên next array element:

|  | `sum` | `current` | result |
| --- | --- | --- | --- |
| first call | `0` | `1` | `1` |
| second call | `1` | `2` | `3` |
| third call | `3` | `3` | `6` |
| fourth call | `6` | `4` | `10` |
| fifth call | `10` | `5` | `15` |

Ở đây chúng ta có thể clearly see rằng result của previous call becomes first argument của next.

Chúng ta cũng có thể omit initial value:

```
let arr = [1, 2, 3, 4, 5];

// removed initial value từ reduce (không có 0)
let result = arr.reduce((sum, current) => sum + current);

alert( result ); // 15
```

Result là same. Đó là vì nếu không có initial, sau đó `reduce` takes first element của array như initial value và starts iteration từ 2nd element.

Calculation table là same như ở trên, trừ first row.

Nhưng such use requires extreme care. Nếu array là empty, sau đó `reduce` call không có initial value gives một error.

Đây là một ví例:

```
let arr = [];

// Error: Reduce của empty array không có initial value
// nếu initial value existed, reduce sẽ trả về nó cho empty arr.
arr.reduce((sum, current) => sum + current);
```

Vì vậy được advised để luôn specify initial value.

Method [arr.reduceRight](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/reduceRight) làm same nhưng goes từ right sang left.

## [Array.isArray](#array-isarray)

Arrays không form một separate language type. Chúng được based trên objects.

Vì vậy `typeof` không help để distinguish một plain object từ một array:

```
alert(typeof {}); // object
alert(typeof []); // object (same)
```

…Nhưng arrays được used so often mà có một special method cho điều đó: [Array.isArray(value)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/isArray). Nó trả về `true` nếu `value` là một array, và `false` ngược lại.

```
alert(Array.isArray({})); // false

alert(Array.isArray([])); // true
```

## [Most methods support "thisArg"](#most-methods-support-thisarg)

Almost tất cả array methods mà calls functions – như `find`, `filter`, `map`, với exception đáng kể của `sort`, accept một optional additional parameter `thisArg`.

Parameter này không được giải thích trong các sections ở trên, vì nó rarely được used. Nhưng cho completeness, chúng ta phải cover nó.

Đây là full syntax của这些 methods:

```
arr.find(func, thisArg);
arr.filter(func, thisArg);
arr.map(func, thisArg);
// ...
// thisArg là optional last argument
```

Value của `thisArg` parameter becomes `this` cho `func`.

Ví例, ở đây chúng ta sử dụng một method của `army` object như một filter, và `thisArg` passes context:

```
let army = {
  minAge: 18,
  maxAge: 27,
  canJoin(user) {
    return user.age >= this.minAge && user.age < this.maxAge;
  }
};

let users = [
  {age: 16},
  {age: 20},
  {age: 23},
  {age: 30}
];

// find users, cho who army.canJoin trả về true
let soldiers = users.filter(army.canJoin, army);

alert(soldiers.length); // 2
alert(soldiers[0].age); // 20
alert(soldiers[1].age); // 23
```

Nếu trong ví例 trên chúng ta sử dụng `users.filter(army.canJoin)`, sau đó `army.canJoin` sẽ được called như một standalone function, với `this=undefined`, do đó leading đến instant error.

Một call đến `users.filter(army.canJoin, army)` có thể được thay thế với `users.filter(user => army.canJoin(user))`, mà làm same. Latter được used nhiều hơn, vì nó a little easier để understand cho most people.

## [Tổng kết](#summary)

Một cheat sheet của array methods:

- Để add/remove elements:

  - `push(...items)` – adds items đến end,
  - `pop()` – extracts một element từ end,
  - `shift()` – extracts một element từ beginning,
  - `unshift(...items)` – adds items đến beginning.
  - `splice(pos, deleteCount, ...items)` – tại index `pos` deletes `deleteCount` elements và inserts `items`.
  - `slice(start, end)` – creates một new array, copies elements từ index `start` till `end` (không inclusive) vào nó.
  - `concat(...items)` – returns một new array: copies tất cả members của current một và adds `items` vào nó. Nếu bất kỳ của `items` là một array, sau đó elements của nó được take.
- Để search trong elements:

  - `indexOf/lastIndexOf(item, pos)` – look cho `item` bắt đầu từ position `pos`, và trả về index hoặc `-1` nếu not found.
  - `includes(value)` – trả về `true` nếu array có `value`, ngược lại `false`.
  - `find/filter(func)` – filter elements qua function, trả về first/all values mà makes it trả về `true`.
  - `findIndex` là like `find`, nhưng trả về index thay vì một value.
- Để iterate qua elements:

  - `forEach(func)` – calls `func` cho mọi element, không trả về gì.
- Để transform array:

  - `map(func)` – creates một new array từ results của calling `func` cho mọi element.
  - `sort(func)` – sorts array in-place, sau đó trả về nó.
  - `reverse()` – reverses array in-place, sau đó trả về nó.
  - `split/join` – convert một string sang array và ngược lại.
  - `reduce/reduceRight(func, initial)` – calculate một single value qua array bằng cách calling `func` cho mỗi element và passing một intermediate result giữa các calls.
- Additionally:

  - `Array.isArray(value)` checks `value` cho being một array, nếu vậy trả về `true`, ngược lại `false`.

Please note rằng methods `sort`, `reverse` và `splice` modifies array本身.

These methods là những most used ones, chúng cover 99% của use cases. Nhưng có một vài others:

- [arr.some(fn)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/some)/[arr.every(fn)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/every) checks array.

  Function `fn` được called trên mỗi element của array tương tự như `map`. Nếu any/all results là `true`, trả về `true`, ngược lại `false`.

  These methods behave sort của like `||` và `&&` operators: nếu `fn` trả về một truthy value, `arr.some()` ngay lập tức trả về `true` và stops iterating qua rest của items; nếu `fn` trả về một falsy value, `arr.every()` ngay lập tức trả về `false` và stops iterating qua rest của items cũng.

  Chúng ta có thể sử dụng `every` để compare arrays:

  ```
  function arraysEqual(arr1, arr2) {
    return arr1.length === arr2.length && arr1.every((value, index) => value === arr2[index]);
  }

  alert( arraysEqual([1, 2], [1, 2])); // true
  ```
- [arr.fill(value, start, end)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/fill) – fills array với repeating `value` từ index `start` đến `end`.
- [arr.copyWithin(target, start, end)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/copyWithin) – copies elements của nó từ position `start` till position `end` vào *bản thân*, tại position `target` (overwrites existing).
- [arr.flat(depth)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/flat)/[arr.flatMap(fn)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/flatMap) tạo một new flat array từ một multidimensional array.

Cho full list, xem [manual](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array).

At first sight, có thể seem rằng có so many methods, quite difficult để remember. Nhưng thực tế, điều đó dễ dàng hơn nhiều.

Look through cheat sheet just để be aware của chúng. Sau đó solve tasks của chương này để practice, vì vậy bạn có experience với array methods.

Sau đó bất kỳ lúc nào bạn cần để do anything với một array, và bạn không biết làm thế nào – come here, look tại cheat sheet và find right method. Examples sẽ giúp bạn để viết nó correctly. Soon bạn sẽ automatically remember các methods, không có specific efforts từ phía bạn.

---

---

## Các bài tập

## [Các bài tập](#tasks)

### [Translate border-left-width sang borderLeftWidth](#translate-border-left-width-to-borderleftwidth)

mức độ quan trọng: 5

Viết function `camelize(str)` mà changes dash-separated words như "my-short-string" thành camel-cased "myShortString".

Tức là: removes tất cả dashes, mỗi word sau dash trở thành uppercased.

Các ví例:

```
camelize("background-color") == 'backgroundColor';
camelize("list-style-image") == 'listStyleImage';
camelize("-webkit-transition") == 'WebkitTransition';
```

P.S. Hint: sử dụng `split` để split string vào một array, transform nó và `join` back.

[Mở một sandbox với tests.](https://plnkr.co/edit/dAF0dZ4YJPWUo1fa?p=preview)

lời giải

```
function camelize(str) {
  return str
    .split('-') // splits 'my-long-word' vào array ['my', 'long', 'word']
    .map(
      // capitalizes first letters của tất cả array items trừ first one
      // converts ['my', 'long', 'word'] vào ['my', 'Long', 'Word']
      (word, index) => index == 0 ? word : word[0].toUpperCase() + word.slice(1)
    )
    .join(''); // joins ['my', 'Long', 'Word'] vào 'myLongWord'
}
```

[Mở solution với tests trong một sandbox.](https://plnkr.co/edit/g0rn2sRMwfr1CM0a?p=preview)

### [Filter range](#filter-range)

mức độ quan trọng: 4

Viết function `filterRange(arr, a, b)` mà gets một array `arr`, look cho các elements với values cao hơn hoặc bằng `a` và lower hoặc bằng `b` và trả về result như một array.

Function không nên modify array. Nó nên trả về new array.

Ví例:

```
let arr = [5, 3, 8, 1];

let filtered = filterRange(arr, 1, 4);

alert( filtered ); // 3,1 (matching values)

alert( arr ); // 5,3,8,1 (not modified)
```

[Mở một sandbox với tests.](https://plnkr.co/edit/qw1z3b5aNgvbQOMQ?p=preview)

lời giải

```
function filterRange(arr, a, b) {
  // added brackets quanh expression cho better readability
  return arr.filter(item => (a <= item && item <= b));
}

let arr = [5, 3, 8, 1];

let filtered = filterRange(arr, 1, 4);

alert( filtered ); // 3,1 (matching values)

alert( arr ); // 5,3,8,1 (not modified)
```

[Mở solution với tests trong một sandbox.](https://plnkr.co/edit/laSpPelqqxEKI5n3?p=preview)

### [Filter range "in place"]( #filter-range-in-place)

mức độ quan trọng: 4

Viết function `filterRangeInPlace(arr, a, b)` mà gets một array `arr` và removes từ nó tất cả values ngoại trừ những mà là giữa `a` và `b`. Test là: `a ≤ arr[i] ≤ b`.

Function nên chỉ modify array. Nó không nên trả về gì.

Ví例:

```
let arr = [5, 3, 8, 1];

filterRangeInPlace(arr, 1, 4); // removed numbers ngoại trừ từ 1 đến 4

alert( arr ); // [3, 1]
```

[Mở một sandbox với tests.](https://plnkr.co/edit/34AaQvUB4VBEpPu1?p=preview)

lời giải

```
function filterRangeInPlace(arr, a, b) {

  for (let i = 0; i < arr.length; i++) {
    let val = arr[i];

    // remove nếu outside của interval
    if (val < a || val > b) {
      arr.splice(i, 1);
      i--;
    }
  }

}

let arr = [5, 3, 8, 1];

filterRangeInPlace(arr, 1, 4); // removed numbers ngoại trừ từ 1 đến 4

alert( arr ); // [3, 1]
```

[Mở solution với tests trong một sandbox.](https://plnkr.co/edit/j80aBKHMgBo6i5SE?p=preview)

### [Sort trong decreasing order](#sort-in-decreasing-order)

mức độ quan trọng: 4

```
let arr = [5, 2, 1, -10, 8];

// ... your code để sort nó trong decreasing order

alert( arr ); // 8, 5, 2, 1, -10
```

lời giải

```
let arr = [5, 2, 1, -10, 8];

arr.sort((a, b) => b - a);

alert( arr );
```

### [Copy và sort array](#copy-and-sort-array)

mức độ quan trọng: 5

Chúng ta có một array của strings `arr`. Chúng ta muốn có một sorted copy của nó, nhưng giữ `arr` unmodified.

Tạo function `copySorted(arr)` mà trả về such copy.

```
let arr = ["HTML", "JavaScript", "CSS"];

let sorted = copySorted(arr);

alert( sorted ); // CSS, HTML, JavaScript
alert( arr ); // HTML, JavaScript, CSS (no changes)
```

lời giải

Chúng ta có thể sử dụng `slice()` để make một copy và run sort trên nó:

```
function copySorted(arr) {
  return arr.slice().sort();
}

let arr = ["HTML", "JavaScript", "CSS"];

let sorted = copySorted(arr);

alert( sorted );
alert( arr );
```

### [Tạo một extendable calculator](#create-an-extendable-calculator)

mức độ quan trọng: 5

Tạo constructor function `Calculator` mà tạo "extendable" calculator objects.

Task gồm hai parts.

1. First, implement method `calculate(str)` mà takes một string như `"1 + 2"` trong format "NUMBER operator NUMBER" (space-delimited) và trả về result. Should understand plus `+` và minus `-`.

   Usage ví例:

   ```
   let calc = new Calculator;

   alert( calc.calculate("3 + 7") ); // 10
   ```
2. Sau đó thêm method `addMethod(name, func)` mà teaches calculator một new operation. Nó takes operator `name` và two-argument function `func(a,b)` mà implements nó.

   Ví例, hãy add multiplication `*`, division `/` và power `**`:

   ```
   let powerCalc = new Calculator;
   powerCalc.addMethod("*", (a, b) => a * b);
   powerCalc.addMethod("/", (a, b) => a / b);
   powerCalc.addMethod("**", (a, b) => a ** b);

   let result = powerCalc.calculate("2 ** 3");
   alert( result ); // 8
   ```

- Không parentheses hoặc complex expressions trong task này.
- Numbers và operator được delimited với exactly một space.
- Có thể có error handling nếu bạn muốn thêm nó.

[Mở một sandbox với tests.](https://plnkr.co/edit/A5OT4UUNYiIOziiQ?p=preview)

lời giải

- Please note cách methods được stored. Chúng được simply added vào `this.methods` property.
- Tất cả tests và numeric conversions được done trong `calculate` method. Trong tương lai nó có thể được extended để support more complex expressions.

```
function Calculator() {

  this.methods = {
    "-": (a, b) => a - b,
    "+": (a, b) => a + b
  };

  this.calculate = function(str) {

    let split = str.split(' '),
      a = +split[0],
      op = split[1],
      b = +split[2];

    if (!this.methods[op] || isNaN(a) || isNaN(b)) {
      return NaN;
    }

    return this.methods[op](a, b);
  };

  this.addMethod = function(name, func) {
    this.methods[name] = func;
  };
}
```

[Mở solution với tests trong một sandbox.](https://plnkr.co/edit/ITgICzRf4STvCgso?p=preview)

### [Map to names](#map-to-names)

mức độ quan trọng: 5

Bạn có một array của `user` objects, mỗi one có `user.name`. Viết code mà converts nó vào một array của names.

Ví例:

```
let john = { name: "John", age: 25 };
let pete = { name: "Pete", age: 30 };
let mary = { name: "Mary", age: 28 };

let users = [ john, pete, mary ];

let names = /* ... your code */

alert( names ); // John, Pete, Mary
```

lời giải

```
let john = { name: "John", age: 25 };
let pete = { name: "Pete", age: 30 };
let mary = { name: "Mary", age: 28 };

let users = [ john, pete, mary ];

let names = users.map(item => item.name);

alert( names ); // John, Pete, Mary
```

### [Map to objects](#map-to-objects)

mức độ quan trọng: 5

Bạn có một array của `user` objects, mỗi one có `name`, `surname` và `id`.

Viết code để tạo một another array từ nó, của objects với `id` và `fullName`, nơi `fullName` được generated từ `name` và `surname`.

Ví例:

```
let john = { name: "John", surname: "Smith", id: 1 };
let pete = { name: "Pete", surname: "Hunt", id: 2 };
let mary = { name: "Mary", surname: "Key", id: 3 };

let users = [ john, pete, mary ];

let usersMapped = /* ... your code ... */

/*
usersMapped = [
  { fullName: "John Smith", id: 1 },
  { fullName: "Pete Hunt", id: 2 },
  { fullName: "Mary Key", id: 3 }
]
*/

alert( usersMapped[0].id ) // 1
alert( usersMapped[0].fullName ) // John Smith
```

Vì vậy, thực sự bạn need để map một array của objects đến một another. Try sử dụng `=>` ở đây. Có một small catch.

lời giải

```
let john = { name: "John", surname: "Smith", id: 1 };
let pete = { name: "Pete", surname: "Hunt", id: 2 };
let mary = { name: "Mary", surname: "Key", id: 3 };

let users = [ john, pete, mary ];

let usersMapped = users.map(user => ({
  fullName: `${user.name} ${user.surname}`,
  id: user.id
}));

/*
usersMapped = [
  { fullName: "John Smith", id: 1 },
  { fullName: "Pete Hunt", id: 2 },
  { fullName: "Mary Key", id: 3 }
]
*/

alert( usersMapped[0].id ); // 1
alert( usersMapped[0].fullName ); // John Smith
```

Please note rằng trong arrow functions chúng ta need để sử dụng additional brackets.

Chúng ta không thể viết như thế này:

```
let usersMapped = users.map(user => {
  fullName: `${user.name} ${user.surname}`,
  id: user.id
});
```

Như chúng ta remember, có hai arrow functions: không có body `value => expr` và với body `value => {...}`.

Ở đây JavaScript sẽ treat `{` như start của function body, không phải start của object. Workaround là wrap chúng trong "normal" brackets:

```
let usersMapped = users.map(user => ({
  fullName: `${user.name} ${user.surname}`,
  id: user.id
}));
```

Giờ fine.

### [Sort users bởi age](#sort-users-by-age)

mức độ quan trọng: 5

Viết function `sortByAge(users)` mà gets một array của objects với `age` property và sorts chúng bởi `age`.

Ví例:

```
let john = { name: "John", age: 25 };
let pete = { name: "Pete", age: 30 };
let mary = { name: "Mary", age: 28 };

let arr = [ pete, john, mary ];

sortByAge(arr);

// giờ: [john, mary, pete]
alert(arr[0].name); // John
alert(arr[1].name); // Mary
alert(arr[2].name); // Pete
```

lời giải

```
function sortByAge(arr) {
  arr.sort((a, b) => a.age - b.age);
}

let john = { name: "John", age: 25 };
let pete = { name: "Pete", age: 30 };
let mary = { name: "Mary", age: 28 };

let arr = [ pete, john, mary ];

sortByAge(arr);

// giờ sorted là: [john, mary, pete]
alert(arr[0].name); // John
alert(arr[1].name); // Mary
alert(arr[2].name); // Pete
```

### [Shuffle một array](#shuffle-an-array)

mức độ quan trọng: 3

Viết function `shuffle(array)` mà shuffles (randomly reorders) elements của array.

Multiple runs của `shuffle` có thể lead đến different orders của elements. Ví例:

```
let arr = [1, 2, 3];

shuffle(arr);
// arr = [3, 2, 1]

shuffle(arr);
// arr = [2, 1, 3]

shuffle(arr);
// arr = [3, 1, 2]
// ...
```

Tất cả element orders nên have equal probability. Ví例, `[1,2,3]` có thể được reordered như `[1,2,3]` hoặc `[1,3,2]` hoặc `[3,1,2]` v.v., với equal probability của mỗi case.

lời giải

Simple solution có thể là:

```
function shuffle(array) {
  array.sort(() => Math.random() - 0.5);
}

let arr = [1, 2, 3];
shuffle(arr);
alert(arr);
```

Điều somewhat works, vì `Math.random() - 0.5` là một random number mà có thể là positive hoặc negative, vì vậy sorting function reorders elements randomly.

Nhưng vì sorting function không meant để được used theo cách này, không phải tất cả permutations có same probability.

Ví例, xem xét code dưới đây. Nó chạy `shuffle` 1000000 times và counts appearances của tất cả possible results:

```
function shuffle(array) {
  array.sort(() => Math.random() - 0.5);
}

// counts của appearances cho tất cả possible permutations
let count = {
  '123': 0,
  '132': 0,
  '213': 0,
  '231': 0,
  '321': 0,
  '312': 0
};

for (let i = 0; i < 1000000; i++) {
  let array = [1, 2, 3];
  shuffle(array);
  count[array.join('')]++;
}

// show counts của tất cả possible permutations
for (let key in count) {
  alert(`${key}: ${count[key]}`);
}
```

Một ví例 output:

```
123: 250706
132: 124425
213: 249618
231: 124880
312: 125148
321: 125223
```

Chúng ta có thể clearly see bias: `123` và `213` xuất hiện much more often hơn others.

Result của code có thể vary giữa JavaScript engines, nhưng chúng ta có thể already see rằng approach là unreliable.

Tại sao nó không work? Nói chung, `sort` là một "black box": chúng ta throw một array và một comparison function vào nó và expect array để được sorted. Nhưng do utter randomness của comparison black box goes mad, và how exactly nó goes mad depends trên concrete implementation mà differs giữa engines.

Có các good ways khác để do task. Ví例, có một great algorithm được gọi là [Fisher-Yates shuffle](https://en.wikipedia.org/wiki/Fisher%E2%80%93Yates_shuffle). Idea là để walk array trong reverse order và swap mỗi element với một random một trước nó:

```
function shuffle(array) {
  for (let i = array.length - 1; i > 0; i--) {
    let j = Math.floor(Math.random() * (i + 1)); // random index từ 0 đến i

    // swap elements array[i] và array[j]
    // chúng ta sử dụng "destructuring assignment" syntax để achieve điều đó
    // bạn sẽ find more details về syntax đó trong các chapters sau
    // same có thể được viết như:
    // let t = array[i]; array[i] = array[j]; array[j] = t
    [array[i], array[j]] = [array[j], array[i]];
  }
}
```

Hãy test nó same way:

```
function shuffle(array) {
  for (let i = array.length - 1; i > 0; i--) {
    let j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
}

// counts của appearances cho tất cả possible permutations
let count = {
  '123': 0,
  '132': 0,
  '213': 0,
  '231': 0,
  '321': 0,
  '312': 0
};

for (let i = 0; i < 1000000; i++) {
  let array = [1, 2, 3];
  shuffle(array);
  count[array.join('')]++;
}

// show counts của tất cả possible permutations
for (let key in count) {
  alert(`${key}: ${count[key]}`);
}
```

Example output:

```
123: 166693
132: 166647
213: 166628
231: 167517
312: 166199
321: 166316
```

Looks good giờ. Tất cả permutations appear với same probability.

Cũng, performance-wise Fisher-Yates algorithm là much better, không có "sorting" overhead.

### [Get average age](#get-average-age)

mức độ quan trọng: 4

Viết function `getAverageAge(users)` mà gets một array của objects với property `age` và trả về average age.

Formula cho average là `(age1 + age2 + ... + ageN) / N`.

Ví例:

```
let john = { name: "John", age: 25 };
let pete = { name: "Pete", age: 30 };
let mary = { name: "Mary", age: 29 };

let arr = [ john, pete, mary ];

alert( getAverageAge(arr) ); // (25 + 30 + 29) / 3 = 28
```

lời giải

```
function getAverageAge(users) {
  return users.reduce((prev, user) => prev + user.age, 0) / users.length;
}

let john = { name: "John", age: 25 };
let pete = { name: "Pete", age: 30 };
let mary = { name: "Mary", age: 29 };

let arr = [ john, pete, mary ];

alert( getAverageAge(arr) ); // 28
```

### [Filter unique array members](#filter-unique-array-members)

mức độ quan trọng: 4

Hãy `arr` là một array.

Tạo function `unique(arr)` mà nên trả về một array với unique items của `arr`.

Ví例:

```
function unique(arr) {
  /* your code */
}

let strings = ["Hare", "Krishna", "Hare", "Krishna",
  "Krishna", "Krishna", "Hare", "Hare", ":-O"
];

alert( unique(strings) ); // Hare, Krishna, :-O
```

[Mở một sandbox với tests.](https://plnkr.co/edit/mFMUjLrwRvMtnn3X?p=preview)

lời giải

Hãy walk array items:

- Cho mỗi item chúng ta sẽ check nếu resulting array đã có item đó.
- Nếu vậy, sau đó ignore, ngược lại add đến results.

```
function unique(arr) {
  let result = [];

  for (let str of arr) {
    if (!result.includes(str)) {
      result.push(str);
    }
  }

  return result;
}

let strings = ["Hare", "Krishna", "Hare", "Krishna",
  "Krishna", "Krishna", "Hare", "Hare", ":-O"
];

alert( unique(strings) ); // Hare, Krishna, :-O
```

Code work, nhưng có một potential performance problem trong nó.

Method `result.includes(str)` internally walks array `result` và compares mỗi element chống lại `str` để find match.

Vì vậy nếu có `100` elements trong `result` và no one matches `str`, sau đó nó will walk whole `result` và do exactly `100` comparisons. Và nếu `result` là large, như `10000`, sau đó sẽ có `10000` comparisons.

Đó là không phải problem本身, vì JavaScript engines là very fast, vì vậy walk `10000` array là matter của microseconds.

Nhưng chúng ta do such test cho mỗi element của `arr`, trong `for` loop.

Vì vậy nếu `arr.length` là `10000` chúng ta sẽ có something like `10000*10000` = 100 millions của comparisons. Đó là a lot.

Vì vậy solution chỉ good cho small arrays.

Further trong chapter [Map và Set](/map-set) chúng ta sẽ see làm thế nào để optimize nó.

[Mở solution với tests trong một sandbox.](https://plnkr.co/edit/OzceFOlUD2uLSUkZ?p=preview)

### [Create keyed object từ array](#create-keyed-object-from-array)

mức độ quan trọng: 4

Hãy nói chúng ta received một array của users trong hình thức `{id:..., name:..., age:... }`.

Tạo function `groupById(arr)` mà creates một object từ nó, với `id` như key, và array items như values.

Ví例:

```
let users = [
  {id: 'john', name: "John Smith", age: 20},
  {id: 'ann', name: "Ann Smith", age: 24},
  {id: 'pete', name: "Pete Peterson", age: 31},
];

let usersById = groupById(users);

/*
// sau khi call chúng ta nên have:

usersById = {
  john: {id: 'john', name: "John Smith", age: 20},
  ann: {id: 'ann', name: "Ann Smith", age: 24},
  pete: {id: 'pete', name: "Pete Peterson", age: 31},
}
*/
```

Such function là really handy khi làm việc với server data.

Trong task này chúng ta assume rằng `id` là unique. Có thể có không có hai array items với cùng `id`.

Please sử dụng array `.reduce` method trong solution.

[Mở một sandbox với tests.](https://plnkr.co/edit/ShPqltMuCH00bAlM?p=preview)

lời giải

```
function groupById(array) {
  return array.reduce((obj, value) => {
    obj[value.id] = value;
    return obj;
  }, {})
}
```

[Mở solution với tests trong một sandbox.](https://plnkr.co/edit/PRYORtEl1Sm930JM?p=preview)
