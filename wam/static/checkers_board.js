//window.onload = function(event) {
//	draw_board();
//}


function draw_board(pieces) {
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
				context2D.fillStyle = "#d00000";
			}
			else
			{
				context2D.fillStyle = "#303030";
			}
			context2D.fillRect(x, y, 50, 50);
		}
	}

	draw_pieces(pieces, canvas, context2D);
}

function draw_pieces(pieces, canvas, context2D) {
	red_piece = new Image();
	red_piece.src = '/static/red_piece.gif';
	red_king_piece = new Image();
	red_king_piece.src = '/static/red_king_piece.gif';
	black_piece = new Image();
	black_piece.src = '/static/black_piece.gif';
	black_king_piece = new Image();
	black_king_piece.src = '/static/black_king_piece.gif';

	for (var row = 0; row < 8; row++)
	{
		for (var column = 0; column < 8; column++)
		{
			var x = column * 50;
			var y = row * 50;
			var piece = pieces[row][column];
			console.log(piece);
			switch(piece){
				case 'b':
					context2D.drawImage(black_piece, x, y, 50, 50);
					break;
				case 'B':
					context2D.drawImage(black_king_piece, x, y, 50, 50);
					break;
				case 'r':
					context2D.drawImage(red_piece, x, y, 50, 50);
					break;
				case 'R':
					context2D.drawImage(red_king_piece, x, y, 50, 50);
					break;
			}
		}
	}
}
