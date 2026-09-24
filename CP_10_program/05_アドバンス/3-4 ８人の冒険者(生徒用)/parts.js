//画像のリスト
let base = document.getElementsByClassName("base")
let guides = document.getElementsByClassName("guides")
let chara = document.getElementsByClassName("chara")
let leader = document.getElementsByClassName("leader")
let subleader = document.getElementsByClassName("subleader")
let member = document.getElementsByClassName("member")
let hyouka = document.getElementsByClassName("hyouka")
let yakuwarib = document.getElementsByClassName("yakuwarib")
let uns = document.getElementsByClassName("uns")
let unnotuyosa = document.getElementsByClassName("unnotuyosa")

//効果音のリスト
let oto = []

//固定データ（変わらないデータ）
let window1 = { sx:630, sy:480 } //ウィンドウの横の長さと縦の長さ
let timers //タイマー制御用
let timerv = 30 //ゲームの実行タイマ値(小さいと速い)
let canvas //キャンバス

//作業データ（ゲームの状態によって値が変わります）
let timer = timerv //ゲームの実行タイマー
let mode = 0 //ゲームの状態（0:タイトル画面,1:プレイ画面,2:キャラ画面,8:確認画面,9:結果画面）
let moused //マウスの座標
let powers = [6, 5, 4, 3, 5, 6, 4, 3] //各キャラのパワー
let untuyosav = [0, 0, 1, 2, 0, 0, 1, 2] //各キャラの運の強さの初期値
let untuyosavr = [0, 0, 0, 0, 0, 0, 0, 0] //各キャラの運の強さ＋乱数値(コンピュータでは乱数値ゼロ)
let selectnum = -1 //クリックされたキャラの番号
let leadernum = -1 //リーダーの番号(-1:未指定)
let subleadernum = -1 //サブリーダーの番号(-1:未指定)
let membernum = -1 //メンバーの番号(-1:未指定)
let ptakarabako = [0, 0, 0] //プレイヤーのリーダー,サブリーダー,メンバーの宝箱数
let unplus = [0, 0, 0] //プレイヤーのリーダー,サブリーダー,メンバーのうんの強さによる加算数
let playerkei = 0; //プレイヤーの宝箱数合計
let cleadernum = -1 //コンピュータのリーダーの番号(-1:未指定)
let csubleadernum = -1 //コンピュータのサブリーダーの   番号(-1:未指定)
let cmembernum = -1 //コンピュータのメンバーの番号(-1:未指定)
let ctakarabako = [0, 0, 0] //コンピュータのリーダー,サブリーダー,メンバーの宝箱数
let compkei = 0 //コンピュータの宝箱数合計
let slidecnt = 0 //キャラ画面のスライド用カウンタ
let yakuwaribai = [[4, 3, 2], [3, 4, 2], [2, 3, 4], [1, 1, 3]] //性格ごとのリーダ、サブリーダ、メンバーの役割の倍率
let seikaku = [0, 0, 0, 0, 0, 0, 0, 0] //キャラの性格番号(0:指導者,1:参謀,2:裏方,3:臆病)
let sukinac = [0, 0, 0, 0, 0, 0, 0, 0] //キャラの好きなリーダーカード番号(0～3)
let sukinaleader = [-1, 6, 3, 7] //好きなリーダーのキャラ番号(-1:なし)
let sukinazouka  = [ 0, 2, 3, 4] //好きなリーダーの時のパワー増加
let subpowerplus = 0 //好きなリーダーの時のサブリーダのパワー増加値
let mempowerplus = 0 //好きなリーダーの時のメンバーのパワー増加値
let takaracnt = 0 //結果画面の宝箱表示用カウンタ
let hyoukanum = 0 //評価番号(0:最高です,1:おみごと,2:十分です,3:まあまあ…,4:ざんねん…)

//最初に１回だけやること（起動処理）
function init() {
    canvas = document.getElementById('canvas') //キャンバスを得る
    ctx = canvas.getContext('2d') //キャンバスの情報（コンテキスト）を得る
    canvas.addEventListener('click', onclick_canvas, false) //クリックされた時の処理を指定
    start() //開始処理を呼ぶ
}

//背景に９枚の画像を並べる
function haikei9() {
    for (let j = 0; j < 3; j++) { //縦３行でくり返す
        for (let i = 0; i < 3; i++) { //横３列でくり返す
            ctx.drawImage(base[1], i * 210, j * 160) //背景画像[0]を表示
        }
    }
}

//キャラ画像をクリックしたらクリックされたキャラの番号を返す
function charapage() {
    for (let j = 0; j < 3; j++) { //縦３行でくり返す
        for (let i = 0; i < 3; i++) { //横３列でくり返す
            if (i !== 1 || j !== 1) { //中央でなければ
                if (moused.x >= i * 210 && moused.x <= i * 210 + 105 &&
                   moused.y >= j * 160 && moused.y <= j * 160 + 159) {
                    return charnum(i, j) //i列j行のキャラ番号を返す
                }
            }
        }
    }
    return -1;
}

//リーダかサブリーダかメンバを選んでいて決定をクリックしたらTrueを返す
function kettei() {
    if (leadernum !== -1 ||  subleadernum !== -1 || membernum !== -1) { //選んでいる？
        if (moused.x >= 210 && moused.x <= 420 &&
           moused.y >= 160 && moused.y <= 320) { //中央でクリック？
            return true
        }
    }
    return false
}

//リーダーボタンがクリックされていたらリーダーにする
function leaderbutton() {
    for (let j = 0; j < 3; j++) { //縦３行でくり返す
        for (let i = 0; i < 3; i++) { //横３列でくり返す
            if (i !== 1 || j !== 1) { //中央でなければ
                let n = charnum(i, j) //i列j行のキャラ番号を返す
                if (moused.x >= i * 210 + 120 && moused.x <= i * 210 + 190 &&
                   moused.y >= j * 160 + 94 && moused.y <= j * 160 + 115) {
                    if (n === subleadernum) { //すでにリーダーなら
                        subleadernum = -1 //リーダーではなくなる
                    }
                    if (n === membernum) { //すでにメンバーなら
                        membernum = -1 //メンバーではなくなる
                    }
                    leadernum = n //リーダー決定
                    return //くり返しを抜ける
                }
            }
        }
    }
}

//サブリーダーボタンがクリックされていたらサブリーダーにする
function subleaderbutton() {
    for (let j = 0; j < 3; j++) { //縦３行でくり返す
        for (let i = 0; i < 3; i++) { //横３列でくり返す
            if (i !== 1 || j !== 1) { //中央でなければ
                let n = charnum(i, j) //i列j行のキャラ番号を返す
                if (moused.x >= i * 210 + 120 && moused.x <= i * 210 + 190 &&
                   moused.y >= j * 160 + 116 && moused.y <= j * 160 + 137) {
                    if (n === leadernum) { //すでにリーダーなら
                        leadernum = -1 //リーダーではなくなる
                    }
                    if (n === membernum) { //すでにメンバーなら
                        membernum = -1 //メンバーではなくなる
                    }
                    subleadernum = n //サブリーダー決定
                    return //くり返しを抜ける
                }
            }
        }
    }
}

//メンバーボタンがクリックされていたらメンバーにする
function memberbutton() {
    for (let j = 0; j < 3; j++) { //縦３行でくり返す
        for (let i = 0; i < 3; i++) { //横３列でくり返す
            if (i !== 1 || j !== 1) { //中央でなければ
                let n = charnum(i, j) //i列j行のキャラ番号を返す
                if (moused.x >= i * 210 + 120 && moused.x <= i * 210 + 190 &&
                   moused.y >= j * 160 + 138 && moused.y <= j * 160 + 159) {
                    if (n === leadernum) { //すでにリーダーなら
                        leadernum = -1 //リーダーではなくなる
                    }
                    if (n === subleadernum) { //すでにサブリーダーなら
                        subleadernum = -1 //サブリーダーではなくなる
                    }
                    membernum = n //メンバー決定
                    return //くり返しを抜ける
                }
            }
        }
    }
}

//マウスの座標を得る
function mousezahyo(canvas, event) {
    let rect = canvas.getBoundingClientRect() //キャンバスの位置を得る
    return { //座標を計算して返す
        x: event.clientX - rect.left,
        y: event.clientY - rect.top
    }
}

//i列j行のキャラ番号を返す
function charnum(i, j) {
    let charamap = [0, 1, 2, 3, -1, 4, 5, 6, 7] //キャラの配置(中央はガイド用)
    return charamap[j * 3 + i]
}

//評価を決める
function kekkahyouka() {
    if (playerkei >= compkei) { //最高です！
        return 0
    } else if (playerkei > compkei * 0.80) { //おみごと！
        return 1
    } else if (playerkei > compkei * 0.70) { //十分です！
        return 2
    } else if (playerkei > compkei * 0.50) { //まあまあ…
        return 3
    } else { //ざんねん…
        return 4
    }
}

//コンピュータの計算結果を表示する
function compkekka() {
    let pname = ["レッド", "パープル", "ブラウン", "ブルー", "オレンジ", "ホワイト", "グリーン", "ピンク"] //各キャラの色
    if (moused.x >= 420 && moused.y >= 320) {
        alert("コンピュータの計算結果：\n"
        + "リーダー："     + pname[cleadernum]    + "(" + ctakarabako[0] + ")\n"
        + "サブリーダー：" + pname[csubleadernum] + "(" + ctakarabako[1] + ")\n"
        + "メンバー："     + pname[cmembernum]    + "(" + ctakarabako[2] + ")\n"
        + "宝箱の合計数：" + compkei + "\n"
        + "※うんの強さの乱数の分は加算していません")
    }
}

//結果画面にリーダの情報を表示する
function drawleaderk() {
    if (leadernum !== -1) { //リーダーを選んでいる？
        ctx.drawImage(chara[leadernum], 0, 0) //右上にリーダーのキャラ画像を表示
        ctx.drawImage(leader[1], 120, 94) //リーダボタンを表示
        ctx.drawImage(subleader[0], 120, 116) //サブリーダボタンを表示
        ctx.drawImage(member[0], 120, 138) //メンバーボタンを表示
        let p = powers[leadernum] + " x " + yakuwaribai[seikaku[leadernum]][0] + " + " + unplus[0] + " = " + ptakarabako[0]
        ctx.fillText(p, 120, 80) //宝箱の計算式と数を表示
    }
}

//結果画面にサブリーダの情報を表示する
function drawsubleaderk() {
    if (subleadernum !== -1) { //サブリーダーを選んでいる？
        ctx.drawImage(chara[subleadernum], 0, 160) //右中にサブリーダーのキャラ画像を表示
        ctx.drawImage(leader[0], 120, 254) //リーダボタンを表示
        ctx.drawImage(subleader[1], 120, 276) //サブリーダボタンを表示
        ctx.drawImage(member[0], 120, 298) //メンバーボタンを表示
        let p = "(" + powers[subleadernum] + " + " + subpowerplus + ")"
        p = p + " x " + yakuwaribai[seikaku[subleadernum]][1] + " + " + unplus[1] + " = " + ptakarabako[1]
        ctx.fillText(p, 120, 240) //宝箱の数を表示
    }
}

//結果画面にメンバーの情報を表示する
function drawmemberk() {
    if (membernum !== -1) { //メンバーを選んでいる？
        ctx.drawImage(chara[membernum], 0, 320) //右下にメンバーのキャラ画像を表示
        ctx.drawImage(leader[0], 120, 414) //リーダボタンを表示
        ctx.drawImage(subleader[0], 120, 436) //サブリーダボタンを表示
        ctx.drawImage(member[1], 120, 458) //メンバーボタンを表示
        let p = "(" + powers[membernum] + " + " + mempowerplus + ")"
        p = p + " x " + yakuwaribai[seikaku[membernum]][2] + " + " + unplus[2] + " = " + ptakarabako[2]
        ctx.fillText(p, 120, 400) //宝箱の数を表示
    }
}

//リーダーの宝箱の数を計算
function leadertakarabako() {
    if (leadernum !== -1) { //リーダーを選んでいる？
        return powers[leadernum] * yakuwaribai[seikaku[leadernum]][0] + unplus[0] //リーダーの宝箱の数を計算して返す
    } else {
        return 0
    }
}

//サブリーダーの宝箱の数を計算
function subleadertakarabako() {
    if (subleadernum !== -1) { //サブリーダーを選んでいる？
        let wpower = powers[subleadernum] //サブリーダーのパワーを得る
        if (leadernum === sukinaleader[sukinac[subleadernum]]) { //サブリーダーの好きなリーダー？
            subpowerplus = sukinazouka[sukinac[subleadernum]]
            wpower +=  subpowerplus //パワーに加算
        }
        return wpower * yakuwaribai[seikaku[subleadernum]][1] + unplus[1] //サブリーダーの宝箱の数を計算
    } else {
        return 0
    }
}

//メンバーの宝箱の数を計算
function membertakarabako() {
    if (membernum !== -1) { //メンバーを選んでいる？
        let wpower = powers[membernum] //メンバーのパワーを得る
        if (leadernum === sukinaleader[sukinac[membernum]]) { //メンバーの好きなリーダー？
            mempowerplus = sukinazouka[sukinac[membernum]]
            wpower += mempowerplus //パワーに加算
        }
        return wpower * yakuwaribai[seikaku[membernum]][2] + unplus[2] //メンバーの宝箱の数を計算
    } else {
        return 0
    }
}

//コンピュータがベストメンバーを選んで宝箱の数を計算
function comptakarabako() {
    for (let i = 0; i < 8; i++) { //8人全員をリーダ候補としてくり返す
        for (let j = 0; j < 8; j++) { //8人全員をサブリーダ候補としてくり返す
            for (let k = 0; k < 8; k++) { //8人全員をメンバ候補としてくり返す
                if (j !== i && k !== i && k !== j) { //リーダ、サブリーダ、メンバが別人ならば
                    let cleader = powers[i] //リーダー候補のパワーを得る
                    cleader *= yakuwaribai[seikaku[i]][0] //役割の倍率をかける
                    cleader += untuyosavr[i] //うんの強さの分を加算
                    let csubleader = powers[j] //サブリーダー候補のパワーを得る
                    if (i === sukinaleader[sukinac[j]]) { //リーダーが好きなリーダー？
                        csubleader += sukinazouka[sukinac[j]]; //パワーに加算
                    }
                    csubleader *= yakuwaribai[seikaku[j]][1] //役割の倍率をかける
                    csubleader += untuyosavr[j] //うんの強さの分を加算
                    let cmember = powers[k] //メンバ候補のパワーを得る
                    if (i === sukinaleader[sukinac[k]]) { //リーダーが好きなリーダー？
                        cmember += sukinazouka[sukinac[k]]; //パワーに加算
                    }
                    cmember *= yakuwaribai[seikaku[k]][2] //役割の倍率をかける
                    cmember += untuyosavr[k] //うんの強さの分を加算
                    if (compkei < cleader + csubleader + cmember) { //最大？
                        cleadernum = i
                        csubleadernum = j
                        cmembernum = k
                        ctakarabako[0] = cleader
                        ctakarabako[1] = csubleader
                        ctakarabako[2] = cmember
                        compkei = cleader + csubleader + cmember //コンピュータの宝箱数合計を更新
                    }
                }
            }
        }
    }
}

//プレイ画面をえがく
function drawplay(i, j) {
	let n = charnum(i, j) //i列j行のキャラ番号を得る
    ctx.drawImage(chara[n], i * 210, j * 160) //キャラ画像[0～7]を表示
	if (n === leadernum) { //キャラ[n]はリーダか？
	    ctx.drawImage(leader[1], i * 210 + 115, j * 160 + 94) //リーダボタンをon表示
	} else {
	    ctx.drawImage(leader[0], i * 210 + 115, j * 160 + 94) //リーダボタンをoff表示
	}
	if (n === subleadernum) { //キャラ[n]はサブリーダか？
	    ctx.drawImage(subleader[1], i * 210 + 115, j * 160 + 115) //サブリーダボタンをon表示
	} else {
	    ctx.drawImage(subleader[0], i * 210 + 115, j * 160 + 115) //サブリーダボタンをoff表示
	}
	if (n === membernum) { //キャラ[n]はメンバーか？
	    ctx.drawImage(member[1], i * 210 + 115, j * 160 + 136) //メンバーボタンをon表示
	} else {
	    ctx.drawImage(member[0], i * 210 + 115, j * 160 + 136) //メンバーボタンをoff表示
	}
    ctx.font = '13pt Arial' //文字サイズを指定
    ctx.fillText(yakuwaribai[seikaku[n]][0], i * 210 + 187, j * 160 + 110) //リーダーの時の倍率を表示
    ctx.fillText(yakuwaribai[seikaku[n]][1], i * 210 + 187, j * 160 + 131) //サブリーダーの時の倍率を表示
    ctx.fillText(yakuwaribai[seikaku[n]][2], i * 210 + 187, j * 160 + 152) //メンバーの時の倍率を表示
    ctx.font = '30pt Arial' //文字サイズを指定
    ctx.fillText(powers[n], i * 210 + 5, j * 160 + 35) //パワーを表示
}

//結果画面にガイドを表示
function kekkaguide() {
    ctx.drawImage(guides[4], 420, 0) //右上にガイド画像[4]を表示
    ctx.drawImage(guides[5], 420, 320) //右下にガイド[5]を表示
}

//プレイ画面にうんのつよさをえがく
function drawplayun(i, j) {
    let n = charnum(i, j) //i列j行のキャラ番号を得る
    ctx.drawImage(uns[untuyosav[n]], i * 210 + 120, j * 160 + 52) //うんのよさ[0～2]を表示
}

//運の強さの分＋乱数の宝箱の数を得る
function unplustakarabako() {
    for (let i = 0; i < 8; i++) { //8人分くり返す
        if (untuyosav[i] > 0) { //うんの強さが1以上？
            untuyosavr[i] = untuyosav[i] * 5 + Math.floor(Math.random() * 3) //5倍して0～2を加算
        }
    }
    unplus[0] = untuyosavr[leadernum] //リーダーのうんの強さによる加算分
    unplus[1] = untuyosavr[subleadernum] //サブリーダーのうんの強さによる加算分
    unplus[2] = untuyosavr[membernum] //メンバーリーダのうんの強さによる加算分
}

//コンピュータ用に運の強さの分だけの宝箱の数を得る
function cunplustakarabako() {
    for (let i = 0; i < 8; i++) { //8人分くり返す
        untuyosavr[i] = untuyosav[i] * 5 //5倍
    }
}

//結果画面に宝箱の合計数を画像付きで表示
function drawkekka(n) {
    ctx.font = '46pt Arial' //文字サイズを指定
    ctx.fillText(n, 525, 48) //プレイヤーの宝箱数の合計を表示
    for (let i = 0; i < n; i++) { //個数分繰り返す
        ctx.drawImage(takara, 420 + i % 10 * 20, 50 + Math.floor(i / 10) * 9) //うんのよさ[0～2]を表示
    }
}
