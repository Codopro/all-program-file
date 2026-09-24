//画像のリスト
let janken = document.getElementsByClassName("janken")

//固定データ（変わらないデータ）
let window1 = { sx:640, sy:480 } //ウィンドウの大きさ(横とたての長さ)
let timerno //タイマー制御用
let canvas //キャンバス
let computer_hand = 0
let player_hand = 0
let computer_point = 0
let player_point = 0
let shohai = []
const gu_hand = 0
const tyoki_hand = 1
const pa_hand = 2
const make = 0
const kati = 1
const aiko = 2

//作業データ（ゲームの状態によって値が変わります）
let timerv = 250 //ゲームの実行タイマー値(小さいと速い)
let ctx //画像などをえがくためのしかけの入り口
let timer = timerv //ゲームの実行タイマー
let mode = 0 //ゲームの状態

//最初に１回だけやること（起動処理）
function init() {
    canvas = document.getElementById('canvas') //キャンバスを得る
    ctx = canvas.getContext('2d') //キャンバスの情報（コンテキスト）を得る
    addEventListener('keydown', keyDown, true) //キーをおし終えた時にやることを示す
    addEventListener('keyup', keyUp, true) //キーがおされた時にやることを示す

    start() //開始処理を呼ぶ
}

function janken_draw_kekka() {
    ctx.drawImage(haikei, 0, 0, 640, 480) //背景画像を表示
    ctx.drawImage(janken_key, 50, 275, 250, 150) //キー画像を表示
    ctx.drawImage(janken[computer_hand], 350, 50, 200, 200) //コンピュータの手を表示
    if (player_hand === 0) {
        ctx.drawImage(gu, 100, 50, 200, 200) //グーの画像を表示
    } else if (player_hand === 1) {
        ctx.drawImage(choki, 100, 50, 200, 200) //チョキの画像を表示
    } else {
        ctx.drawImage(pa, 100, 50, 200, 200) //パーの画像を表示
    }
    if (player_win === 0) {
        ctx.fillText("あなたの負け...", 10, 40)
    } else if (player_win === 1) {
        ctx.fillText("あなたの勝ち！", 10, 40)
    } else {
        ctx.fillText("あいこ", 10, 40);
    }
    for (let i = 0; i < shohai.length; i++) {
        if (shohai[i] === 0) {
            ctx.fillText("× | 〇", 500, 300 + i * 30)
        } else {
            ctx.fillText("〇 | ×", 500, 300 + i * 30)
        }
    }
    ctx.fillText("-------", 500, 440)
    ctx.fillText(player_point + ' vs ' + computer_point, 520, 460)
    ctx.fillText("エンターキーを押してね", 100, 470);
}

function janken_hantei() {
    player_win = make
    if (player_hand === gu_hand) {
        if (computer_hand === tyoki_hand) {
            player_win = kati
        }
    } else if (player_hand === tyoki_hand) {
        if (computer_hand === pa_hand) {
            player_win = kati
        }
    } else if (player_hand === pa_hand) {
        if (computer_hand === gu_hand) {
            player_win = kati
        }
    }
    if (computer_hand === player_hand) {
        player_win = aiko
    }
    
    if (player_win === make) {
        computer_point++
        shohai.push(player_win)
    } else if (player_win === kati) {
        player_point++
        shohai.push(player_win)
    }
}

