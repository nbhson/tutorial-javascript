# JavaScript Runtime

## Mục Lục

1. [Giới Thiệu](#giới-thiệu)
2. [JavaScript Runtime là gì?](#javascript-runtime-là-gì)
3. [Các Thành Phần Chính của JavaScript Runtime](#các-thành-phần-chính-của-javascript-runtime)
4. [JavaScript Engine](#javascript-engine)
5. [Call Stack (Ngăn Xếp Gọi)](#call-stack-ngăn-xếp-gọi)
6. [Heap (Vùng Nhớ Động)](#heap-vùng-nhớ-động)
7. [Event Loop](#event-loop)
8. [Callback Queue (Hàng Đợi Callback)](#callback-queue-hàng-đợi-callback)
9. [Web APIs (Browser APIs)](#web-apis-browser-apis)
10. [Microtask Queue và Macrotask Queue](#microtask-queue-và-macrotask-queue)
11. [Memory Management (Quản Lý Bộ Nhớ)](#memory-management-quản-lý-bộ-nhớ)
12. [Garbage Collection (Thu Gom Rác)](#garbage-collection-thu-gom-rác)
13. [Các Loại JavaScript Runtime](#các-loại-javascript-runtime)
14. [Concurrency Model (Mô Hình Đồng Thời)](#concurrency-model-mô-hình-đồng-thời)
15. [Execution Context (Ngữ Cảnh Thực Thi)](#execution-context-ngữ-cảnh-thực-thi)
16. [Hoisting và Scope](#hoisting-và-scope)
17. [Closures (Đóng Gói)](#closures-đóng-gói)
18. [This Binding](#this-binding)
19. [Prototype Chain](#prototype-chain)
20. [Error Handling](#error-handling)
21. [Performance Optimization](#performance-optimization)
22. [Best Practices](#best-practices)
23. [Tài Liệu Tham Khảo](#tài-liệu-tham-khảo)

---

## Giới Thiệu

JavaScript Runtime là môi trường thực thi JavaScript, cung cấp tất cả các thành phần cần thiết để chạy mã JavaScript. Hiểu rõ về JavaScript Runtime là nền tảng quan trọng để viết code JavaScript hiệu quả và debug các vấn đề phức tạp.

---

## JavaScript Runtime là gì?

**JavaScript Runtime** là một môi trường phần mềm cung cấp các thành phần cần thiết để thực thi mã JavaScript. Nó bao gồm:

- **JavaScript Engine**: Thực thi và biên dịch mã JavaScript
- **Call Stack**: Quản lý việc thực thi các hàm
- **Heap**: Lưu trữ các object và biến
- **Event Loop**: Điều phối việc thực thi các tác vụ bất đồng bộ
- **Callback Queue**: Hàng đợi các callback chờ thực thi
- **Web APIs** (trong browser) hoặc **C++ APIs** (trong Node.js): Cung cấp các chức năng bất đồng bộ

---

## Các Thành Phần Chính của JavaScript Runtime

### Kiến Trúc Tổng Quan

```
┌─────────────────────────────────────────────────────────┐
│                    JavaScript Runtime                    │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐         ┌──────────────┐             │
│  │ Call Stack   │         │     Heap     │             │
│  │              │         │              │             │
│  │ - Functions  │         │ - Objects    │             │
│  │ - Variables  │         │ - Closures   │             │
│  └──────────────┘         └──────────────┘             │
│                                                          │
│  ┌──────────────────────────────────────────┐          │
│  │         Event Loop                       │          │
│  │  (Đồng bộ Call Stack và Callback Queue)  │          │
│  └──────────────────────────────────────────┘          │
│                                                          │
│  ┌──────────────┐         ┌──────────────┐             │
│  │ Callback     │         │   Web APIs   │             │
│  │ Queue        │         │              │             │
│  │              │         │ - setTimeout │             │
│  │ - Callbacks  │         │ - fetch      │             │
│  │ - Events     │         │ - DOM APIs   │             │
│  └──────────────┘         └──────────────┘             │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

![Run Time](./Screenshot%202025-11-06%20at%2021.50.48.png)

---

## JavaScript Engine

### Định Nghĩa

**JavaScript Engine** là một chương trình hoặc thư viện thực thi mã JavaScript. Nó chịu trách nhiệm:

- **Parsing**: Phân tích cú pháp mã JavaScript
- **Compilation**: Biên dịch mã thành bytecode hoặc machine code
- **Execution**: Thực thi mã đã biên dịch
- **Optimization**: Tối ưu hóa hiệu suất thực thi

### Các JavaScript Engine Phổ Biến

| Engine | Runtime | Mô Tả |
|--------|---------|-------|
| **V8** | Chrome, Node.js, Edge | Engine được phát triển bởi Google, sử dụng JIT compilation |
| **SpiderMonkey** | Firefox | Engine đầu tiên của JavaScript, được phát triển bởi Mozilla |
| **JavaScriptCore (Nitro)** | Safari | Engine của Apple, được sử dụng trong WebKit |
| **Chakra** | Edge (cũ) | Engine của Microsoft (đã được thay thế bằng V8) |

### Quy Trình Hoạt Động của Engine

```
Source Code
    ↓
[Parser] → AST (Abstract Syntax Tree)
    ↓
[Interpreter] → Bytecode
    ↓
[Compiler] → Optimized Machine Code
    ↓
Execution
```

---

## Call Stack (Ngăn Xếp Gọi)

### Định Nghĩa

**Call Stack** là một cấu trúc dữ liệu dạng stack (LIFO - Last In First Out) theo dõi các hàm đang được thực thi. Mỗi khi một hàm được gọi, nó được đẩy vào stack. Khi hàm hoàn thành, nó được lấy ra khỏi stack.

### Đặc Điểm

- **LIFO (Last In First Out)**: Hàm được gọi cuối cùng sẽ hoàn thành đầu tiên
- **Single-threaded**: Chỉ một hàm được thực thi tại một thời điểm
- **Synchronous**: Các hàm được thực thi tuần tự, từ trên xuống dưới

### Ví Dụ

```javascript
function first() {
    console.log('First function');
    second();
    console.log('First function - end');
}

function second() {
    console.log('Second function');
    third();
    console.log('Second function - end');
}

function third() {
    console.log('Third function');
}

first();
```

**Call Stack Flow:**

```
[empty]
    ↓
[first]          // first() được gọi
    ↓
[first, second]  // second() được gọi từ first()
    ↓
[first, second, third]  // third() được gọi từ second()
    ↓
[first, second]  // third() hoàn thành
    ↓
[first]          // second() hoàn thành
    ↓
[empty]          // first() hoàn thành
```

### Stack Overflow

Khi call stack vượt quá giới hạn, sẽ xảy ra lỗi **Stack Overflow**:

```javascript
function recursive() {
    recursive(); // Gọi đệ quy vô hạn
}

recursive(); // RangeError: Maximum call stack size exceeded
```

---

## Heap (Vùng Nhớ Động)

### Định Nghĩa

**Heap** là vùng nhớ không có cấu trúc, nơi lưu trữ các object, array, function, và các biến có kích thước lớn. Khác với Call Stack, Heap không có thứ tự cụ thể và được quản lý bởi Garbage Collector.

### Đặc Điểm

- **Unstructured**: Không có cấu trúc cố định
- **Dynamic Allocation**: Cấp phát bộ nhớ động
- **Garbage Collected**: Tự động giải phóng bộ nhớ không sử dụng
- **Reference-based**: Lưu trữ các object thông qua tham chiếu

### Ví Dụ

```javascript
// Object được lưu trong Heap
let person = {
    name: 'John',
    age: 30,
    address: {
        city: 'Hanoi',
        country: 'Vietnam'
    }
};

// Array được lưu trong Heap
let numbers = [1, 2, 3, 4, 5];

// Function được lưu trong Heap
function greet() {
    console.log('Hello!');
}
```

### Memory Layout

```
┌─────────────────┐
│   Call Stack    │  ← Biến primitive, tham chiếu
│                 │
│   person (ref)  │──┐
│   numbers (ref) │  │
└─────────────────┘  │
                     │
┌─────────────────┐  │
│      Heap       │  │
│                 │  │
│  {name, age}    │◄─┘
│  [1,2,3,4,5]    │
│  function(){}   │
└─────────────────┘
```

---

## Event Loop

### Định Nghĩa

**Event Loop** là cơ chế cho phép JavaScript thực hiện các tác vụ bất đồng bộ mặc dù JavaScript là ngôn ngữ single-threaded. Event Loop liên tục kiểm tra Call Stack và Callback Queue, đưa các callback từ queue vào stack khi stack trống.

### Cơ Chế Hoạt Động

```
1. Thực thi code đồng bộ trong Call Stack
2. Khi gặp code bất đồng bộ (setTimeout, fetch, etc.)
   → Gửi đến Web APIs
3. Web APIs xử lý và đưa callback vào Callback Queue
4. Event Loop kiểm tra:
   - Nếu Call Stack trống → Lấy callback từ Queue → Đưa vào Stack
   - Nếu Call Stack không trống → Chờ
5. Lặp lại từ bước 1
```

### Ví Dụ

```javascript
console.log('1. Start');

setTimeout(() => {
    console.log('2. Timeout');
}, 0);

console.log('3. End');
```

**Output:**
```
1. Start
3. End
2. Timeout
```

**Giải Thích:**
1. `console.log('1. Start')` được thực thi ngay
2. `setTimeout` được gửi đến Web APIs, callback được đưa vào Queue
3. `console.log('3. End')` được thực thi ngay
4. Call Stack trống, Event Loop đưa callback từ Queue vào Stack
5. `console.log('2. Timeout')` được thực thi

---

## Callback Queue (Hàng Đợi Callback)

### Định Nghĩa

**Callback Queue** (còn gọi là **Task Queue** hoặc **Message Queue**) là hàng đợi chứa các callback đang chờ được thực thi. Các callback được thêm vào queue bởi Web APIs sau khi hoàn thành tác vụ bất đồng bộ.

### Đặc Điểm

- **FIFO (First In First Out)**: Callback được thêm vào trước sẽ được thực thi trước
- **Asynchronous**: Chứa các callback từ các tác vụ bất đồng bộ
- **Event-driven**: Được kích hoạt bởi các sự kiện

### Các Loại Callback Queue

1. **Macrotask Queue**: setTimeout, setInterval, I/O operations
2. **Microtask Queue**: Promise.then(), queueMicrotask(), MutationObserver

---

## Web APIs (Browser APIs)

### Định Nghĩa

**Web APIs** là các API được cung cấp bởi trình duyệt, cho phép JavaScript tương tác với môi trường bên ngoài. Các API này chạy trên các thread riêng biệt, không chặn main thread.

### Các Web API Phổ Biến

| API | Mô Tả | Ví Dụ |
|-----|-------|-------|
| **DOM API** | Thao tác với DOM | `document.getElementById()` |
| **Fetch API** | Gửi HTTP requests | `fetch('/api/data')` |
| **setTimeout/setInterval** | Đặt lịch thực thi | `setTimeout(() => {}, 1000)` |
| **Geolocation API** | Lấy vị trí địa lý | `navigator.geolocation.getCurrentPosition()` |
| **LocalStorage API** | Lưu trữ dữ liệu local | `localStorage.setItem('key', 'value')` |
| **WebSocket API** | Kết nối WebSocket | `new WebSocket('ws://...')` |
| **Canvas API** | Vẽ đồ họa 2D | `canvas.getContext('2d')` |
| **Audio/Video API** | Xử lý media | `new Audio('sound.mp3')` |

### Ví Dụ

```javascript
// DOM API
const button = document.getElementById('myButton');
button.addEventListener('click', () => {
    console.log('Button clicked');
});

// Fetch API
fetch('https://api.example.com/data')
    .then(response => response.json())
    .then(data => console.log(data));

// setTimeout
setTimeout(() => {
    console.log('Delayed execution');
}, 1000);
```

---

## Microtask Queue và Macrotask Queue

### Sự Khác Biệt

JavaScript có **hai loại queue** với **ưu tiên khác nhau**:

#### 1. Microtask Queue (Ưu tiên cao)

- **Thực thi ngay** sau khi Call Stack trống
- **Ưu tiên cao hơn** Macrotask Queue
- **Ví dụ**: Promise.then(), queueMicrotask(), MutationObserver

#### 2. Macrotask Queue (Ưu tiên thấp)

- **Thực thi sau** Microtask Queue
- **Ví dụ**: setTimeout, setInterval, I/O operations, UI rendering

### Thứ Tự Thực Thi

```
1. Call Stack (code đồng bộ)
2. Microtask Queue (Promise, queueMicrotask)
3. Macrotask Queue (setTimeout, setInterval)
4. Render (UI update)
```

### Ví Dụ

```javascript
console.log('1. Start');

setTimeout(() => {
    console.log('2. setTimeout');
}, 0);

Promise.resolve().then(() => {
    console.log('3. Promise');
});

queueMicrotask(() => {
    console.log('4. queueMicrotask');
});

console.log('5. End');
```

**Output:**
```
1. Start
5. End
3. Promise
4. queueMicrotask
2. setTimeout
```

**Giải Thích:**
1. Code đồng bộ chạy trước: `1. Start`, `5. End`
2. Microtask Queue chạy tiếp: `3. Promise`, `4. queueMicrotask`
3. Macrotask Queue chạy cuối: `2. setTimeout`

---

## Memory Management (Quản Lý Bộ Nhớ)

### Tổng Quan

JavaScript sử dụng **automatic memory management**, nghĩa là developer không cần phải tự cấp phát và giải phóng bộ nhớ. Tuy nhiên, hiểu cách JavaScript quản lý bộ nhớ giúp tránh memory leaks.

### Vòng Đời Bộ Nhớ

```
1. Allocation (Cấp phát)
   ↓
2. Usage (Sử dụng)
   ↓
3. Release (Giải phóng)
```

### Các Loại Bộ Nhớ

#### 1. Stack Memory
- Lưu trữ biến primitive và tham chiếu
- Tự động giải phóng khi function kết thúc
- Nhanh và có giới hạn

#### 2. Heap Memory
- Lưu trữ object, array, function
- Được quản lý bởi Garbage Collector
- Chậm hơn nhưng linh hoạt hơn

### Memory Leaks (Rò Rỉ Bộ Nhớ)

#### 1. Global Variables

```javascript
// ❌ Memory leak
function createGlobal() {
    globalVar = "I'm global"; // Thiếu var/let/const
}

// ✅ Cách sửa
function createLocal() {
    let localVar = "I'm local";
}
```

#### 2. Event Listeners

```javascript
// ❌ Memory leak
function addListener() {
    const button = document.getElementById('myButton');
    button.addEventListener('click', function() {
        console.log('clicked');
    });
    // Event listener không được remove
}

// ✅ Cách sửa
function addListener() {
    const button = document.getElementById('myButton');
    const handler = function() {
        console.log('clicked');
    };
    button.addEventListener('click', handler);
    
    // Remove khi cần
    button.removeEventListener('click', handler);
}
```

#### 3. Closures

```javascript
// ❌ Memory leak tiềm ẩn
function outer() {
    const largeData = new Array(1000000).fill('data');
    return function inner() {
        console.log('inner');
        // largeData vẫn được giữ trong memory
    };
}

// ✅ Cách sửa: Giải phóng reference khi không cần
function outer() {
    const largeData = new Array(1000000).fill('data');
    return function inner() {
        console.log('inner');
    };
    // largeData sẽ được GC sau khi outer() kết thúc
}
```

#### 4. Timers

```javascript
// ❌ Memory leak
const intervalId = setInterval(() => {
    console.log('Running');
}, 1000);
// Không clear interval

// ✅ Cách sửa
const intervalId = setInterval(() => {
    console.log('Running');
}, 1000);

// Clear khi cần
clearInterval(intervalId);
```

---

## Garbage Collection (Thu Gom Rác)

### Định Nghĩa

**Garbage Collection (GC)** là quá trình tự động giải phóng bộ nhớ không còn được sử dụng. JavaScript engine sử dụng các thuật toán GC để quản lý bộ nhớ.

### Các Thuật Toán GC

#### 1. Mark and Sweep (Phổ biến nhất)

**Cơ chế:**
1. **Mark**: Đánh dấu tất cả các object có thể truy cập được
2. **Sweep**: Xóa các object không được đánh dấu

**Ưu điểm:**
- Xử lý được circular references
- Hiệu quả với heap lớn

**Ví dụ:**
```javascript
let obj1 = {};
let obj2 = {};
obj1.ref = obj2;
obj2.ref = obj1;

obj1 = null;
obj2 = null;
// Cả hai object sẽ được GC vì không thể truy cập được
```

#### 2. Reference Counting (Cũ, ít dùng)

**Cơ chế:**
- Đếm số lượng tham chiếu đến object
- Khi count = 0, object được giải phóng

**Nhược điểm:**
- Không xử lý được circular references
- Hiệu suất kém với object lớn

### Các Loại GC

#### 1. Minor GC (Young Generation)
- Thu gom objects tạm thời, có tuổi thọ ngắn
- Chạy thường xuyên và nhanh
- Sử dụng "Copying" algorithm

#### 2. Major GC (Old Generation)
- Thu gom objects có tuổi thọ dài
- Chạy ít thường xuyên hơn nhưng chậm hơn
- Sử dụng "Mark and Sweep" algorithm

### Tối Ưu Hóa GC

```javascript
// ❌ Tạo nhiều object không cần thiết
function processData(data) {
    for (let i = 0; i < data.length; i++) {
        const obj = { index: i, value: data[i] };
        // obj được tạo và hủy liên tục
    }
}

// ✅ Tái sử dụng object
function processData(data) {
    const obj = {};
    for (let i = 0; i < data.length; i++) {
        obj.index = i;
        obj.value = data[i];
        // Tái sử dụng cùng một object
    }
}
```

---

## Các Loại JavaScript Runtime

### 1. Browser Runtime

**Môi trường:** Trình duyệt web (Chrome, Firefox, Safari, Edge)

**Đặc điểm:**
- Có **DOM API** để thao tác với HTML
- Có **BOM (Browser Object Model)** để tương tác với trình duyệt
- Có **Web APIs** (fetch, localStorage, etc.)
- **Sandboxed**: Bị giới hạn bởi security policies

**Ví dụ:**
```javascript
// Browser-specific APIs
document.getElementById('myElement');
window.location.href = 'https://example.com';
localStorage.setItem('key', 'value');
```

### 2. Node.js Runtime

**Môi trường:** Server-side, command line

**Đặc điểm:**
- **Không có DOM**: Không thể truy cập document, window
- Có **File System API**: Đọc/ghi file
- Có **Network APIs**: Tạo server, kết nối database
- Có **Process API**: Tương tác với hệ điều hành

**Ví dụ:**
```javascript
// Node.js-specific APIs
const fs = require('fs');
const http = require('http');
process.env.NODE_ENV;
```

### 3. Deno Runtime

**Môi trường:** Modern JavaScript/TypeScript runtime

**Đặc điểm:**
- **Security by default**: Cần permission rõ ràng
- **Built-in TypeScript**: Hỗ trợ TypeScript natively
- **Standard library**: Không cần npm
- **Web-compatible APIs**: Sử dụng Web Standards

**Ví dụ:**
```javascript
// Deno-specific APIs
const file = await Deno.readTextFile('data.txt');
const response = await fetch('https://api.example.com');
```

### 4. Bun Runtime

**Môi trường:** Fast JavaScript runtime

**Đặc điểm:**
- **Extremely fast**: Được viết bằng Zig
- **Built-in bundler**: Không cần webpack
- **Native TypeScript**: Hỗ trợ TypeScript
- **Compatible**: Tương thích với Node.js và browser APIs

---

## Concurrency Model (Mô Hình Đồng Thời)

### Single-Threaded vs Multi-Threaded

**JavaScript là single-threaded**, nghĩa là chỉ có một thread thực thi code tại một thời điểm. Tuy nhiên, JavaScript có thể xử lý các tác vụ bất đồng bộ thông qua:

- **Event Loop**: Điều phối các tác vụ
- **Web Workers**: Chạy code trên thread riêng
- **Async/Await**: Cú pháp cho code bất đồng bộ

### Event-Driven Architecture

JavaScript sử dụng **event-driven architecture**:

```javascript
// Event-driven programming
button.addEventListener('click', handleClick);
window.addEventListener('load', handleLoad);
document.addEventListener('DOMContentLoaded', handleDOMReady);
```

### Web Workers

**Web Workers** cho phép chạy JavaScript trên thread riêng:

```javascript
// main.js
const worker = new Worker('worker.js');
worker.postMessage('Hello from main thread');
worker.onmessage = (e) => {
    console.log('Message from worker:', e.data);
};

// worker.js
self.onmessage = (e) => {
    console.log('Message from main:', e.data);
    self.postMessage('Hello from worker thread');
};
```

---

## Execution Context (Ngữ Cảnh Thực Thi)

### Định Nghĩa

**Execution Context** là môi trường trong đó JavaScript code được thực thi. Mỗi khi một function được gọi, một execution context mới được tạo.

### Các Loại Execution Context

#### 1. Global Execution Context
- Được tạo khi script bắt đầu chạy
- Chỉ có một global context trong mỗi program
- Chứa global variables và functions

#### 2. Function Execution Context
- Được tạo mỗi khi function được gọi
- Có thể có nhiều function contexts
- Chứa local variables và parameters

#### 3. Eval Execution Context
- Được tạo khi code trong `eval()` được thực thi
- Ít được sử dụng

### Cấu Trúc Execution Context

```
Execution Context
├── Variable Environment
│   ├── let, const, var declarations
│   └── function declarations
├── Lexical Environment
│   ├── Outer environment reference
│   └── Environment record
├── This Binding
└── Scope Chain
```

### Ví Dụ

```javascript
let globalVar = 'global';

function outer() {
    let outerVar = 'outer';
    
    function inner() {
        let innerVar = 'inner';
        console.log(globalVar, outerVar, innerVar);
    }
    
    inner();
}

outer();
```

**Execution Context Stack:**
```
[Global Context]
    ↓
[Global Context, Outer Context]
    ↓
[Global Context, Outer Context, Inner Context]
```

---

## Hoisting và Scope

### Hoisting

**Hoisting** là cơ chế JavaScript di chuyển các khai báo lên đầu scope trước khi thực thi code.

#### Function Hoisting

```javascript
// Function declaration được hoist
sayHello(); // ✅ Hoạt động

function sayHello() {
    console.log('Hello');
}
```

#### Variable Hoisting

```javascript
// var được hoist nhưng không được khởi tạo
console.log(x); // undefined (không phải ReferenceError)
var x = 5;

// let/const được hoist nhưng trong "Temporal Dead Zone"
console.log(y); // ReferenceError
let y = 5;
```

### Scope

**Scope** xác định phạm vi truy cập của biến.

#### 1. Global Scope

```javascript
let globalVar = 'global';

function test() {
    console.log(globalVar); // ✅ Có thể truy cập
}
```

#### 2. Function Scope

```javascript
function test() {
    let functionVar = 'function';
    console.log(functionVar); // ✅ Có thể truy cập
}

console.log(functionVar); // ❌ ReferenceError
```

#### 3. Block Scope

```javascript
if (true) {
    let blockVar = 'block';
    console.log(blockVar); // ✅ Có thể truy cập
}

console.log(blockVar); // ❌ ReferenceError
```

---

## Closures (Đóng Gói)

### Định Nghĩa

**Closure** là khả năng của function truy cập các biến từ scope bên ngoài ngay cả sau khi function bên ngoài đã kết thúc.

### Ví Dụ Cơ Bản

```javascript
function outer() {
    let outerVar = 'I am outside!';
    
    function inner() {
        console.log(outerVar); // Truy cập outerVar từ outer scope
    }
    
    return inner;
}

const myFunction = outer();
myFunction(); // "I am outside!"
```

### Ứng Dụng

#### 1. Data Privacy

```javascript
function createCounter() {
    let count = 0; // Private variable
    
    return {
        increment: () => ++count,
        decrement: () => --count,
        getCount: () => count
    };
}

const counter = createCounter();
console.log(counter.getCount()); // 0
counter.increment();
console.log(counter.getCount()); // 1
// count không thể truy cập trực tiếp từ bên ngoài
```

#### 2. Function Factories

```javascript
function createMultiplier(multiplier) {
    return function(number) {
        return number * multiplier;
    };
}

const double = createMultiplier(2);
const triple = createMultiplier(3);

console.log(double(5)); // 10
console.log(triple(5)); // 15
```

---

## This Binding

### Định Nghĩa

**this** là một keyword đặc biệt trong JavaScript, tham chiếu đến object mà function đang được gọi.

### Các Cách Bind This

#### 1. Default Binding

```javascript
function greet() {
    console.log(this); // Window (browser) hoặc global (Node.js)
}

greet();
```

#### 2. Implicit Binding

```javascript
const person = {
    name: 'John',
    greet: function() {
        console.log(this.name); // 'John'
    }
};

person.greet();
```

#### 3. Explicit Binding

```javascript
function greet() {
    console.log(this.name);
}

const person = { name: 'John' };

greet.call(person);    // 'John'
greet.apply(person);   // 'John'
const boundGreet = greet.bind(person);
boundGreet();          // 'John'
```

#### 4. New Binding

```javascript
function Person(name) {
    this.name = name;
}

const john = new Person('John');
console.log(john.name); // 'John'
```

#### 5. Arrow Functions

```javascript
const person = {
    name: 'John',
    greet: () => {
        console.log(this.name); // undefined (không có this binding)
    },
    greetRegular: function() {
        const arrow = () => {
            console.log(this.name); // 'John' (lexical this)
        };
        arrow();
    }
};
```

---

## Prototype Chain

### Định Nghĩa

**Prototype Chain** là cơ chế JavaScript sử dụng để kế thừa properties và methods từ các object khác.

### Prototype

Mỗi object trong JavaScript có một **prototype**, là một object khác mà nó kế thừa properties và methods.

```javascript
const obj = {};
console.log(obj.toString); // [Function: toString] - từ Object.prototype
```

### Prototype Chain

```javascript
function Person(name) {
    this.name = name;
}

Person.prototype.greet = function() {
    return `Hello, I'm ${this.name}`;
};

const john = new Person('John');
console.log(john.greet()); // "Hello, I'm John"

// Prototype chain: john → Person.prototype → Object.prototype → null
```

### Inheritance

```javascript
function Animal(name) {
    this.name = name;
}

Animal.prototype.speak = function() {
    console.log(`${this.name} makes a sound`);
};

function Dog(name, breed) {
    Animal.call(this, name);
    this.breed = breed;
}

Dog.prototype = Object.create(Animal.prototype);
Dog.prototype.constructor = Dog;

Dog.prototype.speak = function() {
    console.log(`${this.name} barks`);
};

const dog = new Dog('Buddy', 'Golden Retriever');
dog.speak(); // "Buddy barks"
```

---

## Error Handling

### Try-Catch-Finally

```javascript
try {
    // Code có thể gây lỗi
    const result = riskyOperation();
    console.log(result);
} catch (error) {
    // Xử lý lỗi
    console.error('Error:', error.message);
} finally {
    // Luôn được thực thi
    console.log('Cleanup');
}
```

### Error Types

```javascript
// SyntaxError
const x = ; // SyntaxError

// ReferenceError
console.log(undefinedVar); // ReferenceError

// TypeError
null.someMethod(); // TypeError

// RangeError
new Array(-1); // RangeError
```

### Custom Errors

```javascript
class CustomError extends Error {
    constructor(message, code) {
        super(message);
        this.name = 'CustomError';
        this.code = code;
    }
}

try {
    throw new CustomError('Something went wrong', 500);
} catch (error) {
    if (error instanceof CustomError) {
        console.error(`Error ${error.code}: ${error.message}`);
    }
}
```

---

## Performance Optimization

### 1. Avoid Global Variables

```javascript
// ❌ Chậm
var globalVar = 'value';
function test() {
    return globalVar;
}

// ✅ Nhanh hơn
function test() {
    const localVar = 'value';
    return localVar;
}
```

### 2. Use const và let thay vì var

```javascript
// ✅ Tốt hơn
const PI = 3.14159;
let counter = 0;
```

### 3. Minimize DOM Access

```javascript
// ❌ Chậm
for (let i = 0; i < 1000; i++) {
    document.getElementById('element').innerHTML += i;
}

// ✅ Nhanh hơn
const element = document.getElementById('element');
let html = '';
for (let i = 0; i < 1000; i++) {
    html += i;
}
element.innerHTML = html;
```

### 4. Debounce và Throttle

```javascript
// Debounce
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Throttle
function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}
```

### 5. Lazy Loading

```javascript
// Lazy load images
const images = document.querySelectorAll('img[data-src]');
const imageObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const img = entry.target;
            img.src = img.dataset.src;
            observer.unobserve(img);
        }
    });
});

images.forEach(img => imageObserver.observe(img));
```

---

## Best Practices

### 1. Sử dụng Strict Mode

```javascript
'use strict';

// Giúp phát hiện lỗi sớm
// Ngăn sử dụng biến chưa khai báo
// Ngăn xóa properties không thể xóa
```

### 2. Tránh Memory Leaks

```javascript
// ✅ Luôn cleanup
const button = document.getElementById('button');
const handler = () => console.log('clicked');
button.addEventListener('click', handler);

// Cleanup khi không cần
button.removeEventListener('click', handler);
```

### 3. Sử dụng Async/Await

```javascript
// ✅ Dễ đọc hơn
async function fetchData() {
    try {
        const response = await fetch('/api/data');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error:', error);
    }
}
```

### 4. Code Organization

```javascript
// ✅ Tổ chức code rõ ràng
// utils.js
export function formatDate(date) {
    // ...
}

// api.js
export async function fetchUser(id) {
    // ...
}

// main.js
import { formatDate } from './utils.js';
import { fetchUser } from './api.js';
```

### 5. Error Handling

```javascript
// ✅ Luôn xử lý lỗi
async function processData() {
    try {
        const data = await fetchData();
        return process(data);
    } catch (error) {
        console.error('Processing failed:', error);
        throw error; // Re-throw nếu cần
    }
}
```

---

## Tài Liệu Tham Khảo

### Tài Liệu Chính Thức

- [MDN Web Docs - JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
- [ECMAScript Specification](https://tc39.es/ecma262/)
- [V8 Engine Blog](https://v8.dev/blog)
- [Node.js Documentation](https://nodejs.org/docs/)

### Bài Viết và Hướng Dẫn

- [JavaScript.info - The Modern JavaScript Tutorial](https://javascript.info/)
- [Philip Roberts: What the heck is the event loop?](https://www.youtube.com/watch?v=8aGhZQkoFbQ)
- [Jake Archibald: In The Loop](https://www.youtube.com/watch?v=cCOL7MC4Pl0)

### Công Cụ Debug

- [Chrome DevTools](https://developer.chrome.com/docs/devtools/)
- [Firefox Developer Tools](https://developer.mozilla.org/en-US/docs/Tools)
- [Node.js Inspector](https://nodejs.org/en/docs/guides/debugging-getting-started/)

### Performance Tools

- [Chrome Performance Profiler](https://developer.chrome.com/docs/devtools/performance/)
- [Memory Profiler](https://developer.chrome.com/docs/devtools/memory-problems/)
- [Lighthouse](https://developers.google.com/web/tools/lighthouse)

---

## Kết Luận

JavaScript Runtime là một hệ thống phức tạp nhưng mạnh mẽ, cho phép JavaScript thực thi code hiệu quả và xử lý các tác vụ bất đồng bộ. Hiểu rõ về các thành phần như Call Stack, Heap, Event Loop, và Garbage Collection giúp developers viết code tốt hơn, debug hiệu quả hơn, và tối ưu hóa performance.

**Những điểm quan trọng cần nhớ:**

1. JavaScript là **single-threaded** nhưng có thể xử lý **asynchronous operations** thông qua Event Loop
2. **Call Stack** quản lý việc thực thi các hàm đồng bộ
3. **Event Loop** điều phối việc thực thi các callback bất đồng bộ
4. **Garbage Collector** tự động quản lý bộ nhớ, nhưng cần tránh memory leaks
5. **Microtask Queue** có ưu tiên cao hơn **Macrotask Queue**
6. Hiểu rõ **Execution Context**, **Scope**, và **Closures** giúp viết code tốt hơn

---

**Tác giả:** JavaScript Tutorial Series  
**Cập nhật:** 2025  
**Phiên bản:** 1.0

