# Introduction to browser events

> Source: [https://javascript.info/introduction-browser-events](https://javascript.info/introduction-browser-events)

<!-- fetched: 2026-09-14 -->

*An event* is a signal that something has happened. All DOM nodes generate such signals (but events are not limited to DOM).

Here’s a list of the most useful DOM events, just to take a look at:

**Mouse events:**

- `click` – when the mouse clicks on an element (touchscreen devices generate it on a tap).
- `contextmenu` – when the mouse right-clicks on an element.
- `mouseover` / `mouseout` – when the mouse cursor comes over / leaves an element.
- `mousedown` / `mouseup` – when the mouse button is pressed / released over an element.
- `mousemove` – when the mouse is moved.

**Keyboard events:**

- `keydown` and `keyup` – when a keyboard key is pressed and released.

**Form element events:**

- `submit` – when the visitor submits a `<form>`.
- `focus` – when the visitor focuses on an element, e.g. on an `<input>`.

**Document events:**

- `DOMContentLoaded` – when the HTML is loaded and processed, DOM is fully built.

**CSS events:**

- `transitionend` – when a CSS-animation finishes.

There are many other events. We’ll get into more details of particular events in upcoming chapters.

## [Event handlers](#event-handlers)

To react on events we can assign a *handler* – a function that runs in case of an event.

Handlers are a way to run JavaScript code in case of user actions.

There are several ways to assign a handler. Let’s see them, starting from the simplest one.

### [HTML-attribute](#html-attribute)

A handler can be set in HTML with an attribute named `on<event>`.

For instance, to assign a `click` handler for an `input`, we can use `onclick`, like here:

```
<input value="Click me" onclick="alert('Click!')" type="button">
```

On mouse click, the code inside `onclick` runs.

Please note that inside `onclick` we use single quotes, because the attribute itself is in double quotes. If we forget that the code is inside the attribute and use double quotes inside, like this: `onclick="alert("Click!")"`, then it won’t work right.

An HTML-attribute is not a convenient place to write a lot of code, so we’d better create a JavaScript function and call it there.

Here a click runs the function `countRabbits()`:

```
<script>
  function countRabbits() {
    for(let i=1; i<=3; i++) {
      alert("Rabbit number " + i);
    }
  }
</script>

<input type="button" onclick="countRabbits()" value="Count rabbits!">
```

As we know, HTML attribute names are not case-sensitive, so `ONCLICK` works as well as `onClick` and `onCLICK`… But usually attributes are lowercased: `onclick`.

### [DOM property](#dom-property)

We can assign a handler using a DOM property `on<event>`.

For instance, `elem.onclick`:

```
<input id="elem" type="button" value="Click me">
<script>
  elem.onclick = function() {
    alert('Thank you');
  };
</script>
```

If the handler is assigned using an HTML-attribute then the browser reads it, creates a new function from the attribute content and writes it to the DOM property.

So this way is actually the same as the previous one.

These two code pieces work the same:

1. Only HTML:

   ```
   <input type="button" onclick="alert('Click!')" value="Button">
   ```
2. HTML + JS:

   ```
   <input type="button" id="button" value="Button">
   <script>
     button.onclick = function() {
       alert('Click!');
     };
   </script>
   ```

In the first example, the HTML attribute is used to initialize the `button.onclick`, while in the second example – the script, that’s all the difference.

**As there’s only one `onclick` property, we can’t assign more than one event handler.**

In the example below adding a handler with JavaScript overwrites the existing handler:

```
<input type="button" id="elem" onclick="alert('Before')" value="Click me">
<script>
  elem.onclick = function() { // overwrites the existing handler
    alert('After'); // only this will be shown
  };
</script>
```

To remove a handler – assign `elem.onclick = null`.

## [Accessing the element: this](#accessing-the-element-this)

The value of `this` inside a handler is the element. The one which has the handler on it.

In the code below `button` shows its contents using `this.innerHTML`:

```
<button onclick="alert(this.innerHTML)">Click me</button>
```

## [Possible mistakes](#possible-mistakes)

If you’re starting to work with events – please note some subtleties.

We can set an existing function as a handler:

```
function sayThanks() {
  alert('Thanks!');
}

elem.onclick = sayThanks;
```

But be careful: the function should be assigned as `sayThanks`, not `sayThanks()`.

```
// right
button.onclick = sayThanks;

// wrong
button.onclick = sayThanks();
```

If we add parentheses, then `sayThanks()` becomes a function call. So the last line actually takes the *result* of the function execution, that is `undefined` (as the function returns nothing), and assigns it to `onclick`. That doesn’t work.

…On the other hand, in the markup we do need the parentheses:

```
<input type="button" id="button" onclick="sayThanks()">
```

The difference is easy to explain. When the browser reads the attribute, it creates a handler function with body from the attribute content.

So the markup generates this property:

```
button.onclick = function() {
  sayThanks(); // <-- the attribute content goes here
};
```

**Don’t use `setAttribute` for handlers.**

Such a call won’t work:

```
// a click on <body> will generate errors,
// because attributes are always strings, function becomes a string
document.body.setAttribute('onclick', function() { alert(1) });
```

**DOM-property case matters.**

Assign a handler to `elem.onclick`, not `elem.ONCLICK`, because DOM properties are case-sensitive.

## [addEventListener](#addeventlistener)

The fundamental problem of the aforementioned ways to assign handlers is that we *can’t assign multiple handlers to one event*.

Let’s say, one part of our code wants to highlight a button on click, and another one wants to show a message on the same click.

We’d like to assign two event handlers for that. But a new DOM property will overwrite the existing one:

```
input.onclick = function() { alert(1); }
// ...
input.onclick = function() { alert(2); } // replaces the previous handler
```

Developers of web standards understood that long ago and suggested an alternative way of managing handlers using the special methods `addEventListener` and `removeEventListener` which aren’t bound by such constraint.

The syntax to add a handler:

```
element.addEventListener(event, handler, [options]);
```

`event`
:   Event name, e.g. `"click"`.

`handler`
:   The handler function.

`options`
:   An additional optional object with properties:

    - `once`: if `true`, then the listener is automatically removed after it triggers.
    - `capture`: the phase where to handle the event, to be covered later in the chapter [Bubbling and capturing](/bubbling-and-capturing). For historical reasons, `options` can also be `false/true`, that’s the same as `{capture: false/true}`.
    - `passive`: if `true`, then the handler will not call `preventDefault()`, we’ll explain that later in [Browser default actions](/default-browser-action).

To remove the handler, use `removeEventListener`:

```
element.removeEventListener(event, handler, [options]);
```

Removal requires the same function

To remove a handler we should pass exactly the same function as was assigned.

This doesn’t work:

```
elem.addEventListener( "click" , () => alert('Thanks!'));
// ....
elem.removeEventListener( "click", () => alert('Thanks!'));
```

The handler won’t be removed, because `removeEventListener` gets another function – with the same code, but that doesn’t matter, as it’s a different function object.

Here’s the right way:

```
function handler() {
  alert( 'Thanks!' );
}

input.addEventListener("click", handler);
// ....
input.removeEventListener("click", handler);
```

Please note – if we don’t store the function in a variable, then we can’t remove it. There’s no way to “read back” handlers assigned by `addEventListener`.

Multiple calls to `addEventListener` allow it to add multiple handlers, like this:

```
<input id="elem" type="button" value="Click me"/>

<script>
  function handler1() {
    alert('Thanks!');
  };

  function handler2() {
    alert('Thanks again!');
  }

  elem.onclick = () => alert("Hello");
  elem.addEventListener("click", handler1); // Thanks!
  elem.addEventListener("click", handler2); // Thanks again!
</script>
```

As we can see in the example above, we can set handlers *both* using a DOM-property and `addEventListener`. But generally we use only one of these ways.

For some events, handlers only work with `addEventListener`

There exist events that can’t be assigned via a DOM-property. Only with `addEventListener`.

For instance, the `DOMContentLoaded` event, that triggers when the document is loaded and the DOM has been built.

```
// will never run
document.onDOMContentLoaded = function() {
  alert("DOM built");
};
```

```
// this way it works
document.addEventListener("DOMContentLoaded", function() {
  alert("DOM built");
});
```

So `addEventListener` is more universal. Although, such events are an exception rather than the rule.

## [Event object](#event-object)

To properly handle an event we’d want to know more about what’s happened. Not just a “click” or a “keydown”, but what were the pointer coordinates? Which key was pressed? And so on.

When an event happens, the browser creates an *event object*, puts details into it and passes it as an argument to the handler.

Here’s an example of getting pointer coordinates from the event object:

```
<input type="button" value="Click me" id="elem">

<script>
  elem.onclick = function(event) {
    // show event type, element and coordinates of the click
    alert(event.type + " at " + event.currentTarget);
    alert("Coordinates: " + event.clientX + ":" + event.clientY);
  };
</script>
```

Some properties of `event` object:

`event.type`
:   Event type, here it’s `"click"`.

`event.currentTarget`
:   Element that handled the event. That’s exactly the same as `this`, unless the handler is an arrow function, or its `this` is bound to something else, then we can get the element from `event.currentTarget`.

`event.clientX` / `event.clientY`
:   Window-relative coordinates of the cursor, for pointer events.

There are more properties. Many of them depend on the event type: keyboard events have one set of properties, pointer events – another one, we’ll study them later when as we move on to the details of different events.

The event object is also available in HTML handlers

If we assign a handler in HTML, we can also use the `event` object, like this:

```
<input type="button" onclick="alert(event.type)" value="Event type">
```

That’s possible because when the browser reads the attribute, it creates a handler like this: `function(event) { alert(event.type) }`. That is: its first argument is called `"event"`, and the body is taken from the attribute.

## [Object handlers: handleEvent](#object-handlers-handleevent)

We can assign not just a function, but an object as an event handler using `addEventListener`. When an event occurs, its `handleEvent` method is called.

For instance:

```
<button id="elem">Click me</button>

<script>
  let obj = {
    handleEvent(event) {
      alert(event.type + " at " + event.currentTarget);
    }
  };

  elem.addEventListener('click', obj);
</script>
```

As we can see, when `addEventListener` receives an object as the handler, it calls `obj.handleEvent(event)` in case of an event.

We could also use objects of a custom class, like this:

```
<button id="elem">Click me</button>

<script>
  class Menu {
    handleEvent(event) {
      switch(event.type) {
        case 'mousedown':
          elem.innerHTML = "Mouse button pressed";
          break;
        case 'mouseup':
          elem.innerHTML += "...and released.";
          break;
      }
    }
  }

  let menu = new Menu();

  elem.addEventListener('mousedown', menu);
  elem.addEventListener('mouseup', menu);
</script>
```

Here the same object handles both events. Please note that we need to explicitly setup the events to listen using `addEventListener`. The `menu` object only gets `mousedown` and `mouseup` here, not any other types of events.

The method `handleEvent` does not have to do all the job by itself. It can call other event-specific methods instead, like this:

```
<button id="elem">Click me</button>

<script>
  class Menu {
    handleEvent(event) {
      // mousedown -> onMousedown
      let method = 'on' + event.type[0].toUpperCase() + event.type.slice(1);
      this[method](event);
    }

    onMousedown() {
      elem.innerHTML = "Mouse button pressed";
    }

    onMouseup() {
      elem.innerHTML += "...and released.";
    }
  }

  let menu = new Menu();
  elem.addEventListener('mousedown', menu);
  elem.addEventListener('mouseup', menu);
</script>
```

Now event handlers are clearly separated, that may be easier to support.

## [Summary](#summary)

There are 3 ways to assign event handlers:

1. HTML attribute: `onclick="..."`.
2. DOM property: `elem.onclick = function`.
3. Methods: `elem.addEventListener(event, handler[, phase])` to add, `removeEventListener` to remove.

HTML attributes are used sparingly, because JavaScript in the middle of an HTML tag looks a little bit odd and alien. Also can’t write lots of code in there.

DOM properties are ok to use, but we can’t assign more than one handler of the particular event. In many cases that limitation is not pressing.

The last way is the most flexible, but it is also the longest to write. There are few events that only work with it, for instance `transitionend` and `DOMContentLoaded` (to be covered). Also `addEventListener` supports objects as event handlers. In that case the method `handleEvent` is called in case of the event.

No matter how you assign the handler – it gets an event object as the first argument. That object contains the details about what’s happened.

We’ll learn more about events in general and about different types of events in the next chapters.

---

---

## Tasks

## [Tasks](#tasks)

### [Hide on click](#hide-on-click)

importance: 5

Add JavaScript to the `button` to make `<div id="text">` disappear when we click it.

The demo:

[Open a sandbox for the task.](https://plnkr.co/edit/6IFBx7wDt0dZMqP1?p=preview)

solution

[Open the solution in a sandbox.](https://plnkr.co/edit/PAzsU3E4l4hhkTAl?p=preview)

### [Hide self](#hide-self)

importance: 5

Create a button that hides itself on click.

Like this:

solution

Can use `this` in the handler to reference “the element itself” here:

```
<input type="button" onclick="this.hidden=true" value="Click to hide">
```

### [Which handlers run?](#which-handlers-run)

importance: 5

There’s a button in the variable. There are no handlers on it.

Which handlers run on click after the following code? Which alerts show up?

```
button.addEventListener("click", () => alert("1"));

button.removeEventListener("click", () => alert("1"));

button.onclick = () => alert(2);
```

solution

The answer: `1` and `2`.

The first handler triggers, because it’s not removed by `removeEventListener`. To remove the handler we need to pass exactly the function that was assigned. And in the code a new function is passed, that looks the same, but is still another function.

To remove a function object, we need to store a reference to it, like this:

```
function handler() {
  alert(1);
}

button.addEventListener("click", handler);
button.removeEventListener("click", handler);
```

The handler `button.onclick` works independently and in addition to `addEventListener`.

### [Move the ball across the field](#move-the-ball-across-the-field)

importance: 5

Move the ball across the field to a click. Like this:

Requirements:

- The ball center should come exactly under the pointer on click (if possible without crossing the field edge).
- CSS-animation is welcome.
- The ball must not cross field boundaries.
- When the page is scrolled, nothing should break.

Notes:

- The code should also work with different ball and field sizes, not be bound to any fixed values.
- Use properties `event.clientX/event.clientY` for click coordinates.

[Open a sandbox for the task.](https://plnkr.co/edit/IGCSLHiEspDxro6B?p=preview)

solution

First we need to choose a method of positioning the ball.

We can’t use `position:fixed` for it, because scrolling the page would move the ball from the field.

So we should use `position:absolute` and, to make the positioning really solid, make `field` itself positioned.

Then the ball will be positioned relatively to the field:

```
#field {
  width: 200px;
  height: 150px;
  position: relative;
}

#ball {
  position: absolute;
  left: 0; /* relative to the closest positioned ancestor (field) */
  top: 0;
  transition: 1s all; /* CSS animation for left/top makes the ball fly */
}
```

Next we need to assign the correct `ball.style.left/top`. They contain field-relative coordinates now.

Here’s the picture:

![](/task/move-ball-field/move-ball-coords.svg)

We have `event.clientX/clientY` – window-relative coordinates of the click.

To get field-relative `left` coordinate of the click, we can substract the field left edge and the border width:

```
let left = event.clientX - fieldCoords.left - field.clientLeft;
```

Normally, `ball.style.left` means the “left edge of the element” (the ball). So if we assign that `left`, then the ball edge, not center, would be under the mouse cursor.

We need to move the ball half-width left and half-height up to make it center.

So the final `left` would be:

```
let left = event.clientX - fieldCoords.left - field.clientLeft - ball.offsetWidth/2;
```

The vertical coordinate is calculated using the same logic.

Please note that the ball width/height must be known at the time we access `ball.offsetWidth`. Should be specified in HTML or CSS.

[Open the solution in a sandbox.](https://plnkr.co/edit/wuQbNr1Sz9GuDim1?p=preview)

### [Create a sliding menu](#create-a-sliding-menu)

importance: 5

Create a menu that opens/collapses on click:

P.S. HTML/CSS of the source document is to be modified.

[Open a sandbox for the task.](https://plnkr.co/edit/FaUkuVA0NqIkeOxr?p=preview)

solution

HTML/CSS

#### HTML/CSS

First let’s create HTML/CSS.

A menu is a standalone graphical component on the page, so it’s better to put it into a single DOM element.

A list of menu items can be laid out as a list `ul/li`.

Here’s the example structure:

```
<div class="menu">
  <span class="title">Sweeties (click me)!</span>
  <ul>
    <li>Cake</li>
    <li>Donut</li>
    <li>Honey</li>
  </ul>
</div>
```

We use `<span>` for the title, because `<div>` has an implicit `display:block` on it, and it will occupy 100% of the horizontal width.

Like this:

```
<div style="border: solid red 1px" onclick="alert(1)">Sweeties (click me)!</div>
```

So if we set `onclick` on it, then it will catch clicks to the right of the text.

As `<span>` has an implicit `display: inline`, it occupies exactly enough place to fit all the text:

```
<span style="border: solid red 1px" onclick="alert(1)">Sweeties (click me)!</span>
```

Toggling the menu

#### Toggling the menu

Toggling the menu should change the arrow and show/hide the menu list.

All these changes are perfectly handled by CSS. In JavaScript we should label the current state of the menu by adding/removing the class `.open`.

Without it, the menu will be closed:

```
.menu ul {
  margin: 0;
  list-style: none;
  padding-left: 20px;
  display: none;
}

.menu .title::before {
  content: '▶ ';
  font-size: 80%;
  color: green;
}
```

…And with `.open` the arrow changes and the list shows up:

```
.menu.open .title::before {
  content: '▼ ';
}

.menu.open ul {
  display: block;
}
```

[Open the solution in a sandbox.](https://plnkr.co/edit/PYMbEaFxTp7NBw8y?p=preview)

### [Add a closing button](#add-a-closing-button)

importance: 5

There’s a list of messages.

Use JavaScript to add a closing button to the right-upper corner of each message.

The result should look like this:

[Open a sandbox for the task.](https://plnkr.co/edit/IHg4ZICFUtAhqi8n?p=preview)

solution

To add the button we can use either `position:absolute` (and make the pane `position:relative`) or `float:right`. The `float:right` has the benefit that the button never overlaps the text, but `position:absolute` gives more freedom. So the choice is yours.

Then for each pane the code can be like:

```
pane.insertAdjacentHTML("afterbegin", '<button class="remove-button">[x]</button>');
```

Then the `<button>` becomes `pane.firstChild`, so we can add a handler to it like this:

```
pane.firstChild.onclick = () => pane.remove();
```

[Open the solution in a sandbox.](https://plnkr.co/edit/a1RbQkIgBi9pzbGe?p=preview)

### [Carousel](#carousel)

importance: 4

Create a “carousel” – a ribbon of images that can be scrolled by clicking on arrows.

Later we can add more features to it: infinite scrolling, dynamic loading etc.

P.S. For this task HTML/CSS structure is actually 90% of the solution.

[Open a sandbox for the task.](https://plnkr.co/edit/vw9EAQcWlH1Xw9Nj?p=preview)

solution

The images ribbon can be represented as `ul/li` list of images `<img>`.

Normally, such a ribbon is wide, but we put a fixed-size `<div>` around to “cut” it, so that only a part of the ribbon is visible:

![](/task/carousel/carousel1.svg)

To make the list show horizontally we need to apply correct CSS properties for `<li>`, like `display: inline-block`.

For `<img>` we should also adjust `display`, because by default it’s `inline`. There’s extra space reserved under `inline` elements for “letter tails”, so we can use `display:block` to remove it.

To do the scrolling, we can shift `<ul>`. There are many ways to do it, for instance by changing `margin-left` or (better performance) use `transform: translateX()`:

![](/task/carousel/carousel2.svg)

The outer `<div>` has a fixed width, so “extra” images are cut.

The whole carousel is a self-contained “graphical component” on the page, so we’d better wrap it into a single `<div class="carousel">` and style things inside it.

[Open the solution in a sandbox.](https://plnkr.co/edit/2xa7Ra0Bkq3yUndf?p=preview)