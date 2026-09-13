# Đệ quy (Recursion) — Thực hành chi tiết — [Level: Intermediate]

## 🔑 Khái niệm cốt lõi

**Đệ quy** là kỹ thuật mà một hàm **gọi lại chính nó** để giải bài toán bằng cách thu nhỏ nó dần thành những phiên bản đơn giản hơn, cho đến khi gặp **trường hợp cơ sở** (base case) — điều kiện dừng.

File `app.js` có hai ví dụ kinh điển:

```js
function factorial(n) {
  return n <= 1 ? 1 : n * factorial(n - 1);
}
console.log(factorial(5), factorial(6)); // 120 720

function fib(n) {
  return n <= 1 ? n : fib(n - 1) + fib(n - 2);
}
console.log(fib(7)); // 13
```

**Cách `factorial(4)` chạy** (step-by-step trace):

```
factorial(4)
= 4 * factorial(3)
= 4 * (3 * factorial(2))
= 4 * (3 * (2 * factorial(1)))
= 4 * (3 * (2 * 1))          ← factorial(1) = 1 (base case)
= 4 * 3 * 2 * 1
= 24
```

**Base case** là điều kiện dừng — nếu thiếu, hàm gọi chính nó không bao giờ kết thúc và nổ `Maximum call stack size exceeded` (tràn ngăn xếp call stack).

**Cơ chế hoạt động**: mỗi lần gọi đệ quy, JavaScript engine tạo một **execution context mới** và push lên **call stack**. Khi base case đạt được, các context lần lượt pop ra, "tháo ngược" từ dưới lên, tính toán và trả về kết quả cuối cùng.

## 📐 Cấu trúc / Cú pháp

### Cấu trúc cơ bản
```js
function recursiveFunction(param) {
  // Base case — điều kiện dừng
  if (baseCondition) {
    return baseValue;
  }
  // Recursive case — gọi lại chính mình với input nhỏ hơn
  return recursiveFunction(smallerParam);
}
```

### Two parts rule
Mọi recursive function đúng phải có:
1. **Base case** — điều kiện dừng, không gọi đệ quy tiếp.
2. **Recursive case** — gọi chính mình với input tiến về base case.

### Recursive patterns phổ biến
```js
// 1. Counting down
function countDown(n) {
  if (n <= 0) return;
  console.log(n);
  countDown(n - 1);
}

// 2. Counting up (using call stack to reverse)
function countUp(n) {
  if (n <= 0) return;
  countUp(n - 1);
  console.log(n); // in sau khi recursive call return
}

// 3. Sum array
function sumArray(arr) {
  if (arr.length === 0) return 0;
  return arr[0] + sumArray(arr.slice(1));
}

// 4. Flatten nested array
function flatten(arr) {
  let out = [];
  for (const item of arr) {
    if (Array.isArray(item)) out = out.concat(flatten(item));
    else out.push(item);
  }
  return out;
}
```

## ✅ Điểm mạnh

1. **Rất tự nhiên** cho bài toán có cấu trúc lặp lại (cây, thư mục, chuỗi lồng nhau) — code gần với định nghĩa toán học.
2. **Code gọn và gần với công thức toán học** — `n! = n * (n-1)!` đọc như công thức, không cần loop phức tạp.
3. **Dễ chứng minh đúng sai** khi base case hợp lý — induction proof áp dụng được.
4. **Hữu ích khi duyệt cấu trúc phân cấp** — comment trả lời lồng nhau, JSON lồng, DOM tree, thư mục.
5. **Kết hợp tốt với chia để trị** (divide & conquer) như quicksort, mergesort, binary search.
6. **Giải quyết bài toán backtracking** — mê cung, sudoku, tạo hoán vị, N-queens.
7. **Không cần biến đếm external** — state được giữ trong call stack frames.
8. **Easy to reason about** cho tree/graph problems — mỗi node xử lý tương tự node con.
9. **Memoization dễ áp dụng** — cache kết quả trung gian để tránh tính lại (fibonacci O(2^n) → O(n)).
10. **Elegant solution** cho problems with recursive structure — AVL trees, expression trees, syntax parsing.

## ⚠️ Bẫy thường gặp & Hạn chế

1. **Phải có base case** — nếu không dẫn đến tràn call stack (stack overflow). JavaScript call stack giới hạn ~10k-15k frames.
   ```js
   // ❌ Vô hạn — không có base case
   function boom() { boom(); }
   boom(); // RangeError: Maximum call stack size exceeded

   // ✅ Có base case
   function safe(n) {
     if (n <= 0) return;
     safe(n - 1);
   }
   ```

2. **Mỗi lần gọi đệ quy tốn một frame trong call stack** — độ sâu quá lớn sẽ lỗi (khoảng vài chục nghìn).
   ```js
   // ❌ Over 10000 recursions → stack overflow
   function deep(n) {
     if (n === 0) return;
     return deep(n - 1) + 1;
   }
   deep(20000); // RangeError

   // ✅ Convert to iteration for large n
   function deepIter(n) {
     let result = 0;
     for (let i = 0; i < n; i++) result++;
     return result;
   }
   ```

3. **`fib` kiểu đơn giản có độ phức tạp mũ O(2^n)** — lãng phí (tính lặp lại vô số lần); nên dùng memoization hoặc vòng lặp cho số lớn.
   ```js
   // ❌ O(2^n) — tính lại fib(2) nhiều lần
   function fibBad(n) {
     if (n <= 1) return n;
     return fibBad(n - 1) + fibBad(n - 2);
   }
   fibBad(50); // rất lâu!

   // ✅ O(n) với memoization
   function fibMemo(n, memo = {}) {
     if (n in memo) return memo[n];
     if (n <= 1) return n;
     memo[n] = fibMemo(n - 1, memo) + fibMemo(n - 2, memo);
     return memo[n];
   }
   console.log(fibMemo(50)); // 12586269025 — instant!
   ```

4. **Đệ quy đôi khi khó đọc và khó debug** hơn vòng lặp, đặc biệt với người mới — nhiều tầng call stack.
5. **Tail recursion không được optimize** trong JavaScript engines (trừ Safari) — vẫn tạo stack frame mới mỗi lần gọi.
   ```js
   // Tail recursive — vẫn stack overflow vì JS không có TCO
   function factTail(n, acc = 1) {
     if (n <= 1) return acc;
     return factTail(n - 1, n * acc); // tail call, nhưng không được optimize
   }
   factTail(20000); // RangeError vẫn xảy ra
   ```

6. **Memory leak risk** — mỗi stack frame giữ reference đến biến closure, accumulate memory.
7. **Khó convert từ iterative ↔ recursive** — cần tư duy khác biệt.

## 💡 Khi nào dùng

1. **Tính giai thừa**, lũy thừa, dãy Fibonacci (nhỏ) — ví dụ kinh điển, base case rõ ràng.
2. **Duyệt cây DOM**, cây thư mục, cây bình luận — cấu trúc phân cấp tự nhiên cho recursion.
3. **Duyệt/flatten object hoặc mảng lồng nhau** nhiều tầng — depth không xác định trước.
4. **Thuật toán chia để trị**: quicksort, mergesort, binary search — split problem in half.
5. **Backtracking**: giải mê cung, sudoku, tạo hoán vị, tám quân hậu — explore all possibilities.
6. **Parse recursive grammar** — JSON, XML, HTML AST, expression trees.
7. **Directory traversal** — đọc hết file trong thư mục và các thư mục con.
8. **Tree data structure operations** — insert, delete, search, traverse BST, AVL.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Giai thừa (file `app.js`)
```js
// Nội dung app.js trong thư mục
function factorial(n) {
  return n <= 1 ? 1 : n * factorial(n - 1);
}
console.log(factorial(5), factorial(6)); // 120 720

// Trace factorial(4):
// factorial(4) = 4 * factorial(3)
// factorial(3) = 3 * factorial(2)
// factorial(2) = 2 * factorial(1)
// factorial(1) = 1  (base case)
// → 4 * 3 * 2 * 1 = 24
```

### Ví dụ 2: Fibonacci (file `app.js`)
```js
// Nội dung app.js trong thư mục
function fib(n) {
  return n <= 1 ? n : fib(n - 1) + fib(n - 2);
}
console.log(fib(7)); // 13
// fib(7) = fib(6) + fib(5)
//        = (fib(5)+fib(4)) + (fib(4)+fib(3))
//        = ... = 13
```

### Ví dụ 3: Đệ quy duyệt mảng lồng nhau — flatten (file `app.js`)
```js
// Nội dung app.js trong thư mục
function flatten(arr) {
  let out = [];
  for (const item of arr) {
    if (Array.isArray(item)) out = out.concat(flatten(item));
    else out.push(item);
  }
  return out;
}
console.log(flatten([1, [2, [3, 4]], 5])); // [1, 2, 3, 4, 5]
```

### Ví dụ 4: Tính tổng mảng bằng đệ quy
```js
function sumArray(arr) {
  if (arr.length === 0) return 0;           // base case
  return arr[0] + sumArray(arr.slice(1));   // recursive case
}
console.log(sumArray([1, 2, 3, 4, 5])); // 15

// ✅ Tốt hơn: dùng reduce (iterative, không stack overflow)
console.log([1, 2, 3, 4, 5].reduce((a, b) => a + b, 0)); // 15
```

### Ví dụ 5: Fibonacci với memoization — O(n)
```js
function fibMemo(n, memo = {}) {
  if (n in memo) return memo[n];           // đã tính, trả cache
  if (n <= 1) return n;                    // base case
  memo[n] = fibMemo(n - 1, memo) + fibMemo(n - 2, memo); // tính và cache
  return memo[n];
}
console.log(fibMemo(50)); // 12586269025 — instant! (vs minutes với naive)

// Reverse memoization (top-down → bottom-up iterative)
function fibIterative(n) {
  if (n <= 1) return n;
  let a = 0, b = 1;
  for (let i = 2; i <= n; i++) {
    [a, b] = [b, a + b]; // swap + add
  }
  return b;
}
console.log(fibIterative(50)); // 12586269025
```

### Ví dụ 6: Duyệt cây DOM (conceptual)
```js
function traverseDOM(node, callback, depth = 0) {
  callback(node, depth); // xử lý node hiện tại
  for (const child of node.children) {
    traverseDOM(child, callback, depth + 1); // đệ quy child
  }
}

// Usage: in ra tất cả element tags trong DOM
traverseDOM(document.body, (node, depth) => {
  console.log(" ".repeat(depth * 2) + node.tagName);
});
```

### Ví dụ 7: Kiểm tra palindrome (chuỗi đảo ngược)
```js
function isPalindrome(str) {
  const s = str.toLowerCase().replace(/[^a-z0-9]/g, "");
  if (s.length <= 1) return true;              // base case
  if (s[0] !== s[s.length - 1]) return false;  // mismatch
  return isPalindrome(s.slice(1, -1));         // recursive: bỏ đầu và cuối
}
console.log(isPalindrome("A man a plan a canal Panama")); // true
console.log(isPalindrome("hello")); // false
```

### Ví dụ 8: Deep clone object bằng đệ quy
```js
function deepClone(obj) {
  if (obj === null || typeof obj !== "object") return obj; // base case: primitive
  if (Array.isArray(obj)) return obj.map(deepClone);        // array case
  const cloned = {};
  for (const key in obj) {
    if (obj.hasOwnProperty(key)) {
      cloned[key] = deepClone(obj[key]); // recursive for nested objects
    }
  }
  return cloned;
}

const original = { a: 1, b: { c: 2, d: [3, 4] } };
const copy = deepClone(original);
copy.b.c = 99;
console.log(original.b.c); // 2 — không bị ảnh hưởng (deep clone successful)
```

### Ví dụ 9: Directory tree printer
```js
// Giả lập filesystem structure
const filesystem = {
  name: "root",
  children: [
    { name: "docs", children: [
      { name: "readme.txt", children: [] },
      { name: "guide.md", children: [] }
    ]},
    { name: "src", children: [
      { name: "app.js", children: [] },
      { name: "utils", children: [
        { name: "helper.js", children: [] }
      ]}
    ]}
  ]
};

function printTree(node, indent = 0) {
  console.log(" ".repeat(indent * 2) + node.name);
  for (const child of node.children) {
    printTree(child, indent + 1);
  }
}
printTree(filesystem);
// root
//   docs
//     readme.txt
//     guide.md
//   src
//     app.js
//     utils
//       helper.js
```

### Ví dụ 10: QuickSort — divide and conquer
```js
function quickSort(arr) {
  if (arr.length <= 1) return arr; // base case

  const pivot = arr[Math.floor(arr.length / 2)];
  const left = arr.filter(x => x < pivot);
  const middle = arr.filter(x => x === pivot);
  const right = arr.filter(x => x > pivot);

  return [...quickSort(left), ...middle, ...quickSort(right)];
  // recursive case: sort left and right, then combine
}
console.log(quickSort([3, 1, 4, 1, 5, 9, 2, 6])); // [1, 1, 2, 3, 4, 5, 6, 9]
// Time: O(n log n) average, Space: O(n) due to array creation
```

## 🔬 So sánh với alternatives

| Phương án | Ưu điểm | Nhược điểm | Phù hợp khi |
|---|---|---|---|
| **Recursion** | Natural cho tree/complex structure | Stack overflow risk, memory overhead | Tree traversal, divide & conquer |
| **Iteration (loop)** | No stack limit, memory efficient | Harder for recursive structures | Linear data, simple loops |
| **Iteration + stack** | Simulate recursion explicitly | More code, manual management | Deep recursion avoidance |
| **Memoization** | O(n) vs O(2^n) for fib | Extra memory for cache | Overlapping subproblems |
| **Tail recursion** | Theoretical O(1) stack | Not supported in JS engines | Theoretical CS, other languages |

## 📊 Performance & Best Practices

**Performance analysis**:
- **Naive Fibonacci**: O(2^n) — doubles with each increment. Unusable for n > 40.
- **Memoized Fibonacci**: O(n) time, O(n) space — instant for n < 10000.
- **QuickSort**: O(n log n) average, O(n²) worst case — recursive but practical.
- **Deep recursion (>10k)**: stack overflow in V8 — use iterative or chunk processing.
- **Recursion overhead**: each call creates new stack frame (~hundreds of bytes) — significant for deep trees.

**Best practices**:
- **Luôn có base case** — test với input nhỏ (0, 1, empty array) trước.
- **Giảm input size** mỗi lần gọi — đảm bảo tiến về base case.
- **Dùng memoization** khi có overlapping subproblems (fibonacci, path counting).
- **Convert to iterative** khi depth > 1000 — avoid stack overflow.
- **Tail recursion** — viết để compiler optimize (không được JS support, nhưng good practice).
- **Use `Array.prototype` methods** thay recursion cho flat arrays — `map`, `filter`, `reduce` đã optimized.
- **Profile recursive functions** — `console.time` để đo thời gian, so sánh với iterative version.
- **Guard against infinite recursion** — max depth parameter với fallback to iterative.
- **Prefer iterative for linear problems** — loop hơn recursion cho array sum, flatten (unless depth unknown).
- **Document base case và recursive case** — comment rõ trong code để maintainer hiểu.

**Khi nào nên dùng recursion**:
- ✅ Cấu trúc phân cấp (cây, đồ thị, directory).
- ✅ Divide & conquer algorithms (quicksort, mergesort).
- ✅ Backtracking problems (maze, puzzle, permutation).
- ✅ Depth không xác định trước (nested JSON, comments).
- ❌ Linear iteration — dùng loop thay thế.
- ❌ Deep recursion (>5000 frames) — dùng iterative hoặc chunked processing.

## 🔗 Liên kết chéo

- Tổng quan Functions: `09_functions/README.md` — khái niệm hàm, recursion context.
- Arrow functions: `09_functions/01_parameters-and-arrow/03_arrow-functions/` — arrow trong recursive function.
- Arguments object: `09_functions/01_parameters-and-arrow/05_arguments-object/` — arguments trong recursion.
- Call stack: `09_functions/02_scope-closure-strict-mode/05_function-stack/` — call stack overflow explanation.
- Closure: `09_functions/02_scope-closure-strict-mode/03_closure/` — closure trong memoization.
- Loops: `05_loops-and-iterations/01_loops/` — loop alternative cho recursion.
- Exceptional handling: `07_exceptional-handling/02_try-catch-finally/` — catch stack overflow error.
- Operators: `08_expressions-and-operators/01_operators/` — toán tử trong recursive expression.
