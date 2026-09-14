# JSON methods, toJSON

> Nguồn: [https://javascript.info/json](https://javascript.info/json)

<!-- fetched: 2026-09-14 -->

Hãy nói chúng ta có một complex object, và chúng ta muốn convert nó vào một string, để send nó qua network, hoặc just để output nó cho logging purposes.

Tự nhiên, một string như vậy nên include tất cả important properties.

Chúng ta có thể implement conversion như thế này:

```
let user = {
  name: "John",
  age: 30,

  toString() {
    return `{name: "${this.name}", age: ${this.age}}`;
  }
};

alert(user); // {name: "John", age: 30}
```

…Nhưng trong quá trình phát triển, new properties được thêm, old properties được rename và removed. Updating这样的 `toString` every time có thể become một pain. Chúng ta có thể try để loop qua properties trong nó, nhưng nếu object là complex và có nested objects trong properties? Chúng ta cần để implement conversion của chúng cũng.

Glücklicherweise, không có need để viết code để handle tất cả điều này. Task đã được solved already.

## [JSON.stringify](#json-stringify)

[JSON](https://en.wikipedia.org/wiki/JSON) (JavaScript Object Notation) là một general format để represent values và objects. Nó được described trong [RFC 4627](https://tools.ietf.org/html/rfc4627) standard. Initially nó được made cho JavaScript, nhưng nhiều anderen languages có libraries để handle nó cũng. Vì vậy dễ dàng để sử dụng JSON cho data exchange khi client sử dụng JavaScript và server được viết trên Ruby/PHP/Java/Whatever.

JavaScript provides các methods:

- `JSON.stringify` để convert objects vào JSON.
- `JSON.parse` để convert JSON trở lại thành object.

Ví例, ở đây chúng ta `JSON.stringify` một student:

```
let student = {
  name: 'John',
  age: 30,
  isAdmin: false,
  courses: ['html', 'css', 'js'],
  spouse: null
};

let json = JSON.stringify(student);

alert(typeof json); // we've got một string!

alert(json);
/* JSON-encoded object:
{
  "name": "John",
  "age": 30,
  "isAdmin": false,
  "courses": ["html", "css", "js"],
  "spouse": null
}
*/
```

Method `JSON.stringify(student)` takes object và converts nó vào một string.

Resulting `json` string được gọi là *JSON-encoded* hoặc *serialized* hoặc *stringified* hoặc *marshalled* object. Chúng ta ready để send nó qua wire hoặc put trong một plain data store.

Xin lưu ý rằng một JSON-encoded object có several important differences từ object literal:

- Strings sử dụng double quotes. Không có single quotes hoặc backticks trong JSON. Vì vậy `'John'` becomes `"John"`.
- Object property names được double-quoted cũng. Đó là obligatory. Vì vậy `age:30` becomes `"age":30`.

`JSON.stringify` có thể được áp dụng cho primitives cũng.

JSON support following data types:

- Objects `{ ... }`
- Arrays `[ ... ]`
- Primitives:
  - strings,
  - numbers,
  - boolean values `true/false`,
  - `null`.

Ví例:

```
// một number trong JSON là chỉ một number
alert( JSON.stringify(1) ) // 1

// một string trong JSON vẫn là một string, nhưng double-quoted
alert( JSON.stringify('test') ) // "test"

alert( JSON.stringify(true) ); // true

alert( JSON.stringify([1, 2, 3]) ); // [1,2,3]
```

JSON là một data-only language-independent specification, vì vậy một số JavaScript-specific object properties bị skipped bởi `JSON.stringify`.

Cụ thể:

- Function properties (methods).
- Symbolic keys và values.
- Properties mà store `undefined`.

```
let user = {
  sayHi() { // bị ignored
    alert("Hello");
  },
  [Symbol("id")]: 123, // bị ignored
  something: undefined // bị ignored
};

alert( JSON.stringify(user) ); // {} (empty object)
```

Thông thường điều đó là fine. Nếu đó là không phải những gì chúng ta muốn, sau đó soon chúng ta sẽ see làm thế nào để customize process.

Great thing là nested objects được support và converted tự động.

Ví例:

```
let meetup = {
  title: "Conference",
  room: {
    number: 23,
    participants: ["john", "ann"]
  }
};

alert( JSON.stringify(meetup) );
/* Whole structure được stringified:
{
  "title":"Conference",
  "room":{"number":23,"participants":["john","ann"]},
}
*/
```

Important limitation: không có circular references.

Ví例:

```
let room = {
  number: 23
};

let meetup = {
  title: "Conference",
  participants: ["john", "ann"]
};

meetup.place = room;       // meetup references room
room.occupiedBy = meetup; // room references meetup

JSON.stringify(meetup); // Error: Converting circular structure đến JSON
```

Ở đây, conversion fails, vì circular reference: `room.occupiedBy` references `meetup`, và `meetup.place` references `room`:

![](/article/json/json-meetup.svg)

## [Excluding và transforming: replacer](#excluding-and-transforming-replacer)

Full syntax của `JSON.stringify` là:

```
let json = JSON.stringify(value[, replacer, space])
```

value
:   Một value để encode.

replacer
:   Array của properties để encode hoặc một mapping function `function(key, value)`.

space
:   Amount của space để sử dụng cho formatting

Most of the time, `JSON.stringify` được used với first argument only. Nhưng nếu chúng ta cần để fine-tune replacement process, như để filter out circular references, chúng ta có thể sử dụng second argument của `JSON.stringify`.

Nếu chúng ta pass một array của properties đến nó, chỉ这些 properties sẽ được encoded.

Ví例:

```
let room = {
  number: 23
};

let meetup = {
  title: "Conference",
  participants: [{name: "John"}, {name: "Alice"}],
  place: room // meetup references room
};

room.occupiedBy = meetup; // room references meetup

alert( JSON.stringify(meetup, ['title', 'participants']) );
// {"title":"Conference","participants":[{},{}]}
```

Ở đây chúng ta có thể quá strict. Property list được áp dụng cho whole object structure. Vì vậy các objects trong `participants` là empty, vì `name` không phải trong list.

Hãy include trong list every property ngoại trừ `room.occupiedBy` mà would cause circular reference:

```
let room = {
  number: 23
};

let meetup = {
  title: "Conference",
  participants: [{name: "John"}, {name: "Alice"}],
  place: room // meetup references room
};

room.occupiedBy = meetup; // room references meetup

alert( JSON.stringify(meetup, ['title', 'participants', 'place', 'name', 'number']) );
/*
{
  "title":"Conference",
  "participants":[{"name":"John"},{"name":"Alice"}],
  "place":{"number":23}
}
*/
```

Giờ everything ngoại trừ `occupiedBy` được serialized. Nhưng list của properties là quite long.

Glücklicherweise, chúng ta có thể sử dụng một function thay vì một array như `replacer`.

Function sẽ được called cho mỗi `(key, value)` pair và nên return "replaced" value, mà sẽ được used thay vì original một. Hoặc `undefined` nếu value là để be skipped.

Trong case của chúng ta, chúng ta có thể return `value` "as is" cho everything ngoại trừ `occupiedBy`. Để ignore `occupiedBy`, code dưới đây trả về `undefined`:

```
let room = {
  number: 23
};

let meetup = {
  title: "Conference",
  participants: [{name: "John"}, {name: "Alice"}],
  place: room // meetup references room
};

room.occupiedBy = meetup; // room references meetup

alert( JSON.stringify(meetup, function replacer(key, value) {
  alert(`${key}: ${value}`);
  return (key == 'occupiedBy') ? undefined : value;
}));

/* key:value pairs mà come đến replacer:
:             [object Object]
title:        Conference
participants: [object Object],[object Object]
0:            [object Object]
name:         John
1:            [object Object]
name:         Alice
place:        [object Object]
number:       23
occupiedBy: [object Object]
*/
```

Xin lưu ý rằng `replacer` function gets mọi key/value pair bao gồm nested objects và array items. Nó được applied recursively. Value của `this` bên trong `replacer` là object mà contains current property.

First call là special. Nó được làm sử dụng một special "wrapper object": `{"": meetup}`. Nói cách khác, first `(key, value)` pair có một empty key, và value là target object như là whole. Đó là lý do tại sao first line là `":[object Object]"` trong ví例 ở trên.

Idea là để provide as much power cho `replacer` như có thể: nó có một chance để analyze và replace/skip ngay cả whole object nếu necessary.

## [Formatting: space](#formatting-space)

Third argument của `JSON.stringify(value, replacer, space)` là number của spaces để sử dụng cho pretty formatting.

Previously, tất cả stringified objects có không indents và extra spaces. Điều đó là fine nếu chúng ta muốn để send một object qua network. `space` argument được used exclusively cho nice output.

Ở đây `space = 2` tells JavaScript để show nested objects trên multiple lines, với indentation của 2 spaces bên trong một object:

```
let user = {
  name: "John",
  age: 25,
  roles: {
    isAdmin: false,
    isEditor: true
  }
};

alert(JSON.stringify(user, null, 2));
/* hai-space indents:
{
  "name": "John",
  "age": 25,
  "roles": {
    "isAdmin": false,
    "isEditor": true
  }
}
*/

/* cho JSON.stringify(user, null, 4) result sẽ là more indented:
{
    "name": "John",
    "age": 25,
    "roles": {
        "isAdmin": false,
        "isEditor": true
    }
}
*/
```

Third argument cũng có thể là một string. Trong case này, string được used cho indentation thay vì một number của spaces.

`space` parameter được used solely cho logging và nice-output purposes.

## [Custom "toJSON"](#custom-tojson)

Giống như `toString` cho string conversion, một object có thể提供 method `toJSON` cho to-JSON conversion. `JSON.stringify` tự động gọi nó nếu available.

Ví例:

```
let room = {
  number: 23
};

let meetup = {
  title: "Conference",
  date: new Date(Date.UTC(2017, 0, 1)),
  room
};

alert( JSON.stringify(meetup) );
/*
  {
    "title":"Conference",
    "date":"2017-01-01T00:00:00.000Z",  // (1)
    "room": {"number":23}               // (2)
  }
*/
```

Ở đây chúng ta có thể thấy `date` `(1)` became một string. Đó là vì tất cả các dates có một built-in `toJSON` method mà returns một kind của string như vậy.

Giờ hãy add một custom `toJSON` cho object `room` `(2)` của chúng ta:

```
let room = {
  number: 23,
  toJSON() {
    return this.number;
  }
};

let meetup = {
  title: "Conference",
  room
};

alert( JSON.stringify(room) ); // 23

alert( JSON.stringify(meetup) );
/*
  {
    "title":"Conference",
    "room": 23
  }
*/
```

Như chúng ta có thể see, `toJSON` được used cho cả direct call `JSON.stringify(room)` và khi `room` được nested trong một encoded object khác.

## [JSON.parse](#json-parse)

Để decode một JSON-string, chúng ta cần một another method tên là [JSON.parse](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON/parse).

Syntax:

```
let value = JSON.parse(str[, reviver]);
```

str
:   JSON-string để parse.

reviver
:   Optional function(key,value) sẽ được called cho mỗi `(key, value)` pair và có thể transform value.

Ví例:

```
// stringified array
let numbers = "[0, 1, 2, 3]";

numbers = JSON.parse(numbers);

alert( numbers[1] ); // 1
```

Hoặc cho nested objects:

```
let userData = '{ "name": "John", "age": 35, "isAdmin": false, "friends": [0,1,2,3] }';

let user = JSON.parse(userData);

alert( user.friends[1] ); // 1
```

JSON có thể complex như necessary, objects và arrays có thể include các objects và arrays khác. Nhưng chúng phải obey same JSON format.

Đây là những mistakes thông thường trong hand-written JSON (đôi khi chúng ta phải viết nó cho debugging purposes):

```
let json = `{
  name: "John",                     // mistake: property name không có quotes
  "surname": 'Smith',               // mistake: single quotes trong value (phải là double)
  'isAdmin': false                  // mistake: single quotes trong key (phải là double)
  "birthday": new Date(2000, 2, 3), // mistake: không có "new" được allowed, chỉ bare values
  "friends": [0,1,2,3]              // tại đây tất cả fine
}`;
```

Bên cạnh đó, JSON không support comments. Thêm một comment đến JSON makes nó invalid.

Có một altro format tên là [JSON5](https://json5.org/), mà allows unquoted keys, comments v.v. Nhưng đây là một standalone library, không phải trong specification của language.

Regular JSON là that strict không phải vì developers của nó lazy, nhưng để allow easy, reliable và rất fast implementations của parsing algorithm.

## [Sử dụng reviver](#using-reviver)

Imagine, chúng ta received một stringified `meetup` object từ server.

Nó看起来 như thế này:

```
// title: (meetup title), date: (meetup date)
let str = '{"title":"Conference","date":"2017-11-30T12:00:00.000Z"}';
```

…Và giờ chúng ta cần để *deserialize* nó, để trở lại thành JavaScript object.

Hãy làm điều đó bằng cách gọi `JSON.parse`:

```
let str = '{"title":"Conference","date":"2017-11-30T12:00:00.000Z"}';

let meetup = JSON.parse(str);

alert( meetup.date.getDate() ); // Error!
```

Whoops! Một error!

Value của `meetup.date` là một string, không phải là một `Date` object. Làm thế nào `JSON.parse` có thể know rằng nó nên transform string đó vào một `Date`?

Hãy pass đến `JSON.parse` một reviving function như second argument, mà trả về tất cả values "as is", nhưng `date` sẽ trở thành một `Date`:

```
let str = '{"title":"Conference","date":"2017-11-30T12:00:00.000Z"}';

let meetup = JSON.parse(str, function(key, value) {
  if (key == 'date') return new Date(value);
  return value;
});

alert( meetup.date.getDate() ); // work giờ!
```

Nhân tiện, điều đó work cho nested objects cũng:

```
let schedule = `{
  "meetups": [
    {"title":"Conference","date":"2017-11-30T12:00:00.000Z"},
    {"title":"Birthday","date":"2017-04-18T12:00:00.000Z"}
  ]
}`;

schedule = JSON.parse(schedule, function(key, value) {
  if (key == 'date') return new Date(value);
  return value;
});

alert( schedule.meetups[1].date.getDate() ); // work!
```

## [Tổng kết](#summary)

- JSON là một data format mà có independent standard của nó và libraries cho most programming languages.
- JSON支持 plain objects, arrays, strings, numbers, booleans, và `null`.
- JavaScript provides methods [JSON.stringify](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON/stringify) để serialize vào JSON và [JSON.parse](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON/parse) để đọc từ JSON.
- Cả hai methods hỗ trợ transformer functions cho smart reading/writing.
- Nếu một object có `toJSON`, sau đó nó được called bởi `JSON.stringify`.

---

---

## Các bài tập

## [Các bài tập](#tasks)

### [Turn object vào JSON và back](#turn-the-object-into-json-and-back)

mức độ quan trọng: 5

Turn `user` vào JSON và sau đó đọc nó back vào một另一个 variable.

```
let user = {
  name: "John Smith",
  age: 35
};
```

lời giải

```
let user = {
  name: "John Smith",
  age: 35
};

let user2 = JSON.parse(JSON.stringify(user));
```

### [Exclude backreferences](#exclude-backreferences)

mức độ quan trọng: 5

Trong simple cases của circular references, chúng ta có thể exclude một offending property từ serialization bởi tên của nó.

Nhưng đôi khi chúng ta không thể just sử dụng name, vì nó có thể được used cả trong circular references và normal properties. Vì vậy chúng ta có thể check property bởi giá trị của nó.

Viết `replacer` function để stringify everything, nhưng remove properties mà references `meetup`:

```
let room = {
  number: 23
};

let meetup = {
  title: "Conference",
  occupiedBy: [{name: "John"}, {name: "Alice"}],
  place: room
};

// circular references
room.occupiedBy = meetup;
meetup.self = meetup;

alert( JSON.stringify(meetup, function replacer(key, value) {
  /* your code */
}));

/* result nên là:
{
  "title":"Conference",
  "occupiedBy":[{"name":"John"},{"name":"Alice"}],
  "place":{"number":23}
}
*/
```

lời giải

```
let room = {
  number: 23
};

let meetup = {
  title: "Conference",
  occupiedBy: [{name: "John"}, {name: "Alice"}],
  place: room
};

room.occupiedBy = meetup;
meetup.self = meetup;

alert( JSON.stringify(meetup, function replacer(key, value) {
  return (key != "" && value == meetup) ? undefined : value;
}));

/*
{
  "title":"Conference",
  "occupiedBy":[{"name":"John"},{"name":"Alice"}],
  "place":{"number":23}
}
*/
```

Ở đây chúng ta cũng cần để test `key==""` để exclude first call nơi nó là normal rằng `value` là `meetup`.
