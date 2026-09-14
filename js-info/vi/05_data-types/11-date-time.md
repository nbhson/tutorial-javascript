# Date và time

> Nguồn: [https://javascript.info/date](https://javascript.info/date)

<!-- fetched: 2026-09-14 -->

Hãy meet một new built-in object: [Date](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date). Nó store date, time và provides methods cho date/time management.

Ví例, chúng ta có thể sử dụng nó để store creation/modification times, để measure time, hoặc just để print out current date.

## [Creation](#creation)

Để tạo một new `Date` object call `new Date()` với một trong các following arguments:

`new Date()`
:   Không có arguments – create một `Date` object cho current date và time:

    ```
    let now = new Date();
    alert( now ); // shows current date/time
    ```

`new Date(milliseconds)`
:   Create một `Date` object với time equal đến number của milliseconds (1/1000 của một second) passed sau Jan 1st của 1970 UTC+0.

    ```
    // 0 means 01.01.1970 UTC+0
    let Jan01_1970 = new Date(0);
    alert( Jan01_1970 );

    // giờ add 24 hours, get 02.01.1970 UTC+0
    let Jan02_1970 = new Date(24 * 3600 * 1000);
    alert( Jan02_1970 );
    ```

    Một integer number representing number của milliseconds đã passed từ beginning của 1970 được gọi là *timestamp*.

    Nó là một lightweight numeric representation của một date. Chúng ta có thể luôn luôn create một date từ một timestamp sử dụng `new Date(timestamp)` và convert existing `Date` object sang một timestamp sử dụng `date.getTime()` method (xem bên dưới).

    Dates trước 01.01.1970 có negative timestamps, ví例:

    ```
    // 31 Dec 1969
    let Dec31_1969 = new Date(-24 * 3600 * 1000);
    alert( Dec31_1969 );
    ```

`new Date(datestring)`
:   Nếu có một single argument, và nó's một string, sau đó nó được parsed tự động. Algorithm là same như `Date.parse` sử dụng, chúng ta sẽ cover nó sau.

    ```
    let date = new Date("2017-01-26");
    alert(date);
    // Time không được set, vì vậy nó được assumed là midnight GMT và
    // được adjust theo timezone code được run trong
    // Vì vậy result có thể là
    // Thu Jan 26 2017 11:00:00 GMT+1100 (Australian Eastern Daylight Time)
    // hoặc
    // Wed Jan 25 2017 16:00:00 GMT-0800 (Pacific Standard Time)
    ```

`new Date(year, month, date, hours, minutes, seconds, ms)`
:   Create date với given components trong local time zone. Chỉ first two arguments là obligatory.

    - `year` nên có 4 digits. Cho compatibility, 2 digits cũng được accepted và considered `19xx`, ví例 `98` là same như `1998` ở đây, nhưng luôn luôn sử dụng 4 digits là strongly encouraged.
    - `month` count bắt đầu từ `0` (Jan), đến `11` (Dec).
    - `date` parameter thực sự là day của month, nếu absent sau đó `1` được assumed.
    - Nếu `hours/minutes/seconds/ms` là absent, chúng được assumed để equal `0`.

    Ví例:

    ```
    new Date(2011, 0, 1, 0, 0, 0, 0); // 1 Jan 2011, 00:00:00
    new Date(2011, 0, 1); // same, hours etc là 0 bởi default
    ```

    Maximal precision là 1 ms (1/1000 sec):

    ```
    let date = new Date(2011, 0, 1, 2, 3, 4, 567);
    alert( date ); // 1.01.2011, 02:03:04.567
    ```

## [Access date components](#access-date-components)

Có các methods để access year, month và vân vân từ `Date` object:

[getFullYear()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/getFullYear)
:   Get year (4 digits)

[getMonth()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/getMonth)
:   Get month, **từ 0 đến 11**.

[getDate()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/getDate)
:   Get day của month, từ 1 đến 31, tên của method看起来 một little bit strange.

[getHours()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/getHours), [getMinutes()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/getMinutes), [getSeconds()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/getSeconds), [getMilliseconds()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/getMilliseconds)
:   Get corresponding time components.

Không `getYear()`, mà là `getFullYear()`

Nhiều JavaScript engines implement một non-standard method `getYear()`. Method này deprecated. Nó trả về 2-digit year đôi khi. Please không bao giờ use nó. Có `getFullYear()` cho year.

Additionally, chúng ta có thể get một day của week:

[getDay()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/getDay)
:   Get day của week, từ `0` (Sunday) đến `6` (Saturday). First day là luôn Sunday, trong một số countries điều đó không phải vậy, nhưng không thể được changed.

**Tất cả các methods trên trả về components tương đối với local time zone.**

Cũng có counterparts UTC của chúng, mà trả về day, month, year và vân vân cho time zone UTC+0: [getUTCFullYear()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/getUTCFullYear), [getUTCMonth()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/getUTCMonth), [getUTCDay()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/getUTCDay). Chỉ insert `"UTC"` right sau `"get"`.

Nếu local time zone của bạn shifted tương đối với UTC, sau đó code dưới đây shows different hours:

```
// current date
let date = new Date();

// hour trong current time zone của bạn
alert( date.getHours() );

// hour trong UTC+0 time zone (London time không có daylight savings)
alert( date.getUTCHours() );
```

Bên cạnh các methods đã cho, có hai specials mà không có một UTC-variant:

[getTime()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/getTime)
:   Returns timestamp cho date – một number của milliseconds passed từ January 1st của 1970 UTC+0.

[getTimezoneOffset()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/getTimezoneOffset)
:   Returns difference giữa UTC và local time zone, trong minutes:

    ```
    // nếu bạn là trong timezone UTC-1, outputs 60
    // nếu bạn là trong timezone UTC+3, outputs -180
    alert( new Date().getTimezoneOffset() );
    ```

## [Setting date components](#setting-date-components)

Following methods allow để set date/time components:

- [`setFullYear(year, [month], [date])`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/setFullYear)
- [`setMonth(month, [date])`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/setMonth)
- [`setDate(date)`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/setDate)
- [`setHours(hour, [min], [sec], [ms])`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/setHours)
- [`setMinutes(min, [sec], [ms])`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/setMinutes)
- [`setSeconds(sec, [ms])`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/setSeconds)
- [`setMilliseconds(ms)`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/setMilliseconds)
- [`setTime(milliseconds)`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/setTime) (sets whole date bởi milliseconds từ 01.01.1970 UTC)

Mỗi một trong số chúng ngoại trừ `setTime()` có một UTC-variant, ví例: `setUTCHours()`.

Như chúng ta có thể see, một số methods có thể set nhiều components tại một time, ví例 `setHours`. Các components mà không được mentioned là không modified.

Ví例:

```
let today = new Date();

today.setHours(0);
alert(today); // vẫn today, nhưng hour được changed đến 0

today.setHours(0, 0, 0, 0);
alert(today); // vẫn today, giờ 00:00:00 sharp.
```

## [Autocorrection](#autocorrection)

*Autocorrection* là một very handy feature của `Date` objects. Chúng ta có thể set out-of-range values, và nó sẽ auto-adjust本身.

Ví例:

```
let date = new Date(2013, 0, 32); // 32 Jan 2013 ?!?
alert(date); // ...là 1st Feb 2013!
```

Out-of-range date components được distributed tự động.

Hãy nói chúng ta cần để increase date "28 Feb 2016" bởi 2 days. Nó có thể là "2 Mar" hoặc "1 Mar" trong case của một leap-year. Chúng ta không cần để think về điều đó. Just add 2 days. `Date` object sẽ làm rest:

```
let date = new Date(2016, 1, 28);
date.setDate(date.getDate() + 2);

alert( date ); // 1 Mar 2016
```

Feature đó thường được used để get date sau given period của time. Ví例, hãy get date cho "70 seconds sau now":

```
let date = new Date();
date.setSeconds(date.getSeconds() + 70);

alert( date ); // shows correct date
```

Chúng ta cũng có thể set zero hoặc thậm chí negative values. Ví例:

```
let date = new Date(2016, 0, 2); // 2 Jan 2016

date.setDate(1); // set day 1 của month
alert( date );

date.setDate(0); // min day là 1, vì vậy last day của previous month được assumed
alert( date ); // 31 Dec 2015
```

## [Date to number, date diff](#date-to-number-date-diff)

Khi một `Date` object được converted sang number, nó become timestamp same như `date.getTime()`:

```
let date = new Date();
alert(+date); // number của milliseconds, same như date.getTime()
```

Important side effect: dates có thể được subtracted, result là difference của chúng trong ms.

Điều đó có thể được used cho time measurements:

```
let start = new Date(); // start measuring time

// do job
for (let i = 0; i < 100000; i++) {
  let doSomething = i * i * i;
}

let end = new Date(); // end measuring time

alert( `Loop took ${end - start} ms` );
```

## [Date.now()](#date-now)

Nếu chúng ta chỉ muốn để measure time, chúng ta không cần `Date` object.

Có một special method `Date.now()` mà trả về current timestamp.

Nó semantically equivalent đến `new Date().getTime()`, nhưng nó không create intermediate `Date` object. Vì vậy nó faster và không put pressure lên garbage collection.

Nó được used chủ yếu cho convenience hoặc khi performance matters, như trong games trong JavaScript hoặc các specialized applications khác.

Vì vậy có lẽ tốt hơn:

```
let start = Date.now(); // milliseconds count từ 1 Jan 1970

// do job
for (let i = 0; i < 100000; i++) {
  let doSomething = i * i * i;
}

let end = Date.now(); // done

alert( `Loop took ${end - start} ms` ); // subtract numbers, không phải dates
```

## [Benchmarking](#benchmarking)

Nếu chúng ta muốn một reliable benchmark của CPU-hungry function, chúng ta nên cẩn thận.

Ví例, hãy measure hai functions mà calculate difference giữa hai dates:哪一个 nhanh hơn?

Such performance measurements thường được gọi là "benchmarks".

```
// chúng ta có date1 và date2, function nào nhanh hơn trả về difference của chúng trong ms?
function diffSubtract(date1, date2) {
  return date2 - date1;
}

// hoặc
function diffGetTime(date1, date2) {
  return date2.getTime() - date1.getTime();
}
```

Cả hai làm exactly same thing, nhưng một trong số chúng sử dụng explicit `date.getTime()` để get date trong ms, và one còn lại dựa vào một date-to-number transform. Result của chúng luôn luôn same.

Vì vậy,哪一个 nhanh hơn?

Ideas đầu tiên có thể là để chạy chúng nhiều lần trong hàng và measure time difference. Cho trường hợp của chúng ta, functions là very simple, vì vậy chúng ta phải do it at least 100000 times.

Hãy measure:

```
function diffSubtract(date1, date2) {
  return date2 - date1;
}

function diffGetTime(date1, date2) {
  return date2.getTime() - date1.getTime();
}

function bench(f) {
  let date1 = new Date(0);
  let date2 = new Date();

  let start = Date.now();
  for (let i = 0; i < 100000; i++) f(date1, date2);
  return Date.now() - start;
}

alert( 'Time của diffSubtract: ' + bench(diffSubtract) + 'ms' );
alert( 'Time của diffGetTime: ' + bench(diffGetTime) + 'ms' );
```

Wow! Sử dụng `getTime()` là so much faster! Đó là vì không có type conversion, nó much easier cho engines để optimize.

Okay, chúng ta có một cái gì đó. Nhưng đó là không phải một good benchmark yet.

Imagine rằng tại thời điểm running `bench(diffSubtract)` CPU đang doing something trong parallel, và nó đang taking resources. Và bằng thời điểm running `bench(diffGetTime)` work đó đã finished.

Một pretty real scenario cho một modern multi-process OS.

Như result, first benchmark sẽ có less CPU resources hơn second. Điều đó có thể lead đến wrong results.

**Để benchmarking more reliable, whole pack của benchmarks nên được rerun multiple times.**

Ví例, như thế này:

```
function diffSubtract(date1, date2) {
  return date2 - date1;
}

function diffGetTime(date1, date2) {
  return date2.getTime() - date1.getTime();
}

function bench(f) {
  let date1 = new Date(0);
  let date2 = new Date();

  let start = Date.now();
  for (let i = 0; i < 100000; i++) f(date1, date2);
  return Date.now() - start;
}

let time1 = 0;
let time2 = 0;

// run bench(diffSubtract) và bench(diffGetTime) mỗi 10 times alternating
for (let i = 0; i < 10; i++) {
  time1 += bench(diffSubtract);
  time2 += bench(diffGetTime);
}

alert( 'Total time cho diffSubtract: ' + time1 );
alert( 'Total time cho diffGetTime: ' + time2 );
```

Modern JavaScript engines start applying advanced optimizations chỉ đến "hot code" mà executes many times (không cần để optimize rarely executed things). Vì vậy, trong ví例 ở trên, first executions không được well-optimized. Chúng ta có thể want để add một heat-up run:

```
// added cho "heating up" prior đến main loop
bench(diffSubtract);
bench(diffGetTime);

// giờ benchmark
for (let i = 0; i < 10; i++) {
  time1 += bench(diffSubtract);
  time2 += bench(diffGetTime);
}
```

Be careful làm microbenchmarking

Modern JavaScript engines perform many optimizations. Chúng có thể tweak results của "artificial tests" so với "normal usage", đặc biệt khi chúng ta benchmark something very small, như cách một operator hoạt động, hoặc một built-in function. Vì vậy nếu bạn seriously muốn hiểu performance, sau đó please study cách JavaScript engine làm việc. Và sau đó bạn có lẽ không cần microbenchmarks at all.

Great pack của articles về V8 có thể được found tại <https://mrale.ph>.

## [Date.parse từ một string](#date-parse-from-a-string)

Method [Date.parse(str)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/parse) có thể read một date từ một string.

String format nên là: `YYYY-MM-DDTHH:mm:ss.sssZ`, nơi:

- `YYYY-MM-DD` – là date: year-month-day.
- Character `"T"` được used như delimiter.
- `HH:mm:ss.sss` – là time: hours, minutes, seconds và milliseconds.
- Optional `'Z'` part denotes time zone trong format `+-hh:mm`. Một single letter `Z` sẽ có nghĩa UTC+0.

Shorter variants cũng có thể, như `YYYY-MM-DD` hoặc `YYYY-MM` hoặc thậm chí `YYYY`.

Call đến `Date.parse(str)` parses string trong given format và trả về timestamp (number của milliseconds từ 1 Jan 1970 UTC+0). Nếu format là invalid, trả về `NaN`.

Ví例:

```
let ms = Date.parse('2012-01-26T13:51:50.417-07:00');

alert(ms); // 1327611110417  (timestamp)
```

Chúng ta có thể instantly create một `new Date` object từ timestamp:

```
let date = new Date( Date.parse('2012-01-26T13:51:50.417-07:00') );

alert(date);
```

## [Tổng kết](#summary)

- Date và time trong JavaScript được represented với [Date](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date) object. Chúng ta không thể create "only date" hoặc "only time": `Date` objects luôn luôn carry cả hai.
- Months được counted từ zero (có, January là zero month).
- Days của week trong `getDay()` cũng được counted từ zero (đó là Sunday).
- `Date` auto-corrects本身 khi out-of-range components được set. Good cho adding/subtracting days/months/hours.
- Dates có thể được subtracted, giving difference của chúng trong milliseconds. Đó là vì một `Date` become timestamp khi converted sang một number.
- Sử dụng `Date.now()` để get current timestamp fast.

Note rằng khác với nhiều anderen systems, timestamps trong JavaScript là trong milliseconds, không phải trong seconds.

Đôi khi chúng ta cần more precise time measurements. JavaScript本身 không có một way để measure time trong microseconds (1 millionth của một second), nhưng most environments provide nó. Ví例, browser có [performance.now()](https://developer.mozilla.org/en-US/docs/Web/API/Performance/now) mà gives number của milliseconds từ start của page loading với microsecond precision (3 digits sau point):

```
alert(`Loading started ${performance.now()}ms ago`);
// Something like: "Loading started 34731.26000000001ms ago"
// .26 là microseconds (260 microseconds)
// more than 3 digits sau decimal point là precision errors, chỉ first 3 là correct
```

Node.js có `microtime` module và các ways khác. Về mặt kỹ thuật, almost any device và environment cho phép để get more precision, đó là just không trong `Date`.

---

---

## Các bài tập

## [Các bài tập](#tasks)

### [Create một date](#create-a-date)

mức độ quan trọng: 5

Tạo một `Date` object cho date: Feb 20, 2012, 3:12am. Time zone là local.

Show nó sử dụng `alert`.

lời giải

`new Date` constructor sử dụng local time zone. Vì vậy important thing duy nhất để remember là months bắt đầu từ zero.

Vì vậy February có number 1.

Đây là một ví例 với numbers như date components:

```
//new Date(year, month, date, hour, minute, second, millisecond)
let d1 = new Date(2012, 1, 20, 3, 12);
alert( d1 );
```

Chúng ta cũng có thể tạo một date từ một string, như thế này:

```
//new Date(datastring)
let d2 = new Date("2012-02-20T03:12");
alert( d2 );
```

### [Show weekday](#show-a-weekday)

mức độ quan trọng: 5

Viết function `getWeekDay(date)` để show weekday trong short format: 'MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU'.

Ví例:

```
let date = new Date(2012, 0, 3);  // 3 Jan 2012
alert( getWeekDay(date) );        // nên output "TU"
```

[Mở một sandbox với tests.](https://plnkr.co/edit/w5Wl0rZP07Svy7Y3?p=preview)

lời giải

Method `date.getDay()` trả về number của weekday, bắt đầu từ sunday.

Hãy make một array của weekdays, vì vậy chúng ta có thể get proper day name bởi number của nó:

```
function getWeekDay(date) {
  let days = ['SU', 'MO', 'TU', 'WE', 'TH', 'FR', 'SA'];

  return days[date.getDay()];
}

let date = new Date(2014, 0, 3); // 3 Jan 2014
alert( getWeekDay(date) ); // FR
```

[Mở solution với tests trong một sandbox.](https://plnkr.co/edit/ZjPlwWmWqlM0z3Ny?p=preview)

### [European weekday](#european-weekday)

mức độ quan trọng: 5

Các European countries có days của week bắt đầu với Monday (number 1), sau đó Tuesday (number 2) và till Sunday (number 7). Viết function `getLocalDay(date)` mà trả về "European" day của week cho `date`.

```
let date = new Date(2012, 0, 3);  // 3 Jan 2012
alert( getLocalDay(date) );       // tuesday, nên show 2
```

[Mở một sandbox với tests.](https://plnkr.co/edit/JhFthIjddi6EQNSb?p=preview)

lời giải

```
function getLocalDay(date) {

  let day = date.getDay();

  if (day == 0) { // weekday 0 (sunday) là 7 trong european
    day = 7;
  }

  return day;
}
```

[Mở solution với tests trong một sandbox.](https://plnkr.co/edit/URgnxXZ63sXs43N0?p=preview)

### [Which day của month was many days ago?](#which-day-of-month-was-many-days-ago)

mức độ quan trọng: 4

Tạo function `getDateAgo(date, days)` để trả về day của month `days` ago từ `date`.

Ví例, nếu today là 20th, sau đó `getDateAgo(new Date(), 1)` nên là 19th và `getDateAgo(new Date(), 2)` nên là 18th.

Nên work reliably cho `days=365` hoặc nhiều hơn:

```
let date = new Date(2015, 0, 2);

alert( getDateAgo(date, 1) ); // 1, (1 Jan 2015)
alert( getDateAgo(date, 2) ); // 31, (31 Dec 2014)
alert( getDateAgo(date, 365) ); // 2, (2 Jan 2014)
```

P.S. Function không nên modify given `date`.

[Mở một sandbox với tests.](https://plnkr.co/edit/Am6hZucZGGcYNCTv?p=preview)

lời giải

Idea là simple: để substract given number của days từ `date`:

```
function getDateAgo(date, days) {
  date.setDate(date.getDate() - days);
  return date.getDate();
}
```

…Nhưng function không nên thay đổi `date`. Đó là một important thing, vì outer code mà gives chúng ta date không expect nó để thay đổi.

Để implement nó hãy clone date, như thế này:

```
function getDateAgo(date, days) {
  let dateCopy = new Date(date);

  dateCopy.setDate(date.getDate() - days);
  return dateCopy.getDate();
}

let date = new Date(2015, 0, 2);

alert( getDateAgo(date, 1) ); // 1, (1 Jan 2015)
alert( getDateAgo(date, 2) ); // 31, (31 Dec 2014)
alert( getDateAgo(date, 365) ); // 2, (2 Jan 2014)
```

[Mở solution với tests trong một sandbox.](https://plnkr.co/edit/ak3n6AKGwa3nth59?p=preview)

### [Last day của month?](#last-day-of-month)

mức độ quan trọng: 5

Viết function `getLastDayOfMonth(year, month)` mà trả về last day của month. Đôi khi nó là 30th, 31st hoặc ngay cả 28/29th cho Feb.

Parameters:

- `year` – four-digits year, ví例 2012.
- `month` – month, từ 0 đến 11.

Ví例, `getLastDayOfMonth(2012, 1) = 29` (leap year, Feb).

[Mở một sandbox với tests.](https://plnkr.co/edit/mQ3ST6aen98dHxA0?p=preview)

lời giải

Hãy create một date sử dụng next month, nhưng pass zero như day:

```
function getLastDayOfMonth(year, month) {
  let date = new Date(year, month + 1, 0);
  return date.getDate();
}

alert( getLastDayOfMonth(2012, 0) ); // 31
alert( getLastDayOfMonth(2012, 1) ); // 29
alert( getLastDayOfMonth(2013, 1) ); // 28
```

Normally, dates bắt đầu từ 1, nhưng về mặt kỹ thuật chúng ta có thể pass bất kỳ number nào, date sẽ autoadjust本身. Vì vậy khi chúng ta pass 0, sau đó nó mean "one day trước 1st day của month", nói cách khác: "last day của previous month".

[Mở solution với tests trong một sandbox.](https://plnkr.co/edit/GJa2j6kDX97v1hoG?p=preview)

### [How many seconds have passed today?](#how-many-seconds-have-passed-today)

mức độ quan trọng: 5

Viết function `getSecondsToday()` mà trả về number của seconds từ beginning của today.

Ví例, nếu giờ là `10:00 am`, và không có daylight savings shift, sau đó:

```
getSecondsToday() == 36000 // (3600 * 10)
```

Function nên work trong bất kỳ day nào. Tức là, nó không nên có một hard-coded value của "today".

lời giải

Để get number của seconds, chúng ta có thể generate một date sử dụng current day và time 00:00:00, sau đó substract nó từ "now".

Difference là number của milliseconds từ beginning của day, mà chúng ta nên divide bằng 1000 để get seconds:

```
function getSecondsToday() {
  let now = new Date();

  // create object sử dụng current day/month/year
  let today = new Date(now.getFullYear(), now.getMonth(), now.getDate());

  let diff = now - today; // ms difference
  return Math.round(diff / 1000); // make seconds
}

alert( getSecondsToday() );
```

Một alternative solution sẽ là để get hours/minutes/seconds và convert chúng vào seconds:

```
function getSecondsToday() {
  let d = new Date();
  return d.getHours() * 3600 + d.getMinutes() * 60 + d.getSeconds();
}

alert( getSecondsToday() );
```

### [How many seconds till tomorrow?](#how-many-seconds-till-tomorrow)

mức độ quan trọng: 5

Tạo function `getSecondsToTomorrow()` mà trả về number của seconds till tomorrow.

Ví例, nếu giờ là `23:00`, sau đó:

```
getSecondsToTomorrow() == 3600
```

P.S. Function nên work tại bất kỳ day nào, "today" không được hardcoded.

lời giải

Để get number của milliseconds till tomorrow, chúng ta có thể từ "tomorrow 00:00:00" substract current date.

Trước tiên, chúng ta generate "tomorrow", và sau đó làm điều đó:

```
function getSecondsToTomorrow() {
  let now = new Date();

  // tomorrow date
  let tomorrow = new Date(now.getFullYear(), now.getMonth(), now.getDate()+1);

  let diff = tomorrow - now; // difference trong ms
  return Math.round(diff / 1000); // convert sang seconds
}
```

Alternative solution:

```
function getSecondsToTomorrow() {
  let now = new Date();
  let hour = now.getHours();
  let minutes = now.getMinutes();
  let seconds = now.getSeconds();
  let totalSecondsToday = (hour * 60 + minutes) * 60 + seconds;
  let totalSecondsInADay = 86400;

  return totalSecondsInADay - totalSecondsToday;
}
```

Please note rằng nhiều countries có Daylight Savings Time (DST), vì vậy có thể có days với 23 hoặc 25 hours. Chúng ta có thể want để treat such days riêng.

### [Format relative date](#format-the-relative-date)

mức độ quan trọng: 4

Viết function `formatDate(date)` mà nên format `date` như sau:

- Nếu từ `date` passed less than 1 second, sau đó `"right now"`.
- Ngược lại, nếu từ `date` passed less than 1 minute, sau đó `"n sec. ago"`.
- Ngược lại, nếu less than một hour, sau đó `"m min. ago"`.
- Ngược lại, full date trong format `"DD.MM.YY HH:mm"`. Tức là: `"day.month.year hours:minutes"`, tất cả trong 2-digit format, ví例. `31.12.16 10:00`.

Ví例:

```
alert( formatDate(new Date(new Date - 1)) ); // "right now"

alert( formatDate(new Date(new Date - 30 * 1000)) ); // "30 sec. ago"

alert( formatDate(new Date(new Date - 5 * 60 * 1000)) ); // "5 min. ago"

// yesterday's date như 31.12.16 20:00
alert( formatDate(new Date(new Date - 86400 * 1000)) );
```

[Mở một sandbox với tests.](https://plnkr.co/edit/ZWpjBPAr0KAXsjIC?p=preview)

lời giải

Để get time từ `date` till now – hãy substract dates.

```
function formatDate(date) {
  let diff = new Date() - date; // difference trong milliseconds

  if (diff < 1000) { // less than 1 second
    return 'right now';
  }

  let sec = Math.floor(diff / 1000); // convert diff sang seconds

  if (sec < 60) {
    return sec + ' sec. ago';
  }

  let min = Math.floor(diff / 60000); // convert diff sang minutes
  if (min < 60) {
    return min + ' min. ago';
  }

  // format date
  // add leading zeroes đến single-digit day/month/hours/minutes
  let d = date;
  d = [
    '0' + d.getDate(),
    '0' + (d.getMonth() + 1),
    '' + d.getFullYear(),
    '0' + d.getHours(),
    '0' + d.getMinutes()
  ].map(component => component.slice(-2)); // take last 2 digits của mỗi component

  // join components vào date
  return d.slice(0, 3).join('.') + ' ' + d.slice(3).join(':');
}

alert( formatDate(new Date(new Date - 1)) ); // "right now"

alert( formatDate(new Date(new Date - 30 * 1000)) ); // "30 sec. ago"

alert( formatDate(new Date(new Date - 5 * 60 * 1000)) ); // "5 min. ago"

// yesterday's date như 31.12.2016 20:00
alert( formatDate(new Date(new Date - 86400 * 1000)) );
```

Alternative solution:

```
function formatDate(date) {
  let dayOfMonth = date.getDate();
  let month = date.getMonth() + 1;
  let year = date.getFullYear();
  let hour = date.getHours();
  let minutes = date.getMinutes();
  let diffMs = new Date() - date;
  let diffSec = Math.round(diffMs / 1000);
  let diffMin = diffSec / 60;
  let diffHour = diffMin / 60;

  // formatting
  year = year.toString().slice(-2);
  month = month < 10 ? '0' + month : month;
  dayOfMonth = dayOfMonth < 10 ? '0' + dayOfMonth : dayOfMonth;
  hour = hour < 10 ? '0' + hour : hour;
  minutes = minutes < 10 ? '0' + minutes : minutes;

  if (diffSec < 1) {
    return 'right now';
  } else if (diffMin < 1) {
    return `${diffSec} sec. ago`
  } else if (diffHour < 1) {
    return `${diffMin} min. ago`
  } else {
    return `${dayOfMonth}.${month}.${year} ${hour}:${minutes}`
  }
}
```

[Mở solution với tests trong một sandbox.](https://plnkr.co/edit/7ddZvBCnN68gruHs?p=preview)
