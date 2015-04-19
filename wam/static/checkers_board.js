window.onload = function() {
    var canvas = document.getElementById("checkerboard");
	var context2D = canvas.getContext("2d");

	for (var row = 0; row < 8; row ++)
	{
		for (var column = 0; column < 8; column ++)
		{
			// coordinates of the top-left corner
			var x = column * 50;
			var y = row * 50;

			if (column % 2 == row % 2)
			{
				context2D.fillStyle = "red";
			}
			else
			{
				context2D.fillStyle = "black";

			}
			context2D.fillRect(x, y, 50, 50);
		}
	}
}
