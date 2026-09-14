# JavaScript.info — Toàn bộ bài học (175 articles)

> Mirror 1:1 từ https://javascript.info — cập nhật lần cuối: **2026-09-14**
> Toàn bộ 175 bài leaf (không tính trang section) đã được fetch và chuyển sang Markdown, giữ nguyên ví dụ, hình ảnh, tasks & solutions.

## Cách đọc
Mỗi thư mục `js/XX_.../` tương ứng 1 chương của javascript.info. Mỗi file `.md` có header `> Source: https://javascript.info/<slug>` và `<!-- fetched: YYYY-MM-DD -->`.

Chạy ví dụ: mở file, copy code block và chạy `node` hoặc trong browser console.

## Tổng quan 3 phần

### Part 1 — The JavaScript Language (14 chương, 76 bài)
| Thư mục | Chương javascript.info | Số bài | Slugs |
|---|---|---|---|
| `01_introduction/` | Getting started — An Introduction | 4 | `intro`, `manuals-specifications`, `code-editors`, `devtools` |
| `02_first-steps/` | Fundamentals | 18 | `hello-world`, `structure`, `strict-mode`, `variables`, `types`, `alert-prompt-confirm`, `type-conversions`, `operators`, `comparison`, `ifelse`, `logical-operators`, `nullish-coalescing-operator`, `while-for`, `switch`, `function-basics`, `function-expressions`, `arrow-functions-basics`, `javascript-specials` |
| `03_code-quality/` | Code quality | 6 | `debugging-chrome`, `coding-style`, `comments`, `ninja-code`, `testing-mocha`, `polyfills` |
| `04_objects-basics/` | Objects: the basics | 8 | `object`, `object-copy`, `garbage-collection`, `object-methods`, `constructor-new`, `optional-chaining`, `symbol`, `object-toprimitive` |
| `05_data-types/` | Data types | 12 | `primitives-methods`, `number`, `string`, `array`, `array-methods`, `iterable`, `map-set`, `weakmap-weakset`, `keys-values-entries`, `destructuring-assignment`, `date`, `json` |
| `06_advanced-functions/` | Advanced working with functions | 11 | `recursion`, `rest-parameters-spread`, `closure`, `var`, `global-object`, `function-object`, `new-function`, `settimeout-setinterval`, `call-apply-decorators`, `bind`, `arrow-functions` |
| `07_object-properties/` | Object properties | 2 | `property-descriptors`, `property-accessors` |
| `08_prototypes/` | Prototypes, inheritance | 4 | `prototype-inheritance`, `function-prototype`, `native-prototypes`, `prototype-methods` |
| `09_classes/` | Classes | 7 | `class`, `class-inheritance`, `static-properties-methods`, `private-protected-properties-methods`, `extend-natives`, `instanceof`, `mixins` |
| `10_error-handling/` | Error handling | 2 | `try-catch`, `custom-errors` |
| `11_async/` | Promises, async/await | 8 | `callbacks`, `promise-basics`, `promise-chaining`, `promise-error-handling`, `promise-api`, `promisify`, `microtask-queue`, `async-await` |
| `12_generators/` | Generators, advanced iteration | 2 | `generators`, `async-iterators-generators` |
| `13_modules/` | Modules | 3 | `modules-intro`, `import-export`, `modules-dynamic-imports` |
| `14_misc/` | Miscellaneous | 7 | `proxy`, `eval`, `currying-partials`, `reference-type`, `bigint`, `unicode`, `weakref-finalizationregistry` |

### Part 2 — Browser: Document, Events, Interfaces (6 chương, 44 bài)
| Thư mục | Chương | Số bài | Slugs |
|---|---|---|---|
| `20_browser-document/` | Document | 11 | `browser-environment`, `dom-nodes`, `dom-navigation`, `searching-elements-dom`, `basic-dom-node-properties`, `dom-attributes-and-properties`, `modifying-document`, `styles-and-classes`, `size-and-scroll`, `size-and-scroll-window`, `coordinates` |
| `21_events-intro/` | Introduction to Events | 5 | `introduction-browser-events`, `bubbling-and-capturing`, `event-delegation`, `default-browser-action`, `dispatch-events` |
| `22_ui-events/` | UI Events | 6 | `mouse-events-basics`, `mousemove-mouseover-mouseout-mouseenter-mouseleave`, `mouse-drag-and-drop`, `pointer-events`, `keyboard-events`, `onscroll` |
| `23_forms-controls/` | Forms, controls | 4 | `form-elements`, `focus-blur`, `events-change-input`, `forms-submit` |
| `24_loading/` | Document and resource loading | 3 | `onload-ondomcontentloaded`, `script-async-defer`, `onload-onerror` |
| `25_ui-misc/` | Miscellaneous | 3 | `mutation-observer`, `selection-range`, `event-loop` |

### Part 3 — Additional articles (8 chương, 55 bài)
| Thư mục | Chương | Số bài | Slugs |
|---|---|---|---|
| `30_frames-windows/` | Frames and windows | 3 | `popup-windows`, `cross-window-communication`, `clickjacking` |
| `31_binary-files/` | Binary data, files | 4 | `arraybuffer-binary-arrays`, `text-decoder`, `blob`, `file` |
| `32_network/` | Network requests | 12 | `fetch`, `formdata`, `fetch-progress`, `fetch-abort`, `fetch-crossorigin`, `fetch-api`, `url`, `xmlhttprequest`, `resume-upload`, `long-polling`, `websocket`, `server-sent-events` |
| `33_storage/` | Storing data in the browser | 3 | `cookie`, `localstorage`, `indexeddb` |
| `34_animation/` | Animation | 3 | `bezier-curve`, `css-animations`, `js-animation` |
| `35_web-components/` | Web components | 7 | `webcomponents-intro`, `custom-elements`, `shadow-dom`, `template-element`, `slots-composition`, `shadow-dom-style`, `shadow-dom-events` |
| `36_regular-expressions/` | Regular expressions | 17 | `regexp-introduction`, `regexp-character-classes`, `regexp-unicode`, `regexp-anchors`, `regexp-multiline-mode`, `regexp-boundary`, `regexp-escaping`, `regexp-character-sets-and-ranges`, `regexp-quantifiers`, `regexp-greedy-and-lazy`, `regexp-groups`, `regexp-backreferences`, `regexp-alternation`, `regexp-lookahead-lookbehind`, `regexp-catastrophic-backtracking`, `regexp-sticky`, `regexp-methods` |

**Tổng cộng: 175 bài leaf + 27 trang section = 202 URLs tutorial (không tính tasks/about).**

## Chi tiết từng bài (đã review 2026-09-14)

Tất cả 175 file đã được kiểm tra:
- Giữ nguyên tiêu đề, anchors, code blocks, hình ảnh (`/article/...` giữ đường dẫn gốc)
- Giữ nguyên phần **Tasks** + solution (nếu có) — ví dụ `js/02_first-steps/04_variables.md:346` có 3 tasks
- Không cắt bớt nội dung — file dài nhất `js/05_data-types/05-array-methods.md` (1526 dòng), ngắn nhất vẫn đầy đủ (ví dụ `js/01_introduction/02_manuals-specifications.md` 40 dòng là đúng vì bài gốc ngắn)

### Xác minh cập nhật (2026-09-14)
- Fetch trực tiếp `https://javascript.info/tutorial/map` ngày 2026-09-14 — so sánh 205 href unique, trừ 27 section + 3 meta → 175 leaf — khớp chính xác số file local `find js -name "*.md" | wc -l = 175`
- Spot-check `curl -sk https://javascript.info/variables` (57457 bytes) và `https://javascript.info/array-methods` (131810 bytes) — nội dung tasks/solutions khớp bản local
- Tất cả file có `<!-- fetched: 2026-09-14 -->` (ngày hiện tại), không phát hiện bài mới hay thay đổi nội dung kể từ lần fetch trước

## Cập nhật lần này
- Không thêm thư mục mới — đã đủ 100% (27 thư mục trong `js/`)
- Không phát hiện nội dung mới cần patch (javascript.info không thay đổi giữa 2026-09-14 và hiện tại)
- Tạo file tổng hợp này (`js/README.md`) để tra cứu nhanh, bổ sung bảng mapping slug → file
- Giữ nguyên cấu trúc song song với roadmap.sh (`00_…` → `21_…`) — `js/` là mirror javascript.info, không xung đột

## Tham khảo
- javascript.info: https://javascript.info/
- MDN: https://developer.mozilla.org/en-US/docs/Web/JavaScript
- Roadmap: https://roadmap.sh/javascript

---
*Generated: 2026-09-14 — 175/175 articles mirrored, verified via tutorial/map + curl spot-checks*
