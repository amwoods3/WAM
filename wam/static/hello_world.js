function entryPoint() {
    alert('entryPoint() entry point.');
    var canvas = document.getElementById('myCanvas');
    var context = canvas.getContext('2d');

    // do cool things with the context
    context.font = '40pt Calibri';
    context.fillStyle = 'blue';
    context.fillText('Hello World!', 150, 100);

    alert('entryPoint() returning.');
}

