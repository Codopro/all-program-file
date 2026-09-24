//画像のリスト
let slimeb = document.getElementsByClassName("slimeb")
let slime = document.getElementsByClassName("slime")
let nextimg = document.getElementsByClassName("nextimg")

//固定データ（変わらないデータ）
let window1 = { sx:640, sy:480 } //ウィンドウの横の長さと縦の長さ
let timerno //タイマー制御用
let timerv = 30 //ゲームの実行タイマ値(小さいと速い)
let canvas //キャンバス
let cols = 6 //ステージの列数
let erasecount = 16 //消去カウント
let getpoint = 10 //３つ並んだ時のポイント
let rensapoint = 100 //れんさした時のポイント
let slimesize = 34 //スライムのサイズ
let falldiv = 16 //スライムズが1回に落ちる割合（減らすと速く落ちる）
let stagex = 58 //ステージの左上のX座標
let bonusrate = 0.05 //ボーナススライムが出る確率

//作業データ（ゲームの状態によって値が変わります）
let timer = timerv //ゲームの実行タイマー
let mode = 0 //ゲームの状態（0:タイトルモード,5:プレイモード,6:並びチェックモード,7:消去モード,9:ゲームオーバーモード）
let yokokus = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]] //予告のスライムズ[0]～[5]のスライム３つずつ
let slimes = [0,0,0] //落下中のスライムズ
let slimenum = 3 //スライムの種類数(※4以上は後半で使用)
let smap = [[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]] //ステージマップ(-1:空き,0～5:スライム,10～15:消えるスライム)
let slimexy = { x:102, y:-102 } //落下中のスライムズの初期座標
let score = 0 //スコア
let point = 0 //今回のポイント
let erasecounter = 0 //消去カウンタ
let rensacounter = -1 //れんさカウンタ(-1:未カウント,0～:れんさ回数)
let norensacnt = 0 //れんさ無しカウンタ
let hiscore = [0,0,0] //ハイスコア[0]～[2]
let lines = 13 //ステージの行数
let smapxy = { dx:0, dy:0 } //ステージマップに最後にセットしたスライムの位置
let lastslime = -1 //ステージマップに最後にセットしたスライムの色

//最初に１回だけやること（起動処理）
function init() {
    canvas = document.getElementById('canvas') //キャンバスを得る
    ctx = canvas.getContext('2d') //キャンバスの情報（コンテキスト）を得る
    addEventListener('keydown', keyDown, true) //キーが押し終わった時にやることを示す
    addEventListener('keyup', keyUp, true) //キーが押された時にやることを示す
    start() //開始処理を呼ぶ
}

//落下中のスライムズの左上座標から３つめのスライムの位置を得て返す
function getmap(myxy) {
    let st = { dx:0, dy:0 } //位置情報を返すためのデータ
    st.dx = Math.floor(slimexy.x / slimesize) //X座標から位置sを得る
    st.dy = Math.floor(slimexy.y / slimesize) + 3 //Y座標から位置tを得る
    return st //位置情報を返す
}

//同色のスライムが３つ並んでいるか、れんさしているかなどをチェックする
function narabicheck() {
    mode = 5 //並んでいない場合はプレイモードに戻すためにいったんプレイモードにする
    for (let i = 0; i < cols; i++) { //ステージの全列についてくり返す
        for (let j = 0; j < lines; j++) { //ステージの全行についてくり返す
            if (smap[i][j] !== -1) { //空でなければ
                if (i < cols - 2 && smap[i][j] % 10 === smap[i + 1][j] % 10 && smap[i][j] % 10 === smap[i + 2][j] % 10) { //横3並び？
                    mode = 7 //消去モードにする
                    smap[i    ][j] = smap[i    ][j] + 10 //並んでいるとする
                    smap[i + 1][j] = smap[i + 1][j] + 10 //並んでいるとする
                    smap[i + 2][j] = smap[i + 2][j] + 10 //並んでいるとする
                    point = point + getpoint //ポイント加算
                }
                if (j < lines - 2 && smap[i][j] % 10 === smap[i][j + 1] % 10 && smap[i][j] % 10 === smap[i][j + 2] % 10) { //縦3並び？
                    mode = 7 //消去モードにする
                    smap[i][j    ] = smap[i][j    ] + 10 //並んでいるとする
                    smap[i][j + 1] = smap[i][j + 1] + 10 //並んでいるとする
                    smap[i][j + 2] = smap[i][j + 2] + 10 //並んでいるとする
                    point = point + getpoint //ポイント加算
                }
                if (i < cols - 2 && j < lines - 2 && smap[i][j] % 10 === smap[i + 1][j + 1] % 10 && smap[i][j] % 10 === smap[i + 2][j + 2] % 10) { //右下3並び？
                    mode = 7 //消去モードにする
                    smap[i    ][j    ] = smap[i    ][j    ] + 10 //並んでいるとする
                    smap[i + 1][j + 1] = smap[i + 1][j + 1] + 10 //並んでいるとする
                    smap[i + 2][j + 2] = smap[i + 2][j + 2] + 10 //並んでいるとする
                    point = point + getpoint //ポイント加算
                }
                if (i >= 2 && j < lines - 2 && smap[i][j] % 10 === smap[i - 1][j + 1] % 10 && smap[i][j] % 10 === smap[i - 2][j + 2] % 10) { //左下3並び？
                    mode = 7 //消去モードにする
                    smap[i    ][j    ] = smap[i    ][j    ] + 10 //並んでいるとする
                    smap[i - 1][j + 1] = smap[i - 1][j + 1] + 10 //並んでいるとする
                    smap[i - 2][j + 2] = smap[i - 2][j + 2] + 10 //並んでいるとする
                    point = point + getpoint //ポイント加算
                }
            }
        }
    }
    if (mode === 7) { //並びがあり消去モードになっていたら
        erasecnt = erasecount //消去カウンタをセット
        if (rensacounter === -1) { //れんさカウンタが「なし」ならば
            rensacounter = 0  //れんさカウント「有り」にする
        } else { //れんさカウント「有り」ならば
            rensacounter = rensacounter + 1 //れんさカウントアップ
            point = point + rensapoint //ポイントにれんさポイントを加算
        }
    } else { //並びゼロならば
        score = score + point //ポイントをスコアに加算
        point = 0 //ポイントをクリア
    }
}

//予告をセットして落下するスライムズにコピーする
function setyokoku(mi) {
    for (let j = 0; j < 3; j++) { //それぞれのスライム３匹についてくり返す
        yokokus[mi][j] = Math.floor(Math.random() * slimenum) //乱数でどのスライムか決める
        if (mi === 0) { //予告[0]ならば
            slimes[j] = yokokus[0][j] //落下するスライムズにコピーする
        }
    }
}

//予告を前にずらして新しい予告をセットする
function setnewyokoku() {
    for (let i = 1; i <= 5; i++) { //予告[1]～[5]についてくり返す
        for (let j = 0; j < 3; j++) { //それぞれのスライム３匹についてくり返す
            yokokus[i - 1][j] = yokokus[i][j] //前にずらす
        }
    }
    for (let j = 0; j < 3; j++) { //スライム３匹についてくり返す
        setyokoku(5) //予告[5]をセットする
    }
}

//落下中スライムズがさらに落下できるかどうかを返す
function canslimefall() {
    let st = getmap(slimexy) //落下中スライムズの左上座標から３つめのスライムの位置を得る
    return (slimexy.y + slimesize * 3 < slimesize * lines && smap[st.dx][st.dy] === -1) //底ではなくステージマップが空きの位置か？
}

//落下中スライムズをステージマップにセットして次のスライムズを用意する
function endslimefall() {
	lastslime = slimes[2] //ステージマップに最後にセットするスライムの色を取っておく
    smapxy = getmap(slimexy) //落下中スライムズの左上座標から３つめのスライムの位置を得る
    for (let j = 0; j < 3; j++) { //落下中スライムズの各スライムについてくり返す
        smap[smapxy.dx][smapxy.dy - 3 + j] = slimes[j] //各スライムをステージマップにセットする
        slimes[j] = yokokus[0][j] //次のスライムズのために予告[0]から落下中スライムズにセットする
    }
    slimexy = { x:102, y:-102 } //次の落下中スライムズの初期座標をセット
    rensacounter = -1 //れんさカウンタを「なし」にする
}

//落下中スライムズを左に動かす
function moveleft() {
    let st = getmap(slimexy) //落下中スライムズの左上座標から３つめのスライムの位置を得る
    if (st.dy >= 0 && smap[st.dx - 1][st.dy] === -1) { //３つめのスライムが表示されていて左側が開いていたら
        slimexy.x = slimexy.x - slimesize //スライム１つ分、左に移動
    }
}

//落下中スライムズを右に動かす
function moveright() {
    let st = getmap(slimexy) //落下中スライムズの左上座標から３つめのスライムの位置を得る
    if (st.dy >= 0 && smap[st.dx + 1][st.dy] === -1) { //３つめのスライムが表示されていて右側が開いていたら
        slimexy.x = slimexy.x + slimesize //スライム１つ分、右に移動
    }
}

//そろった並びに含まれているスライムを消す
function eraseslime() {
    for (let i = 0; i < cols; i++) { //ステージの全列についてくり返す
        for (let j = 0; j < lines; j++) { //ステージの全行についてくり返す
            if (smap[i][j] >= 10) { //並びにふくまれていたら
                smap[i][j] = -1 //消す
                for (let k = j; k > 0; k--) { //その上にある全スライムについてくり返す
                    if (smap[i][k] > 10) { //それも並びにふくまれていたら
                        smap[i][k] = -1 //消す
                    }
                    smap[i][k] = smap[i][k - 1] //１つ下にずらす
                }
                smap[i][0] = -1 //その列のもっとも上は無条件で消す
            }
        }
    }
}

//落下中のスライムズをえがく
function drawslimes() {
    for (let j = 0; j < 3; j++) { //落下中のスライムズのスライム３つについてくり返す
        ctx.drawImage(slime[slimes[j]], slimexy.x + stagex, slimesize * j + Math.floor(slimexy.y)) //スライムズをえがく
    }
}

//はいけいをえがく
function drawhaikei() {
    ctx.drawImage(haikei, 0, 0) //はいけい画像を表示
}

//予告を表示する
function drawyokoku() {
    for (let i = 0; i < 6; i++) { //全予告についてくり返す
        ctx.drawImage(nextimg[i], 51 * i + 320, 114) //ネクストナンバー画像[0]～[5]を表示
        ctx.drawImage(nextbar, 51 * i + 320, 160) //ネクストバー画像を表示
        for (let j = 0; j < 3; j++) { //それぞれのスライム３つについてくり返す
            ctx.drawImage(slime[yokokus[i][j]], 51 * i + 320, slimesize * j + 160)
        }
    }
}

//ステージ上のスライムを表示する
function drawstageslime() {
    for (let i = 0; i < cols; i++) { //ステージの全列についてくり返す
        for (let j = 0; j < lines; j++) { //ステージの全行についてくり返す
            if (smap[i][j] !== -1) { //空でなければ
                ctx.drawImage(slime[smap[i][j] % 10], slimesize * i + stagex, slimesize * j) //スライムを表示
            }
        }
    }
}

//ステージ上の並んでいるスライムのはいけいを光らせる
function drawslimebacklight() {
    for (let i = 0; i < cols; i++) { //ステージの全列についてくり返す
        for (let j = 0; j < lines; j++) { //ステージの全行についてくり返す
            if (smap[i][j] >= 10) { //並んでいれば
                ctx.drawImage(shine, slimesize * i + stagex, slimesize * j) //スライムのはいけいの光画像を表示する
            }
        }
    }
}

//ゲームオーバーを表示
function drawgameover() {
    ctx.font = '80pt Arial' //文字サイズを指定
    ctx.fillStyle = 'Red' //文字を赤色に
    ctx.fillText('Game Over', 45, 257) //文字列'Game Over'を表示
}

//れんさ数を表示
function drawrensa() {
    if (rensacounter >= 0) { //れんさ数があれば
        ctx.font = '16pt Arial' //文字サイズを指定
        ctx.fillStyle = 'White' //文字を白色に
        ctx.fillText(rensacounter, 400, 323) //れんさ数をれんさ数ボードに表示
    }
}

//ポイントを表示
function drawpoint() {
    if (point > 0) { //ポイントが得られていたら
        ctx.font = '16pt Arial' //文字サイズを指定
        ctx.fillStyle = 'White' //文字を白色に
        ctx.fillText(("00000" + point).slice(-5), 394, 376) //ポイントをポイントボードに5桁で表示
    }
}

//スコアを表示
function drawscore() {
    ctx.font = '16pt Arial' //文字サイズを指定
    ctx.fillStyle = 'White' //文字を白色に
    ctx.fillText(("000000" + score).slice(-6), 382, 429) //スコアをスコアボードに6桁で表示
}

//リプレイを表示
function drawreplay() {
    ctx.font = '16pt Arial' //文字サイズを指定
    ctx.fillStyle = 'White' //文字を白色に
    ctx.fillText("Hit ENTER", 483, 409) //"Hit ENTER"をメッセージボードに表示
    ctx.fillText("to Replay", 503, 429) //"to Replay"をその下に表示
}

//ハイスコアのタイトルを表示
function drawhiscoretitle() {
    ctx.font = '16pt Arial' //文字サイズを指定
    ctx.fillStyle = 'white' //白色に設定
    ctx.fillText("HI-SCORE", 483, 318) //メッセージボードの上に"HI-SCORE"を表示
}

//ハイスコアを表示
function drawhiscore(rank) {
    ctx.font = '16pt Arial' //文字サイズを指定
    ctx.fillStyle = 'white' //白色に設定
    ctx.fillText("(" + rank + ") " + ("000000" + hiscore[rank - 1]).slice(-6), 483, 20 * rank + 318) //順位とハイスコア(6桁)を表示
}

//ハイスコアの更新
function hiscoreupdate(myscore) {
    if (hiscore[2] < myscore) { //ランクイン（現在の最下位より大）？
        hiscore[2] = myscore //仮に最下位とする
        for (let i = 2; i > 0; i--) { //1位までについてくり返す
            if (hiscore[i - 1] < hiscore[i]) { //逆順になっていたら
                let temp = hiscore[i - 1]
                hiscore[i - 1] = hiscore[i] //交換する
                hiscore[i] = temp
            } else { //でなければ
                break //更新完了
            }
        }
    }
}

//ステージ上のスライムを１行ずつ上にずらす
function slimeslideup() {
    for (let i = 0; i < cols; i++) { //ステージの全列についてくり返す
        for (let j = 1; j < lines; j++) { //ステージの2行目から全行についてくり返す
            smap[i][j - 1] = smap[i][j] //１つ上にずらす
        }
    }
    for (let i = 0; i < cols; i++) { //ステージ最下行の全列についてくり返す
        smap[i][lines - 1] = -1 //空にする
    }
    lines = lines - 1 //ステージの行数を１行減らす
    norensacnt = 0 //れんさ無しカウンタをクリア
}

//ステージ上のスライムを１行ずつ下にずらす
function slimeslidedown() {
    for (let i = 0; i < cols; i++) { //ステージの全列についてくり返す
        for (let j = lines - 1; j >= 0; j--) { //ステージの全行について下から上へくり返す
            smap[i][j + 1] = smap[i][j] //１つ下にずらす
        }
    }
    for (let i = 0; i < cols; i++) { //ステージ最上行の全列についてくり返す
        smap[i][0] = -1 //空にする
    }
    lines = lines + 1 //ステージの行数を1行戻す
}

//ボーナススライムズの直下の色のスライムを全て消去対象にする
function bonuscheck() {
    if (smapxy.dy < lines) { //ボーナススライムズが着いた位置がステージの底ではなければ
        let col = smap[smapxy.dx][smapxy.dy] //ボーナススライムズの直下のスライムの色を得る
        for (let i = 0; i < cols; i++) { //ステージの全列についてくり返す
            for (let j = 0; j < lines; j++) { //ステージの全行についてくり返す
                if (smap[i][j] === col) { //同じ色であれば
                    smap[i][j] = smap[i][j] + 10 //消去対象にする
                }
            }
        }
    }
}
