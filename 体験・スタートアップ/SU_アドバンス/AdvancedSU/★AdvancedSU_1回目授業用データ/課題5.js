// コメントだよ
function draw() {
    for(let i = 0; i < 6; i++) {
        if(i < 3) {
            ctx.drawImage(image, 60 + 40 * i, 275)
        }
    }
}
