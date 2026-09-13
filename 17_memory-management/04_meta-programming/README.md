# Metaprogramming — Proxy và Reflect — [Level: Advanced]

## 🔑 Kh khái niệm cốt lõi

**Metaprogramming** là kỹ thuật lập trình trong đó chương trình có thể **đọc, sinh, phân tích hoặc tự sửa đổi** chính chương trình (hoặc chương trình khác) khi đang chạy. Trong JavaScript, metaprogramming hiện thực qua hai cơ chế chính:

### Reflection (Khả năng nhìn vào cấu trúc)
- **Introspection**: chỉ đọc cấu trúc object — `Object.keys()`, `Object.getOwnPropertyNames()`, `Reflect.ownKeys()`.
- **Self-Modification**: sửa đổi chính mình — tự thêm property, thay đổi descriptor qua `Object.defineProperty()`.
- **Intercession**: thay đổi ngữ nghĩa của toán tử/hành vi mặc định — đây là chỗ **Proxy** hoạt động.

### Reflect API (ES6)
Tập hàm tiện ích chuẩn hóa các thao tác thường làm thủ công. Hoạt động như counterparts của các object operations:
- `Reflect.get(target, prop, receiver)` — tương đương `target[prop]`
- `Reflect.set(target, prop, value, receiver)` — tương đương `target[prop] = value`
- `Reflect.has(target, prop)` — tương đương `prop in target`
- `Reflect.deleteProperty(target, prop)` — tương đương `delete target[prop]`
- `Reflect.construct(target, args)` — tương đương `new Target(...args)`
- `Reflect.apply(target, thisArg, args)` — tương đương `target.call(thisArg, ...args)`
- `Reflect.ownKeys(target)` — liệt kê tất cả keys (including symbols)
- `Reflect.defineProperty(target, prop, descriptor)` — tương đương `Object.defineProperty`

### Proxy (ES6) — "Wraper" can thiệp hành vi
Proxy bọc quanh object `target`, cho phép **trap** (can thiệp) các thao tác qua `handler`:
- `get` — chặn đọc property
- `set` — chặn ghi property
- `has` — chặn `in` operator
- `apply` — chặn function call
- `construct` — chặn `new`
- `deleteProperty` — chặn `delete`
- `ownKeys` — chặn `Object.keys()`, `for...in`
- `getPrototypeOf` / `setPrototypeOf` — chặn prototype manipulation
- `isExtensible` / `preventExtensions` — chặn extension
- `defineProperty` — chặn `Object.defineProperty`
- `getOwnPropertyDescriptor` — chặn `Object.getOwnPropertyDescriptor`

**Kết hợp kinh điển**: `Proxy` = nơi viết logic can thiệp; `Reflect` = nơi gọi **đúng hành vi mặc định** bên trong trap (giữ nguyên ngữ nghĩa gốc). Pattern này gọi là "forward with interception".

File `app.js` trong thư mục này là ví dụ hoàn chỉnh: Proxy log mỗi lần GET/SET property trên object `employee` và dùng `Reflect` để chuyển tiếp mặc định.

## 📐 Cấu trúc / Cú pháp

### Proxy cơ bản
```js
const target = { message: 'Hello' };
const handler = {
  get(trapTarget, prop, receiver) {
    console.log(`Đã đọc property: ${prop}`);
    return Reflect.get(trapTarget, prop, receiver); // forward default
  },
  set(trapTarget, prop, value, receiver) {
    console.log(`Đã gán property: ${prop} = ${value}`);
    return Reflect.set(trapTarget, prop, value, receiver); // forward default
  }
};
const proxy = new Proxy(target, handler);
console.log(proxy.message); // "Đã đọc property: message" → "Hello"
proxy.message = 'World';    // "Đã gán property: message = World"
```

### Các trap phổ biến
| Trap | Intercept | Default via Reflect |
|---|---|---|
| `get(target, prop, receiver)` | `proxy.prop`, `proxy['prop']` | `Reflect.get(...)` |
| `set(target, prop, value, receiver)` | `proxy.prop = val` | `Reflect.set(...)` |
| `has(target, prop)` | `prop in proxy` | `Reflect.has(...)` |
| `deleteProperty(target, prop)` | `delete proxy.prop` | `Reflect.deleteProperty(...)` |
| `apply(target, thisArg, args)` | `proxy(...)` | `Reflect.apply(...)` |
| `construct(target, args)` | `new proxy(...)` | `Reflect.construct(...)` |
| `ownKeys(target)` | `Object.keys(proxy)`, `for...in` | `Reflect.ownKeys(...)` |
| `getPrototypeOf(target)` | `Object.getPrototypeOf(proxy)` | `Reflect.getPrototypeOf(...)` |

### Handler pattern — validation
```js
const validator = {
  set(target, prop, value) {
    if (prop === 'age' && !Number.isInteger(value)) {
      throw new TypeError(`age must be integer, got ${typeof value}`);
    }
    if (prop === 'age' && value < 0) {
      throw new TypeError('age cannot be negative');
    }
    return Reflect.set(target, prop, value);
  }
};
const person = new Proxy({ age: 0 }, validator);
person.age = 25;   // ✅
person.age = 'abc'; // ❌ TypeError
```

## ✅ Điểm mạnh — Tại sao nên dùng

1. **Không xâm lấn** — kiểm soát hành vi object từ bên ngoài mà không sửa code gốc.
2. **Reactivity** — phát hiện và phản ứng với mọi thay đổi property — nền tảng Vue/Polymer reactivity system.
3. **Validation/tiền-điều-kiện** — chặn gán giá trị sai (loại, phạm vi) ngay tại `set` trap — single point of truth.
4. **Computed/derived property** — tính `fullName` từ `firstName` + `lastName` tại `get` trap — lazy computed.
5. **Friendly error cho property không tồn tại** — tại `get` trap, trả message thân thiện thay vì `undefined`.
6. **Logging/audit** — ghi nhật ký mọi truy cập hoặc thay đổi dữ liệu nhạy cảm mà code ứng dụng không đổi.
7. **Mock/stub testing** — bọc object thật bằng Proxy để ghi nhận method calls trong unit test.
8. **Immutable proxy** — `set` trap throw error → object read-only từ bên ngoài.
9. **Default values** — `get` trap trả default khi property không tồn tại.
10. **Serialization customization** — `ownKeys` + `get` trap kiểm soát JSON.stringify output.

## ⚠️ Bẫy thường gặp & Hạn chế

### Bẫy 1: Hiệu năng — mỗi truy cập qua proxy tốn thêm trap
```js
const proxy = new Proxy(obj, handler);
// Mỗi proxy.prop = get trap call → Reflect.get → return
// Hot loop qua proxy chậm hơn 5-10x so với direct access
// ⚠️ Đừng bọc proxy vào "hot path" vô tội vạ
```

### Bẫy 2: Khó gỡ lỗi
```js
const proxy = new Proxy(obj, {
  get(target, prop) {
    return target[prop]; // lỗi ở đây khó trace — stack trace không hiện proxy
  }
});
// Debug phải "nhìn xuyên proxy" mới hiểu tại sao
```

### Bẫy 3: Ma thuật quá mức
```js
// Viết nhiều proxy lồng proxy → code khó đọc, khó suy đoán
// Giới hạn proxy đúng chỗ — không bọc mọi object
```

### Bẫy 4: `Reflect.set` trả false khi không thể set
```js
const obj = { get readonly() { return 1; } };
const proxy = new Proxy(obj, {
  set(target, prop, value) {
    return Reflect.set(target, prop, value); // false nếu non-writable
  }
});
const result = proxy.readonly = 2; // result = false, không throw!
// Cần check return value hoặc throw lỗi explicitly
```

### Bẫy 5: Proxy không clone được bằng structuredClone
```js
const proxy = new Proxy({ a: 1 }, handler);
structuredClone(proxy); // ❌ TypeError: Could not create a cloned copy of a Proxy object
// Fix: clone target trước, không clone proxy
```

### Bẫy 6: ` instanceof Proxy` không hoạt động
```js
const proxy = new Proxy({}, handler);
console.log(proxy instanceof Object); // true (proxy forwards to target)
// Nhưng Object.getPrototypeOf(proxy) !== Object.prototype nếu handler can thiệp
```

## 💡 Khi nào dùng — Tình huống thực tế

1. **Xây dựng system reactive** (state → UI) kiểu Vue — proxy thay cho việc poll hay setter thủ công.
2. **Validate input/API boundary** ở một điểm tập trung thay vì rải rác nhiều chỗ trong code.
3. **Log/audit** mọi truy cập hoặc thay đổi dữ liệu nhạy cảm (financial data, user PII).
4. **Tạo "computed" property ảo** (như `fullName`) hay message thân thiện cho field không tồn tại.
5. **Bọc thư viện bên thứ ba** để thêm hành vi (thống kê, cache, đảo ngược) mà không fork code.
6. **Mock object cho testing** — ghi nhận method calls, xác nhận gọi đúng số lần.
7. **Deep read-only** — frozen object có thể bị mutate qua prototype chain; proxy chặn được.
8. **Routing/URL proxy** — `get` trap redirect property access đến URL params.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Log proxy cơ bản (file `app.js`)
```js
const employee = {
  firstName: 'Tapas',
  lastName: 'Adhikary'
};

const logHandler = {
  get(target, field) {
    console.log('GET', field);              // truy vấn trước
    return Reflect.get(target, field);      // forward hành vi mặc định
  },
  set(target, key, value) {
    console.log('SET', key, '=', value);
    return Reflect.set(target, key, value); // forward hành vi mặc định
  }
};

const p = new Proxy(employee, logHandler);
console.log(p.firstName);   // GET firstName -> Tapas
console.log(p.lastName);    // GET lastName -> Adhikary
p.age = 15;                 // SET age = 15
console.log(p.age);         // GET age -> 15
console.log(p);             // handler & target both visible
console.log(employee);      // target cũng có age = 15 (shared)
```

### Ví dụ 2: Validation proxy
```js
function createValidatedPerson(initial) {
  return new Proxy(initial, {
    set(target, key, value) {
      if (key === 'age') {
        if (!Number.isInteger(value)) throw new TypeError('age must be integer');
        if (value < 0 || value > 150) throw new RangeError('age out of range');
      }
      if (key === 'email' && !value.includes('@')) {
        throw new TypeError('invalid email');
      }
      return Reflect.set(target, key, value);
    }
  });
}

const person = createValidatedPerson({ name: 'Sơn', age: 25, email: 'son@example.com' });
person.age = 30;        // ✅
person.age = 'abc';     // ❌ TypeError: age must be integer
person.email = 'bad';   // ❌ TypeError: invalid email
```

### Ví dụ 3: Computed property proxy
```js
const person = { firstName: 'Nguyễn', lastName: 'Sơn' };
const proxy = new Proxy(person, {
  get(target, prop) {
    if (prop === 'fullName') {
      return `${target.firstName} ${target.lastName}`; // computed on-the-fly
    }
    return Reflect.get(target, prop);
  }
});
console.log(proxy.fullName); // 'Nguyễn Sơn' — computed từ firstName + lastName
person.firstName = 'Trần';
console.log(proxy.fullName); // 'Trần Sơn' — tự động cập nhật
```

### Ví dụ 4: Default value proxy
```js
const config = { timeout: 5000 };
const proxy = new Proxy(config, {
  get(target, prop) {
    if (!(prop in target)) {
      return `Default for ${prop}`; // trả default thay vì undefined
    }
    return Reflect.get(target, prop);
  }
});
console.log(proxy.timeout);      // 5000
console.log(proxy.retries);      // "Default for retries" — không undefined
console.log(proxy.unknownProp);  // "Default for unknownProp"
```

### Ví dụ 5: Read-only proxy (immutable)
```js
function readonly(obj) {
  return new Proxy(obj, {
    set(_target, prop, _value) {
      throw new TypeError(`Cannot set readonly property: ${String(prop)}`);
    }
  });
}
const state = readonly({ count: 0, name: 'app' });
state.count = 1; // ❌ TypeError: Cannot set readonly property: count
```

### Ví dụ 6: Trapping `in` operator
```js
const target = { a: 1, b: 2 };
const handler = {
  has(target, prop) {
    console.log(`Check '${prop}' in target`);
    return prop in target; // hoặc logic custom
  }
};
const proxy = new Proxy(target, handler);
console.log('a' in proxy); // "Check 'a' in target" → true
console.log('z' in proxy); // "Check 'z' in target" → false
```

### Ví dụ 7: Function proxy (trap apply)
```js
function add(a, b) { return a + b; }
const loggedAdd = new Proxy(add, {
  apply(target, thisArg, args) {
    console.log(`add(${args.join(', ')})`);
    return Reflect.apply(target, thisArg, args);
  }
});
console.log(loggedAdd(2, 3)); // "add(2, 3)" → 5
```

### Ví dụ 8: Array proxy — track changes
```js
function createTrackedArray(initial = []) {
  return new Proxy(initial, {
    set(target, prop, value) {
      if (isNaN(parseInt(prop))) {
        // Không phải index — forward bình thường
        return Reflect.set(target, prop, value);
      }
      const old = target[prop];
      console.log(`Array[${prop}]: ${old} → ${value}`);
      return Reflect.set(target, prop, value);
    },
    deleteProperty(target, prop) {
      console.log(`Array[${prop}] deleted`);
      return Reflect.deleteProperty(target, prop);
    }
  });
}
const arr = createTrackedArray([1, 2, 3]);
arr[0] = 10;  // "Array[0]: 1 → 10"
arr[5] = 5;   // "Array[5]: undefined → 5"
delete arr[1]; // "Array[1] deleted"
```

## 🔬 So sánh với alternatives

| Cách tiếp cận | Ưu điểm | Nhược điểm | Phù hợp khi |
|---|---|---|---|
| **Proxy + Reflect** | Can thiệp mọi thao tác, linh hoạt | Overhead performance, khó debug | Validation, reactivity, logging |
| **Object.defineProperty** | Standard, không cần wrapper | Chỉ trap property riêng lẻ, không catch all | Thuộc tính cố định, getter/setter |
| **Class với getter/setter** | Type-safe, IDE autocomplete | Phải redefine class, không áp dụng object có sẵn | Class design từ đầu |
| **Manual wrapper object** | Đơn giản, dễ hiểu | Không đồng bộ với target tự động | Object nhỏ, ít property |
| **Immutable.js / Immer** | Immutable data structures | Thư viện ngoài, bundle size tăng | State management phức tạp |

## 📊 Performance & Best Practices

- **Proxy overhead**: mỗi trap call ~10-100ns thêm so với direct access. Hot loop qua proxy chậm hơn 5-10x — đừng dùng trong animation frame.
- **Reflect là bắt buộc trong handler** — không `return target[prop]` trực tiếp (gây infinite recursion).
- **Nhẫn đạo khi bọc** — chỉ bọc object ở boundary (API response, user input), không bọc mọi object trong app.
- **Return true from set** — `set` trap phải return boolean (true = success), nếu false → Strict Mode throw TypeError.
- **Test handler comprehensively** — mỗi trap có thể có edge cases; test cả valid và invalid paths.
- **Deep proxy vs shallow proxy** — deep proxy (bọc nested object) phức tạp hơn, dễ bug — cân nhắc shallow trước.
- **Use Proxy.revocable()** khi cần thu hồi proxy — `proxyRevocable.revoke()` cắt connection proxy ↔ target.
- **Browser compatibility**: IE không support Proxy — cần polyfill hoặc fallback.

## 🔗 Liên kết chéo

- Xem thêm: `17_memory-management/04_meta-programming/` — file `app.js` demo log proxy cơ bản.
- Xem thêm: `18_dom-apis/02_dom-advanced/05_reactivity/` — Proxy-based reactivity cho UI.
- Xem thêm: `17_memory-management/03_v8-engine/` — hidden class impact khi dùng Proxy.
- Xem thêm: `17_memory-management/01_memory-lifecycle-gc/` — proxy object và GC behavior.
- Xem thêm: MDN Web Docs — Proxy, Reflect.
