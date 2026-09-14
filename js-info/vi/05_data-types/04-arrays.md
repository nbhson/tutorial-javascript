# Mảng (Arrays)

> Nguồn: [https://javascript.info/array](https://javascript.info/array)

<!-- fetched: 2026-09-14 -->

Objects cho phép bạn store keyed collections của values. Điều đó fine.

Nhưng quite often chúng ta find rằng chúng ta need một *ordered collection*, nơi chúng ta có một 1st, a 2nd, a 3rd element và vân vân. Ví例, chúng ta need cái đó để store một list của cái gì đó: users, goods, HTML elements v.v.

Không convenient để sử dụng một object ở đây, vì nó provides no methods để manage order của elements. Chúng ta không thể insert một new property "between" những existing ones. Objects đơn giản không meant cho such use.

Có một special data structure tên là `Array`, để store ordered collections.

## [Declaration](#declaration)

Có hai syntaxes cho creating một empty array:

```
let arr = new Array();
let arr = [];
```

Almost tất cả thời gian, second syntax được sử dụng. Chúng ta có thể supply initial elements trong brackets:

```
let fruits = ["Táo", "Cam", "Mơ"];
```

Array elements được numbered, bắt đầu từ zero.

Chúng ta có thể get một element bởi number của nó trong square brackets:

```
let fruits = ["Táo", "Cam", "Mơ"];

alert( fruits[0] ); // Táo
alert( fruits[1] ); // Cam
alert( fruits[2] ); // Mơ
```

Chúng ta có thể thay đổi một element:

```
fruits[2] = 'Lê'; // giờ ["Táo", "Cam", "Lê"]
```

…Hoặc thêm một new one vào array:

```
fruits[3] = 'Chanh'; // giờ ["Táo", "Cam", "Lê", "Chanh"]
```

Total count của các elements trong array là `length` của nó:

```
let fruits = ["Táo", "Cam", "Mơ"];

alert( fruits.length ); // 3
```

Chúng ta cũng có thể sử dụng `alert` để show whole array.

```
let fruits = ["Táo", "Cam", "Mơ"];

alert( fruits ); // Táo,Cam,Mơ
```

Một array có thể store các elements của bất kỳ type nào.

Ví例:

```
// mix của values
let arr = [ 'Táo', { name: 'John' }, true, function() { alert('Xin chào'); } ];

// get object tại index 1 và sau đó show name của nó
alert( arr[1].name ); // John

// get function tại index 3 và run nó
arr[3](); // Xin chào
```

Trailing comma

Một array, giống như một object, có thể end với逗号:

```
let fruits = [
  "Táo",
  "Cam",
  "Mơ",
];
```

"Trailing comma" style makes it easier để insert/remove items, vì tất cả các dòng trở nên alike.

## [Get last elements với "at"](#get-last-elements-with-at)

Một recent addition

Đây là một recent addition cho language.
Các browsers cũ có thể cần [polyfills](https://javascript.info/polyfills).

Hãy nói chúng ta muốn last element của array.

Một số programming languages cho phép sử dụng negative indexes cho cùng purpose, như `fruits[-1]`.

Tuy nhiên, trong JavaScript nó không work. Result sẽ là `undefined`, vì index trong square brackets được treat literally.

Chúng ta có thể explicitly calculate last element index và sau đó access nó: `fruits[fruits.length - 1]`.

```
let fruits = ["Táo", "Cam", "Mơ"];

alert( fruits[fruits.length-1] ); // Mơ
```

Hơi cumbersome, phải không? Chúng ta cần để viết variable name hai lần.

Glücklicherweise, có một shorter syntax: `fruits.at(-1)`:

```
let fruits = ["Táo", "Cam", "Mơ"];

// same như fruits[fruits.length-1]
alert( fruits.at(-1) ); // Mơ
```

Nói cách khác, `arr.at(i)`:
- exactly same như `arr[i]`, nếu `i >= 0`.
- cho các negative values của `i`, nó steps back từ end của array.

## [Methods pop/push, shift/unshift](#methods-pop-push-shift-unshift)

Một [queue](https://en.wikipedia.org/wiki/Queue_(abstract_data_type)) là một trong những most common uses của một array. Trong computer science, điều đó mean một ordered collection của elements mà supports hai operations:

- `push` appends một element đến end.
- `shift` get một element từ beginning, advancing queue, vì vậy 2nd element trở thành 1st.

![](/article/array/queue.svg)

Arrays supports cả hai operations.

Trong thực tế chúng ta need nó rất often. Ví例, một queue của messages mà need để shown trên màn hình.

Có một另一个 use case cho arrays – data structure tên là [stack](https://en.wikipedia.org/wiki/Stack_(abstract_data_type)).

Nó supports hai operations:

- `push` adds một element đến end.
- `pop` takes một element từ end.

Vì vậy new elements được added hoặc taken luôn luôn từ "end".

Stack được illustrated như một pack của cards: new cards được added đến top hoặc taken từ top:

![](/article/array/stack.svg)

Cho stacks, latest pushed item được received first, đó cũng được gọi là LIFO (Last-In-First-Out) principle. Cho queues, chúng ta có FIFO (First-In-First-Out).

Arrays trong JavaScript có thể work cả như một queue và như một stack. Chúng allow bạn để add/remove elements, cả đến/from beginning hoặc end.

Trong computer science, data structure mà allows điều đó, được gọi là [deque](https://en.wikipedia.org/wiki/Double-ended_queue).

**Methods mà work với end của array:**

`pop`
:   Extract last element của array và trả về nó:

    ```
    let fruits = ["Táo", "Cam", "Lê"];

    alert( fruits.pop() ); // remove "Lê" và alert nó

    alert( fruits ); // Táo, Cam
    ```

    Cả `fruits.pop()` và `fruits.at(-1)` trả về last element của array, nhưng `fruits.pop()` cũng modifies array bằng cách remove nó.

`push`
:   Append element đến end của array:

    ```
    let fruits = ["Táo", "Cam"];

    fruits.push("Lê");

    alert( fruits ); // Táo, Cam, Lê
    ```

    Call `fruits.push(...)` là equal đến `fruits[fruits.length] = ...`.

**Methods mà work với beginning của array:**

`shift`
:   Extract first element của array và trả về nó:

    ```
    let fruits = ["Táo", "Cam", "Lê"];

    alert( fruits.shift() ); // remove Táo và alert nó

    alert( fruits ); // Cam, Lê
    ```

`unshift`
:   Add element đến beginning của array:

    ```
    let fruits = ["Cam", "Lê"];

    fruits.unshift('Táo');

    alert( fruits ); // Táo, Cam, Lê
    ```

Methods `push` và `unshift` có thể add nhiều elements tại một time:

```
let fruits = ["Táo"];

fruits.push("Cam", "Lê");
fruits.unshift("Dứa", "Chanh");

// ["Dứa", "Chanh", "Táo", "Cam", "Lê"]
alert( fruits );
```

## [Internals](#internals)

Một array là một special kind của object. Square brackets được sử dụng để access một property `arr[0]` thực sự đến từ object syntax. Đó essentially là same như `obj[key]`, nơi `arr` là object, trong khi numbers được sử dụng như keys.

Chúng extend objects providing special methods để work với ordered collections của data và cũng `length` property. Nhưng at the core nó vẫn là object.

Remember, có only eight basic data types trong JavaScript (xem [Data types](/types) chapter để biết thêm info). Array là một object và vì vậy behave như một object.

Ví例, nó được copied by reference:

```
let fruits = ["Chuối"]

let arr = fruits; // copy by reference (hai variables reference cùng array)

alert( arr === fruits ); // true

arr.push("Lê"); // modify array by reference

alert( fruits ); // Chuối, Lê - 2 items giờ
```

…Nhưng cái làm arrays really special là internal representation. Engine tries để store elements của nó trong contiguous memory area, một sau另一个, như được depicted trên illustrations trong chương này, và có other optimizations cũng, để make arrays work really fast.

Nhưng chúng all break nếu chúng ta quit work với một array như với "ordered collection" và start work với nó như là nó were một regular object.

Ví例, về mặt kỹ thuật chúng ta có thể làm cái này:

```
let fruits = []; // make một array

fruits[99999] = 5; // assign một property với index far greater hơn length

fruits.age = 25; // create một property với arbitrary name
```

Điều đó là possible, vì arrays là objects at their base. Chúng ta có thể add bất kỳ properties đến chúng.

Nhưng engine sẽ see rằng chúng ta đang work với array như với một regular object. Array-specific optimizations are not suited cho such cases và sẽ được turned off, benefits của chúng disappear.

Các ways để misuse một array:

- Add một non-numeric property như `arr.test = 5`.
- Make holes, như: add `arr[0]` và sau đó `arr[1000]` (và không có gì giữa chúng).
- Fill array trong reverse order, như `arr[1000]`, `arr[999]` và vân vân.

Hãy think của arrays như special structures để work với *ordered data*. Chúng provide special methods cho điều đó. Arrays được carefully tuned inside JavaScript engines để work với contiguous ordered data, please use them theo cách đó. Và nếu bạn need arbitrary keys, chances là high rằng bạn thực sự require một regular object `{}`.

## [Performance](#performance)

Methods `push/pop` chạy fast, trong khi `shift/unshift` là slow.

![](/article/array/array-speed.svg)

Tại sao nó fast hơn để work với end của một array hơn là beginning? Hãy xem những gì happening trong quá trình execution:

```
fruits.shift(); // take 1 element từ beginning
```

Không đủ để take và remove element với index `0`. Các elements khác cần để được renumbered cũng.

`shift` operation must do 3 things:

1. Remove element với index `0`.
2. Move tất cả elements sang trái, renumber chúng từ index `1` đến `0`, từ `2` đến `1` và vân vân.
3. Update `length` property.

![](/article/array/array-shift.svg)

**Càng nhiều elements trong array, càng nhiều time để move them, more in-memory operations.**

Similar thing happens với `unshift`: để add một element đến beginning của array, chúng ta cần trước tiên move existing elements sang phải, increasing их indexes.

Và còn `push/pop` thì sao? Chúng không need để move anything. Để extract một element từ end, `pop` method cleans index và shortens `length`.

Các actions cho `pop` operation:

```
fruits.pop(); // take 1 element từ end
```

![](/article/array/array-pop.svg)

**`pop` method không need để move anything, vì các elements khác giữ nguyên indexes của chúng. Đó là lý do tại sao nó blazingly fast.**

Similar thing với `push` method.

## [Loops](#loops)

Một trong những oldest ways để cycle array items là `for` loop qua indexes:

```
let arr = ["Táo", "Cam", "Lê"];

for (let i = 0; i < arr.length; i++) {
  alert( arr[i] );
}
```

Nhưng cho arrays có một another form của loop, `for..of`:

```
let fruits = ["Táo", "Cam", "Mơ"];

// iterates qua array elements
for (let fruit of fruits) {
  alert( fruit );
}
```

`for..of` không give access đến number của current element, chỉ value của nó, nhưng trong hầu hết các cases điều đó là enough. Và nó shorter.

Về mặt kỹ thuật, vì arrays là objects, nó cũng possible để sử dụng `for..in`:

```
let arr = ["Táo", "Cam", "Lê"];

for (let key in arr) {
  alert( arr[key] ); // Táo, Cam, Lê
}
```

Nhưng thực tế đó là một bad idea. Có potential problems với nó:

1. Loop `for..in` iterates qua *tất cả properties*, không chỉ numeric ones.

   Có所谓的 "array-like" objects trong browser và trong other environments, mà *look like arrays*. Tức là, chúng có `length` và indexes properties, nhưng chúng có thể cũng có其他 non-numeric properties và methods, mà chúng ta thường không need. `for..in` loop sẽ liệt kê them though. Vì vậy nếu chúng ta need để work với array-like objects, sau đó những "extra" properties có thể become một problem.
2. `for..in` loop được optimized cho generic objects, không phải arrays, và do đó là 10-100 times slower. Tất nhiên, nó vẫn very fast. Speedup có thể only matter trong bottlenecks. Nhưng vẫn chúng ta nên aware của difference.

Nói chung, chúng ta không nên sử dụng `for..in` cho arrays.

## [Một word về "length"](#a-word-about-length)

`length` property tự động updates khi chúng ta modify array. Để precise hơn, nó thực sự không phải là count của values trong array, nhưng greatest numeric index plus one.

Ví例, một single element với một large index gives một big length:

```
let fruits = [];
fruits[123] = "Táo";

alert( fruits.length ); // 124
```

Note rằng chúng ta thường không sử dụng arrays như vậy.

Một interesting thing khác về `length` property là nó's writable.

Nếu chúng ta tăng nó manually, không có gì interesting happens. Nhưng nếu chúng ta giảm nó, array được truncated. Process là irreversible, đây là ví例:

```
let arr = [1, 2, 3, 4, 5];

arr.length = 2; // truncate to 2 elements
alert( arr ); // [1, 2]

arr.length = 5; // return length back
alert( arr[3] ); // undefined: values không return
```

Vì vậy, simplest way để clear array là: `arr.length = 0;`.

## [new Array()](#new-array)

Có một another syntax để create một array:

```
let arr = new Array("Táo", "Cam", "v.v.");
```

Nó rarely được sử dụng, vì square brackets `[]` ngắn hơn. Cũng có một tricky feature với nó.

Nếu `new Array` được called với một single argument mà là một number, sau đó nó creates một array *không có items, nhưng với given length*.

Hãy xem một người có thể shoot themselves trong foot như thế nào:

```
let arr = new Array(2); // sẽ create một array của [2] ?

alert( arr[0] ); // undefined! không có elements.

alert( arr.length ); // length 2
```

Để tránh such surprises, chúng ta thường sử dụng square brackets, trừ khi chúng ta thực sự biết những gì chúng ta đang làm.

## [Multidimensional arrays](#multidimensional-arrays)

Arrays có thể có items mà cũng là arrays. Chúng ta có thể sử dụng nó cho multidimensional arrays, ví例 để store matrices:

```
let matrix = [
  [1, 2, 3],
  [4, 5, 6],
  [7, 8, 9]
];

alert( matrix[0][1] ); // 2, second value của first inner array
```

## [toString](#tostring)

Arrays có implementation riêng của `toString` method mà trả về một comma-separated list của elements.

Ví例:

```
let arr = [1, 2, 3];

alert( arr ); // 1,2,3
alert( String(arr) === '1,2,3' ); // true
```

Cũng, hãy thử cái này:

```
alert( [] + 1 ); // "1"
alert( [1] + 1 ); // "11"
alert( [1,2] + 1 ); // "1,21"
```

Arrays không có `Symbol.toPrimitive`, neither một viable `valueOf`, chúng implement only `toString` conversion, vì vậy ở đây `[]` becomes một empty string, `[1]` becomes `"1"` và `[1,2]` becomes `"1,2"`.

Khi binary plus `"+"` operator adds something đến một string, nó converts nó sang một string cũng, vì vậy next step看起来 như thế này:

```
alert( "" + 1 ); // "1"
alert( "1" + 1 ); // "11"
alert( "1,2" + 1 ); // "1,21"
```

## [Don't compare arrays với `==`](#don-t-compare-arrays-with)

Arrays trong JavaScript, khác với một số otros programming languages, không nên được compare với operator `==`.

Operator này không có special treatment cho arrays, nó work với chúng như với bất kỳ objects nào.

Hãy recall các rules:

- Hai objects là equal `==` chỉ khi chúng là references đến cùng object.
- Nếu một trong số arguments của `==` là một object, và một cái kia là một primitive, sau đó object được converted đến primitive, như được giải thích trong chương [Object to primitive conversion](/object-toprimitive).
- …Với exception của `null` và `undefined` mà equal `==` nhau và không bằng bất kỳ thing nào khác.

Strict comparison `===` còn simpler hơn, vì nó không convert types.

Vì vậy, nếu chúng ta compare arrays với `==`, chúng không bao giờ same, trừ khi chúng ta compare hai variables mà references exactly cùng array.

Ví例:

```
alert( [] == [] ); // false
alert( [0] == [0] ); // false
```

These arrays là technically different objects. Vì vậy chúng không equal. `==` operator không làm item-by-item comparison.

Comparison với primitives có thể give seemingly strange results cũng:

```
alert( 0 == [] ); // true

alert('0' == [] ); // false
```

Ở đây, trong cả hai cases, chúng ta compare một primitive với một array object. Vì vậy array `[]` được converted đến primitive cho purpose của comparison và becomes một empty string `''`.

Sau đó comparison process goes on với các primitives, như được described trong chương [Type Conversions](/type-conversions):

```
// sau khi [] được converted đến ''
alert( 0 == '' ); // true, vì '' được converted đến number 0

alert('0' == '' ); // false, không có type conversion, different strings
```

Vì vậy, làm thế nào để compare arrays?

Đơn giản: không sử dụng `==` operator. Thay vào đó, compare chúng item-by-item trong một loop hoặc sử dụng iteration methods được giải thích trong chương sau.

## [Tổng kết](#summary)

Array là một special kind của object, suited để store và manage ordered data items.

Declaration:

```
// square brackets (usual)
let arr = [item1, item2...];

// new Array (exceptionally rare)
let arr = new Array(item1, item2...);
```

Call đến `new Array(number)` creates một array với given length, nhưng không có elements.

- `length` property là array length hoặc, để precise hơn, last numeric index plus one. Nó được auto-adjusted bởi array methods.
- Nếu chúng ta shorten `length` manually, array được truncated.

Getting elements:

- we có thể get element bởi index, như `arr[0]`
- cũng chúng ta có thể sử dụng `at(i)` method mà allows negative indexes. Cho negative values của `i`, nó steps back từ end của array. Nếu `i >= 0`, nó work same như `arr[i]`.

Chúng ta có thể sử dụng một array như một deque với các operations sau:

- `push(...items)` adds `items` đến end.
- `pop()` removes element từ end và trả về nó.
- `shift()` removes element từ beginning và trả về nó.
- `unshift(...items)` adds `items` đến beginning.

Để loop qua elements của array:

- `for (let i=0; i<arr.length; i++)` – works fastest, old-browser-compatible.
- `for (let item of arr)` – modern syntax cho items only,
- `for (let i in arr)` – không bao giờ sử dụng.

Để compare arrays, không sử dụng `==` operator (cũng như `>`, `<` và others), vì chúng không có special treatment cho arrays. Chúng handle chúng như bất kỳ objects nào, và đó không phải những gì chúng ta thường muốn.

Thay vào đó bạn có thể sử dụng `for..of` loop để compare arrays item-by-item.

Chúng ta sẽ continue với arrays và study more methods để add, remove, extract elements và sort arrays trong chương sau [Array methods](/array-methods).

---

---

## Các bài tập

## [Các bài tập](#tasks)

### [Is array copied?](#is-array-copied)

mức độ quan trọng: 3

Đây là result sẽ là gì?

```
let fruits = ["Táo", "Quýt", "Chanh"];

// push một new value vào "copy"
let shoppingCart = fruits;
shoppingCart.push("Chuối");

// what's in fruits?
alert( fruits.length ); // ?
```

lời giải

Result là `4`:

```
let fruits = ["Táo", "Quýt", "Chanh"];

let shoppingCart = fruits;

shoppingCart.push("Chuối");

alert( fruits.length ); // 4
```

Đó là vì arrays là objects. Vì vậy cả `shoppingCart` và `fruits` là references đến cùng array.

### [Array operations.](#array-operations)

mức độ quan trọng: 5

Hãy thử 5 array operations.

1. Create một array `styles` với items "Jazz" và "Blues".
2. Append "Rock-n-Roll" đến end.
3. Replace value trong middle với "Classics". Code của bạn cho finding middle value nên work cho bất kỳ arrays với odd length.
4. Strip off first element của array và show nó.
5. Prepend `Rap` và `Reggae` đến array.

Array trong quá trình:

```
Jazz, Blues
Jazz, Blues, Rock-n-Roll
Jazz, Classics, Rock-n-Roll
Classics, Rock-n-Roll
Rap, Reggae, Classics, Rock-n-Roll
```

lời giải

```
let styles = ["Jazz", "Blues"];
styles.push("Rock-n-Roll");
styles[Math.floor((styles.length - 1) / 2)] = "Classics";
alert( styles.shift() );
styles.unshift("Rap", "Reggae");
```

### [Calling trong một array context](#calling-in-an-array-context)

mức độ quan trọng: 5

Result là gì? Tại sao?

```
let arr = ["a", "b"];

arr.push(function() {
  alert( this );
});

arr[2](); // ?
```

lời giải

Call `arr[2]()` là syntactically good old `obj[method]()`, trong role của `obj` chúng ta có `arr`, và trong role của `method` chúng ta có `2`.

Vì vậy chúng ta có một call của function `arr[2]` như một object method. Naturally, nó receives `this` referencing object `arr` và outputs array:

```
let arr = ["a", "b"];

arr.push(function() {
  alert( this );
})

arr[2](); // a,b,function(){...}
```

Array có 3 values: initially nó có hai, plus function.

### [Sum input numbers](#sum-input-numbers)

mức độ quan trọng: 4

Viết function `sumInput()` mà:

- Hỏi user cho values sử dụng `prompt` và stores values trong array.
- Finishes asking khi user enter một non-numeric value, một empty string, hoặc nhấn "Cancel".
- Calculates và returns sum của array items.

P.S. Một zero `0` là một valid number, please không stop input trên zero.

[Chạy demo](#)

lời giải

Please note subtle, nhưng important detail của solution. Chúng ta không convert `value` sang number instantly sau `prompt`, vì sau `value = +value` chúng ta sẽ không thể tell một empty string (stop sign) từ zero (valid number). Chúng ta làm nó sau đó thay vì.

```
function sumInput() {

  let numbers = [];

  while (true) {

    let value = prompt("Một số please?", 0);

    // should we cancel?
    if (value === "" || value === null || !isFinite(value)) break;

    numbers.push(+value);
  }

  let sum = 0;
  for (let number of numbers) {
    sum += number;
  }
  return sum;
}

alert( sumInput() );
```

### [Một maximal subarray](#a-maximal-subarray)

mức độ quan trọng: 2

Input là một array của numbers, ví例 `arr = [1, -2, 3, 4, -9, 6]`.

Task là: find contiguous subarray của `arr` với maximal sum của items.

Viết function `getMaxSubSum(arr)` mà sẽ trả về sum đó.

Ví例:

```
getMaxSubSum([-1, 2, 3, -9]) == 5 (sum của highlighted items)
getMaxSubSum([2, -1, 2, 3, -9]) == 6
getMaxSubSum([-1, 2, 3, -9, 11]) == 11
getMaxSubSum([-2, -1, 1, 2]) == 3
getMaxSubSum([100, -9, 2, -3, 5]) == 100
getMaxSubSum([1, 2, 3]) == 6 (take all)
```

Nếu tất cả items là negative, điều đó mean rằng chúng ta take none (subarray là empty), vì vậy sum là zero:

```
getMaxSubSum([-1, -2, -3]) = 0
```

Hãy try để think của một fast solution: [O(n2)](https://en.wikipedia.org/wiki/Big_O_notation) hoặc thậm chí O(n) nếu bạn có thể.

[Mở một sandbox với tests.](https://plnkr.co/edit/39Z6ipw79WjiEIVP?p=preview)

lời giải

Slow solution

#### Slow solution

Chúng ta có thể calculate tất cả possible subsums.

Simplest way là để take every element và calculate sums của tất cả subarrays bắt đầu từ nó.

Ví例 cho `[-1, 2, 3, -9, 11]`:

```
// Bắt đầu từ -1:
-1
-1 + 2
-1 + 2 + 3
-1 + 2 + 3 + (-9)
-1 + 2 + 3 + (-9) + 11

// Bắt đầu từ 2:
2
2 + 3
2 + 3 + (-9)
2 + 3 + (-9) + 11

// Bắt đầu từ 3:
3
3 + (-9)
3 + (-9) + 11

// Bắt đầu từ -9
-9
-9 + 11

// Bắt đầu từ 11
11
```

Code thực sự là một nested loop: external loop qua array elements, và internal counts subsums bắt đầu với current element.

```
function getMaxSubSum(arr) {
  let maxSum = 0; // nếu chúng ta take no elements, zero sẽ được returned

  for (let i = 0; i < arr.length; i++) {
    let sumFixedStart = 0;
    for (let j = i; j < arr.length; j++) {
      sumFixedStart += arr[j];
      maxSum = Math.max(maxSum, sumFixedStart);
    }
  }

  return maxSum;
}

alert( getMaxSubSum([-1, 2, 3, -9]) ); // 5
alert( getMaxSubSum([-1, 2, 3, -9, 11]) ); // 11
alert( getMaxSubSum([-2, -1, 1, 2]) ); // 3
alert( getMaxSubSum([1, 2, 3]) ); // 6
alert( getMaxSubSum([100, -9, 2, -3, 5]) ); // 100
```

Solution có một time complexity của [O(n2)](https://en.wikipedia.org/wiki/Big_O_notation). Nói cách khác, nếu chúng ta increase array size 2 times, algorithm sẽ work 4 times longer.

Cho big arrays (1000, 10000 hoặc nhiều hơn items) such algorithms có thể lead đến serious sluggishness.

Fast solution

#### Fast solution

Hãy walk array và keep current partial sum của elements trong variable `s`. Nếu `s` becomes negative tại một point, sau đó assign `s=0`. Maximum của tất cả các `s` đó sẽ là answer.

Nếu description là too vague, please see code, nó ngắn enough:

```
function getMaxSubSum(arr) {
  let maxSum = 0;
  let partialSum = 0;

  for (let item of arr) { // cho mỗi item của arr
    partialSum += item; // add nó vào partialSum
    maxSum = Math.max(maxSum, partialSum); // remember maximum
    if (partialSum < 0) partialSum = 0; // zero nếu negative
  }

  return maxSum;
}

alert( getMaxSubSum([-1, 2, 3, -9]) ); // 5
alert( getMaxSubSum([-1, 2, 3, -9, 11]) ); // 11
alert( getMaxSubSum([-2, -1, 1, 2]) ); // 3
alert( getMaxSubSum([100, -9, 2, -3, 5]) ); // 100
alert( getMaxSubSum([1, 2, 3]) ); // 6
alert( getMaxSubSum([-1, -2, -3]) ); // 0
```

Algorithm requires exactly 1 array pass, vì vậy time complexity là O(n).

Bạn có thể find more detailed information về algorithm ở đây: [Maximum subarray problem](http://en.wikipedia.org/wiki/Maximum_subarray_problem). Nếu nó vẫn không obvious tại sao điều đó work, sau đó please trace algorithm trên các ví例 ở trên, see how nó work, điều đó tốt hơn bất kỳ words nào.

[Mở solution với tests trong một sandbox.](https://plnkr.co/edit/aAxNECP2CQce5mkf?p=preview)
