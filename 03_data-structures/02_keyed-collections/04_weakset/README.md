# WeakSet — Set Cua Object References Yeu

> WeakSet: chi chua object, weak reference -> GC-friendly. Khong iterable.

## Khái niệm cốt lõi

```js
const ws = new WeakSet();
ws.add({});      // OK
ws.add([]);      // OK
ws.add(function(){}); // OK
ws.add(null);    // TypeError
ws.add('str');   // TypeError
```

### Khac Set

| | Set | WeakSet |
|---|---|---|
| Value type | Any | Object only |
| Iterable | Yes | No |
| .size | Yes | No |
| add/delete/has | Yes | Yes |
| GC-friendly | No | Yes |
| Memory leak risk | Co (strong refs) | Khong |

## Điểm mạnh

- Khong memory leak — object duoc GC thu hoi tu dong
- Perfect для tracking visited objects без утечек
- Ideal cho observer/cleanup patterns

## Bẫy thường gặp

- Khong iterate duoc, не видно contents
- Нельзя получить size
-只能 add/remove/check has
- Object cung structure nhung khac reference = 2 entries

## Khi nao dung

- Cycle detection trong graph traversal (recursive)
- Track visited DOM nodes tránh xử lý repeat
- Observer pattern metadata without leaking
- Cache với automatic cleanup

## Ví dụ

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
// Khi el bi remove tu DOM va khong con ref -> WeakSet entry tu GC
```

## Liên kết chéo

- Xem: `03_data-structures/02_keyed-collections/02_weakmap` (WeakMap)
- Xem: `17_memory-management/01_memory-lifecycle-gc` (GC principles)
- Xem: `03_data-structures/02_keyed-collections/03_set` (Set comparison)
