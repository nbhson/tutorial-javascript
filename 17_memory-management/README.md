# Quản lý bộ nhớ và hiệu năng — [Level: Intermediate]

## 🔑 Khái niệm cốt lõi

JavaScript quản lý bộ nhớ **tự động** thông qua cơ chế **Garbage Collection (GC)**. Khi bạn tạo biến, object, hàm — dữ liệu được đặt lên bộ nhớ (heap). Khi không còn dùng nữa, engine tự động dọn bằng thuật toán **Mark & Sweep**. Tuy nhiên, developer vẫn có thể vô tình tạo **memory leak** nếu giữ tham chiếu không cần thiết, khiến GC không thể thu hồi.

Các mảng kiến thức trọng tâm:

### Stack vs Heap
- **Stack**: lưu giá trị nguyên thủy (number, string, boolean, null, undefined, symbol, bigint) và **tham chiếu** (reference) đến object. Kích thước cố định, truy cập nhanh.
- **Heap**: lưu object, array, function. Cấp phát động, kích thước thay đổi, được GC quản lý. Biến chứa object chỉ giữ "địa chỉ" trỏ vào heap, không phải bản sao dữ liệu.

```js
let a = 42;           // 42 nằm trên stack (nguyên thủy)
let b = { x: 10 };    // { x: 10 } nằm trên heap, b giữ reference (địa chỉ)
let c = b;            // c cũng trỏ cùng địa chỉ trên heap — không copy object
b.x = 20;
console.log(c.x);     // 20 — vì b và c trỏ cùng object
```

### Vòng đời bộ nhớ
Mọi chương trình đều trải qua 3 bước:
1. **Allocate (cấp phát)**: biến, object, hàm được cấp vùng nhớ khi khai báo/tạo.
2. **Use (sử dụng)**: đọc, ghi, truy cập dữ liệu.
3. **Release (giải phóng)**: trả vùng nhớ về hệ thống khi không dùng nữa — do GC làm.

### GC — Mark & Sweep
Engine xuất phát từ các **root** (biến toàn cục, call stack, DOM hiển thị, module exports...) rồi **đánh dấu (mark)** mọi object reachable. Phần không reachable bị **quét sạch (sweep)**. Khác với reference counting (đếm tham chiếu — bó tay với circular reference), mark & sweep loại bỏ cả vòng tròn tham chiếu.

### V8 Engine Pipeline
V8 (Chrome/Node) chạy theo pipeline: **Parser → Ignition (bytecode) → TurboFan (JIT machine code)**. Với **hidden class** (class ẩn) và **inline caching** — truy cập property gần ngang ngôn ngữ tĩnh.

### Metaprogramming
`Proxy` và `Reflect` cho phép can thiệp hành vi object (validation, log, computed property, reactivity...) — kỹ thuật nâng cao thường đi kèm các bài toán về hiệu năng/động.

Cấu trúc thư mục:
- `01_memory-lifecycle-gc/` — vòng đời bộ nhớ, GC, các loại memory leak.
- `03_v8-engine/` — cách V8 thực thi tối ưu JavaScript.
- `04_meta-programming/` — Proxy / Reflect.

## ✅ Điểm mạnh

1. **Hiểu vòng đời bộ nhớ** giúp viết code không rò rỉ, ổn định khi chạy lâu — biết khi nào phải cắt tham chiếu.
2. **Nắm GC (Mark & Sweep)** tự tin dùng closure, listener, cache — biết khi nào dữ liệu được giải phóng thực sự.
3. **Hiểu V8 + hidden class/inline cache** giúp viết code "thân thiện JIT", tránh deopt hay tạo shape object rời rạc.
4. **WeakMap/WeakSet** cho cache an toàn — mục GC thu hồi tự do khi key hết reference.
5. **Proxy/Reflect** mở ra reactivity, validation, logging mà không sửa code gốc — kỹ năng framework-level.
6. **DevTools Memory** cho phép chụp heap snapshot, so sánh trước/sau để tìm leak chính xác.
7. **Performance.memory API** (Chrome) cho monitor heap usage real-time — useful cho debugging.
8. **Node `--expose-gc`** cho phép ép GC thủ công trong test environment.

## ⚠️ Bẫy thường gặp & Hạn chế

1. **Không có API JS thống nhất để ép GC** — chỉ đoán được qua snapshot, `performance.memory` (Chrome), `--expose-gc` (Node).
2. **Chỉ dùng `performance.memory` được trên Chrome/Chromium** — không tiêu chuẩn, không có trên Firefox/Safari.
3. **`used ≤ total ≤ limit`** — `usedJSHeapSize` giảm chậm (GC trễ đến lúc idle), `totalJSHeapSize` thường giữ capacity.
4. **Proxy làm úp mở hành vi** — gỡ lỗi khó; hidden class mất ổn định (deopt) khi thêm/xóa property không nhất quán.
5. **GC không chạy ngay** — memory giảm sau vài giây, hoặc chờ "Take Heap Snapshot" mới thấy rõ.
6. **Circular reference không phải lúc nào cũng leak** — mark & sweep xử lý được, chỉ leak khi vẫn còn đường từ root.

## 💡 Khi nào dùng — Tình huống thực tế

1. **Kiểm tra/sửa memory leak** trong SPA chạy lâu — danh sách không lọc, tab chuyển qua lại, toast accumulate.
2. **Tối ưu render/reflow** cho ứng dụng lớn — giảm tần suất can thiệp trực tiếp vào DOM.
3. **Viết thư viện/framework** cần kiểm soát bộ nhớ, cache, hoặc phản ứng với dữ liệu (reactivity).
4. **Xử lý dữ liệu lớn** (stream, bảng dài) — tránh giữ toàn bộ trong bộ nhớ, dùng WeakMap thay Map.
5. **Metaprogramming**: proxy-validate input, biến object thành reactive, tạo "computed property".
6. **Benchmark performance** — đo hidden class impact, inline cache hit rate qua `--trace-opt`.
7. **Debug detached DOM** — node bị gỡ khỏi trang nhưng JS vẫn giữ reference → tìm qua heap snapshot.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Leak qua global variable (quên let/const)
```js
function leak() {
  globalArr = new Array(1e6).fill(0); // ❌ thiếu var/let/const → biến global
}
leak();
// globalArr tồn tại mãi, GC không thể dọn
```

### Ví dụ 2: GC dọn được circular reference
```js
const a = {}, b = {};
a.ref = b;
b.ref = a;
// Khi không còn tham chiếu từ root:
a = null;
b = null;
// Mark & Sweep: cả a và b đều unreachable → GC thu hồi
```

### Ví dụ 3: WeakMap — cache an toàn
```js
const cache = new WeakMap();
let key = { id: 1 };
cache.set(key, "cached value");
key = null; // key hết reference → entry trong WeakMap sẵn sàng bị GC thu hồi
// Không giống Map — Map giữ key mạnh, WeakMap giữ key yếu
```

### Ví dụ 4: Event listener leak
```js
const btn = document.getElementById('btn');
const handler = () => console.log('click');
btn.addEventListener('click', handler);
// Quên removeEventListener khi component unmount → handler + closure giữ mãi
btn.removeEventListener('click', handler); // ✅ phải gọi khi không cần
```

### Ví dụ 5: Closure giữ data lớn
```js
function create() {
  const bigData = new Array(1e6).fill('x'); // dữ liệu lớn
  return function() {
    console.log('sum', bigData.length);      // closure giữ bigData
  };
}
const cb = create();  // bigData được giữ mãi theo cb — dù create() đã return
// Fix: nếu cb không cần bigData sau khi init, null nó trong closure
```

### Ví dụ 6: Timer leak
```js
const id = setInterval(() => {
  console.log('tick');
}, 1000);
// Quên clearInterval → tick mãi, callback + closure giữ mọi thứ
clearInterval(id); // ✅ gọi khi component unmount
```

### Ví dụ 7: Hidden class pattern (V8 optimization)
```js
// Tạo object đồng dạng → cùng hidden class → access nhanh
function Person(name, age) {
  this.name = name;  // offset 0
  this.age = age;    // offset 1
}
const p1 = new Person('Alice', 30);
const p2 = new Person('Bob', 25);
// p1 và p2 cùng shape → V8 tái sử dụng hidden class

// Hỏng: thêm property khác thứ tự
const p3 = new Person('Carol', 28);
p3.city = 'Hanoi'; // tạo hidden class mới cho p3 → deopt
```

### Ví dụ 8: Proxy reactivity cơ bản
```js
const state = { count: 0 };
const proxy = new Proxy(state, {
  set(target, key, value) {
    console.log(`set ${key} = ${value}`);
    target[key] = value;
    updateUI(); // tự động cập nhật UI
    return true;
  }
});
proxy.count++; // set count = 1 → UI tự cập nhật
```

## 🔬 So sánh với alternatives

| Cách tiếp cận | Ưu điểm | Nhược điểm | Khi nào chọn |
|---|---|---|---|
| **Thuần JS GC** | Không cần config, tự động | Khó kiểm soát exact timing | App thông thường |
| **WeakMap cache** | Auto GC khi key hết ref | Chỉ accept object key | Cache theo object |
| **Manual null** | Kiểm soát được | Dễ quên, buggy | Tài nguyên lớn, lifecycle rõ |
| **Objec pool** | Tái sử dụng, giảm allocate | Phức tạp, phải quản lý | Performance-critical path |
| **Disposable pattern** | Rõ ràng, testable | Boilerplate thêm | Framework, library |

## 📊 Performance & Best Practices

- **Đo trước khi sửa**: luôn có baseline từ heap snapshot hoặc `performance.memory` trước khi optimize.
- **Avoid allocations in hot loops**: tạo object mới trong vòng lặp dày → GC pressure → jank.
- **Use typed arrays** cho số: `Int32Array` nhanh hơn `Array<number>` và ít GC pressure hơn.
- **Dispose pattern**: component unmount → clear all timers, remove all listeners, null all refs.
- **WeakMap over Map for caches**: khi key là object và muốn GC tự dọn.
- **Batch DOM mutations**: dùng `DocumentFragment` hoặc `innerHTML` batch thay vì append từng node.
- **Monitor trong dev**: DevTools Memory tab — take snapshot trước/sau action, so sánh retained size.
- **Production tip**: `performance.getEntriesByType('memory')` đọc heap stats trên Chrome.

## 🔗 Liên kết chéo

- Xem thêm: `17_memory-management/01_memory-lifecycle-gc/` — chi tiết GC và vòng đời bộ nhớ.
- Xem thêm: `17_memory-management/01_memory-lifecycle-gc/01_garbage-collection/` — demo GC đầy đủ.
- Xem thêm: `17_memory-management/01_memory-lifecycle-gc/02_memory-leaks/` — 4 pattern leak kinh điển.
- Xem thêm: `17_memory-management/03_v8-engine/` — hidden class, inline cache, JIT pipeline.
- Xem thêm: `17_memory-management/04_meta-programming/` — Proxy/Reflect cho reactivity.
- Xem thêm: `19_browser-devtools/01_devtools-memory/` — thực hành heap snapshot tìm leak.
- Xem thêm: `18_dom-apis/` — detached DOM nodes và memory leak trong SPA.
