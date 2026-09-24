//画像のリスト
let num = document.getElementsByClassName("num")
let msg = document.getElementsByClassName("msg")
let haikei = document.getElementsByClassName("haikei")

//効果音のリスト
let oto = []

//固定データ（変わらないデータ）
let window1 = { sx:640, sy:480 } //ウィンドウの横の長さと縦の長さ
let timerno //タイマー制御用
let timerv = 30 //ゲームの実行タイマー値(小さいと速い)
let canvas //キャンバス
let fuchi = 20 //パネルのふちのドット数
let maxcols = 7 //パズルの行数＝列数の最大

//作業データ（ゲームの状態によって値が変わります）
let timer = timerv //ゲームの実行タイマー
let mode = 0 //ゲームの状態（ 0:タイトル, 5:プレイ, 6:タイムアップ, 7:レベルアップ, 8:ゲームクリア, 9:ゲームオーバー）
let mouse //マウスの座標
let cols = 3 //パズルの行数＝列数
let bombs = cols - 2 //ばくだん数＝パズルの行数 - 2
let boxs = cols * cols //箱数＝パズルの行数×パズルの行数
let boxsize = (window1.sy - fuchi * 2) / cols //箱の大きさ
let map = [] //マップ（-1:空,0～7:周りのばくだん数,9:ばくだん）
let vmap = [] //表示用マップ（-2:箱, -1:空, 0～7:まわりのばくだん数, 8:フラグ, 9:ばくだん）
let flags = 0 //フラグ数
let gametimer = cols * 20 //ゲームタイマー
let zlist = [] //自動オープン用のゼロである箱のリスト
let znum = 0 //ゼロである箱の数

//最初に１回だけやること（起動処理）
function init() {
    canvas = document.getElementById('canvas') //キャンバスを得る
    ctx = canvas.getContext('2d') //キャンバスの情報（コンテキスト）を得る
    canvas.addEventListener('click', onclick_canvas, false) //クリックされた時の処理を指定
    start() //開始処理を呼ぶ
}

//マウスの座標を得る
function mousezahyo(canvas, event) {
    let rect = canvas.getBoundingClientRect() //キャンバスの位置を得る
    return { //座標を計算して返す
        x: event.clientX - rect.left,
        y: event.clientY - rect.top
    }
}

//箱画像を表示
function drawbox(i, j, no = -2) {
    let x = boxsize * i + fuchi
    let y = boxsize * j + fuchi
    if (no === -2) {
        ctx.drawImage(box, x, y, boxsize, boxsize) //箱画像を表示
    } else if (no === -1) {
        ctx.drawImage(empty, x, y, boxsize, boxsize) //空箱画像を表示
    } else if (no === 9) {
        ctx.drawImage(bomb, x, y, boxsize, boxsize) //ばくだん画像を表示
    } else if (no === 8) {
        ctx.drawImage(flag, x, y, boxsize, boxsize) //フラグ画像を表示
    } else {
        ctx.drawImage(num[no], x, y, boxsize, boxsize) //数字画像[no]を表示
    }
}

//ばくだん数をえがく
function drawbombs(mybombs) {
    ctx.font = '30pt Arial' //文字サイズを指定
    ctx.fillStyle = 'white' //白色に設定
    ctx.fillText(":" + mybombs, 545, 230) //「:ばくだん数」を表示
}

//フラグ数をえがく
function drawflags(myflags) {
    ctx.font = '30pt Arial' //文字サイズを指定
    ctx.fillStyle = 'white' //白色に設定
    ctx.fillText(":" + myflags, 545, 280) //「:フラグ数」を表示
}

//ゲームタイマーをえがく
function drawtimer(mytimer) {
    ctx.font = '36pt Arial' //文字サイズを指定
    ctx.fillStyle = 'white' //白色に設定
    let inttimer = Math.ceil(mytimer)
    ctx.fillText(("000" + inttimer).slice(-3), 510, 400) //ゲームタイマーを3桁で表示
}


//マップを用意する
function setmap() {
    for (let i = 0; i < cols; i++) { //列数の分だけくり返す
        map[i] = []; //その列のマップを用意する
        vmap[i] = []; //その列の表示マップを用意する
        for (let j = 0; j < cols; j++) { //行数の分だけくり返す
            map[i][j] = -1 //マップを空にする
            vmap[i][j] = -2 //表示マップを箱にする
        }
    }
}

//ばくだんをセットする
function setbomb(mybombs) {
    for (let i = 0; i < mybombs; i++) { //ばくだんの数だけくり返す
        for (;;) { //breakするまでくり返す
            let x = Math.floor(Math.random() * cols) //ばくだんの列を乱数で決める
            let y = Math.floor(Math.random() * cols) //ばくだんの行を乱数で決める
            if (map[x][y] === -1) { //決まった位置が空ならば
                map[x][y] = 9 //そこにばくだんをセットする
                break //１つ決定
            }
        }
    }
}

//周囲のばくだん数をセットする
function setbombs() {
    for (let i = 0; i < cols; i++) { //列数の分だけくり返す
        for (let j = 0; j < cols; j++) { //行数の分だけくり返す
            if (map[i][j] !== 9) { //ばくだんでなければ
                map[i][j] = getbnums(i, j) //周囲のばくだん数をセットする
            }
        }
    }
}

//周囲のばくだん数を返す
function getbnums(x, y) {
    let n = 0
    if (x > 0 && y > 0 && map[x - 1][y - 1] === 9) { //左上があってばくだんならば
        n++; //ばくだん数加算
    }
    if (y > 0 && map[x][y - 1] === 9) { //上があってばくだんならば
        n++; //ばくだん数加算
    }
    if (x < cols - 1 && y > 0 && map[x + 1][y - 1] === 9) { //右上があってばくだんならば
        n++; //ばくだん数加算
    }
    if (x > 0 && map[x - 1][y] === 9) { //左があってばくだんならば
        n++; //ばくだん数加算
    }
    if (x < cols - 1 && map[x + 1][y] === 9) { //右があってばくだんならば
        n++; //ばくだん数加算
    }
    if (x > 0 && y < cols - 1 && map[x - 1][y + 1] === 9) { //左下があってばくだんならば
        n++; //ばくだん数加算
    }
    if (y < cols - 1 && map[x][y + 1] === 9) { //下があってばくだんならば
        n++; //ばくだん数加算
    }
    if (x < cols - 1 && y < cols - 1 && map[x + 1][y + 1] === 9) { //右下があってばくだんならば
        n++; //ばくだん数加算
    }
    return n;
}

//マップのどこがクリックされたかを返す
function getmousemap(mymouse) {
    let xy = { x:0, y:0 } //返却値用
    xy.x = Math.floor((mymouse.x - fuchi) / boxsize) //ふちを差し引いてから箱の大きさで割って整数に
    xy.y = Math.floor((mymouse.y - fuchi) / boxsize) //ふちを差し引いてから箱の大きさで割って整数に
    if (xy.x < cols && xy.y < cols) { //マップの上であれば
        return xy //どこがクリックされたかを返す
    } else { //でなければ
        xy.x = -1 //マップの外をセットして
        return xy //外がクリックされたと返す
    }
}

//フラグボタンがクリックされたかを返す
function isflag(mymouse) {
    let x = (mymouse.x - fuchi) / boxsize //ふちを差し引いてから箱の大きさで割る
    x = x - Math.floor(x) //小数点以下のみを得る
    let y = (mymouse.y - fuchi) / boxsize //ふちを差し引いてから箱の大きさで割る
    y = y - Math.floor(y) //小数点以下のみを得る
    return  x > 0.75 && y < 0.25 //箱の右上端だったかどうかを返す
}

//「先に進む」ボタンがクリックされたかを返す
function isnext(mymouse) {
    return mymouse.x > 490 && mymouse.x < 610 && mymouse.y > 325 && mymouse.y < 385
}

//「もう１度」ボタンがクリックされたかを返す
function isagain(mymouse) {
    return mymouse.x > 490 && mymouse.x < 610 && mymouse.y > 385 && mymouse.y < 445
}

//開いていなければ自動で開く
function autoopen(x, y) {
    if (x >= 0 && y >= 0 && x < cols && y < cols && vmap[x][y] === -2) { //箱があり開いていなければ
        vmap[x][y] = map[x][y] //箱を開いて中を表示する
        boxs-- //箱数を減らす
        if (map[x][y] === 0) { //ゼロならば(※これ以降はC-3用)
            let myxy  = { x:0, y:0 } //リストに入れるための入れ物を用意する
            myxy.x = x //入れ物にxをセット
            myxy.y = y //入れ物にyをセット
            zlist[znum] = myxy //ゼロである箱のリストに入れる
            znum++ //ゼロである箱の数を1増やす
        }
    }
}

//種明かし＝全て開く
function taneakashi() {
    for (let i = 0; i < cols; i++) { //列数の分だけくり返す
        for (let j = 0; j < cols; j++) { //行数の分だけくり返す
            vmap[i][j] = map[i][j] //種明かし
        }
    }
}
