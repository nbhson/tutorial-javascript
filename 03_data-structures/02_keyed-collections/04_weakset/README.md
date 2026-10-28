# WeakSet — Set Của Object References Yếu

> WeakSet: chỉ chứa object, weak reference -> GC-friendly. Không iterable.

## Khái niệm cốt lõi

```js
const ws = new WeakSet();
ws.add({});      // OK
ws.add([]);      // OK
ws.add(function(){}); // OK
ws.add(null);    // TypeError
ws.add('str');   // TypeError
```

WeakSet là "hộp kiểm" (marker box): bạn chỉ có thể hỏi **"object này có trong hộp không?"** (`has`), thêm vào (`add`), hoặc bỏ ra (`delete`) — không liệt kê, không đếm, không đọc nội dung. Khi object bị GC, nó tự rời khỏi hộp.

Cách hình dung dễ nhất: WeakSet = WeakMap mà value luôn là `true`:

```js
// 2 dòng này tương đương về mặt ngữ nghĩa
const ws = new WeakSet();
ws.add(obj);

const wm = new WeakMap();
wm.set(obj, true);
```

Vì vậy câu hỏi "khi nào dùng WeakSet thay vì WeakMap?" có câu trả lời đơn giản: **khi bạn không cần gắn dữ liệu, chỉ cần đánh dấu**.

### Khác Set

| | Set | WeakSet |
|---|---|---|
| Value type | Any | Object only |
| Iterable | Yes | No |
| .size | Yes | No |
| add/delete/has | Yes | Yes |
| GC-friendly | No | Yes |
| Memory leak risk | Có (strong refs) | Không |

## Điểm mạnh

- Không memory leak — object được GC thu hồi tự động
- Perfect để tracking visited objects không rò rỉ
- Ideal cho observer/cleanup patterns

## Bẫy thường gặp

- Không iterate được, không xem được contents
- Không lấy được size
- Chỉ có thể add/remove/check has
- Object cùng structure nhưng khác reference = 2 entries
- Không lưu được primitive (string, number) — TypeError, không phải silent fail

```js
// Bẫy: tưởng rằng có thể "xem" WeakSet để debug
const ws = new WeakSet();
ws.add({ a: 1 });
console.log(ws);           // WeakSet {} — không nhìn thấy gì
console.log([...ws]);      // TypeError: ws is not iterable
// Debug duy nhất khả dĩ: ws.has(ObjRef) với chính ObjRef bạn đang giữ
```

## Khi nào dùng

- Cycle detection trong graph traversal (recursive)
- Track visited DOM nodes tránh xử lý repeat
- Observer pattern metadata without leaking
- Cache với automatic cleanup

## Ví dụ 1: Cycle detection trong object graph

```js
// Cycle detection trong object graph
function hasCycle(obj, visited = new WeakSet()) {
  if (typeof obj !== 'object' || obj === null) return false;
  if (visited.has(obj)) return true;
  visited.add(obj);
  return Object.values(obj).some(v => hasCycle(v, visited));
}

const obj = { a: 1 };
obj.self = obj; // circular
console.log(hasCycle(obj)); // true
```

Tại sao phải là WeakSet chứ không phải Set? Trong graph lớn (ví dụ đang traverse toàn bộ state tree), Set sẽ giữ strong reference tới **mọi node đã đi qua** trong suốt thời gian chạy hàm — làm nặng heap và ngược tinh thần "traverse" (bạn vô hiệu hóa GC trong lúc duyệt). WeakSet đánh dấu mà không giữ chặt.

Ứng dụng thực tế của pattern này: `JSON.stringify` bị throw khi gặp circular reference — bạn có thể dùng chính WeakSet trên để kiểm tra trước, hoặc viết hàm serialize an toàn:

```js
function safeStringify(value, seen = new WeakSet()) {
  if (typeof value === "object" && value !== null) {
    if (seen.has(value)) return "[Circular]";
    seen.add(value);
    return Object.fromEntries(
      Object.entries(value).map(([k, v]) => [k, safeStringify(v, seen)])
    );
  }
  return value;
}

const node = { name: "root" };
node.child = { parent: node };
console.log(JSON.stringify(safeStringify(node))); // không throw
```

## Ví dụ 2: DOM node tracking — auto cleanup

```js
// DOM node tracking — auto cleanup
const trackedElements = new WeakSet();

function track(el) {
  trackedElements.add(el);
  el.addEventListener('click', () => {
    if (trackedElements.has(el)) {
      console.log('clicked tracked element');
    }
  });
}

document.querySelectorAll('.watch').forEach(track);
// Khi el bị remove từ DOM và không còn ref -> WeakSet entry tự GC
```

Use case điển hình: một thư viện widget đánh dấu "element này tôi đã init rồi" để không init hai lần. Với Set thường, các element bị remove khỏi DOM vẫn bị giữ trong Set mãi → leak. WeakSet: element remove + không còn biến nào tham chiếu → tự sạch.

## Ví dụ 3: Guard "chỉ xử lý mỗi object một lần"

```js
const processed = new WeakSet();

function processNode(el) {
  if (processed.has(el)) return; // idempotent — gọi nhiều lần vô hại
  processed.add(el);
  initWidget(el);
}

// An toàn khi gọi lại, ví dụ do MutationObserver bắn nhiều lần
const observer = new MutationObserver((mutations) => {
  document.querySelectorAll(".widget:not(.ready)").forEach(processNode);
});
observer.observe(document.body, { childList: true, subtree: true });
```

Đây là cách nhiều thư viện lightweight (lazy-load, intersection helper) chống double-init mà không cần ghi attribute lên element (`data-initialized="true"` cũng được, nhưng WeakMap/WeakSet "sạch" hơn — không bẩn DOM markup).

## WeakSet vs WeakMap vs Set — chọn nhanh

| Tình huống | Chọn |
|---|---|
| Đánh dấu object "đã xử lý", không cần dữ liệu kèm | **WeakSet** |
| Đánh dấu + gắn dữ liệu (metadata) | **WeakMap** |
| Cần liệt kê/đếm mọi phần tử đánh dấu | Set/Map (chấp nhận quản lý cleanup tay) |
| Đánh dấu giá trị primitive | Set (primitive không thể là weak key) |

## Ghi chú: WeakRef & FinalizationRegistry

WeakSet thuộc "họ weak reference" cùng WeakMap, WeakRef và FinalizationRegistry. Cặp WeakRef/FinalizationRegistry (ES2021) cho phép giữ tham chiếu yếu tự do hơn và nhận callback khi object bị GC — trình bày chi tiết trong overview nhóm (`03_data-structures/02_keyed-collections/README.md`) và mirror js-info (`js-info/vi/14_misc/weakref-finalizationregistry/`). Nguyên tắc chung của cả họ: **weak reference là tối ưu bộ nhớ, không phải công cụ cleanup logic** — đừng dựa vào GC để đóng connection hay xóa file.

## Ví dụ 4: Khi nào WeakSet là lựa chọn SAI

Hiểu giới hạn giúp bạn không cố "xoay" WeakSet làm việc nó không thiết kế để làm:

```js
// ❌ Cần đếm có bao nhiêu object đang được track? Không có .size.
// → Nếu cần đếm, nghĩa là bạn cần "sở hữu" các object → đó là Set, không phải WeakSet.

// ❌ Cần xuất danh sách ra JSON hoặc gửi lên server? Không liệt kê được.
// → WeakSet chỉ có nghĩa khi object sống trong cùng runtime của bạn.

// ❌ Cần lưu cấu hình kèm theo mỗi object?
// → WeakMap (có value), hoặc Map nếu cần duyệt.

// ✅ Đúng chỗ của WeakSet: "đánh dấu rồi quên" — marker, guard, chống double-init,
//    cycle detection — nơi bạn KHÔNG bao giờ cần đếm hay liệt kê.
```

Một cách nhớ nhanh: **Set là "danh sách" (bạn sở hữu), WeakSet là "bảng theo dõi" (object tự quản lý sự sống còn của chính nó)**.

## Checklist tự kiểm tra

- [ ] Biết WeakSet chỉ chứa object, không chứa primitive
- [ ] Hiểu WeakSet ≈ WeakMap với value luôn là true — chọn theo nhu cầu có/không cần dữ liệu kèm
- [ ] Viết được cycle detection bằng WeakSet
- [ ] Dùng được WeakSet làm guard chống double-init
- [ ] Biết WeakSet không iterate/đếm được — và vì sao đó là thiết kế có chủ đích

## Liên kết chéo

- Xem: `03_data-structures/02_keyed-collections/02_weakmap` (WeakMap)
- Xem: `17_memory-management/01_memory-lifecycle-gc` (GC principles)
- Xem: `03_data-structures/02_keyed-collections/03_set` (Set comparison)
- Tài liệu: [MDN — WeakSet](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/WeakSet)
