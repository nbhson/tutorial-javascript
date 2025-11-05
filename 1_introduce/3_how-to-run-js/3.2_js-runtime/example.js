

setTimeout(() => {
    console.log('4. Timeout');
}, 0);

Promise.resolve().then(() => {
    console.log('3. Promise');
});

for (let i = 0; i < 50; i++) {
    console.log('1. For loop');
}

console.log('2. Start');


// ❌ Memory leak
{
     globalVar = "I'm global"; // Thiếu var/let/const
}

console.log(globalVar);