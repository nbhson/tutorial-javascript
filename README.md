# JavaScript Tutorial — Full Course (javascript.info mirror)

> Tổng hợp toàn bộ bài học từ **https://javascript.info/** — 175 bài, 27 thư mục, bao phủ 3 phần chính.

## 📚 Cấu trúc

### Part 1 — The JavaScript Language (76 lessons)

| Thư mục | Bài học |
|---|---|
| `js/01_introduction/` | What is JavaScript, Manuals & Specifications, Code Editors, Developer Console |
| `js/02_first-steps/` | Hello World, Code Structure, Strict Mode, Variables, Data Types, Interaction, Type Conversions, Operators, Comparisons, Conditional Branching, Logical Operators, Nullish Coalescing, Loops, Switch, Functions, Function Expressions, Arrow Functions, JavaScript Specials |
| `js/03_code-quality/` | Debugging in Browser, Coding Style, Comments, Ninja Code, Testing with Mocha, Polyfills & Transpilers |
| `js/04_objects-basics/` | Objects, Object References & Copying, Garbage Collection, Object Methods & this, Constructor & new, Optional Chaining, Symbol Type, Object to Primitive Conversion |
| `js/05_data-types/` | Methods of Primitives, Numbers, Strings, Arrays, Array Methods, Iterables, Map & Set, WeakMap & WeakSet, Object.keys/values/entries, Destructuring Assignment, Date & Time, JSON |
| `js/06_advanced-functions/` | Recursion & Stack, Rest Parameters & Spread, Variable Scope & Closure, The Old "var", Global Object, Function Object & NFE, The "new Function" Syntax, Scheduling (setTimeout/setInterval), Decorators & call/apply, Function Binding, Arrow Functions Revisited |
| `js/07_object-properties/` | Property Flags & Descriptors, Property Getters & Setters |
| `js/08_prototypes/` | Prototypal Inheritance, F.prototype, Native Prototypes, Prototype Methods |
| `js/09_classes/` | Class Basic Syntax, Class Inheritance, Static Properties & Methods, Private & Protected, Extending Built-in Classes, instanceof, Mixins |
| `js/10_error-handling/` | try...catch, Custom Errors |
| `js/11_async/` | Callbacks, Promise, Promise Chaining, Error Handling with Promises, Promise API, Promisification, Microtasks, Async/Await |
| `js/12_generators/` | Generators, Async Iterators & Generators |
| `js/13_modules/` | Modules Introduction, Export & Import, Dynamic Imports |
| `js/14_misc/` | Proxy & Reflect, Eval, Currying, Reference Type, BigInt, Unicode, WeakRef & FinalizationRegistry |

### Part 2 — Browser: Document, Events, Interfaces (44 lessons)

| Thư mục | Bài học |
|---|---|
| `js/20_browser-document/` | Browser Environment, DOM Tree, Walking the DOM, Searching Elements, DOM Node Properties, Attributes & Properties, Modifying Document, Styles & Classes, Element Size & Scrolling, Window Sizes, Coordinates |
| `js/21_events-intro/` | Browser Events, Bubbling & Capturing, Event Delegation, Default Browser Actions, Dispatching Custom Events |
| `js/22_ui-events/` | Mouse Events, Mouse Movement (mouseover/out, mouseenter/leave), Drag'n'Drop, Pointer Events, Keyboard Events, Scrolling |
| `js/23_forms-controls/` | Form Properties & Methods, Focus/Blur, Change/Input/Cut/Copy/Paste Events, Forms Submit |
| `js/24_loading/` | DOMContentLoaded/load/unload, Script Async/Defer, Resource Loading (onload/onerror) |
| `js/25_ui-misc/` | Mutation Observer, Selection & Range, Event Loop (Microtasks & Macrotasks) |

### Part 3 — Additional Articles (55 lessons)

| Thư mục | Bài học |
|---|---|
| `js/30_frames-windows/` | Popups & Window Methods, Cross-window Communication, Clickjacking Attack |
| `js/31_binary-files/` | ArrayBuffer & Binary Arrays, TextDecoder & TextEncoder, Blob, File & FileReader |
| `js/32_network/` | Fetch, FormData, Fetch Progress, Fetch Abort, Fetch Cross-Origin, Fetch API, URL Objects, XMLHttpRequest, Resumable File Upload, Long Polling, WebSocket, Server Sent Events |
| `js/33_storage/` | Cookies, LocalStorage & SessionStorage, IndexedDB |
| `js/34_animation/` | Bezier Curve, CSS Animations, JavaScript Animations |
| `js/35_web-components/` | Web Components Intro, Custom Elements, Shadow DOM, Template Element, Shadow DOM Slots & Composition, Shadow DOM Styling, Shadow DOM & Events |
| `js/36_regular-expressions/` | Patterns & Flags, Character Classes, Unicode (flag "u"), Anchors (^$), Multiline Mode, Word Boundary (\b), Escaping, Sets & Ranges, Quantifiers (+,*,?), Greedy & Lazy, Capturing Groups, Backreferences, Alternation (\|), Lookahead & Lookbehind, Catastrophic Backtracking, Sticky Flag, RegExp Methods |

## 🚀 Cách sử dụng

```bash
# Xem danh sách bài học
ls js/

# Đọc bài học cụ thể
cat js/02_first-steps/04_variables.md

# Tìm kiếm nội dung
grep -r "Promise" js/11_async/

# Đếm tổng số bài
find js -name "*.md" ! -name "README.md" | wc -l
```

## 📊 Thống kê

- **Tổng số bài học:** 175
- **Part 1 (JavaScript Language):** 76 lessons
- **Part 2 (Browser):** 44 lessons  
- **Part 3 (Additional):** 55 lessons
- **Ngày cập nhật:** 2026-09-14

## 🔗 Nguồn gốc

Mỗi file trong `js/` đều có header:
```markdown
> Source: [https://javascript.info/<slug>](https://javascript.info/<slug>)
<!-- fetched: 2026-09-14 -->
```
