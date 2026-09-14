# Reference Type

> Source: [https://javascript.info/reference-type](https://javascript.info/reference-type)

<!-- fetched: 2026-09-14 -->

In-depth language feature

This article covers an advanced topic, to understand certain edge-cases better.

It’s not important. Many experienced developers live fine without knowing it. Read on if you want to know how things work under the hood.

A dynamically evaluated method call can lose `this`.

For instance:

```
let user = {
  name: "John",
  hi() { alert(this.name); },
  bye() { alert("Bye"); }
};

user.hi(); // works

// now let's call user.hi or user.bye depending on the name
(user.name == "John" ? user.hi : user.bye)(); // Error!
```

On the last line there is a conditional operator that chooses either `user.hi` or `user.bye`. In this case the result is `user.hi`.

Then the method is immediately called with parentheses `()`. But it doesn’t work correctly!

As you can see, the call results in an error, because the value of `"this"` inside the call becomes `undefined`.

This works (object dot method):

```
user.hi();
```

This doesn’t (evaluated method):

```
(user.name == "John" ? user.hi : user.bye)(); // Error!
```

Why? If we want to understand why it happens, let’s get under the hood of how `obj.method()` call works.

## [Reference type explained](#reference-type-explained)

Looking closely, we may notice two operations in `obj.method()` statement:

1. First, the dot `'.'` retrieves the property `obj.method`.
2. Then parentheses `()` execute it.

So, how does the information about `this` get passed from the first part to the second one?

If we put these operations on separate lines, then `this` will be lost for sure:

```
let user = {
  name: "John",
  hi() { alert(this.name); }
};

// split getting and calling the method in two lines
let hi = user.hi;
hi(); // Error, because this is undefined
```

Here `hi = user.hi` puts the function into the variable, and then on the last line it is completely standalone, and so there’s no `this`.

**To make `user.hi()` calls work, JavaScript uses a trick – the dot `'.'` returns not a function, but a value of the special [Reference Type](https://tc39.github.io/ecma262/#sec-reference-specification-type).**

The Reference Type is a “specification type”. We can’t explicitly use it, but it is used internally by the language.

The value of Reference Type is a three-value combination `(base, name, strict)`, where:

- `base` is the object.
- `name` is the property name.
- `strict` is true if `use strict` is in effect.

The result of a property access `user.hi` is not a function, but a value of Reference Type. For `user.hi` in strict mode it is:

```
// Reference Type value
(user, "hi", true)
```

When parentheses `()` are called on the Reference Type, they receive the full information about the object and its method, and can set the right `this` (`user` in this case).

Reference type is a special “intermediary” internal type, with the purpose to pass information from dot `.` to calling parentheses `()`.

Any other operation like assignment `hi = user.hi` discards the reference type as a whole, takes the value of `user.hi` (a function) and passes it on. So any further operation “loses” `this`.

So, as the result, the value of `this` is only passed the right way if the function is called directly using a dot `obj.method()` or square brackets `obj['method']()` syntax (they do the same here). There are various ways to solve this problem such as [func.bind()](/bind#solution-2-bind).

## [Summary](#summary)

Reference Type is an internal type of the language.

Reading a property, such as with dot `.` in `obj.method()` returns not exactly the property value, but a special “reference type” value that stores both the property value and the object it was taken from.

That’s for the subsequent method call `()` to get the object and set `this` to it.

For all other operations, the reference type automatically becomes the property value (a function in our case).

The whole mechanics is hidden from our eyes. It only matters in subtle cases, such as when a method is obtained dynamically from the object, using an expression.

---

---

## Tasks

## [Tasks](#tasks)

### [Syntax check](#syntax-check)

importance: 2

What is the result of this code?

```
let user = {
  name: "John",
  go: function() { alert(this.name) }
}

(user.go)()
```

P.S. There’s a pitfall :)

solution

**Error**!

Try it:

```
let user = {
  name: "John",
  go: function() { alert(this.name) }
}

(user.go)() // error!
```

The error message in most browsers does not give us much of a clue about what went wrong.

**The error appears because a semicolon is missing after `user = {...}`.**

JavaScript does not auto-insert a semicolon before a bracket `(user.go)()`, so it reads the code like:

```
let user = { go:... }(user.go)()
```

Then we can also see that such a joint expression is syntactically a call of the object `{ go: ... }` as a function with the argument `(user.go)`. And that also happens on the same line with `let user`, so the `user` object has not yet even been defined, hence the error.

If we insert the semicolon, all is fine:

```
let user = {
  name: "John",
  go: function() { alert(this.name) }
};

(user.go)() // John
```

Please note that parentheses around `(user.go)` do nothing here. Usually they setup the order of operations, but here the dot `.` works first anyway, so there’s no effect. Only the semicolon thing matters.

### [Explain the value of "this"](#explain-the-value-of-this)

importance: 3

In the code below we intend to call `obj.go()` method 4 times in a row.

But calls `(1)` and `(2)` works differently from `(3)` and `(4)`. Why?

```
let obj, method;

obj = {
  go: function() { alert(this); }
};

obj.go();               // (1) [object Object]

(obj.go)();             // (2) [object Object]

(method = obj.go)();    // (3) undefined

(obj.go || obj.stop)(); // (4) undefined
```

solution

Here’s the explanations.

1. That’s a regular object method call.
2. The same, parentheses do not change the order of operations here, the dot is first anyway.
3. Here we have a more complex call `(expression)()`. The call works as if it were split into two lines:

   ```
   f = obj.go; // calculate the expression
   f();        // call what we have
   ```

   Here `f()` is executed as a function, without `this`.
4. The similar thing as `(3)`, to the left of the parentheses `()` we have an expression.

To explain the behavior of `(3)` and `(4)` we need to recall that property accessors (dot or square brackets) return a value of the Reference Type.

Any operation on it except a method call (like assignment `=` or `||`) turns it into an ordinary value, which does not carry the information allowing to set `this`.