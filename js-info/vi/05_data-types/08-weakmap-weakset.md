# WeakMap và WeakSet

> Nguồn: [https://javascript.info/weakmap-weakset](https://javascript.info/weakmap-weakset)

<!-- fetched: 2026-09-14 -->

Như chúng ta biết từ chương [Garbage collection](/garbage-collection), JavaScript engine giữ một value trong bộ nhớ trong khi nó là "reachable" và có thể được used.

Ví例:

```
let john = { name: "John" };

// object có thể được accessed, john là reference đến nó

// overwrite reference
john = null;

// object sẽ được removed từ bộ nhớ
```

Thông thường, properties của một object hoặc elements của một array hoặc another data structure được considered reachable và kept trong bộ nhớ trong khi data structure đó tồn tại.

Ví例, nếu chúng ta put một object vào một array, sau đó trong khi array còn sống, object sẽ alive như vậy, ngay cả khi không có其他 references đến nó.

Như thế này:

```
let john = { name: "John" };

let array = [ john ];

john = null; // overwrite reference

// object trước đó referenced bởi john được stored bên trong array
// vì vậy nó sẽ không được garbage-collected
// chúng ta có thể get nó như array[0]
```

Tương tự, nếu chúng ta sử dụng một object như key trong một regular `Map`, sau đó trong khi `Map` tồn tại, object đó tồn tại như vậy. Nó occupying memory và có thể không được garbage collected.

Ví例:

```
let john = { name: "John" };

let map = new Map();
map.set(john, "...");

john = null; // overwrite reference

// john được stored bên trong map,
// chúng ta có thể get nó bằng cách sử dụng map.keys()
```

[`WeakMap`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/WeakMap) fundamentally different trong khía cạnh này. Nó không prevent garbage-collection của key objects.

Hãy xem điều đó mean gì trên examples.

## [WeakMap](#weakmap)

Difference đầu tiên giữa [`Map`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map) và [`WeakMap`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/WeakMap) là keys phải là objects, không phải primitive values:

```
let weakMap = new WeakMap();

let obj = {};

weakMap.set(obj, "ok"); // work fine (object key)

// không thể sử dụng một string như key
weakMap.set("test", "Whoops"); // Error, vì "test" không phải là object
```

Giờ, nếu chúng ta sử dụng một object như key trong nó, và không có其他 references đến object đó – nó sẽ được removed từ bộ nhớ (và từ map) tự động.

```
let john = { name: "John" };

let weakMap = new WeakMap();
weakMap.set(john, "...");

john = null; // overwrite reference

// john được removed từ bộ nhớ!
```

So sánh nó với regular `Map` example ở trên. Giờ nếu `john` chỉ tồn tại như key của `WeakMap` – nó sẽ tự động được deleted từ map (và bộ nhớ).

`WeakMap` không support iteration và methods `keys()`, `values()`, `entries()`, vì vậy không có way để get tất cả keys hoặc values từ nó.

`WeakMap` có только following methods:

- [`weakMap.set(key, value)`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/WeakMap/set)
- [`weakMap.get(key)`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/WeakMap/get)
- [`weakMap.delete(key)`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/WeakMap/delete)
- [`weakMap.has(key)`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/WeakMap/has)

Tại sao limitation như vậy? Đó là vì technical reasons. Nếu object đã lost all other references (như `john` trong code ở trên), sau đó nó sẽ được garbage-collected tự động. Nhưng technically nó không exactly được specified *khi cleanup happens*.

JavaScript engine decides điều đó. Nó có thể choose để perform memory cleanup ngay lập tức hoặc để wait và làm cleaning sau đó khi more deletions xảy ra. Về mặt kỹ thuật, current element count của một `WeakMap` không được know. Engine có thể đã cleaned nó hoặc không, hoặc đã làm nó partially. Cho lý do đó, methods mà access tất cả keys/values không được support.

Giờ, chúng ta cần một data structure như vậy ở đâu?

## [Use case: additional data](#use-case-additional-data)

Main area của application cho `WeakMap` là *additional data storage*.

Nếu chúng ta đang làm việc với một object mà "thuộc về" another code, có thể là một third-party library, và muốn store một số data associated với nó, chỉ tồn tại trong khi object còn sống – sau đó `WeakMap` là exactly những gì được needed.

Chúng ta put data vào một `WeakMap`, sử dụng object như key, và khi object được garbage collected, data đó sẽ tự động disappear.

```
weakMap.set(john, "secret documents");
// nếu john die, secret documents sẽ bị destroyed tự động
```

Hãy xem một ví例.

Ví例, chúng ta có code mà giữ một visit count cho users. Information được stored trong một map: một user object là key và visit count là value. Khi một user leaves (object của nó được garbage collected), chúng ta không muốn store visit count của họ nữa.

Đây là một ví例 của counting function với `Map`:

```
// 📁 visitsCount.js
let visitsCountMap = new Map(); // map: user => visits count

// increase visits count
function countUser(user) {
  let count = visitsCountMap.get(user) || 0;
  visitsCountMap.set(user, count + 1);
}
```

Và đây là another part của code, có thể một file khác sử dụng nó:

```
// 📁 main.js
let john = { name: "John" };

countUser(john); // count visits của anh ấy

// sau đó john leaves chúng ta
john = null;
```

Giờ, `john` object nên được garbage collected, nhưng remains trong memory, vì nó là key trong `visitsCountMap`.

Chúng ta cần để clean `visitsCountMap` khi chúng ta remove users, nếu không nó sẽ grow trong memory indefinitely. Such cleaning có thể become một tedious task trong các kiến trúc phức tạp.

Chúng ta có thể avoid nó bằng cách switch sang `WeakMap` thay vì:

```
// 📁 visitsCount.js
let visitsCountMap = new WeakMap(); // weakmap: user => visits count

// increase visits count
function countUser(user) {
  let count = visitsCountMap.get(user) || 0;
  visitsCountMap.set(user, count + 1);
}
```

Giờ chúng ta không cần để clean `visitsCountMap`. Sau khi `john` object become unreachable, bằng mọi cách ngoại trừ như một key của `WeakMap`, nó được removed từ bộ nhớ, cùng với information bởi key đó từ `WeakMap`.

## [Use case: caching](#use-case-caching)

Một另一个 common ví例 là caching. Chúng ta có thể store ("cache") results từ một function, vì vậy future calls trên cùng object có thể reuse nó.

Để achieve điều đó, chúng ta có thể sử dụng `Map` (không optimal scenario):

```
// 📁 cache.js
let cache = new Map();

// calculate và remember result
function process(obj) {
  if (!cache.has(obj)) {
    let result = /* calculations của result cho */ obj;

    cache.set(obj, result);
    return result;
  }

  return cache.get(obj);
}

// Giờ chúng ta sử dụng process() trong một file khác:

// 📁 main.js
let obj = {/* giả sử chúng ta có một object */};

let result1 = process(obj); // calculated

// ...sau đó, từ một chỗ khác của code...
let result2 = process(obj); // remembered result taken từ cache

// ...sau đó, khi object không cần thiết nữa:
obj = null;

alert(cache.size); // 1 (Ouch! Object vẫn trong cache, taking memory!)
```

Cho multiple calls của `process(obj)` với cùng object, nó chỉ calculate result lần đầu tiên, và sau đó just take nó từ `cache`. Nhược điểm là chúng ta cần để clean `cache` khi object không cần thiết nữa.

Nếu chúng ta replace `Map` với `WeakMap`, sau đó problem này disappears. Cached result sẽ được removed từ bộ nhớ tự động sau khi object được garbage collected.

```
// 📁 cache.js
let cache = new WeakMap();

// calculate và remember result
function process(obj) {
  if (!cache.has(obj)) {
    let result = /* calculate result cho */ obj;

    cache.set(obj, result);
    return result;
  }

  return cache.get(obj);
}

// 📁 main.js
let obj = {/* một object nào đó */};

let result1 = process(obj);
let result2 = process(obj);

// ...sau đó, khi object không cần thiết nữa:
obj = null;

// Không thể get cache.size, vì nó là WeakMap,
// nhưng nó là 0 hoặc soon sẽ là 0
// Khi obj được garbage collected, cached data sẽ được removed
```

## [WeakSet](#weakset)

[`WeakSet`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/WeakSet) behave similarly:

- Nó là analogous đến `Set`, nhưng chúng ta chỉ có thể add objects đến `WeakSet` (không phải primitives).
- Một object tồn tại trong set trong khi nó reachable từ một chỗ khác.
- Giống như `Set`, nó支持 [`add`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Weakset/add), [`has`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Weakset/has) và [`delete`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Weakset/delete), nhưng không có `size`, `keys()` và không có iterations.

Being "weak", nó cũng serve như additional storage. Nhưng không phải cho arbitrary data, rather cho "yes/no" facts. Một membership trong `WeakSet` có thể mean một cái gì đó về object.

Ví例, chúng ta có thể add users đến `WeakSet` để keep track của những ai đã visited site của chúng ta:

```
let visitedSet = new WeakSet();

let john = { name: "John" };
let pete = { name: "Pete" };
let mary = { name: "Mary" };

visitedSet.add(john); // John đã visited chúng ta
visitedSet.add(pete); // Sau đó Pete
visitedSet.add(john); // John một lần nữa

// visitedSet có 2 users giờ

// check nếu John đã visited?
alert(visitedSet.has(john)); // true

// check nếu Mary đã visited?
alert(visitedSet.has(mary)); // false

john = null;

// visitedSet sẽ được cleaned tự động
```

Limitation notable nhất của `WeakMap` và `WeakSet` là absence của iterations, và inability để get tất cả current content. Điều đó có thể看起来 inconvenient, nhưng không prevent `WeakMap/WeakSet` khỏi doing main job – be một "additional" storage của data cho objects mà được stored/managed tại một chỗ khác.

## [Tổng kết](#summary)

[`WeakMap`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/WeakMap) là `Map`-like collection mà allows only objects như keys và removes chúng cùng với associated value một khi chúng become inaccessible bởi các其他方式.

[`WeakSet`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/WeakSet) là `Set`-like collection mà chỉ store objects và removes chúng một khi chúng become inaccessible bởi các其他方式.

Main advantages là họ có weak reference đến objects, vì vậy chúng có thể được removed dễ dàng bởi garbage collector.

Điều đó đi kèm với cost của không có support cho `clear`, `size`, `keys`, `values`…

`WeakMap` và `WeakSet` được sử dụng như "secondary" data structures trong addition đến "primary" object storage. Một khi object được removed từ primary storage, nếu nó chỉ được found như key của `WeakMap` hoặc trong một `WeakSet`, nó sẽ được cleaned up tự động.

---

---

## Các bài tập

## [Các bài tập](#tasks)

### [Store "unread" flags](#store-unread-flags)

mức độ quan trọng: 5

Có một array của messages:

```
let messages = [
  {text: "Hello", from: "John"},
  {text: "How goes?", from: "John"},
  {text: "See you soon", from: "Alice"}
];
```

Code của bạn có thể access nó, nhưng messages được managed bởi code của người khác. New messages được thêm, old ones được removed thường xuyên bởi code đó, và bạn không know exact moments khi điều đó xảy ra.

Giờ, cấu trúc data nào bạn có thể sử dụng để store information về whether message "đã được đọc"? Structure phải well-suited để give answer "đã được đọc chưa?" cho given message object.

P.S. Khi message được removed từ `messages`, nó nên disappear từ structure của bạn cũng.

P.P.S. Chúng ta không nên modify message objects, add properties của chúng ta vào chúng. Vì chúng được managed bởi code của người khác, điều đó có thể lead đến bad consequences.

lời giải

Hãy store read messages trong `WeakSet`:

```
let messages = [
  {text: "Hello", from: "John"},
  {text: "How goes?", from: "John"},
  {text: "See you soon", from: "Alice"}
];

let readMessages = new WeakSet();

// hai messages đã được read
readMessages.add(messages[0]);
readMessages.add(messages[1]);
// readMessages có 2 elements

// ...hãy đọc lại first message!
readMessages.add(messages[0]);
// readMessages vẫn có 2 unique elements

// answer: message[0] đã được read chưa?
alert("Read message 0: " + readMessages.has(messages[0])); // true

messages.shift();
// giờ readMessages có 1 element (technically memory có thể được cleaned sau)
```

`WeakSet` cho phép lưu trữ một set của messages và dễ dàng check cho existence của một message trong nó.

Nó cleans up本身 tự động. Tradeoff là chúng ta không thể iterate qua nó, không thể get "all read messages" từ nó trực tiếp. Nhưng chúng ta có thể làm điều đó bằng cách iterating qua tất cả messages và filtering những mà trong set.

Một另一个, different solution có thể là để add một property như `message.isRead=true` đến một message sau khi nó được read. Như message objects được managed bởi another code, điều đó nói chung discouraged, nhưng chúng ta có thể sử dụng một symbolic property để avoid conflicts.

Như thế này:

```
// symbolic property chỉ được known bởi code của chúng ta
let isRead = Symbol("isRead");
messages[0][isRead] = true;
```

Giờ third-party code có lẽ sẽ không see extra property của chúng ta.

Mặc dù symbols cho phép để降低 probability của problems, sử dụng `WeakSet` là better từ architectural point của view.

### [Store read dates](#store-read-dates)

mức độ quan trọng: 5

Có một array của messages như trong [previous task](/task/recipients-read). Situation là tương tự.

```
let messages = [
  {text: "Hello", from: "John"},
  {text: "How goes?", from: "John"},
  {text: "See you soon", from: "Alice"}
];
```

Question giờ là: cấu trúc data nào bạn sẽ đề xuất để store information: "khi message được read?".

Trong previous task chúng ta chỉ need để store "yes/no" fact. Giờ chúng ta cần để store date, và nó chỉ nên remain trong memory cho đến khi message được garbage collected.

P.S. Dates có thể được存储 như objects của built-in `Date` class, mà chúng ta sẽ cover sau.

lời giải

Để store một date, chúng ta có thể sử dụng `WeakMap`:

```
let messages = [
  {text: "Hello", from: "John"},
  {text: "How goes?", from: "John"},
  {text: "See you soon", from: "Alice"}
];

let readMap = new WeakMap();

readMap.set(messages[0], new Date(2017, 1, 1));
// Date object chúng ta sẽ study sau
```
