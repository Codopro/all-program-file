//画像のリスト
let wall = document.getElementsByClassName("wall")
let ball = document.getElementsByClassName("ball")

//効果音のリスト
let oto = []

//固定データ（変わらないデータ）
let window1 = { sx:640, sy:480 } //ウィンドウ（キャンバス）の大きさ
let timerno //タイマー制御用
let timerv = 20 //ゲームの実行タイマ値(小さいと速い)
let canvas //キャンバス
let cols = 14 //城へきの列数
let lines = 14 //城へきの行数
let walls = { x:24, y:24 } //城へきの大きさ
let walltops = { x:152, y:24 } //城へきの左上の初期座標
let padxys = { x:272, y:432 } //パドルの初期座標
let pads = { x:96, y:24 } //パドルの大きさ
let padspeed = 15 //パドルの左右移動量
let balls = { x:24, y:24 } //ボールの大きさ
let ballxys = { x:padxys.x + 36, y:padxys.y } //ボールの初期座標
let ballspeed = 3 //ボールの上下左右移動量
let ballvs = 1 //ボールの初期方向（0:左上,1:右上,2:右下,3:左下）
let restballs = 2 //初期残りボール数

//作業データ（ゲームの状態によって値が変わります）
let timer = timerv //ゲームの実行タイマー
let mode = 0 //ゲームの状態（0:タイトルモード,3:発射待ちアニメモード,4:発射待ちモード,5:プレイモード,7:クリアモード,8:ロストモード,9:ゲームオーバーモード）
let walltop =  { x:walltops.x, y:walltops.y } //城へきの左上の座標
let stageno = 0 //ステージ番号
let lapno = 0 //ラップ番号
let padxy = { x:padxys.x, y:padxys.y } //パドルの座標
let ballxy = { x:ballxys.x, y:ballxys.y } //ボールの座標
let ballv = ballvs //ボールの方向（0:左上,1:右上,2:右下,3:左下）
let restball = restballs //残りボール数
let animecnt = -1 //アニメーションカウンタ
let wmove = 0.2 //城へき移動量
let ballwall = {i:-1, j:-1} //ボールが当たったかべの位置

//最初に１回だけやること（起動処理）
function init() {
    canvas = document.getElementById('canvas') //キャンバスを得る
    ctx = canvas.getContext('2d') //キャンバスの情報（コンテキスト）を得る
    addEventListener('keydown', keyDown, true) //キーが押し終わった時にやることを示す
    addEventListener('keyup', keyUp, true) //キーが押された時にやることを示す
    start() //開始処理を呼ぶ
}

//"Hit ENTER to play"を表示
function drawstart() {
    ctx.font = '18pt Arial' //文字サイズを指定
    ctx.fillStyle = 'Blue' //文字を青色に
    ctx.fillText("Hit ENTER to start", 224, 432) //"Hit ENTER to start"を表示
}

//城へきと姫（小）をえがく
function drawwall() {
    let himedraw = 0 //姫（小）はまだえがいていない
    for (let j = 0; j < lines; j++) { //城へきの全行についてくり返す
        for (let i = 0; i < cols; i++) { //城へきの全列についてくり返す
            if (nmap[i][j] === 9) { //姫（小）？
                if (himedraw === 0) { //姫（小）はまだえがいていない?
                    ctx.drawImage(himemini, walltop.x + i * walls.x, walltop.y + walls.y * j) //姫（小）を表示する
                    himedraw = 1 //姫（小）は表示済
                }
            } else if (nmap[i][j] !== -1) { //かべ？
                ctx.drawImage(wall[nmap[i][j]], walltop.x + i * walls.x, walltop.y + walls.y * j) //かべ各種を表示する
            }
        }
    }
}

//ボールが上左右端についたら向きを変える
function edgecheck(v, xy) {
    if (v === 0) { //ボールの方向が左上ならば
        if (xy.y < 1) { //上端ならば
            return 3 //ボールの方向を左下にする
        } else if (xy.x < 1) { //左端ならば
            return 1 //ボールの方向を右上にする
        }
    } else if (v === 1) { //ボールの方向が右上ならば
        if (xy.y < 1) { //上端ならば
            return 2 //ボールの方向を右下にする
        } else if (xy.x > window1.sx - balls.x) { //右端ならば
            return 0 //ボールの方向を左上にする
        }
    } else if (v === 2) { //ボールの方向が右下ならば
        if (xy.x > window1.sx - balls.x) { //右端ならば
            return 3 //ボールの方向を左下にする
        }
    } else { //ボールの方向が左下ならば
        if (xy.x < 1) { //左端ならば
            return 2 //ボールの方向を右下にする
        }
    }
    return v //ボールの方向を変更しない
}

//ボールがパドルについたら向きを変える
function padcheck(v, bxy, pxy) { //ボールの方向,ボールの座標,パドルの座標
    if (v === 2 &&
        bxy.y + balls.y > pxy.y && bxy.y + balls.y < pxy.y + pads.y &&
        bxy.x + balls.x >= pxy.x && bxy.x <= pxy.x + pads.x + balls.x / 4) { //ボールの方向が右下でパドルに着いていたら
        return 1 //ボールの方向を右上にする
    } else
    if (v === 3 &&
        bxy.y + balls.y > pxy.y && bxy.y + balls.y < pxy.y + pads.y &&
        bxy.x >= pxy.x - balls.x / 4 && bxy.x <= pxy.x + pads.x) { //ボールの方向が左下でパドルに着いていたら
        return 0 //ボールの方向を左上にする
    } else { //ボールがパドルについてなければ
        return v //ボールの方向を変更しない
    }
}

//残りボール数を表示
function drawrestball(restball) {
    for (let i = 0; i < restball; i++) { //残りボールの数だけくり返す
        ctx.drawImage(ball[1], 610 - 24 * i, 10) //ボール画像[1]を表示
    }
}

//ボールとパドルの状態を元に戻す
function ballback() {
    padxy.x = padxys.x //パドルの座標を戻す
    padxy.y = padxys.y //パドルの座標を戻す
    ballxys = { x:padxys.x + 36, y:padxys.y } //ボールの初期座標を再計算する
    ballxy = { x:ballxys.x, y:ballxys.y } //ボールの座標を戻す
    ballv = ballvs //ボールの方向を戻す
    walltop.x = walltops.x //城へきの座標を戻す
}

//"Hit ENTER to next"を表示
function drawnext() {
    ctx.font = '18pt Arial' //文字サイズを指定
    ctx.fillStyle = 'Blue' //文字を青色に
    ctx.fillText("Hit ENTER to next", 224, 432) //"Hit ENTER to next"を表示
}

//ボールが何かについたか調べて、かべについたらかべを消し、鉄かべならかべにする
function wallcheck(xy) {
    ballwall = getwall(xy) //ボールが何かに当たっていたらそのかべの位置（添字）を返す
    if (ballwall.i === -1) { //何にも当たっていなかったら
        return -1 //-1(空)を返す
    } else if (nmap[ballwall.i][ballwall.j] === 9) { //姫ならば
        return 9 //9(姫)を返す
    } else if (nmap[ballwall.i][ballwall.j] === 2) { //鉄かべならば
        nmap[ballwall.i][ballwall.j] = 1 //かべにする
    } else if (nmap[ballwall.i][ballwall.j] === 0 || nmap[ballwall.i][ballwall.j] === 1) { //かべか城ならば
        nmap[ballwall.i][ballwall.j] = -1 //消す
    } else if (nmap[ballwall.i][ballwall.j] === 3) { //ボーナスつきのかべならば
        if (restball < 5) { //残りボール数が5未満であれば
            restball = restball + 1 //残りボール数を増やす
        }
        nmap[ballwall.i][ballwall.j] = -1 //ボーナスつきのかべを消す
    }
    return 0 //0(かべ)を返す
}

//ボールがかべについたら向きを変える
function wallbound(v, xy) {
    let ballwallxy = getwallxy(ballwall.i, ballwall.j) //当たったかべの座標を求める
    if (v === 0) { //ボールの方向が左上なら
        if (Math.abs((ballwallxy.x + walls.x) - xy.x) > Math.abs((ballwallxy.y + walls.y) - xy.y)) { //横のぶつかりならば
            return 3 //ボールの方向を左下にする
        } else  { //たてのぶつかりならば
            return 1 //ボールの方向を右上にする
        }
    } else if (v === 1) { //ボールの方向が右上ならば
        if (Math.abs(ballwallxy.x - (xy.x + balls.x)) > Math.abs((ballwallxy.y + walls.y) - xy.y)) { //横のぶつかりならば
            return 2 //ボールの方向を右下にする
        } else  { //たてのぶつかりならば
            return 0 //ボールの方向を左上にする
        }
    } else if (v === 2) { //ボールの方向が右下ならば
        if (Math.abs(ballwallxy.x - (xy.x + balls.x)) > Math.abs(ballwallxy.y - (xy.y + balls.y))) { //横のぶつかりならば
            return 1 //ボールの方向を右上にする
        } else  { //たてのぶつかりならば
            return 3 //ボールの方向を左下にする
        }
    } else { //ボールの方向が左下ならば
        if (Math.abs((ballwallxy.x + walls.x) - xy.x) > Math.abs(ballwallxy.y - (xy.y + balls.y))) { //横のぶつかりならば
            return 0 //ボールの方向を左上にする
        } else  { //たてのぶつかりならば
            return 2 //ボールの方向を右下にする
        }
    }
}

//ボールが何かに当たっていたらその位置（添字）を返す
function getwall(xy) {
    let wij = {i:-1, j:-1} //位置（添字）
    wij.i = Math.floor((xy.x + balls.x / 2 - walltop.x) / walls.x) //ボールの中心X座標から位置iを求める
    wij.j = Math.floor((xy.y + balls.y / 2 - walltop.y) / walls.y) //ボールの中心Y座標から位置jを求める
    if (wij.i >= 0 && wij.i < cols && wij.j >= 0 && wij.j < lines && nmap[wij.i][wij.j] !== -1) { //空でなければ
        return wij //位置（添字）を返す
    } else {
        wij.i = -1 //空であることを返す
        return wij
    }
}

//位置が(i, j)であるかべの座標を返す
function getwallxy(i, j) {
    let wxy = {x:0, y:0} //かべ[i][j]の座標
    wxy.x = walltop.x + walls.x * i //かべのX座標を求める
    wxy.y = walltop.y + walls.y * j //かべのY座標を求める
    return wxy //かべの座標を返す
}

//"Hit ENTER to next stage"を表示
function drawnextstage() {
    ctx.font = '18pt Arial' //文字サイズを指定
    ctx.fillStyle = 'Blue' //文字を青色に
    ctx.fillText("Hit ENTER to next stage", 188, 432) //"Hit ENTER to next stage"を表示
}

//次のステージのマップを読み込む
function setmap(sno) {
    for (let j = 0; j < lines; j++) { //城へきの全行についてくり返す
        for (let i = 0; i < cols; i++) { //城へきの全列についてくり返す
            nmap[i][j] = wmap[sno][i][j] //マップを読み込む
        }
    }
}

//ステージ番号をえがく
function drawstageno() {
    ctx.font = '18pt Arial' //文字サイズを指定
    ctx.fillStyle = 'White' //文字を青色に
    ctx.fillText("Stage : " + (lapno + 1) + "-" + (stageno + 1), 6, 26) //ステージ番号をえがく
}

