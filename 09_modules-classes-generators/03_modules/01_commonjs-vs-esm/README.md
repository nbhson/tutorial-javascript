# Modules: CommonJS vs ESM

|  | CommonJS (Node) | ESM (ES6) |
|---|---|---|
| Syntax | `require/module.exports` | `import/export` |
| Load | sync | async, static |
| File | `.js` (Node) | `type: module` |

```js
// ESM
import {log} from "./logger/index.js";
log("hi");
// CommonJS (Node only)
// const {log}=require("./logger");
```
Dự án này dùng ESM (`09_modules-classes-generators/03_modules/app.js`).
